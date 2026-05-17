from playwright.sync_api import sync_playwright
import time
from core.logger import get_logger

logger = get_logger("BrowserAgent")

class BrowserAgent:
    """
    Playwright-based autonomous browser agent for web interactions.
    """
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def _ensure_started(self):
        if not self.playwright:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=False)
            self.context = self.browser.new_context()
            self.page = self.context.new_page()

    def navigate(self, url: str) -> str:
        """Navigates to the given URL."""
        try:
            self._ensure_started()
            self.page.goto(url, wait_until="domcontentloaded")
            return f"Successfully navigated to {url}"
        except Exception as e:
            logger.error(f"Navigation failed: {e}")
            return f"Failed to navigate: {e}"

    def click_element(self, selector: str) -> str:
        """Clicks an element matching the given CSS selector."""
        try:
            self._ensure_started()
            self.page.click(selector, timeout=5000)
            return f"Clicked element {selector}"
        except Exception as e:
            logger.error(f"Click failed: {e}")
            return f"Failed to click element: {e}"

    def fill_form(self, selector: str, text: str) -> str:
        """Fills an input field matching the CSS selector with text."""
        try:
            self._ensure_started()
            self.page.fill(selector, text, timeout=5000)
            return f"Filled {selector} with text."
        except Exception as e:
            logger.error(f"Fill failed: {e}")
            return f"Failed to fill element: {e}"

    def get_page_content(self) -> str:
        """Extracts the visible text from the current page."""
        try:
            self._ensure_started()
            text = self.page.locator("body").inner_text()
            # truncate to avoid blowing up context window
            return text[:2000]
        except Exception as e:
             logger.error(f"Content extraction failed: {e}")
             return f"Failed to get content: {e}"

    def close(self):
        """Closes the browser session."""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        self.browser = None
        self.playwright = None

browser_agent = BrowserAgent()

def browser_navigate(url: str) -> str:
    """Tool: Navigate the browser to a specific URL."""
    return browser_agent.navigate(url)

def browser_click(selector: str) -> str:
    """Tool: Click an element on the current webpage using a CSS selector."""
    return browser_agent.click_element(selector)

def browser_type(selector: str, text: str) -> str:
    """Tool: Type text into an input field on the current webpage using a CSS selector."""
    return browser_agent.fill_form(selector, text)

def browser_read() -> str:
    """Tool: Read the textual content of the current webpage."""
    return browser_agent.get_page_content()
