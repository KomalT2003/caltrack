# 🚀 Quick Deploy Guide

## Fastest Option: Railway (1 minute)

1. Go to https://railway.app
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Connect your GitHub and select this repo
5. Add environment variable:
   - Key: `GEMINI_API_KEY`
   - Value: Your API key from https://aistudio.google.com/app/apikey
6. Railway auto-deploys! 🎉

Your app will be live at: `https://your-app.up.railway.app`

---

## Alternative: Render (2 minutes)

1. Go to https://render.com
2. New → Web Service
3. Connect GitHub repo
4. Settings:
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && python app.py`
5. Add Environment Variable:
   - `GEMINI_API_KEY` = your key
6. Click "Create Web Service"

Live at: `https://your-app.onrender.com`

---

## Local Network (Share with friends on same WiFi)

```bash
cd backend
python app.py
```

Find your computer's IP:
```bash
ipconfig  # Windows
ifconfig  # Mac/Linux
```

Share: `http://YOUR_IP:8787`

---

## Need Help?

- Get free Gemini API key: https://aistudio.google.com/app/apikey
- Check DEPLOY.md for detailed instructions
- Backend must be running for AI features to work
