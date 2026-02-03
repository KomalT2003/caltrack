# 🚀 CalTrack Deployment Guide (Updated with Login System)

## 📋 What Changed

### New Features:
1. ✅ **Fixed mobile button layout** - "Add Meal" button no longer wraps on phones
2. ✅ **User login system** - Simple username/password authentication
3. ✅ **Cloud database storage** - SQLite database for persistent data across devices
4. ✅ **Data sync** - Your meals are accessible from any device/browser after login

### Files Modified:
- `frontend/index.html` - Added login UI and API integration
- `backend/app.py` - Added auth endpoints and meal management APIs
- `backend/database.py` - NEW: Database layer for users and meals
- `.gitignore` - Added `*.db` to exclude database file

## 🚀 Deployment to Render

### Step 1: Push Changes to GitHub

```bash
# Stage all changes
git add .

# Commit with message
git commit -m "Added login system and database storage"

# Push to GitHub
git push origin main
```

### Step 2: Configure Render

Go to your Render dashboard and update/create your web service:

**Build Command:**
```
pip install -r backend/requirements.txt
```

**Start Command:**
```
cd backend && python app.py
```

**Environment Variables** (add these in Render dashboard):
```
GEMINI_API_KEY = AIzaSyCjXzcduVOtU0bgDW22-oGnUpVqPyCgtBY
SECRET_KEY = your-random-secret-key-change-this-in-production
PORT = 8787
```

> ⚠️ **Important**: Change `SECRET_KEY` to a random string for security!

### Step 3: Deploy

- Click "Manual Deploy" → "Deploy latest commit"
- Or: Render auto-deploys on git push (if enabled)
- Wait 2-3 minutes for deployment

### Step 4: Test

1. Open your Render URL (e.g., `https://caltrack-xyz.onrender.com`)
2. You'll see the login screen
3. Click "Create Account"
4. Enter username and password
5. Start adding meals!

## 📱 Features After Login

- **Add meals** - Voice or text input with AI estimation
- **View history** - All your meals saved in the database
- **Calendar view** - Monthly calorie totals
- **Cross-device sync** - Login from any device to see your data
- **Clear today** - Remove all meals for current day

## 🗄️ Database Details

The app uses SQLite (file: `backend/caltrack.db`):

**Tables:**
- `users` - User accounts (id, username, password_hash)
- `meals` - Meal logs (id, user_id, date, food_description, calories, notes)

**Note**: On Render's free tier, the database will reset on deployment restarts. For production:
- Use Render's Postgres addon, OR
- Use external database like PostgreSQL/MySQL

## 🔐 Security Notes

- Passwords are hashed (SHA-256)
- Sessions use Flask session management
- API requires authentication for meal operations
- API key (GEMINI_API_KEY) is server-side only

## 🐛 Troubleshooting

### Issue: "Module not found" error
- **Solution**: Make sure Build Command includes full path: `pip install -r backend/requirements.txt`

### Issue: Database resets on restart
- **Expected** on Render free tier (uses ephemeral filesystem)
- **Solution**: Upgrade to paid plan with persistent storage, or use external database

### Issue: Login not working
- **Check**: Is SECRET_KEY set in environment variables?
- **Check**: Is backend URL correct? (should match your Render URL)

### Issue: Add Meal button still wrapping
- **Clear browser cache** and hard refresh (Ctrl+Shift+R)

### Issue: Can't see data from other browser
- **Expected**: You must login with the same username/password
- Each user account has separate data

## 📊 API Endpoints

### Authentication
- `POST /api/auth/register` - Create new account
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `GET /api/auth/check` - Check if logged in

### Meals
- `GET /api/meals?date=YYYY-MM-DD` - Get meals for date
- `POST /api/meals` - Add new meal
- `DELETE /api/meals/<id>` - Delete meal
- `DELETE /api/meals/clear?date=YYYY-MM-DD` - Clear all meals for date
- `GET /api/meals/month?year=YYYY&month=MM` - Get monthly summary

### AI
- `POST /api/estimate` - Estimate calories from text (no auth required)

## 🎯 Next Steps (Optional Improvements)

1. **Email verification** - Verify user emails on registration
2. **Password reset** - "Forgot password" functionality
3. **Export data** - Download meals as CSV/JSON
4. **Goals tracking** - Set daily calorie goals
5. **Charts** - Visualize calorie trends over time
6. **Social features** - Share meals with friends

## 📧 Need Help?

- Check Render logs: Dashboard → Your Service → Logs
- Test API locally first: `cd backend && python app.py`
- Open browser console (F12) to see frontend errors

---

**Deployment Status**: Ready to deploy ✅

**Required Environment Variables**:
- `GEMINI_API_KEY` ✅
- `SECRET_KEY` ⚠️ (set a random value)
- `PORT` ✅ (optional, defaults to 8787)
