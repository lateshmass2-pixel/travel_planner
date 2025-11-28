#!/usr/bin/env python3
"""
Test script to verify OpenAI API connection and configuration.
This script tests the OpenAI API key and basic functionality.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

def test_openai_connection():
    """Test the OpenAI API connection."""
    
    # Load environment variables
    load_dotenv()
    
    # Check if API key is set
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY is not set in .env file")
        return False
    
    print("✅ OPENAI_API_KEY is configured")
    print(f"   Key starts with: {api_key[:20]}...")
    
    # Try to create an OpenAI client
    try:
        client = OpenAI(api_key=api_key)
        print("✅ OpenAI client created successfully")
    except Exception as e:
        print(f"❌ Failed to create OpenAI client: {str(e)}")
        return False
    
    # Test a simple API call
    try:
        print("\n🔄 Testing API connection with a simple request...")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": "Say 'API connection successful' in a creative way"}
            ],
            max_tokens=50
        )
        
        message = response.choices[0].message.content
        print(f"✅ API Response: {message}")
        print("\n🎉 All tests passed! The application is ready to generate itineraries.")
        return True
        
    except Exception as e:
        print(f"❌ API call failed: {str(e)}")
        if "authentication" in str(e).lower() or "api_key" in str(e).lower():
            print("   Please verify your OpenAI API key is valid and has sufficient credits.")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("OpenAI Connection Test for Travel Planner")
    print("=" * 60)
    print()
    
    success = test_openai_connection()
    
    print()
    print("=" * 60)
    if success:
        print("Status: ✅ READY")
        print("You can now start the application with: python app.py")
    else:
        print("Status: ❌ FAILED")
        print("Please fix the issues above before running the application.")
    print("=" * 60)
