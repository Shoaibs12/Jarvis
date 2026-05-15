from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
from ai.librechat_client import LibreChatClient

def extract_text(url: str) -> str:
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=6)
    except:
        return ""
    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = soup.find_all("p")
    article_text = " ".join(p.get_text().strip() for p in paragraphs)
    if len(article_text) < 250:
        articles = soup.find_all("article")
        article_text = " ".join(a.get_text().strip() for a in articles)
    return article_text if len(article_text) > 100 else ""

def web_search(query: str) -> str:
    """
    Performs a web search using DuckDuckGo.
    """
    try:
        results = list(DDGS().text(query, max_results=5, region="wt-wt"))
    except Exception as e:
        return f"Search error: {str(e)}"
    if not results:
        return "I couldn't find anything relevant."
    english = [r for r in results if not any(bad in r.get("href", "").lower() for bad in ["zhihu", "qq", "baidu", "yandex"])]
    top = english[0] if english else results[0]
    title = top.get("title", "No title available")
    snippet = top.get("body", "No description")
    link = top.get("href", "")
    return f"Top result:\n{title}\n{snippet}\nLink: {link}"

def fetch_latest_ai_news() -> str:
    """
    Fetches and summarizes the latest AI news via LibreChat.
    """
    try:
        news = list(DDGS().news("latest artificial intelligence news", max_results=3, region="wt-wt"))
    except:
        return "I couldn't fetch AI news due to a network issue."
    if not news:
        return "I couldn't find any recent AI news."

    client = LibreChatClient()
    output = "Here are the latest AI updates:\n\n"

    for i, item in enumerate(news[:3], start=1):
        title = item.get("title", "Untitled")
        body = item.get("body", "")
        url = item.get("url") or item.get("href", "")
        article_text = extract_text(url)

        if article_text:
            messages = [{"role": "user", "content": f"Summarize this AI news in 3 short sentences:\n{article_text}"}]
            summary = client.chat_completion(messages, model="gpt-4o")
        else:
            summary = body

        output += f"🔹 **News {i}: {title}**\n{summary}\n\n"
    return output

def summarize_url(url: str) -> str:
    """
    Summarizes a webpage using LibreChat.
    """
    article_text = extract_text(url)
    if not article_text:
        return "I couldn't read that webpage — it may be blocked or too short."

    client = LibreChatClient()
    messages = [{"role": "user", "content": f"Summarize this webpage in 4 simple sentences:\n{article_text}"}]
    return client.chat_completion(messages, model="gpt-4o")
