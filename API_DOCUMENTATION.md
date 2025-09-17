# PropertyIQ Backend API Documentation

## Overview

The PropertyIQ backend is a FastAPI-based REST API that integrates with ATTOM Data's property database to provide real estate information, investment analytics, and property search capabilities. The backend serves as the data layer for the PropertyIQ real estate investment platform.

## Architecture

### Technology Stack
- **Framework**: FastAPI 0.100.0+
- **Runtime**: Python 3.8+
- **HTTP Client**: aiohttp (async requests)
- **Data Source**: ATTOM Data API
- **Deployment**: Railway (cloud platform)
- **Environment**: Docker containerized

### Core Components

```
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies  
├── Procfile               # Railway deployment config
├── .env                   # Environment variables (local)
└── README.md              # Project documentation
```

## Environment Configuration

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `ATTOM_API_KEY` | ATTOM Data API authentication key | `your_attom_api_key_here` |
| `PORT` | Server port (Railway sets this automatically) | `8000` |
| `PYTHONUNBUFFERED` | Enable Python logging in production | `1` |

### ATTOM API Configuration

```python
ATTOM_BASE_URL = "https://api.gateway.attomdata.com/propertyapi/v1.0.0"
```

The backend uses ATTOM Data's property snapshot endpoint to retrieve comprehensive property information including market values, assessments, and property characteristics.

## API Endpoints

### Health Check

#### `GET /health`

Returns the health status of the backend service.

**Response:**
```json
{
  "status": "healthy",
  "service": "PropertyIQ ATTOM API",
  "attom_configured": true,
  "version": "2.0.0"
}
```

### Property Search

#### `GET /api/v1/properties/search/attom`

Searches for properties using ATTOM Data API based on city and state.

**Parameters:**
- `city` (required): City name (e.g., "Austin")
- `state` (required): State abbreviation (e.g., "TX") 
- `limit` (optional): Number of properties to return (default: 20, max: 100)

**Example Request:**
```
GET /api/v1/properties/search/attom?city=Austin&state=TX&limit=12
```

**Response:**
```json
[
  {
    "id": "244337",
    "address": "311 W 5TH ST UNIT 508, AUSTIN, TX 78701",
    "city": "AUSTIN",
    "state": "TX", 
    "zip_code": "78701",
    "price": 450000,
    "bedrooms": 3,
    "bathrooms": 2.5,
    "square_feet": 1243,
    "year_built": 2002,
    "lot_size": 0,
    "property_type": "condo",
    "latitude": 30.267767,
    "longitude": -97.746478,
    "estimated_value": 450000,
    "property_status": "active",
    "days_on_market": 30,
    "hoa_fee": 0,
    "property_tax_rate": 0.015,
    "description": "This condo features 3 bedrooms and 2.5 bathrooms with 1,243 square feet of living space...",
    "features": ["Updated Kitchen", "Modern Amenities", "Prime Location"],
    "images": ["https://images.unsplash.com/photo-1560448204-603c3d5dd8fd?w=800&q=80"],
    "neighborhood": "AUSTIN",
    "school_rating": null,
    "insurance_estimate": 3600
  }
]
```

### Property Details

#### `GET /api/v1/properties/{property_id}`

Retrieves detailed information for a specific property.

**Parameters:**
- `property_id`: ATTOM property identifier

**Response:**
Returns the same property object structure as the search endpoint with complete details.

### Property Verification

#### `POST /api/v1/properties/verify`

Verifies property data and calculates investment metrics.

**Request Body:**
```json
{
  "address": "123 Main St",
  "city": "Austin",
  "state": "TX",
  "list_price": 450000
}
```

**Response:**
```json
{
  "is_valid": true,
  "verification": {
    "address_verified": true,
    "data_quality": "good", 
    "confidence_score": 0.85
  },
  "metrics": {
    "estimated_monthly_rent": 4500,
    "gross_rent_multiplier": 10.0,
    "cap_rate": 0.08,
    "cash_on_cash_return": 0.12,
    "monthly_cash_flow": 1350
  },
  "calculated_at": "2024-01-01T00:00:00Z"
}
```

### Market Analytics

#### `GET /api/v1/market/analytics`

Retrieves market statistics for a specified area.

**Parameters:**
- `city` (optional): City name
- `state` (optional): State abbreviation  

**Response:**
```json
{
  "city": "Austin",
  "state": "TX",
  "average_price": 450000,
  "median_price": 425000,
  "total_properties": 1250,
  "price_per_sqft": 180,
  "market_trend": "stable",
  "last_updated": "2024-01-01T00:00:00Z"
}
```

## Data Processing

### ATTOM API Integration

The backend implements a sophisticated data extraction system to handle ATTOM's complex nested JSON responses:

#### Price Extraction Strategy

The system attempts multiple price extraction strategies in priority order:

1. **Market Total Value**: `assessment.market.mktttlvalue`
2. **Market Improved Value**: `assessment.market.mktimprvalue`  
3. **Assessed Total Value**: `assessment.assessed.assdttlvalue`
4. **Sale Amount**: `sale.amount`
5. **Property Value**: `summary.propvalue`

#### Property Normalization

Raw ATTOM data is normalized into a consistent format:

```python
def normalize_property_with_enhanced_extraction(attom_property: Dict) -> Dict:
    # Extract core sections
    address = attom_property.get("address", {})
    building = attom_property.get("building", {})
    assessment = attom_property.get("assessment", {})
    
    # Price extraction using multiple strategies
    price = extract_price_from_attom(attom_property)
    
    # Property specifications from nested structure
    rooms = building.get("rooms", {})
    bedrooms = safe_int(rooms.get("beds"))
    bathrooms = safe_float(rooms.get("bathstotal"))
    
    # Return normalized property object
```

### ZIP Code Mapping

The system uses predefined ZIP code mappings for major cities to optimize ATTOM API queries:

```python
CITY_ZIPS = {
    "austin": ["78701", "78702", "78703", "78704", "78705"],
    "dallas": ["75201", "75202", "75203", "75204", "75205"], 
    "houston": ["77001", "77002", "77003", "77004", "77005"],
    "san antonio": ["78201", "78202", "78203", "78204", "78205"]
}
```

## Error Handling

### HTTP Status Codes

- `200`: Success
- `400`: Bad Request (missing parameters)
- `404`: Resource not found
- `500`: Internal server error (ATTOM API failure, processing error)

### Error Response Format

```json
{
  "detail": "Error description",
  "status_code": 500
}
```

### Fallback Mechanisms

When ATTOM API requests fail:
- Returns empty array for search requests
- Logs detailed error information
- Maintains service availability

## Logging

### Log Levels

The backend implements comprehensive logging:

- **INFO**: API requests, response summaries, processing status
- **DEBUG**: Detailed data extraction, ATTOM response structure
- **WARNING**: Data extraction failures, fallback usage
- **ERROR**: API failures, processing exceptions

### Log Format

```
2024-01-01 12:00:00 - PropertyIQ - INFO - 🔍 ATTOM API Request for ZIP 78701
2024-01-01 12:00:01 - PropertyIQ - INFO - 📊 Got 15 properties from ATTOM for ZIP 78701  
2024-01-01 12:00:02 - PropertyIQ - INFO - ✅ Using market_total: $450,000.00
```

## Performance

### Concurrency

- Async/await pattern for non-blocking I/O
- Concurrent ZIP code fetching using `asyncio.gather()`
- Connection pooling via aiohttp ClientSession

### Optimization Strategies

- Limited concurrent ATTOM requests to respect rate limits
- ZIP code batching to minimize API calls
- Response size limiting (100 properties max per request)

## Security

### API Key Management

- ATTOM API key stored as environment variable
- No API key logging or exposure in responses
- Secure header transmission to ATTOM endpoints

### CORS Configuration

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Deployment

### Railway Configuration

**Procfile:**
```
web: python main.py
```

**Runtime Requirements:**
- Python 3.8+
- 512MB RAM minimum
- HTTPS endpoints

### Environment Setup

1. Set ATTOM_API_KEY in Railway environment variables
2. Deploy from GitHub repository
3. Verify health endpoint accessibility
4. Test property search functionality

## Monitoring

### Health Checks

The `/health` endpoint provides service status including:
- Service availability
- ATTOM API key configuration
- Application version

### Logging Monitoring

Key metrics to monitor:
- ATTOM API response times
- Price extraction success rates
- Property normalization failures
- Request/response volumes

## Development

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export ATTOM_API_KEY=your_api_key_here
export PORT=8000

# Run development server
python main.py
```

### Testing

Test the API endpoints:

```bash
# Health check
curl http://localhost:8000/health

# Property search
curl "http://localhost:8000/api/v1/properties/search/attom?city=Austin&state=TX&limit=5"
```

## Troubleshooting

### Common Issues

**Properties return with $0 prices:**
- Check ATTOM API key permissions
- Verify ATTOM subscription includes market value data
- Review extraction logs for field availability

**Empty search results:**
- Verify ZIP code mappings for target cities
- Check ATTOM API rate limits and quotas
- Review network connectivity to ATTOM endpoints

**Coordinate extraction failures:**
- Ensure ATTOM response includes geoid data
- Verify coordinate data types (float conversion)
- Check for null/empty coordinate values

### Debug Logging

Enable detailed logging by setting log level to DEBUG:

```python
logger.setLevel(logging.DEBUG)
```

This provides complete ATTOM response structure analysis and step-by-step property normalization details.

## API Limitations

### ATTOM Data Constraints

- Rate limiting: Varies by subscription tier
- Geographic coverage: US properties only  
- Data freshness: Updated periodically by ATTOM
- Field availability: Depends on property type and data source

### Backend Limitations

- Maximum 100 properties per search request
- Limited to predefined city ZIP codes
- Basic investment metric calculations
- No caching layer implemented

## Future Enhancements

### Planned Features

- Redis caching for improved performance
- Real-time property price updates
- Enhanced investment analysis algorithms
- Additional data sources integration
- Geographic boundary search capabilities

### Scalability Considerations

- Database layer for property caching
- Load balancing for high-traffic scenarios  
- API rate limit management
- Background job processing for data updates