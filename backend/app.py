import os
import json
import re
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)

# Use Google Gemini API for fast, accurate inference
# Get your free API key from: https://aistudio.google.com/app/apikey
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

def estimate_with_gemini(food_description):
    """Use Gemini API with Google Search for accurate calorie data"""
    if not GEMINI_API_KEY:
        raise Exception("No API key - using fallback")
    
    import google.generativeai as genai
    
    genai.configure(api_key=GEMINI_API_KEY)
    
    # List available models and use the first one that supports generateContent
    try:
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        if not available_models:
            raise Exception("No models support generateContent")
        
        # Use the first available model
        model_name = available_models[0].replace('models/', '')
        print(f"📊 Using model: {model_name}")
        model = genai.GenerativeModel(model_name)
        
    except Exception as e:
        print(f"⚠️  Model listing failed: {e}, trying default")
        # Fallback to common model names
        try:
            model = genai.GenerativeModel('gemini-1.5-pro-latest')
        except:
            try:
                model = genai.GenerativeModel('gemini-1.0-pro')
            except:
                raise Exception("Could not initialize any model")
    
    prompt = f"""You are a nutrition expert with access to real-time data. Estimate calories for: "{food_description}"

IMPORTANT INSTRUCTIONS:
1. For BRANDED products (like "Rite Brite protein bar", "Maggi", "KitKat", etc.), use your knowledge of actual nutritional information from verified sources.
2. For quantities like "half", divide the standard serving by 2.
3. For vague quantities, use typical serving sizes.
4. Be PRECISE - use real data from your knowledge base.
5. If you know the exact brand, use that brand's specific nutritional information.

Respond with ONLY a JSON object in this exact format:
{{"calories": <number>, "notes": "<brief note about source or serving size>"}}

No markdown, no code blocks, no extra text - just the JSON object."""
    
    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.3,
                "max_output_tokens": 300,
            }
        )
        
        print(f"🤖 Raw Gemini response: {response.text[:200]}...")
        
        result = extract_json(response.text)
        if not result:
            print(f"❌ Could not parse JSON from: {response.text}")
            raise Exception("Could not parse JSON from response")
        
        print(f"✅ Parsed result: {result}")
        return result
        
    except Exception as e:
        print(f"Gemini API error: {e}")
        raise

def estimate_simple(food_description):
    """Simple rule-based calorie estimation (fallback)"""
    text = food_description.lower()
    
    # Common foods database (approximate calories)
    food_db = {
        "rice": 130, "dal": 100, "chawal": 130, "roti": 70, "chapati": 70,
        "paratha": 150, "naan": 150, "bread": 80, "egg": 70, "chicken": 165,
        "paneer": 260, "milk": 60, "tea": 5, "coffee": 5, "apple": 95,
        "banana": 105, "orange": 60, "samosa": 150, "pakora": 120,
        "biryani": 300, "curry": 150, "sabzi": 80, "dahi": 60, "curd": 60,
        "butter": 100, "ghee": 120, "oil": 120, "sugar": 16, "chocolate": 50,
        "biscuit": 50, "cookie": 50, "cake": 200, "pizza": 250, "burger": 300,
        "pasta": 200, "sandwich": 150, "salad": 50, "soup": 80
    }
    
    # Extract quantities
    spoons = re.search(r'(\d+)\s*(?:spoon|tbsp|tablespoon)', text)
    cups = re.search(r'(\d+)\s*(?:cup|bowl)', text)
    pieces = re.search(r'(\d+)\s*(?:piece|pcs|slice)', text)
    
    calories = 0
    matched_foods = []
    
    for food, cal_per_serving in food_db.items():
        if food in text:
            quantity = 1
            if spoons:
                quantity = int(spoons.group(1)) * 0.5  # spoons are smaller portions
            elif cups:
                quantity = int(cups.group(1))
            elif pieces:
                quantity = int(pieces.group(1))
            
            calories += cal_per_serving * quantity
            matched_foods.append(food)
    
    if calories == 0:
        # Default estimation
        calories = 200
        notes = "Rough estimate - unable to identify specific foods"
    else:
        notes = f"Estimated from: {', '.join(matched_foods)}"
    
    return {"calories": int(calories), "notes": notes}

def extract_json(text):
    """Extract JSON object from model output"""
    if not text:
        return None
    
    text = text.strip()
    
    # Remove markdown code blocks
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    
    # Look for JSON object with better regex
    match = re.search(r'\{[^{}]*"calories"[^{}]*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except:
            pass
    
    # Try parsing the whole text
    try:
        return json.loads(text)
    except:
        pass
    
    # Look for any JSON-like structure
    match = re.search(r'\{.*?\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except:
            pass
    
    # Fallback: look for numbers and create JSON
    cal_match = re.search(r'(\d+)\s*(?:calories|kcal|cal)', text, re.IGNORECASE)
    if cal_match:
        return {"calories": int(cal_match.group(1)), "notes": "Parsed from text"}
    
    # Last resort: look for any number
    num_match = re.search(r'\b(\d{2,4})\b', text)
    if num_match:
        return {"calories": int(num_match.group(1)), "notes": "Estimated"}
    
    return None

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/api/estimate", methods=["POST"])
def estimate_calories():
    try:
        data = request.get_json()
        text = data.get("text", "").strip()
        
        if not text:
            return jsonify({"error": "Missing 'text' field"}), 400
        
        # Try Gemini API first, fallback to simple estimation
        try:
            result = estimate_with_gemini(text)
            print(f"✅ Gemini response: {result}")
        except Exception as gemini_error:
            print(f"⚠️  Gemini failed: {gemini_error}, using fallback")
            result = estimate_simple(text)
            result["notes"] = result.get("notes", "") + " (AI unavailable)"
        
        if not result or "calories" not in result:
            return jsonify({
                "error": "Could not parse calorie estimate",
                "details": "Please try again with a clearer description"
            }), 502
        
        calories = int(result.get("calories", 0))
        notes = result.get("notes", "")
        
        return jsonify({
            "calories": max(0, calories),
            "notes": notes
        })
        
    except Exception as e:
        print(f"❌ Error in /api/estimate: {e}")
        # Fallback to simple estimation on any error
        try:
            result = estimate_simple(text)
            return jsonify({
                "calories": result["calories"],
                "notes": result["notes"] + " (offline mode)"
            })
        except:
            return jsonify({
                "error": "Failed to estimate calories",
                "details": str(e)
            }), 500
        result = extract_json(generated_text)
        
        if not result or "calories" not in result:
            return jsonify({
                "error": "Could not parse calorie estimate from model",
                "details": generated_text[:500]
            }), 502
        
        calories = int(result.get("calories", 0))
        notes = result.get("notes", "")
        
        return jsonify({
            "calories": max(0, calories),
            "notes": notes
        })
        
    except Exception as e:
        print(f"Error in /api/estimate: {e}")
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8787))
    
    print(f"\n{'='*60}")
    if GEMINI_API_KEY:
        print(f"✅ Google Gemini API configured")
        print(f"   API Key: {GEMINI_API_KEY[:20]}...")
        
        # List available models
        try:
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_API_KEY)
            print(f"\n📋 Available models:")
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    print(f"   ✓ {m.name}")
        except Exception as e:
            print(f"   ⚠️  Could not list models: {e}")
        
    else:
        print(f"⚠️  No GEMINI_API_KEY - using offline fallback")
        print(f"   Get free key: https://aistudio.google.com/app/apikey")
        print(f"   Set it: $env:GEMINI_API_KEY='your-key-here'")
    
    print(f"\n🚀 CalTrack server: http://localhost:{port}")
    print(f"{'='*60}\n")
    
    app.run(host="0.0.0.0", port=port, debug=True)
