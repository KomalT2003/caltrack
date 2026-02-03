# CalTrack - AI-Powered Calorie Tracker

A sleek, modern calorie tracking app with AI-powered estimation using Google Gemini.

## 🚀 Quick Deploy

### Option 1: Deploy to Vercel (Recommended - Free)

#### Frontend + Backend Together:

1. **Install Vercel CLI:**
```bash
npm install -g vercel
```

2. **Deploy:**
```bash
cd caltrack
vercel
```

3. **Set Environment Variable:**
In Vercel dashboard, add:
- `GEMINI_API_KEY` = your API key from https://aistudio.google.com/app/apikey

### Option 2: Deploy Separately

#### Frontend (Netlify/Vercel/GitHub Pages):

**Deploy to Netlify:**
```bash
cd frontend
# Drag and drop the folder to https://app.netlify.com/drop
```

**Or use Netlify CLI:**
```bash
npm install -g netlify-cli
cd frontend
netlify deploy --prod
```

#### Backend (Railway/Render/Heroku):

**Deploy to Railway:**
1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub"
3. Select your repo
4. Add environment variable: `GEMINI_API_KEY`
5. Railway auto-detects Python and runs `python app.py`

**Deploy to Render:**
1. Go to https://render.com
2. New Web Service → Connect GitHub
3. Build command: `pip install -r requirements.txt`
4. Start command: `python app.py`
5. Add environment variable: `GEMINI_API_KEY`

### Option 3: Local Network Access

Make it accessible on your local network:

```bash
cd backend
python app.py
# Server runs on http://0.0.0.0:8787
# Access from any device on same WiFi: http://YOUR_IP:8787
```

Find your IP:
```bash
# Windows
ipconfig
# Look for IPv4 Address

# Mac/Linux
ifconfig | grep inet
```

## 📱 Features

- ✨ AI calorie estimation with Google Gemini
- 📅 Monthly calendar view
- 🎤 Voice input support
- 💾 Local storage (privacy-first)
- 🌍 Branded product recognition
- 🎨 Time-of-day themed backgrounds
- 📊 Daily meal tracking

## 🔑 Setup

1. **Get Gemini API Key** (Free):
   - Visit: https://aistudio.google.com/app/apikey
   - Create API key
   - Set environment variable:
     ```bash
     # Windows
     $env:GEMINI_API_KEY="your-key-here"
     
     # Mac/Linux
     export GEMINI_API_KEY="your-key-here"
     ```

2. **Install Dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

3. **Run:**
```bash
python app.py
```

4. **Open:** http://localhost:8787

## 📦 Tech Stack

- **Frontend**: Vanilla JS + Tailwind CSS
- **Backend**: Flask + Google Gemini API
- **Storage**: Browser localStorage
- **AI**: Google Gemini 2.5-flash

## 🌐 Environment Variables

- `GEMINI_API_KEY` - Your Google Gemini API key (required for AI features)
- `PORT` - Server port (default: 8787)

## 📝 License

MIT License - feel free to use and modify!
