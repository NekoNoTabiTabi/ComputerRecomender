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



# Request model for recommendations
class RecommendationRequest(BaseModel):
    preferred_cpu: Optional[str] = None
    cpu_model: Optional[str] = None
    case_size: Optional[str] = None
    cooling: Optional[str] = None
    storage: Optional[str] = None
    ram_pref: Optional[str] = None
    gpu_pref: Optional[str] = None
    psu_pref: Optional[str] = None


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
        return None

    cpu_model = cpu_model.lower()

    if "i9" in cpu_model:
        return "i9"
    elif "i7" in cpu_model:
        return "i7"
    elif "i5" in cpu_model:
        return "i5"
    elif "i3" in cpu_model:
        return "i3"
    

    elif "ryzen 3" in cpu_model:
        return "Ryzen 3"
    elif "ryzen 5" in cpu_model:
        return "Ryzen 5"
    elif "ryzen 7" in cpu_model:
        return "Ryzen 7"
    elif "ryzen 9" in cpu_model:
        return "Ryzen 9"
   
    
    return None


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
def fetch_cpu(db):
    print("hello")
def fetch_components(db, component_type: str, conditions: List[str] = None, params: List = None) -> List[dict]:
    if params is None:
        params = []
    if conditions is None:
        conditions = []

    # Base query for fetching components
    query = f"SELECT * FROM components WHERE component_type = ?"
    params.insert(0, component_type)

    if conditions:
        query += " OR " + " OR ".join(conditions)

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
        print("PREFFERED CPU: ",request.preferred_cpu)
        print("Cpu Model: ",request.cpu_model)
        print("CASE SIZE: ",request.case_size)
        print("COOLING: ",request.cooling)
        print("STORAGE: ",request.storage)
        print("RAM: ",request.ram_pref)
        print("GPU: ",request.gpu_pref)
        print("PSU: ",request.psu_pref)
        
        # "preferred_cpu": preferred_cpu,
        #         "cpu_model": amd_series if preferred_cpu == "AMD" else intel_series,
        #         "form_factor": form_factor,
        #         "cooling": cooling,
        #         "storage": storage,
        #         "ram_pref": ram_pref,
        #         "gpu_pref": gpu_pref,
        #         "psu_pref": psu_pref
       
        
        # 1. Fetch CPU
        cpu_conditions = []

        cpu_params = []
       
        cpus = fetch_components(db, "CPU", cpu_conditions, cpu_params)
        if not cpus:
            raise HTTPException(status_code=404, detail="No suitable CPU found.")
        selected_cpu = cpus[0]
        
       
        
        # Prepare the response
        recommended_build = {
            "CPU": selected_cpu,
     #-------------------need differentr fetch method or sql query   ------
            #"Motherboard": selected_motherboard,
            #"RAM": selected_ram,
            #"GPU": selected_gpu,

            

           # "Storage": selected_storage,
            #"PSU": selected_psu,
           # "Case": selected_case,
            #"Cooler": selected_cooler if selected_cooler else "Using stock cooler"
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