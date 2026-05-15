# JARVIS + LibreChat Backend Setup

This document describes how to spin up LibreChat locally via Docker and connect it to JARVIS.
LibreChat serves as the intelligent backend "brain", routing AI requests dynamically.

## 1. Deploy LibreChat

LibreChat requires Docker and Docker Compose. We recommend using their official deployment:

```bash
# Clone LibreChat
git clone https://github.com/danny-avila/LibreChat.git
cd LibreChat

# Copy the example environment file
cp .env.example .env

# Edit .env to add your API Keys (OpenAI, Gemini, Anthropic, etc.)
# If using Ollama, ensure OLLAMA_HOST is correctly pointed to your local instance.

# Start the services
docker-compose up -d
```

## 2. Generate API Key

1. Once LibreChat is running, navigate to `http://localhost:3080`.
2. Create an admin account and log in.
3. Generate an API Key from the LibreChat settings/admin panel.

## 3. Connect JARVIS to LibreChat

1. In your JARVIS terminal/environment, export the API key:
   ```bash
   export LIBRECHAT_API_KEY="your-generated-key-here"
   ```
2. Run JARVIS:
   ```bash
   python main.py
   ```

JARVIS will now route requests through `http://localhost:3080/api/v1` automatically.
