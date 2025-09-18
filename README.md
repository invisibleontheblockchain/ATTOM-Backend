# PropertyIQ ATTOM Backend

A FastAPI-based real estate data API that integrates with ATTOM Data to provide comprehensive property information for the PropertyIQ frontend application.

## 🚀 Features

- **Complete Frontend Compatibility**: Fully compatible with PropertyIQ frontend data requirements
- **ATTOM Data Integration**: Real-time property data from ATTOM's comprehensive database
- **Enhanced Property Images**: High-quality property images categorized by type and price range
- **Smart Data Normalization**: Intelligent extraction and normalization of property data
- **Comprehensive Logging**: Detailed logging for debugging and monitoring
- **Railway Ready**: Configured for seamless Railway deployment

## 📋 Frontend Compatibility

This backend provides all data fields required by the PropertyIQ frontend:

### Core Property Data
- `id`, `address`, `city`, `state`, `zip_code`
- `price`, `bedrooms`, `bathrooms`, `square_feet`
- `property_type`, `lot_size`, `year_built`
- `latitude`, `longitude` (for mapping)

### Enhanced Features
- `images` - Multiple high-quality images per property
- `description` - AI-generated property descriptions
- `features` - Extracted property features and amenities
- `property_status`, `days_on_market`, `estimated_value`
- `hoa_fee`, `property_tax_rate`, `insurance_estimate`

### API Endpoints
- `GET /api/v1/properties/search/attom` - Property search
- `GET /api/v1/properties/{property_id}` - Property details
- `POST /api/v1/properties/verify` - Property verification
- `GET /api/v1/market/analytics` - Market analytics
- `GET /health` - Health check

## 🛠 Setup

### Prerequisites
- Python 3.8+
- ATTOM Data API key

### Installation

1. **Clone and navigate to the repository**
   ```bash
   cd apps/ATTOM-Backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   # Create .env file
   echo "ATTOM_API_KEY=your_actual_attom_api_key_here" > .env
   echo "PORT=8000" >> .env
   ```

4. **Run the server**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

## 🚢 Railway Deployment

### Option 1: Railway CLI
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Deploy
railway up
```

### Option 2: GitHub Integration
1. Connect your GitHub repository to Railway
2. Set environment variable: `ATTOM_API_KEY=your_actual_api_key`
3. Railway will automatically deploy using the included `railway.json` configuration

### Environment Variables for Railway
```
ATTOM_API_KEY=your_actual_attom_api_key_here
```

## 🔧 Configuration

### Supported Cities
The backend includes ZIP code mappings for:
- Austin, TX
- Dallas, TX
- Houston, TX
- San Antonio, TX

### ATTOM API Integration
- Property snapshot endpoint for search
- Property detail endpoint for individual properties
- Comprehensive error handling and fallbacks
- Rate limiting compliance

## 📊 API Documentation

Once running, visit:
- API Documentation: `http://localhost:8000/docs`
- Alternative Docs: `http://localhost:8000/redoc`
- Health Check: `http://localhost:8000/health`

## 🎯 Frontend Integration

The backend is specifically designed to work with the PropertyIQ frontend:

### Frontend Service Configuration
Update the frontend's `PropertyService.jsx`:
```javascript
const API_BASE = 'https://your-railway-app-url';
```

### Data Flow
1. Frontend searches properties via `/api/v1/properties/search/attom`
2. Backend fetches data from ATTOM API
3. Data is normalized and enhanced with images/descriptions
4. Frontend receives fully compatible property objects

## 🐛 Troubleshooting

### Common Issues

**401 Unauthorized from ATTOM API**
- Verify your ATTOM API key is correct
- Check your ATTOM subscription status
- Ensure API key has proper permissions

**Empty search results**
- Check if the city is supported in `CITY_ZIPS`
- Verify ATTOM API connectivity
- Review server logs for detailed error information

**Frontend connection issues**
- Update frontend API_BASE URL to your Railway deployment
- Ensure CORS is properly configured
- Check network connectivity

### Debugging

Enable detailed logging by setting log level to DEBUG:
```python
logger.setLevel(logging.DEBUG)
```

## 📈 Performance

- Async/await pattern for non-blocking operations
- Concurrent ZIP code fetching
- Connection pooling via aiohttp
- Efficient data normalization

## 🔒 Security

- Environment variable-based API key management
- No sensitive data in logs
- CORS configuration for production
- Input validation and sanitization

## 📝 License

This project is part of the PropertyIQ platform.

## 🤝 Support

For issues related to:
- ATTOM API integration
- Frontend compatibility
- Railway deployment

Check the logs and API documentation for detailed error information.
