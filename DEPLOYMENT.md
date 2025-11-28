# Multi-Modal Travel Planner - Deployment Guide

## 🚀 Quick Start (Development)

### Step 1: Prerequisites
- Python 3.8 or higher
- Gemini API key from [Google AI Studio](https://aistudio.google.com/)
- Modern web browser

### Step 2: Setup

```bash
# Clone the repository
git clone <repository-url>
cd travel_planner

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### Step 3: Run Application

```bash
# Using Flask directly
python app.py

# OR using the run script
python run.py
```

The application will be available at `http://localhost:5000`

## 🔧 Configuration

### Required Environment Variables
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### Optional Environment Variables
```env
FLASK_ENV=development        # development or production
FLASK_DEBUG=True            # Enable debug mode
PORT=5000                   # Server port (default: 5000)
```

## 📦 Dependencies

### Production
- Flask 3.0.0
- Flask-CORS 4.0.0
- google-generativeai 0.3.0
- python-dotenv 1.0.0
- Werkzeug 3.0.1

### Development (Optional)
```bash
pip install -r requirements-dev.txt
```

Includes: pytest, pytest-cov, black, flake8, mypy, pylint

## 🌐 Deployment Options

### 1. Local Development
```bash
python app.py
```
- Runs on `http://localhost:5000`
- Debug mode enabled
- Auto-reload on file changes

### 2. Production with Gunicorn
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 3. Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV FLASK_APP=app.py
ENV GEMINI_API_KEY=$GEMINI_API_KEY
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t travel-planner .
docker run -e GEMINI_API_KEY=your_key -p 5000:5000 travel-planner
```

### 4. Cloud Deployment (Google Cloud)

```bash
# Deploy to Google Cloud Run
gcloud run deploy travel-planner \
  --source . \
  --region us-central1 \
  --set-env-vars GEMINI_API_KEY=your_key \
  --platform managed
```

### 5. Heroku Deployment

Create `Procfile`:
```
web: gunicorn app:app
```

Create `runtime.txt`:
```
python-3.11.7
```

Deploy:
```bash
heroku create travel-planner
heroku config:set GEMINI_API_KEY=your_key
git push heroku main
```

## 📁 Directory Structure

```
travel_planner/
├── app.py                    # Main Flask application
├── config.py                 # Configuration
├── run.py                    # Entry point
├── requirements.txt          # Dependencies
├── .env.example             # Environment template
├── .gitignore               # Git ignore file
├── templates/
│   └── index.html           # Web interface
├── static/
│   ├── styles.css           # Styling
│   └── script.js            # Frontend logic
├── uploads/                 # Temporary files (created at runtime)
└── README.md                # Documentation
```

## 🔐 Security Configuration

### Production Checklist
- [ ] Set `FLASK_ENV=production`
- [ ] Use strong `SECRET_KEY`
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS appropriately
- [ ] Use environment variables for secrets
- [ ] Set up proper logging
- [ ] Configure firewall rules
- [ ] Use a production WSGI server (Gunicorn, uWSGI)
- [ ] Set up monitoring and alerts
- [ ] Configure backup strategy for uploaded files

### Environment Security
```bash
# Generate strong secret key
python -c "import secrets; print(secrets.token_hex(32))"

# Add to .env
SECRET_KEY=your_generated_key_here
```

## 🧪 Testing

### Manual Testing
1. Open `http://localhost:5000` in browser
2. Upload an image (e.g., Eiffel Tower)
3. Enter preferences (e.g., "2 days, family trip")
4. Click "Generate Itinerary"
5. Verify structured output appears

### API Testing
```bash
# Health check
curl http://localhost:5000/api/health

# Generate itinerary
curl -X POST http://localhost:5000/api/generate-itinerary \
  -F "image=@/path/to/image.jpg" \
  -F "preferences=2 days in Paris"
```

## 🐛 Troubleshooting

### Issue: "GEMINI_API_KEY not set"
**Solution**: 
1. Create .env file
2. Add your Gemini API key
3. Restart the application

### Issue: Image upload fails
**Solution**: 
1. Check file size (max 20MB)
2. Verify format (PNG, JPG, JPEG, GIF, WebP)
3. Check disk space in uploads directory

### Issue: API returns errors
**Solution**: 
1. Verify API key is valid
2. Check internet connectivity
3. Review server logs
4. Check rate limiting

### Issue: Port 5000 already in use
**Solution**: 
```bash
# Run on different port
PORT=5001 python app.py

# Or kill process using port 5000
lsof -ti:5000 | xargs kill -9  # Linux/Mac
netstat -ano | findstr :5000    # Windows
```

## 📊 Performance Optimization

### Frontend Optimization
- Minify CSS and JavaScript
- Enable GZIP compression
- Use CDN for static files
- Cache static assets

### Backend Optimization
- Use connection pooling
- Cache API responses
- Implement rate limiting
- Monitor response times

### Sample Nginx Configuration
```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_cache_bypass $http_upgrade;
    }

    location /static/ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

## 📈 Monitoring

### Log Files
- Application logs are printed to console
- Implement proper logging in production
- Configure log rotation

### Metrics to Monitor
- Response time
- Error rate
- API usage
- File upload size
- System resources

## 🔄 Maintenance

### Regular Tasks
1. Update dependencies: `pip install --upgrade -r requirements.txt`
2. Monitor disk usage in uploads directory
3. Review and clean up temporary files
4. Update Gemini API integration if needed
5. Monitor API rate limits

### Backup Strategy
- Back up environment configuration
- Archive uploads periodically
- Version control code changes
- Document API changes

## 📞 Support

For deployment issues:
1. Check logs: `tail -f app.log`
2. Verify configuration: `env | grep GEMINI`
3. Test API: `curl http://localhost:5000/api/health`
4. Review documentation in README.md

## ✅ Deployment Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] .env file configured
- [ ] GEMINI_API_KEY set
- [ ] Application starts without errors
- [ ] Web interface loads
- [ ] Image upload works
- [ ] Itinerary generation works
- [ ] Production security configured
- [ ] Monitoring set up
- [ ] Backup strategy in place

---

**Ready to deploy!** 🚀
