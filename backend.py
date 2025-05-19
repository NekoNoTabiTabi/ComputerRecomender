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
class UserComponentInput(BaseModel):
    #unnecessary?
    preferred_cpu: str
    #needs changing sql 
    cpu_model: str 
    #needs changing sql
    case_size: str
    
    #needs changing sql
    cooling: str

    #needs changing sql
    storage: str 

    ram_pref: str
    gpu_pref: str
    psu_pref: str 


# Utility function to establish DB connection
def get_db_connection():
    try:
        conn = sqlite3.connect(str(DATABASE_URL))
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"DB connection error on {DATABASE_URL}: {e}")


def get_mobo_for_cpu(cpu_socket_type:str):
    try:
             
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
       
       #query
        query = "SELECT * FROM motherboards WHERE socket_type LIKE ? "      
        cursor.execute( query, (f"%{cpu_socket_type}%",))
        
      
        mobo = cursor.fetchall()
        result = [dict(row) for row in mobo]

        print(f"Fetched Motherboards: {result}")
        conn.close()

        if result:
            return {"mobo": result}
        raise HTTPException(status_code=404, detail="mobo not found")
    
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    
#User input 
@app.post("/user_input")
async def get_input(input: UserComponentInput):


    try:
        print(f"Received Input: {input.model_dump()}")
        return input.model_dump()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})

#fetching CPU
@app.get("/user_input/cpu/{preferred_cpu}")
def fetch_cpu(preferred_cpu: str):
    try:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
       
       #query
        query = "SELECT * FROM cpus WHERE series LIKE ? "      
        cursor.execute( query, (f"%{preferred_cpu}%",))
        
      
        cpus = cursor.fetchall()
        result = [dict(row) for row in cpus]

        print(f"Fetched CPUs: {result}")
        conn.close()

        if result:
            return {"cpus": result}

        
        raise HTTPException(status_code=404, detail="CPU not found")
    
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    


#Testing Motherboard fetching
@app.get("/user_input/mobo/{recommeded_mobo}")
def test_mobo_for_cpu(preferred_cpu_socket:str):
    try:
        cpu_socket_type =  preferred_cpu_socket   
    
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
       
       #query
        query = "SELECT * FROM motherboards WHERE socket_type LIKE ? "      
        cursor.execute( query, (f"%{cpu_socket_type}%",))
        
      
        mobo = cursor.fetchall()
        result = [dict(row) for row in mobo]

        print(f"Fetched Motherboards: {result}")
        conn.close()

        if result:
            return {"mobo": result}
        raise HTTPException(status_code=404, detail="mobo not found")
    
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    

#twest GPU retrieval
@app.get("/user_input/gpu/{recommeded_gpu}")
def test_mobo_for_cpu(mobo_gpu_socket:str):
    try:
        
    
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
       
       #query
        query = "SELECT * FROM gpus WHERE compatible_sockets LIKE ? "      
        cursor.execute( query, (f"%{mobo_gpu_socket}%",))
        
      
        gpu = cursor.fetchall()
        result = [dict(row) for row in gpu]

        print(f"Fetched GPU: {result}")
        conn.close()

        if result:
            return {"gpu": result}
        raise HTTPException(status_code=404, detail="GPU not found")
    
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")


#Test PSU retrieval
@app.get("/user_input/psu/{recommeded_psu}")
def test_psu_fetch(components_required_watts:int):
    try:
        components_required_watts += int(components_required_watts * 0.10)
        print(components_required_watts)
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
       
       #query
        query = "SELECT * FROM psus WHERE watt_output <= ? "      
        cursor.execute( query, (f"{components_required_watts}",))
        
      
        psu = cursor.fetchall()
        result = [dict(row) for row in psu]

        print(f"Fetched PSU: {result}")
        conn.close()

        if result:
            return {"gpu": result}
        raise HTTPException(status_code=404, detail="GPU not found")
    
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    

#Test Fetching case test
@app.get("/user_input/case/{recommeded_case}")
def test_mobo_for_cpu(mobo_form_factor:str, pref_size):
    try:
        
    
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
       
       #query
        query = "SELECT * FROM cases WHERE form_factor_compatability LIKE ? AND case_size LIKE ? "      
        cursor.execute( query, (f"%{mobo_form_factor}%",f"%{pref_size}%"))
        
      
        gpu = cursor.fetchall()
        result = [dict(row) for row in gpu]

        print(f"Fetched compatible case: {result}")
        conn.close()

        if result:
            return {"case": result}
        raise HTTPException(status_code=404, detail="case not found")
    
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    
@app.post("/user_build")

# Root endpoint to validate API is running
@app.get("/")
def root():
    return {"message": "PC Builder API is running. Use /recommend endpoint for recommendations."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)