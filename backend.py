from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sqlite3
from pathlib import Path
from typing import Optional, List
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

# CORS Middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database path
BASE_DIR = Path(__file__).parent
DATABASE_URL = BASE_DIR / "components.db"

# Enum classes for better type safety
class CPUBrand(str, Enum):
    INTEL = "Intel"
    AMD = "AMD"
    NO_PREFERENCE = "No Preference"

class UsageScenario(str, Enum):
    GENERAL = "General Computing/Office"
    GAMING_1080P = "Gaming (1080p)"
    GAMING_1440P_4K = "Gaming (1440p/4K)"
    CONTENT_CREATION = "Content Creation (Video/Photo Editing)"
    STREAMING = "Streaming"
    WORKSTATION = "Workstation (3D Rendering, CAD)"
    SERVER = "Server/Development"

class FormFactor(str, Enum):
    MINI_TOWER = "Mini Tower (Compact, limited expansion)"
    MID_TOWER = "Mid Tower (Balanced size and expandability)"
    FULL_TOWER = "Full Tower (Maximum expansion, better cooling)"
    NO_PREFERENCE = "No Preference"

class CoolingSolution(str, Enum):
    STOCK = "Stock Cooler (Included with CPU)"
    AIR = "Air Cooling (Quiet, reliable)"
    LIQUID = "Liquid Cooling (Better performance, aesthetic)"
    NO_PREFERENCE = "No Preference"

class MemoryCapacity(str, Enum):
    GB8 = "8GB"
    GB16 = "16GB"
    GB32 = "32GB"
    GB64 = "64GB+"
    NO_PREFERENCE = "No Preference"

class GPUBrand(str, Enum):
    NVIDIA = "NVIDIA"
    AMD = "AMD"
    NO_PREFERENCE = "No Preference"

class RGBPreference(str, Enum):
    YES = "Yes"
    NO = "No"
    NO_PREFERENCE = "No Preference"

class PSUTier(str, Enum):
    BRONZE = "80+ Bronze"
    GOLD = "80+ Gold"
    PLATINUM = "80+ Platinum"
    NO_PREFERENCE = "No Preference"


# Request model for recommendations
class RecommendationRequest(BaseModel):
    preferred_cpu: Optional[CPUBrand] = CPUBrand.NO_PREFERENCE
    cpu_model: Optional[str] = None
    usage: Optional[UsageScenario] = UsageScenario.GENERAL
    form_factor: Optional[FormFactor] = FormFactor.NO_PREFERENCE
    cooling: Optional[CoolingSolution] = CoolingSolution.NO_PREFERENCE
    storage: Optional[str] = None
    budget_min: Optional[int] = 30000
    budget_max: Optional[int] = 80000
    ram_pref: Optional[MemoryCapacity] = MemoryCapacity.NO_PREFERENCE
    gpu_pref: Optional[GPUBrand] = GPUBrand.NO_PREFERENCE
    rgb_pref: Optional[RGBPreference] = RGBPreference.NO_PREFERENCE
    psu_pref: Optional[PSUTier] = PSUTier.NO_PREFERENCE


# Utility function to establish DB connection
def get_db_connection():
    try:
        conn = sqlite3.connect(str(DATABASE_URL))
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"DB connection error on {DATABASE_URL}: {e}")


# Function to determine CPU tier based on the model name
def get_cpu_tier_requirements(cpu_model: str) -> tuple:
    if not cpu_model or "Select tier" in cpu_model:
        return None, None

    cpu_model = cpu_model.lower()
    if "i3" in cpu_model:
        return "i3", None
    elif "i5" in cpu_model:
        return "i5", None
    elif "i7" in cpu_model:
        return "i7", None
    elif "i9" in cpu_model:
        return "i9", None
    elif "ryzen 3" in cpu_model:
        return "Ryzen 3", None
    elif "ryzen 5" in cpu_model:
        return "Ryzen 5", None
    elif "ryzen 7" in cpu_model:
        return "Ryzen 7", None
    elif "ryzen 9" in cpu_model:
        return "Ryzen 9", None
    elif "budget" in cpu_model:
        return None, "entry"
    elif "mainstream" in cpu_model:
        return None, "mid"
    elif "performance" in cpu_model:
        return None, "high"
    elif "enthusiast" in cpu_model:
        return None, "enthusiast"
    
    return None, None


# Fetch compatible motherboards based on CPU brand and tier
def get_compatible_motherboard_chipsets(cpu_brand: str, cpu_tier: str) -> List[str]:
    if cpu_brand == "Intel":
        if cpu_tier in ["i3", "i5"]:
            return ["B660", "B760", "Z690", "Z790"]
        elif cpu_tier in ["i7", "i9"]:
            return ["Z690", "Z790"]
    elif cpu_brand == "AMD":
        if cpu_tier in ["Ryzen 3", "Ryzen 5"]:
            return ["B650", "B650E"]
        elif cpu_tier in ["Ryzen 7", "Ryzen 9"]:
            return ["B650", "B650E", "X670", "X670E"]
    return []


# Get SQL condition for form factor preference
def get_form_factor_condition(form_factor: FormFactor) -> Optional[str]:
    if form_factor == FormFactor.MINI_TOWER:
        return "form_factor IN ('Mini Tower', 'Micro ATX', 'Mini-ITX')"
    elif form_factor == FormFactor.MID_TOWER:
        return "form_factor = 'ATX'"
    elif form_factor == FormFactor.FULL_TOWER:
        return "form_factor IN ('E-ATX', 'Full Tower')"
    return None


# Function to fetch components from DB with conditions
def fetch_components(db, component_type: str, conditions: List[str] = None, params: List = None) -> List[dict]:
    if params is None:
        params = []
    if conditions is None:
        conditions = []
    
    query = f"SELECT * FROM components WHERE type = ?"
    params.insert(0, component_type)
    
    if conditions:
        query += " AND " + " AND ".join(conditions)
    
    query += " ORDER BY price_estimate DESC"
    
    try:
        cursor = db.execute(query, params)
        return cursor.fetchall()
    except sqlite3.Error as e:
        raise HTTPException(status_code=501, detail=f"DB query error: {e}")


# Endpoint for recommending a build based on user input
@app.post("/recommend")
async def get_recommendation(request: RecommendationRequest):

    try:
        db = get_db_connection()
        print(RecommendationRequest)
        
        # Determine CPU requirements
        cpu_brand = request.preferred_cpu.value if request.preferred_cpu != CPUBrand.NO_PREFERENCE else None
        cpu_tier, performance_tier = get_cpu_tier_requirements(request.cpu_model)
        
        # Fetch compatible components
        # CPU, motherboard, RAM, GPU, etc.
        # Note: Add more fetching logic as required based on other components
        
        # Example CPU selection:
        cpu_conditions = []
        if cpu_brand:
            cpu_conditions.append("(name LIKE ? OR name LIKE ?)")
            params = [f"%{cpu_brand}%", f"%{cpu_brand.lower()}%"]
        
        if cpu_tier:
            cpu_conditions.append("name LIKE ?")
            params.append(f"%{cpu_tier}%")
        
        cpus = fetch_components(db, "CPU", cpu_conditions, params)
        if not cpus:
            raise HTTPException(status_code=404, detail="No suitable CPU found.")
        
        selected_cpu = cpus[0]
        # Similar selection for other components follows...

        return {"recommended_build": "Example build details go here"}
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})



# Root endpoint to validate API is running
@app.get("/")
def root():
    return {"message": "PC Builder API is running. Use /recommend endpoint for recommendations."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)