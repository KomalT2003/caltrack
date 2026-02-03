@echo off
echo ==========================================
echo CalTrack - Starting Backend Server
echo ==========================================
echo.
echo Installing Python dependencies (this may take a few minutes)...
pip install -q flask flask-cors torch transformers accelerate
echo.
echo Starting server...
echo The model will download automatically on first run (~4GB)
echo.
python app.py
