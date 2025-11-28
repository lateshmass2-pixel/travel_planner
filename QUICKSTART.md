# 🚀 Quick Start Guide

Get the Multi-Modal Travel Planner running in **3 simple steps**!

## ⚡ Super Quick Start (1 Command)

```bash
python start.py
```

That's it! The application will:
- ✓ Check all dependencies
- ✓ Verify API configuration
- ✓ Create necessary directories
- ✓ Start the server at http://localhost:5000

## 📋 Detailed Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python start.py
```

### Step 3: Open Your Browser
Navigate to: **http://localhost:5000**

## 🎯 Usage

1. **Upload Image**: Drag & drop or click to upload a destination image
2. **Enter Preferences**: Add your travel preferences (duration, budget, interests)
3. **Generate**: Click "Generate Itinerary" and get your personalized travel plan!

## 🔧 Alternative Run Methods

### Using the simplified runner:
```bash
python run.py
```

### Using Flask directly:
```bash
python app.py
```

## 🌐 Access Points

- **Local**: http://localhost:5000
- **Network**: http://0.0.0.0:5000

## 🔑 API Key Configuration

You need to configure your OpenAI API key:

1. Get your key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create/update the `.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
3. Restart the server

## 🐛 Troubleshooting

### Dependencies Missing
```bash
pip install -r requirements.txt
```

### Port Already in Use
Change the port in `.env`:
```
PORT=8080
```

### Image Upload Issues
- Max file size: 20MB
- Supported formats: PNG, JPG, JPEG, GIF, WebP

## 💡 Tips

- Use clear destination images (landmarks, hotels, attractions)
- Be specific with preferences (e.g., "3 days, $800, family-friendly")
- Review the generated itinerary for practical tips and recommendations
- GPT-4o provides intelligent suggestions based on the image and your preferences

## 🛑 Stop the Server

Press `CTRL+C` in the terminal

---

**Ready to plan your next adventure? Let's go! 🌍✈️**
