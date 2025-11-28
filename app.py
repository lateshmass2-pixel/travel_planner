from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
import base64
from dotenv import load_dotenv
import json
import re

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure OpenAI API
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set. Please set it in your .env file or deployment environment.")

client = OpenAI(api_key=OPENAI_API_KEY)

# Configuration for file uploads
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def encode_image_to_base64(image_path):
    with open(image_path, 'rb') as image_file:
        return base64.standard_b64encode(image_file.read()).decode('utf-8')


def get_image_mime_type(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    mime_types = {
        'png': 'image/png',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'gif': 'image/gif',
        'webp': 'image/webp'
    }
    return mime_types.get(ext, 'image/jpeg')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/generate-itinerary', methods=['POST'])
def generate_itinerary():
    try:
        # Get text input
        text_input = request.form.get('preferences', '')
        
        if not text_input:
            return jsonify({'error': 'Please provide travel preferences'}), 400
        
        # Check if image is provided
        image_file = request.files.get('image')
        
        if not image_file:
            return jsonify({'error': 'Please upload an image of your destination'}), 400
        
        if not allowed_file(image_file.filename):
            return jsonify({'error': 'Invalid file type. Please upload PNG, JPG, GIF, or WebP'}), 400
        
        # Save the uploaded image
        import uuid
        filename = f"{uuid.uuid4()}_{image_file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(filepath)
        
        # Encode image to base64
        image_base64 = encode_image_to_base64(filepath)
        mime_type = get_image_mime_type(image_file.filename)
        
        # Create the prompt for OpenAI with vision capability
        system_prompt = """You are an expert travel planner. Analyze the provided image to identify the destination, 
landmark, or location shown. Then, using the user's preferences and constraints, create a detailed, actionable travel itinerary.

Format your response as a JSON object with the following structure:
{
  "summary": {
    "destination": "City, Country",
    "duration": "X days/nights",
    "trip_type": "Type of trip (e.g., Family, Adventure, Cultural)",
    "estimated_budget": "Budget estimate"
  },
  "itinerary": [
    {
      "day": 1,
      "title": "Day title",
      "activities": [
        {
          "time": "Morning/Afternoon/Evening",
          "name": "Activity name",
          "description": "Description",
          "location": "Location",
          "tips": "Practical tips for this activity"
        }
      ]
    }
  ],
  "dining_recommendations": [
    {
      "name": "Restaurant name",
      "type": "Cuisine type",
      "description": "Description",
      "price_range": "Budget range"
    }
  ],
  "travel_tips": [
    "Tip 1",
    "Tip 2"
  ]
}"""

        user_prompt = f"""Please create a detailed travel itinerary based on this image of my destination and my travel preferences:

User Preferences and Constraints:
{text_input}

Please:
1. Identify the destination from the image
2. Create a structured day-by-day itinerary
3. Provide realistic budget estimates
4. Include practical travel tips
5. Format the response as valid JSON only (no markdown formatting)"""

        # Use OpenAI's GPT-4 Vision API
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=4096,
            temperature=0.7
        )
        
        # Parse the response from OpenAI
        response_text = response.choices[0].message.content
        
        # Try to extract JSON from the response
        try:
            # Remove markdown code blocks if present
            cleaned_text = re.sub(r'```json\s*', '', response_text)
            cleaned_text = re.sub(r'```\s*$', '', cleaned_text)
            cleaned_text = cleaned_text.strip()
            
            json_match = re.search(r'\{[\s\S]*\}', cleaned_text)
            if json_match:
                itinerary_data = json.loads(json_match.group())
            else:
                # If no JSON found, return the raw response
                itinerary_data = {
                    "summary": {
                        "destination": "Destination identified",
                        "duration": "Multiple days",
                        "trip_type": "Travel",
                        "estimated_budget": "Varies"
                    },
                    "content": response_text
                }
        except json.JSONDecodeError:
            itinerary_data = {
                "summary": {
                    "destination": "Destination identified",
                    "duration": "Multiple days",
                    "trip_type": "Travel",
                    "estimated_budget": "Varies"
                },
                "content": response_text
            }
        
        # Clean up the uploaded file
        try:
            os.remove(filepath)
        except:
            pass
        
        return jsonify(itinerary_data)
    
    except Exception as e:
        return jsonify({'error': f'Error generating itinerary: {str(e)}'}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Travel Planner API is running'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
