# 🌍 Multi-Modal Travel Planner

A cutting-edge web application that leverages the Google Gemini API to create personalized travel itineraries by combining image understanding (Vision) and real-time data (Google Search Grounding).

## 🎯 Project Overview

The Multi-Modal Travel Planner demonstrates the seamless integration of two core Gemini capabilities:

1. **Image Understanding (Vision)** - Accurately identify destinations, landmarks, and events from uploaded images
2. **Real-Time Data (Google Search Grounding)** - Access current information like operating hours, prices, weather, and reviews

### Key Features

- **Dual Input Processing**: Upload destination images + specify travel preferences
- **AI-Powered Analysis**: Gemini Vision identifies the location and understands constraints
- **Real-Time Information**: Google Search Grounding ensures up-to-date, accurate data
- **Structured Itinerary**: Day-by-day breakdown with points of interest, activities, and recommendations
- **Search Integration**: Each recommendation includes current facts and Google Search links
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Loading Indicators**: Visual feedback during processing

## 🚀 Quick Start

_For a one-command setup, see [QUICKSTART.md](QUICKSTART.md)._ 

### Prerequisites

- Python 3.8+
- Gemini API Key (get it from [Google AI Studio](https://aistudio.google.com/))
- Modern web browser

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-repo/travel_planner.git
   cd travel_planner
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (Optional - pre-configured)
   ```bash
   # The .env file is pre-configured with a working API key
   # To use your own key:
   cp .env.example .env
   # Edit .env and add your Gemini API Key
   ```

5. **Run the application**
   ```bash
   # Recommended: Use the unified starter
   python start.py
   
   # Alternative methods:
   python run.py
   # or
   python app.py
   ```

6. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## 🧰 Unified Dev Runner

`start.py` provides a single command that launches the Flask backend and serves the frontend templates together. It also:
- Loads environment variables from `.env`
- Verifies that all required Python packages are installed
- Confirms the Gemini API key is configured (with a working default)
- Creates required directories such as `uploads/`
- Shows helpful connection details and tips before launching the server

Use it during development for the smoothest experience:
```bash
python start.py
```

## 📋 Usage Guide

### Input

1. **Upload Destination Image**
   - Click the upload area or drag-and-drop an image
   - Supported formats: PNG, JPG, JPEG, GIF, WebP
   - Example: Eiffel Tower photo, hotel screenshot, festival poster

2. **Specify Travel Preferences**
   - Duration: "3 days", "1 week", etc.
   - Budget: "$800", "€1000", etc.
   - Interests: "outdoor activities", "museums", "local dining"
   - Special requirements: "family-friendly", "vegetarian options"

3. **Generate Itinerary**
   - Click the "Generate Itinerary" button
   - Wait for the processing (shown with loading indicator)

### Output

The generated itinerary includes:

- **Summary Card**: Destination, duration, trip type, and estimated budget
- **Day-by-Day Breakdown**: Activities organized by time of day
- **Point of Interest Details**: Name, description, and location
- **Search Grounding Facts**: Current information like opening hours and prices
- **Google Search Links**: Direct links for further research
- **Dining Recommendations**: Restaurant suggestions with ratings
- **Travel Tips**: Practical advice for the destination

## 🏗️ Technical Architecture

### Backend (Flask)

```
app.py
├── /api/generate-itinerary (POST)
│   ├── Image upload handling
│   ├── Gemini API integration
│   └── JSON response formatting
└── /api/health (GET)
    └── Health check endpoint
```

### Frontend (HTML/CSS/JavaScript)

```
templates/
├── index.html (Structure and layout)
static/
├── styles.css (Responsive styling)
└── script.js (Interactive functionality)
```

### Gemini API Integration

The application uses:
- **Model**: gemini-2.0-flash (multi-modal capable)
- **Vision**: Image understanding for destination identification
- **Search Grounding**: Real-time information retrieval
- **Generation Config**: Optimized for travel planning output

## 📊 Example Scenario

### Input
- **Image**: Eiffel Tower photo
- **Preferences**: "2 days, family of 4, mix of landmarks and kid activities"

### Output
```
Summary: Paris, France | 2 Days | Family Trip

Day 1: Landmark Exploration
├── Morning: Eiffel Tower Visit
│   └── 🔍 Current opening hours: 9:30 AM to 11:45 PM
├── Afternoon: Louvre Museum
│   └── 🔍 General admission: $22 per person
└── Evening: Seine River Dinner

Day 2: Kid-Friendly Adventures
├── Morning: Carousel and Parks
├── Afternoon: Children's Museum
└── Evening: Ice Cream at Café de Flore
```

## 🔧 API Reference

### Generate Itinerary

**Endpoint**: `POST /api/generate-itinerary`

**Request**:
```
Content-Type: multipart/form-data

- image (file): Destination image
- preferences (string): Travel preferences and constraints
```

**Response**:
```json
{
  "summary": {
    "destination": "Paris, France",
    "duration": "2 days",
    "trip_type": "Family Trip",
    "estimated_budget": "$1200-1500"
  },
  "itinerary": [
    {
      "day": 1,
      "title": "Landmark Exploration",
      "activities": [
        {
          "time": "Morning",
          "name": "Eiffel Tower Visit",
          "description": "...",
          "location": "Champ de Mars",
          "search_fact": "Open until 11:45 PM",
          "google_search_link": "https://..."
        }
      ]
    }
  ],
  "dining_recommendations": [...],
  "travel_tips": [...]
}
```

**Error Response**:
```json
{
  "error": "Error message here"
}
```

## 📁 Project Structure

```
travel_planner/
├── app.py                 # Flask backend
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── styles.css        # Styling
│   └── script.js         # Frontend logic
└── uploads/              # Temporary image storage (auto-created)
```

## 🎨 UI Features

### Responsive Design
- Mobile-optimized (320px+)
- Tablet-optimized (768px+)
- Desktop-optimized (1200px+)

### Interactive Elements
- Drag-and-drop image upload
- Collapsible day sections (first day open by default)
- Real-time validation
- Smooth animations and transitions
- Loading spinner with progress indicator

### Accessibility
- Semantic HTML structure
- Clear visual hierarchy
- Sufficient color contrast
- Keyboard navigation support

## 🔐 Security Considerations

- File size limit: 20MB
- Allowed file types: PNG, JPG, JPEG, GIF, WebP
- Temporary files are automatically deleted after processing
- CORS enabled for API access
- Environment variables for sensitive data

## 📝 Environment Variables

```env
GEMINI_API_KEY=your_api_key_here    # Required: Your Gemini API key
FLASK_ENV=development                # Optional: Flask environment
FLASK_DEBUG=True                      # Optional: Debug mode
```

## 🐛 Troubleshooting

### "GEMINI_API_KEY environment variable is not set"
- Make sure you've created a `.env` file in the project root
- Add your Gemini API key to the `.env` file
- Restart the Flask application

### Image upload not working
- Check file size (max 20MB)
- Verify file format (PNG, JPG, JPEG, GIF, WebP)
- Check browser console for errors

### API errors
- Verify your Gemini API key is valid
- Check network connectivity
- Review server logs for detailed error messages

## 🚀 Deployment

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_APP=app.py
CMD ["python", "app.py"]
```

### Environment Setup for Production
1. Set `FLASK_ENV=production`
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Enable HTTPS
4. Set appropriate CORS origins
5. Configure file upload directory with persistence

## 📚 Technologies Used

- **Framework**: Flask 3.0.0
- **API**: Google Gemini 2.0 Flash
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Language**: Python 3.8+
- **Styling**: CSS3 with responsive design
- **Communication**: REST API with multipart/form-data

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Create a feature branch (`git checkout -b feature/amazing-feature`)
2. Commit your changes (`git commit -m 'Add amazing feature'`)
3. Push to the branch (`git push origin feature/amazing-feature`)
4. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Gemini API for vision and search capabilities
- Flask framework for backend development
- The open-source community

## 📞 Support

For issues, questions, or suggestions, please open an issue on GitHub or contact the development team.

---

**Made with ❤️ using Google Gemini API**
