# 🧪 Testing Changes Locally Before Deploying

## Option 1: Test Locally (Recommended)

### Step 1: Install Dependencies (if not already done)
```powershell
cd backend
pip install -r requirements.txt
```

### Step 2: Set Environment Variables
```powershell
# Set your API key (you've already done this)
$env:GEMINI_API_KEY="AIzaSyCjXzcduVOtU0bgDW22-oGnUpVqPyCgtBY"

# Set a secret key for sessions
$env:SECRET_KEY="test-secret-key-123"
```

### Step 3: Run the Server
```powershell
# Make sure you're in the backend directory
cd C:\Users\komalt\OneDrive` -` Microsoft\Desktop\caltrack\backend
python app.py
```

### Step 4: Open in Browser
1. Open your browser to: **http://localhost:8787**
2. Create a test account
3. Add multiple meals (10-15) to test scrolling
4. Check that:
   - ✅ "Add Meal" button doesn't wrap on mobile view (F12 → responsive mode → 375px width)
   - ✅ Meals list scrolls smoothly when many items exist
   - ✅ Meals don't go behind the bottom buttons
   - ✅ Login/logout works
   - ✅ Calendar shows data

### Step 5: Test Mobile View in Browser
Press **F12** to open DevTools:
- Click the device toolbar icon (or Ctrl+Shift+M)
- Select "iPhone 12 Pro" or set width to 375px
- Add 10+ meals and scroll through them
- Verify the scroll area stops before the buttons

---

## Option 2: Deploy to Render and Test

### Step 1: Commit and Push Changes
```powershell
# Make sure you're in the project root
cd C:\Users\komalt\OneDrive` -` Microsoft\Desktop\caltrack

# Check what changed
git status

# Add all changes
git add .

# Commit with a message
git commit -m "Fixed meal list overflow with scrolling"

# Push to GitHub
git push origin main
```

### Step 2: Deploy on Render

**Option A: Auto-Deploy (if enabled)**
- Render will automatically detect the push and deploy
- Wait 2-3 minutes
- Check your Render URL

**Option B: Manual Deploy**
1. Go to your Render dashboard
2. Click on your CalTrack service
3. Click "Manual Deploy" → "Deploy latest commit"
4. Wait for build to complete (2-3 minutes)
5. Click the URL at the top to open your deployed app

### Step 3: Test on Render
- Open your Render URL
- Create/login to account
- Add 10-15 meals
- Test on your phone or browser mobile view
- Verify scrolling works correctly

---

## 🐛 What Was Fixed

### Issue: Meal cards overflow behind buttons
**Before:**
- Many meals → list extends below screen
- Cards go behind "Add Meal" button
- No way to see bottom items

**After:**
- Meals list is scrollable (max-height based on screen size)
- Smooth custom scrollbar
- Header "Today's Meals" sticks to top while scrolling
- Clear separation from bottom buttons
- Works on all screen sizes

---

## 📱 Testing Checklist

- [ ] Open app on localhost:8787
- [ ] Login/create account works
- [ ] Add 1 meal - displays correctly
- [ ] Add 10+ meals - list becomes scrollable
- [ ] Scroll through meals - smooth scrolling
- [ ] Bottom buttons always visible
- [ ] Header sticks while scrolling
- [ ] Calendar view works
- [ ] Mobile view (375px width) - button doesn't wrap
- [ ] Clear all meals works

---

## 🚀 Quick Deploy Commands

```powershell
# All in one - commit and push
cd C:\Users\komalt\OneDrive` -` Microsoft\Desktop\caltrack
git add .
git commit -m "Fixed scrolling overflow issue"
git push origin main
```

Then wait for Render to auto-deploy (if enabled) or click "Manual Deploy" in dashboard.

---

## 💡 Pro Tip: Test Locally First!

Always test locally before deploying to avoid:
- ❌ Breaking production app
- ❌ Wasting deployment time (2-3 min per deploy)
- ❌ Using up free tier build minutes

Local testing is instant and you can iterate quickly!
