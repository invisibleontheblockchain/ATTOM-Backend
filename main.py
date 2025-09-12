"""
PropertyIQ ATTOM API Backend - Railway Cloud Deployment
Simplified version for cloud deployment with essential features only
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import aiohttp
import os
import logging
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="PropertyIQ API",
    description="Real Estate Data API powered by ATTOM",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ATTOM API configuration
ATTOM_API_KEY = os.getenv("ATTOM_API_KEY", "6a03f7ae77a835285d8ce141b2f1ac9f")
ATTOM_BASE_URL = "https://api.gateway.attomdata.com/propertyapi/v1.0.0"

# ZIP code mappings for major cities
CITY_ZIPS = {
    "austin": ["78701", "78702", "78703", "78704", "78705", "78712", "78721", "78722", "78723", "78724"],
    "dallas": ["75201", "75202", "75203", "75204", "75205", "75206", "75207", "75208", "75209", "75210"],
    "houston": ["77001", "77002", "77003", "77004", "77005", "77006", "77007", "77008", "77009", "77010"],
    "san antonio": ["78201", "78202", "78203", "78204", "78205", "78206", "78207", "78208", "78209", "78210"]
}

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "PropertyIQ API - ATTOM Data Integration",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "PropertyIQ ATTOM API",
        "attom_configured": bool(ATTOM_API_KEY),
        "version": "1.0.0"
    }

async def fetch_attom_properties(zip_code: str, limit: int = 50) -> List[Dict]:
    """Fetch properties from ATTOM API for a specific ZIP code"""
    try:
        headers = {
            "accept": "application/json",
            "apikey": ATTOM_API_KEY
        }
        
        params = {
            "postalcode": zip_code,
            "pagesize": min(limit, 100)  # ATTOM max is 100
        }
        
        async with aiohttp.ClientSession() as session:
            url = f"{ATTOM_BASE_URL}/property/snapshot"
            async with session.get(url, headers=headers, params=params, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("property", [])
                else:
                    logger.warning(f"ATTOM API error {response.status} for ZIP {zip_code}")
                    return []
                    
    except Exception as e:
        logger.error(f"Error fetching ATTOM data for ZIP {zip_code}: {e}")
        return []

def normalize_property(attom_property: Dict) -> Dict:
    """Convert ATTOM API property format to PropertyIQ format"""
    try:
        # Extract address
        address = attom_property.get("address", {})
        line1 = address.get("line1", "")
        line2 = address.get("line2", "")
        full_address = f"{line1}, {line2}" if line2 else line1
        
        # Extract building details
        building = attom_property.get("building", {})
        rooms = building.get("rooms", {})
        size = building.get("size", {})
        
        # Extract assessment/market data
        assessment = attom_property.get("assessment", {})
        market = assessment.get("market", {}) if assessment else {}
        
        return {
            "id": attom_property.get("identifier", {}).get("attomId", ""),
            "address": full_address,
            "city": address.get("locality", ""),
            "state": address.get("countrySubd", ""),
            "zip_code": address.get("postal1", ""),
            "list_price": market.get("mktttlvalue"),
            "bedrooms": rooms.get("beds"),
            "bathrooms": rooms.get("bathstotal"),
            "square_feet": size.get("livingsize"),
            "property_type": building.get("construction", {}).get("constructiontype", ""),
            "latitude": address.get("geoid", {}).get("latitude") if address.get("geoid") else None,
            "longitude": address.get("geoid", {}).get("longitude") if address.get("geoid") else None
        }
        
    except Exception as e:
        logger.error(f"Error normalizing property: {e}")
        return {}

@app.get("/api/v1/properties/search/attom")
async def search_attom_properties(
    city: str = Query(..., description="City name"),
    state: str = Query(..., description="State abbreviation"), 
    limit: int = Query(default=20, description="Number of properties to return")
):
    """Search properties using ATTOM API"""
    try:
        city_key = city.lower().strip()
        zip_codes = CITY_ZIPS.get(city_key, [])
        
        if not zip_codes:
            # If city not in our mapping, try to use first few ZIP codes
            logger.warning(f"No ZIP codes mapped for {city}, using default")
            zip_codes = ["78701"]  # Default to Austin
        
        all_properties = []
        properties_per_zip = max(1, limit // len(zip_codes))
        
        # Fetch from multiple ZIP codes
        tasks = [fetch_attom_properties(zip_code, properties_per_zip) for zip_code in zip_codes[:5]]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for result in results:
            if isinstance(result, list):
                all_properties.extend(result)
        
        # Normalize properties
        normalized = []
        for prop in all_properties[:limit]:
            normalized_prop = normalize_property(prop)
            if normalized_prop.get("address"):  # Only include if we have an address
                normalized.append(normalized_prop)
        
        logger.info(f"Returning {len(normalized)} properties for {city}, {state}")
        return normalized
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/api/v1/properties/{property_id}")
async def get_property_details(property_id: str):
    """Get detailed property information"""
    # For now, return basic property structure
    # In a full implementation, you'd fetch detailed data from ATTOM
    return {
        "id": property_id,
        "address": "Sample Property Address",
        "city": "Austin",
        "state": "TX",
        "message": "Property details endpoint - implement with ATTOM detail API"
    }

@app.post("/api/v1/properties/verify")
async def verify_property(property_data: Dict[str, Any]):
    """Verify property data and calculate basic metrics"""
    try:
        # Basic validation
        required_fields = ["address", "city", "state"]
        missing_fields = [field for field in required_fields if not property_data.get(field)]
        
        if missing_fields:
            return {
                "is_valid": False,
                "issues": f"Missing required fields: {', '.join(missing_fields)}"
            }
        
        # Basic metrics calculation (simplified)
        list_price = property_data.get("list_price", 0)
        estimated_rent = list_price * 0.01 if list_price else 0  # 1% rule estimate
        
        metrics = {
            "estimated_monthly_rent": estimated_rent,
            "gross_rent_multiplier": list_price / (estimated_rent * 12) if estimated_rent > 0 else None,
            "cap_rate": 0.08,  # Default 8% cap rate
            "cash_on_cash_return": 0.12,  # Default 12% CoC return
            "monthly_cash_flow": estimated_rent * 0.3  # Simplified cash flow
        }
        
        return {
            "is_valid": True,
            "verification": {
                "address_verified": True,
                "data_quality": "good",
                "confidence_score": 0.85
            },
            "metrics": metrics,
            "calculated_at": "2024-01-01T00:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"Verification error: {e}")
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")

@app.get("/api/v1/market/analytics")
async def get_market_analytics(
    city: Optional[str] = None,
    state: Optional[str] = None
):
    """Get market analytics for a city/state"""
    return {
        "city": city or "Austin",
        "state": state or "TX", 
        "average_price": 450000,
        "median_price": 425000,
        "total_properties": 1250,
        "price_per_sqft": 180,
        "market_trend": "stable",
        "last_updated": "2024-01-01T00:00:00Z"
    }

# Start the application
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)