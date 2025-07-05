# MultiModalMind

## Project Overview

MultiModalMind is a modern AI chat application supporting multi-model AI (OpenAI GPT-4o, Claude, Gemini), web search, image generation, and more. It features a beautiful React UI and an Express backend with PostgreSQL.

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/MultiModalMind.git
cd MultiModalMind
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Configure Environment Variables
Copy the sample environment file and fill in your credentials:
```bash
cp env.sample .env
```
Edit `.env` and provide your database and API keys.

### 4. Generate a SERPAPI Key (for Web Search)
SERPAPI is used to enable web search features in the chat. Follow these steps to get your free API key:

1. Go to the [SerpAPI website](https://serpapi.com/).
2. Click **Sign Up** (top right) and create a free account using your email or Google/GitHub account.
3. After verifying your email and logging in, you will be redirected to your [dashboard](https://serpapi.com/dashboard).
4. Your **API Key** will be displayed at the top of the dashboard (e.g., `1234567890abcdef...`).
5. Copy this key and paste it into your `.env` file as the value for `SERPAPI_KEY`:
   ```env
   SERPAPI_KEY=your-serpapi-key
   ```
6. Save the `.env` file.

**Note:** The free plan allows a limited number of searches per month. For higher usage, consider upgrading your SerpAPI plan.

### 5. Run the Development Server
```bash
npm run dev
```

The app will be available at [http://localhost:5001](http://localhost:5001).

## Additional Notes
- Make sure your database is set up and accessible via the `DATABASE_URL` in your `.env` file.
- You will need valid API keys for OpenAI, Anthropic, and Google Gemini to use all AI features.
- For more details, see the comments in `env.sample`.

---

If you have any questions or issues, please open an issue or contact the maintainer. 