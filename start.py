#!/usr/bin/env python
"""
Unified Development Runner for Multi-Modal Travel Planner
This script makes it easy to run both backend and frontend together
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_requirements():
    """Check if all requirements are installed"""
    try:
        import flask
        import flask_cors
        import openai
        print("✓ All required packages are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing required package: {e.name}")
        print("\nPlease install requirements:")
        print("  pip install -r requirements.txt")
        return False

def check_api_key():
    """Check if OpenAI API key is configured"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("✗ OPENAI_API_KEY environment variable is not set")
        print("\nPlease ensure .env file exists with your API key:")
        print("  OPENAI_API_KEY=your_api_key_here")
        return False
    print("✓ OpenAI API key is configured")
    return True

def create_directories():
    """Create necessary directories"""
    dirs = ['uploads', 'static', 'templates']
    for directory in dirs:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✓ Created {directory}/ directory")

def print_banner():
    """Print application banner"""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        🌍 Multi-Modal Travel Planner 🌍                  ║
║                                                           ║
║        Powered by OpenAI GPT-4o                          ║
║        with Vision Capabilities                           ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
    print(banner)

def main():
    """Main entry point"""
    print_banner()
    
    print("\n🔍 Pre-flight checks...\n")
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check API key
    if not check_api_key():
        sys.exit(1)
    
    # Create necessary directories
    create_directories()
    
    # Get configuration
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print("\n✓ All checks passed!\n")
    print("=" * 60)
    print(f"🚀 Starting Travel Planner Server")
    print("=" * 60)
    print(f"\n📍 Local URL:      http://localhost:{port}")
    print(f"📍 Network URL:    http://0.0.0.0:{port}")
    print(f"\n🔧 Debug Mode:     {'Enabled' if debug else 'Disabled'}")
    print(f"🔄 Auto-reload:    {'Enabled' if debug else 'Disabled'}")
    print("\n💡 Tip: Upload a destination image and provide your travel preferences!")
    print("⚡ Press CTRL+C to stop the server\n")
    print("=" * 60)
    
    # Import and run the Flask app
    try:
        from app import app
        app.run(
            debug=debug,
            host='0.0.0.0',
            port=port,
            use_reloader=debug
        )
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down gracefully...")
        print("Thanks for using Multi-Modal Travel Planner!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting server: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
