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



class PSUTier(str, Enum):
    BRONZE = "80+ Bronze"
    GOLD = "80+ Gold"
    PLATINUM = "80+ Platinum"
    NO_PREFERENCE = "No Preference"


# Request model for recommendations
class RecommendationRequest(BaseModel):
    preferred_cpu: Optional[CPUBrand] = CPUBrand.NO_PREFERENCE
    cpu_model: Optional[str] = None
    form_factor: Optional[FormFactor] = FormFactor.NO_PREFERENCE
    cooling: Optional[CoolingSolution] = CoolingSolution.NO_PREFERENCE
    storage: Optional[str] = None
    ram_pref: Optional[MemoryCapacity] = MemoryCapacity.NO_PREFERENCE
    gpu_pref: Optional[GPUBrand] = GPUBrand.NO_PREFERENCE
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



# Function to fetch components from DB with conditions
def fetch_components(db, component_type: str, conditions: List[str] = None, params: List = None) -> List[dict]:
    if params is None:
        params = []
    if conditions is None:
        conditions = []

    # Base query for fetching components
    query = f"SELECT * FROM components WHERE component_type = ?"
    params.insert(0, component_type)

    if conditions:
        query += " AND " + " AND ".join(conditions)

    query += " ORDER BY id ASC"  # Adjust sorting if needed

    # Debugging: Log the query and parameters
    print(f"Executing query: {query}")
    print(f"With parameters: {params}")

    try:
        cursor = db.execute(query, params)
        results = [dict(row) for row in cursor.fetchall()]
        print(f"Fetched {len(results)} results.")
        return results
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
        
         # Determine CPU requirements
        cpu_brand = request.preferred_cpu.value if request.preferred_cpu != CPUBrand.NO_PREFERENCE else None
        cpu_tier, performance_tier = get_cpu_tier_requirements(request.cpu_model)
        
        # 1. Fetch CPU
        cpu_conditions = []
        cpu_params = []
        if cpu_brand:
            cpu_conditions.append("(name LIKE ? OR name LIKE ?)")
            cpu_params.extend([f"%{cpu_brand}%", f"%{cpu_brand.lower()}%"])
        if cpu_tier:
            cpu_conditions.append("name LIKE ?")
            cpu_params.append(f"%{cpu_tier}%")
        
        cpus = fetch_components(db, "CPU", cpu_conditions, cpu_params)
        if not cpus:
            raise HTTPException(status_code=404, detail="No suitable CPU found.")
        selected_cpu = cpus[0]
        
        # 2. Fetch Motherboard (based on CPU)
        mobo_conditions = []
        mobo_params = []
        
        # Get compatible chipsets
        if cpu_brand and cpu_tier:
            compatible_chipsets = get_compatible_motherboard_chipsets(cpu_brand, cpu_tier)
            if compatible_chipsets:
                placeholders = ",".join(["?"] * len(compatible_chipsets))
                mobo_conditions.append(f"chipset IN ({placeholders})")
                mobo_params.extend(compatible_chipsets)
        
        motherboards = fetch_components(db, "Motherboard", mobo_conditions, mobo_params)
        if not motherboards:
            raise HTTPException(status_code=404, detail="No suitable motherboard found.")
        selected_motherboard = motherboards[0]
        
        # 3. Fetch RAM
        ram_conditions = []
        ram_params = []
        
        if request.ram_pref != MemoryCapacity.NO_PREFERENCE:
            capacity_map = {
                MemoryCapacity.GB8: 8,
                MemoryCapacity.GB16: 16,
                MemoryCapacity.GB32: 32,
                MemoryCapacity.GB64: 64
            }
            ram_conditions.append("capacity >= ?")
            ram_params.append(capacity_map[request.ram_pref])
        
        rams = fetch_components(db, "RAM", ram_conditions, ram_params)
        if not rams:
            raise HTTPException(status_code=404, detail="No suitable RAM found.")
        selected_ram = rams[0]
        
        # 4. Fetch GPU
        gpu_conditions = []
        gpu_params = []
        
        if request.gpu_pref != GPUBrand.NO_PREFERENCE:
            gpu_conditions.append("(name LIKE ? OR name LIKE ?)")
            gpu_params.extend([f"%{request.gpu_pref.value}%", f"%{request.gpu_pref.value.lower()}%"])
        
        # Match GPU tier with CPU tier
        if performance_tier:
            gpu_conditions.append("tier = ?")
            gpu_params.append(performance_tier)
        
        gpus = fetch_components(db, "GPU", gpu_conditions, gpu_params)
        if not gpus:
            raise HTTPException(status_code=404, detail="No suitable GPU found.")
        selected_gpu = gpus[0]
        
        # 8. Fetch Cooler (if needed)
        cooler_conditions = []
        cooler_params = []
        
        if request.cooling != CoolingSolution.NO_PREFERENCE:
            if request.cooling == CoolingSolution.AIR:
                cooler_conditions.append("type = 'Air'")
            elif request.cooling == CoolingSolution.LIQUID:
                cooler_conditions.append("type = 'Liquid'")
            elif request.cooling == CoolingSolution.STOCK:
                # No need for aftermarket cooler
                selected_cooler = None
        
        if cooler_conditions:
            # Ensure compatibility with socket
            if selected_cpu.get('socket'):
                cooler_conditions.append("compatible_sockets LIKE ?")
                cooler_params.append(f"%{selected_cpu['socket']}%")
            
            coolers = fetch_components(db, "Cooler", cooler_conditions, cooler_params)
            if coolers:
                selected_cooler = coolers[0]
            else:
                selected_cooler = None
        else:
            selected_cooler = None
        
        # Prepare the response
        recommended_build = {
            "CPU": selected_cpu,
            "Motherboard": selected_motherboard,
            "RAM": selected_ram,
            "GPU": selected_gpu,

            
#-------------------need differentr fetch method or sql query   ------
           # "Storage": selected_storage,
            #"PSU": selected_psu,
           # "Case": selected_case,
#-------------------need differentr fetch method or sql query <End> ------


            "Cooler": selected_cooler if selected_cooler else "Using stock cooler"
        }
        
        return {"recommended_build": recommended_build}
        
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