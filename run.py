#!/usr/bin/env python
"""
Entry point for the Travel Planner application
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check for required API key
if not os.getenv('GEMINI_API_KEY'):
    print("ERROR: GEMINI_API_KEY environment variable is not set")
    print("Please create a .env file with your Gemini API key")
    print("See .env.example for the required format")
    sys.exit(1)

# Import and run the app
from app import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"Starting Travel Planner on http://localhost:{port}")
    print("Press CTRL+C to stop the server")
    print()
    
    app.run(
        debug=debug,
        host='0.0.0.0',
        port=port,
        use_reloader=debug
    )
