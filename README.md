# 🌍 Multi-Modal Travel Planner

A cutting-edge web application that leverages the OpenAI GPT-4 with Vision API to create personalized travel itineraries by analyzing destination images and user preferences.

## 🎯 Project Overview

The Multi-Modal Travel Planner demonstrates the power of OpenAI's Vision capabilities:

1. **Image Understanding (Vision)** - Accurately identify destinations, landmarks, and events from uploaded images using GPT-4o
2. **Intelligent Planning** - Generate detailed, structured travel itineraries based on your preferences and constraints

### Key Features

- **Dual Input Processing**: Upload destination images + specify travel preferences
- **AI-Powered Analysis**: GPT-4o Vision identifies the location and understands constraints
- **Intelligent Recommendations**: Smart suggestions based on your preferences and constraints
- **Structured Itinerary**: Day-by-day breakdown with points of interest, activities, and recommendations
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Loading Indicators**: Visual feedback during processing

## 🚀 Quick Start

_For a one-command setup, see [QUICKSTART.md](QUICKSTART.md)._ 

### Prerequisites

- Python 3.8+
- OpenAI API Key (get it from [OpenAI Platform](https://platform.openai.com/api-keys))
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

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API Key
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
- Confirms the OpenAI API key is configured
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
- **Point of Interest Details**: Name, description, location, and practical tips
- **Dining Recommendations**: Restaurant suggestions with cuisine types
- **Travel Tips**: Practical advice for the destination

## 🏗️ Technical Architecture

### Backend (Flask)

```
app.py
├── /api/generate-itinerary (POST)
│   ├── Image upload handling
│   ├── OpenAI GPT-4o Vision API integration
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

### OpenAI API Integration

The application uses:
- **Model**: gpt-4o (multi-modal capable)
- **Vision**: Image understanding for destination identification
- **Chat Completions**: Structured JSON response generation
- **Configuration**: Optimized for travel planning output

## 📊 Example Scenario

### Input
- **Image**: Eiffel Tower photo
- **Preferences**: "2 days, family of 4, mix of landmarks and kid activities"

### Output
```
Summary: Paris, France | 2 Days | Family Trip

Day 1: Landmark Exploration
├── Morning: Eiffel Tower Visit
│   └── 💡 Tip: Book tickets in advance to skip the lines
├── Afternoon: Louvre Museum
│   └── 💡 Tip: Allow 3-4 hours for major highlights
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
          "tips": "Book tickets in advance to skip the lines"
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
OPENAI_API_KEY=your_api_key_here    # Required: Your OpenAI API key
FLASK_ENV=development               # Optional: Flask environment
FLASK_DEBUG=True                    # Optional: Debug mode
```

## 🐛 Troubleshooting

### "OPENAI_API_KEY environment variable is not set"
- Make sure you've created a `.env` file in the project root
- Add your OpenAI API key to the `.env` file
- Restart the Flask application

### Image upload not working
- Check file size (max 20MB)
- Verify file format (PNG, JPG, JPEG, GIF, WebP)
- Check browser console for errors

### API errors
- Verify your OpenAI API key is valid
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
- **API**: OpenAI GPT-4o with Vision
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

- OpenAI for GPT-4o with Vision capabilities
- Flask framework for backend development
- The open-source community

## 📞 Support

For issues, questions, or suggestions, please open an issue on GitHub or contact the development team.

---

**Made with ❤️ using OpenAI GPT-4o**
