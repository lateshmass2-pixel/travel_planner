from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
import base64
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

genai.configure(api_key=GEMINI_API_KEY)

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
        
        # Create the prompt for Gemini with explicit instruction for search grounding
        system_prompt = """You are an expert travel planner. Analyze the provided image to identify the destination, 
landmark, or location shown. Then, using the user's preferences and constraints, create a detailed, actionable travel itinerary.

Important: Use Google Search results to find current, real-time information about:
- Operating hours
- Ticket prices
- Current weather
- Local reviews and ratings
- Best routes and transportation options
- Dining recommendations

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
          "search_fact": "Current fact from search (e.g., 'Open until 5 PM', 'Price: $25')",
          "google_search_link": "Link to relevant Google search result"
        }
      ]
    }
  ],
  "dining_recommendations": [
    {
      "name": "Restaurant name",
      "type": "Cuisine type",
      "description": "Description",
      "average_rating": "Rating with search fact"
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
3. Include current, real-time information from search results for each activity
4. Provide realistic budget estimates
5. Include practical travel tips
6. Format the response as the JSON structure specified"""

        # Use the Gemini model with vision capability and search grounding
        # Using gemini-2.0-flash with search grounding
        model = genai.GenerativeModel(
            model_name='gemini-2.0-flash',
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=4096
            )
        )
        
        # Enable search grounding via tools
        tools = [genai.types.Tool(
            google_search_retrieval=genai.types.GoogleSearchRetrieval()
        )]
        
        # Create the content with image and text
        response = model.generate_content(
            [
                system_prompt,
                {
                    "mime_type": mime_type,
                    "data": image_base64
                },
                user_prompt
            ],
            tools=tools
        )
        
        # Parse the response
        response_text = response.text
        
        # Try to extract JSON from the response
        try:
            # Look for JSON in the response
            import re
            json_match = re.search(r'\{[\s\S]*\}', response_text)
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
