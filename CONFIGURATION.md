# OpenAI API Key Configuration Guide

## Overview

This document describes how the OpenAI API key has been configured for the Multi-Modal Travel Planner application.

## Configuration Steps Completed

### 1. Environment File Setup

Created `.env` file in the project root with the following structure:

```env
# OpenAI API Configuration
OPENAI_API_KEY=your-openai-api-key-here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

### 2. Application Integration

The Flask application (`app.py`) automatically loads the API key:

```python
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)
```

### 3. Security

The `.env` file is excluded from version control:
- Added to `.gitignore` (line 28)
- Not tracked by git
- Safe from accidental commits

### 4. Dependencies Updated

Updated `requirements.txt`:
- Changed `openai==1.12.0` to `openai>=1.12.0`
- Allows automatic upgrades to compatible versions
- Current installed version: 2.8.1

### 5. Testing

Created `test_openai_connection.py` to verify:
- API key is loaded correctly
- OpenAI client can be created
- API connection can be established

## How the Application Uses the API Key

### Image Analysis and Itinerary Generation

When a user uploads an image and preferences, the application:

1. **Encodes the image** to base64 format
2. **Sends a request** to OpenAI's GPT-4o model with:
   - System prompt for travel planning
   - User preferences
   - Destination image
3. **Processes the response** into a structured itinerary
4. **Returns JSON** with day-by-day activities, dining, and tips

### API Call Example

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": "You are an expert travel planner..."
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": user_preferences},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
            ]
        }
    ],
    max_tokens=4096,
    temperature=0.7
)
```

## API Key Management

### Current Status

- ✅ **Configured**: API key is properly set in `.env`
- ✅ **Loaded**: Application can read the key
- ✅ **Client Created**: OpenAI client initializes successfully
- ⚠️ **Quota**: Key has exceeded its current quota (billing issue)

### Quota Information

The provided API key returned a quota error:
```
Error code: 429 - You exceeded your current quota
```

To resolve:
1. Visit https://platform.openai.com/account/billing
2. Add credits to your account
3. Verify the key has access to `gpt-4o` model
4. Check usage limits at https://platform.openai.com/account/usage

### Updating the API Key

If you need to use a different API key:

1. Edit `.env` file:
   ```bash
   nano .env
   ```

2. Replace the `OPENAI_API_KEY` value

3. Restart the application:
   ```bash
   python app.py
   ```

4. Test the new key:
   ```bash
   python test_openai_connection.py
   ```

## Environment Variables

### Required Variables

- `OPENAI_API_KEY`: Your OpenAI API key (starts with `sk-`)

### Optional Variables

- `FLASK_ENV`: Environment mode (`development` or `production`)
- `FLASK_DEBUG`: Enable debug mode (`True` or `False`)
- `SECRET_KEY`: Flask secret key for sessions

## Verification Checklist

- [x] `.env` file created
- [x] API key configured
- [x] `.env` excluded from git
- [x] Dependencies installed
- [x] OpenAI library updated
- [x] Application can load the key
- [x] OpenAI client can be created
- [ ] API quota available (requires billing update)

## Troubleshooting

### "OPENAI_API_KEY environment variable is not set"

**Solution**: Ensure `.env` file exists and contains the key

```bash
# Check if .env exists
ls -la .env

# Verify key is set
cat .env | grep OPENAI_API_KEY
```

### "Error code: 429 - You exceeded your current quota"

**Solution**: Add credits to your OpenAI account

1. Visit https://platform.openai.com/account/billing
2. Add a payment method
3. Add credits or set up auto-recharge
4. Wait a few minutes for the changes to take effect

### "Error code: 401 - Incorrect API key"

**Solution**: Verify the API key is correct

1. Check the key at https://platform.openai.com/api-keys
2. Regenerate the key if needed
3. Update `.env` with the new key
4. Restart the application

### Module Not Found Errors

**Solution**: Install dependencies in virtual environment

```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Security Best Practices

1. **Never commit** the `.env` file to version control
2. **Rotate keys regularly** for production applications
3. **Use different keys** for development and production
4. **Monitor usage** to detect unauthorized access
5. **Set spending limits** in your OpenAI account

## API Usage and Costs

The application uses the `gpt-4o` model which costs:
- **Input**: $2.50 per 1M tokens
- **Output**: $10.00 per 1M tokens

Typical itinerary generation uses:
- ~500-1000 input tokens (including image)
- ~2000-4000 output tokens

Estimated cost per itinerary: **$0.03 - $0.05**

## Support

### OpenAI Documentation
- API Reference: https://platform.openai.com/docs/api-reference
- Vision Guide: https://platform.openai.com/docs/guides/vision
- Error Codes: https://platform.openai.com/docs/guides/error-codes

### Application Support
- README.md - Main documentation
- SETUP_COMPLETE.md - Setup summary
- test_openai_connection.py - Connection testing

---

**Last Updated**: November 28, 2024  
**API Key Status**: Configured (pending quota)  
**Application Status**: Ready to use
