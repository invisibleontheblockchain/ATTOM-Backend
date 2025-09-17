# PropertyIQ ATTOM Backend

🏠 **Real Estate Data API powered by ATTOM Data**

## Features
- ✅ ATTOM API integration for property search
- ✅ Property data normalization and validation  
- ✅ Investment metrics calculation
- ✅ Market analytics endpoints
- ✅ FastAPI with automatic documentation
- ✅ Production-ready with Railway deployment

## API Endpoints

- `GET /health` - Health check
- `GET /api/v1/properties/search/attom` - Search properties by city/state
- `GET /api/v1/properties/{id}` - Get property details
- `POST /api/v1/properties/verify` - Verify and calculate metrics
- `GET /api/v1/market/analytics` - Get market analytics

## Quick Deploy to Railway

1. [![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/yourusername/propertyiq-attom-backend)

2. Set environment variables:
   ```env
   ATTOM_API_KEY=your_attom_api_key
   PORT=8000
   PYTHONUNBUFFERED=1
   ```

## Local Development

```bash
pip install -r requirements.txt
python main.py
```

Server runs on http://localhost:8000

## Environment Variables

- `ATTOM_API_KEY` - Your ATTOM Data API key
- `PORT` - Server port (default: 8000)
- `PYTHONUNBUFFERED` - Python logging (set to 1)

## Test Endpoints

```bash
curl https://your-app.railway.app/health
curl "https://your-app.railway.app/api/v1/properties/search/attom?city=Austin&state=TX&limit=5"
```

Built for PropertyIQ platform - Professional real estate investment analysis.

## 📖 Complete Documentation

For comprehensive API documentation, architecture details, and development guides, see:

**[📋 API_DOCUMENTATION.md](./API_DOCUMENTATION.md)**

Includes:
- Complete endpoint documentation with examples
- ATTOM API integration details
- Data processing and normalization workflows
- Deployment and monitoring guides
- Troubleshooting and debugging information
- Performance optimization strategies
