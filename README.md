# JARVIS AI Desktop Assistant

JARVIS is a production-grade, highly responsive desktop AI assistant built for Windows (and compatible environments). Inspired by the cinematic feel of Iron Man's assistant, it is designed as a real-world productivity and automation tool, blending a futuristic holographic user interface with robust, continuous voice interaction.

## Features

JARVIS is designed to run in the background, awaiting activation to assist you with a multitude of tasks via natural voice commands.

### Voice Activation & Continuous Listening
* **Dual Activation Modes:** Wake up JARVIS by saying the wake-word **"Jarvis"** or by using a **Double Clap** (detected via amplitude peak and FFT frequency analysis to avoid false positives).
* **Continuous Mode:** Once activated, JARVIS enters a continuous listening loop, allowing for natural, back-and-forth conversations and multi-step tasks without needing to repeat the wake-word.
* **Exit Commands:** Simply say *"sleep"* or *"stop listening"* to put JARVIS back into standby mode.

### 🧠 Core Intelligence
Powered by Gemini 2.5 Flash, JARVIS features:
* Conversational memory and context retention.
* Natural answers to general questions.
* Task classification to autonomously determine whether you need system control, a web search, or code assistance.

### 💻 System Control & Automation
Command your local machine hands-free:
* **Open Applications:** Launch Chrome, VS Code, Notepad, Calculator, Paint, or CMD. (*"Jarvis, open VS Code"*)
* **Open Websites:** Directly launch popular sites like YouTube, Google, Gmail, WhatsApp, and GitHub. (*"Jarvis, open YouTube"*)
* **Volume Control:** Increase, decrease, mute, or unmute system volume. (*"Jarvis, mute the volume"*)
* **Power Management:** Shutdown, restart, or put your PC to sleep. (*"Jarvis, shut down the system"*)
* **File & Folder Management:** Quickly open your Downloads, Documents, or Desktop folders. (*"Jarvis, open my Downloads folder"*)

### 🌐 Web & Internet Capabilities
Access the web effortlessly:
* **Live Search:** Perform DuckDuckGo searches and get summarized top results. (*"Jarvis, search the web for quantum computing"*)
* **AI News Fetcher:** Retrieve and summarize the latest Artificial Intelligence news. (*"Jarvis, what is the latest AI news?"*)
* **Content Summarization:** Read and summarize web articles directly from URLs.
* **Chrome Integration:** Perform automated Google searches inside your Chrome browser.

### 👨‍💻 Coding Assistant
Built-in assistance for developers:
* **Code Generation:** Ask JARVIS to write Python scripts, web components, or algorithms.
* **Code Explanation:** Request explanations for complex code snippets.
* **Debugging Assistance:** Ask JARVIS to explain errors and propose fixes.

### 🎛️ Futuristic UI
A beautifully crafted GUI using PyQt6:
* Holographic "Arc Reactor" core with smooth pulse and rotation animations.
* Live status indicators showing when JARVIS is "Awaiting Activation", "Listening", "Thinking", or "Speaking".
* Real-time subtitles displaying your transcribed speech and JARVIS's responses.

## Architecture & Tech Stack
* **Language:** Python 3.10+
* **Frontend:** PyQt6
* **Speech-to-Text (STT):** OpenAI Whisper (local, running smoothly via optimized audio chunking)
* **Text-to-Speech (TTS):** Edge-TTS
* **Wake-word Engine:** Porcupine (pvporcupine)
* **Audio Processing:** Sounddevice & Numpy
* **LLM Engine:** Google Gemini (generativeai)
* **Web Search:** DuckDuckGo Search (duckduckgo-search) & BeautifulSoup4

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <repo_url>
   cd jarvis
   ```

2. **Install system dependencies:**
   Ensure you have PortAudio and PyQt6 dependencies installed on your system.
   *Linux (Ubuntu/Debian):*
   ```bash
   sudo apt-get install libportaudio2 portaudio19-dev
   sudo apt-get install libxcb-cursor0 libxkbcommon-x11-0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-xinerama0 libxcb-xinput0 libxcb-xfixes0 libxcb-shape0
   ```

3. **Install Python packages:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: You can generate the exact requirements using `pip freeze > requirements.txt` if not present.)*

4. **Configure API Keys:**
   Update your configuration files in the `config/` directory:
   * `config/gemini_key.py`: Add your Google Gemini API Key.
   * `config/porcupine_key.py`: Add your Picovoice Porcupine Access Key.

5. **Run JARVIS:**
   ```bash
   python main.py
   ```

## Usage Example
1. Start the application (`python main.py`). The UI will appear in standby mode.
2. Clap twice or say *"Jarvis"*. The UI will pulse blue and announce it is listening.
3. Say: *"Open YouTube"* → JARVIS will open the website.
4. Say: *"Search for the latest AI news"* → JARVIS will fetch and read the news.
5. Say: *"Stop listening"* → JARVIS returns to standby mode.

Enjoy your new AI assistant!
