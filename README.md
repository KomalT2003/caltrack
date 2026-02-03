# CalTrack - AI-Powered Calorie Tracking App

A phone-style calorie tracking web app that uses Microsoft's Phi-3.5-mini-instruct model to estimate calories from natural language food descriptions.

## Features

- 🎤 **Voice & Text Input**: Type or speak what you ate
- 🤖 **AI Calorie Estimation**: Powered by Phi-3.5-mini-instruct via transformers
- 🌅 **Time-of-Day Themes**: Background changes based on morning/day/evening/night
- 📱 **Mobile-First Design**: Optimized for phone screens
- 💾 **Local Storage**: Your data stays in your browser

## Requirements

- Python 3.9+
- CUDA-capable GPU (recommended) or CPU
- ~7GB disk space for the model

## Installation

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Model Download

The first run will automatically download the Phi-3.5-mini-instruct model (~4GB). This may take 5-15 minutes depending on your internet connection.

## Running the App

### Start the Backend Server

```bash
cd backend
python app.py
```

The server will:
1. Load the Phi-3.5-mini-instruct model (this takes 30-60 seconds on first run)
2. Start on `http://localhost:8787`
3. Serve both the API and frontend

### Access the App

Open your browser to: **http://localhost:8787**

## Usage

1. **Add a Meal**:
   - Click "+ Add Meal" button
   - Type (e.g., "4 spoons of dal chawal") or click 🎤 to speak
   - Click "✨ Estimate Calories"
   - Click "Add to Today"

2. **View Today's Meals**:
   - See all meals listed with name (left) and calories (right)
   - Total calories shown in the header

3. **Clear Data**:
   - Click "Clear All" to reset today's meals

## API Endpoint

### POST `/api/estimate`

Estimate calories from a food description.

**Request:**
```json
{
  "text": "4 spoons of dal chawal"
}
```

**Response:**
```json
{
  "calories": 320,
  "notes": "Typical portion size assumed"
}
```

## Troubleshooting

### Model Loading Issues

If you see "Model not loaded":
- Wait 30-60 seconds for model initialization
- Check console for error messages
- Ensure you have enough RAM (8GB+ recommended)

### GPU/CUDA Issues

If CUDA is not available:
- The app will automatically fall back to CPU
- Inference will be slower (5-15 seconds per estimate)
- Consider reducing `max_new_tokens` in `app.py` for faster CPU inference

### Speech Recognition Not Working

- Speech recognition uses browser Web Speech API (Chrome/Edge only)
- Requires HTTPS or localhost
- Grant microphone permissions when prompted

## Architecture

- **Frontend**: Vanilla HTML/CSS/JavaScript with Tailwind CSS
- **Backend**: Flask + HuggingFace Transformers
- **Model**: microsoft/Phi-3.5-mini-instruct (3.8B parameters)
- **Storage**: Browser localStorage (client-side)

## Performance Notes

- **First request**: 2-5 seconds (model warmup)
- **Subsequent requests**: 1-3 seconds on GPU, 5-15 seconds on CPU
- **Memory usage**: ~4-6GB RAM with model loaded

## License

MIT License - Feel free to modify and use for your projects!
