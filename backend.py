from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sqlite3
from pathlib import Path
from typing import Optional, List
from pydantic import BaseModel
from enum import Enum

app = FastAPI()


# Database path
BASE_DIR = Path(__file__).parent
DATABASE_URL = BASE_DIR / "components.db"



# Request model for recommendations
class UserComponentInput(BaseModel):
    
    #needs changing sql 
    cpu_model: str 
    #needs changing sql
    case_size: str
    #needs changing sql
    cooling: str 
    #frontend changing
    pref_memory_size: str
    pref_storage_size: int
    pref_memory_type: str
    pref_storage_type: str


#data validation for build
class RecommendedBuildForUser(BaseModel):
    
     recommended_cpu_name:str
     recommended_cpu_price: int
     recommended_gpu_name: str
     recommended_gpu_price: int   
     recommended_mobo_name: str
     recommended_mobo_price: int
     recommended_psu_name: str
     recommended_psu_price: int
     recommended_case_name: str
     recommended_case_price: int
     recommended_cooling_name:str
     recommended_cooling_price: int
     recommended_storage_name: str
     recommended_storage_price:int
     recommended_memory_name: str
     recommended_memory_price: int
     recommended_total_cost: int



#-------------------code thhat interacts with database--------------
#note we are fetching one build muna so we have to use the function Fetchone instead of fetchall here



#function to establish DB connection
def get_db_connection():
    try:
        conn = sqlite3.connect(str(DATABASE_URL))
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"DB connection error on {DATABASE_URL}: {e}")
    
#fetch compatible gpu from database
def fetch_gpu(mobo_gpu_socket):
    try:
        
    
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
       
       #query
        query = "SELECT * FROM gpus WHERE compatible_sockets LIKE ? "      
        cursor.execute( query, (f"%{mobo_gpu_socket}%",))
        
      
        row = cursor.fetchone()
        

        if row:
            gpu = dict(row)

            print(f"Fetched GPU: {gpu}")
            conn.close()
            return {"recommended_gpu": gpu}
        raise HTTPException(status_code=404, detail="GPU not found")
    
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

#fetch mother board with cpu socket
def get_mobo_with_cpu(cpu_socket_type:str):
    try:
             
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
       
       #query
        query = "SELECT * FROM motherboards WHERE socket_type LIKE ? "      
        cursor.execute( query, (f"%{cpu_socket_type}%",))
        
      
        row = cursor.fetchone()
        mobo = dict(row)

        print(f"Fetched Motherboards: {mobo}")
        conn.close()

        if mobo:
            return {"recommended_mobo": mobo}
        raise HTTPException(status_code=404, detail="mobo not found")
    
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

#fetch cpu with user input
def get_cpu(cpu_model:str):
    try:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
       
       #query
        query = "SELECT * FROM cpus WHERE series LIKE ? "      
        cursor.execute( query, (f"%{cpu_model}%",))
        
      
        row = cursor.fetchone()
        cpu = dict(row)
        print(f"Fetched CPUs: {cpu}")
        conn.close()

        if cpu:
            return {"recommended_cpu":  cpu}

        
        raise HTTPException(status_code=404, detail="CPU not found")
    
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

#fetch psu in db
def fetch_psu(components_required_watts:int):
    try:
        components_required_watts += int(components_required_watts * 0.10)
        print(components_required_watts)
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
       
       #query
        query = "SELECT * FROM psus WHERE watt_output >= ? "      
        cursor.execute( query, (f"{components_required_watts}",))
        
      
        row = cursor.fetchone()
        if row:
         psu = dict(row) 

         print(f"Fetched PSU: {psu}")
         conn.close()

        
         return {"recommended_psu": psu}
        raise HTTPException(status_code=404, detail="psu not found")
    
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

#fetch case in db    
def fetch_case(mobo_form_factor:str,pref_size:str):
    try:
        
    
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
       
       #query
        query = "SELECT * FROM cases WHERE form_factor_compatability LIKE ? AND case_size LIKE ? "      
        cursor.execute( query, (f"%{mobo_form_factor}%",f"%{pref_size}%"))
        
      
        row = cursor.fetchone()
        if row:
            case = dict(row)

            print(f"Fetched compatible case: {case}")
            conn.close()

            return {"recommended_case": case}
        else:
            return{"no case in our database compatible with your case preference"}
        raise HTTPException(status_code=404, detail="case not found")
        
        
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    
#fetch cooling in db
def fetch_cooling(mobo_socket_type:str,cooling:str):
    try:
        
    
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
       
       #query
        query = "SELECT * FROM cooling_systems WHERE compatible_sockets LIKE ? AND cooling_type LIKE ? "      
        cursor.execute( query, (f"%{mobo_socket_type}%",f"%{cooling}%"))
        
      
        row = cursor.fetchone()
        if row:
            cooling = dict(row)

            print(f"Fetched compatible cooling: {cooling}")
            conn.close()

            return {"recommended_cooling": cooling}
        else:
            return{"no cooling in our database compatible with your cooling preference check other options"}
        raise HTTPException(status_code=404, detail="case not found")
        
        
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")    

def fetch_storage(pref_storage_type: str, pref_storage_size: int ):
    try:
        
    
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
       
       #query
        query = "SELECT * FROM storage WHERE storage_type LIKE ? AND capacity == ? "      
        cursor.execute( query, (f"%{pref_storage_type}%",f"{pref_storage_size:}"))
        
      
        row = cursor.fetchone()
        if row:
            storage = dict(row)

            print(f"Fetched storage: {storage}")
            conn.close()

            return {"recommended_storage": storage}
        else:
            return{"no cooling in our database compatible with your cooling preference check other options"}
        raise HTTPException(status_code=404, detail="case not found")
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")   

def fetch_memory(pref_memory_type: str, pref_memory_size: str ):
    try:
        
    
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
       
       #query
        query = "SELECT * FROM ram WHERE ram_type LIKE ? AND size LIKE ? "      
        cursor.execute( query, (f"%{pref_memory_type}%",f"%{pref_memory_size}%"))
        
      
        row = cursor.fetchone()
        if row:
            memory = dict(row)

            print(f"Fetched memory: {memory}")
            conn.close()

            return {"recommended_memory": memory}
        else:
            return{"no cooling in our database compatible with your cooling preference check other options"}
        raise HTTPException(status_code=404, detail="case not found")
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")   
#-------------------code thhat interacts with database end--------------

#User input 
@app.post("/get_user_build")
async def get_user_build(input: UserComponentInput):
    try:
     


     #getting the data we need from the database to send the recommended build to the user
     cpu = get_cpu(input.cpu_model)   
     cpu_socket = cpu.get("recommended_cpu", {}).get("socket_type")

     mobo = get_mobo_with_cpu(cpu_socket)
     mobo_gpu_socket = mobo.get("recommended_mobo", {}).get("gpu_socket")
     mobo_form_factor = mobo.get("recommended_mobo", {}).get("form_factor")
     mobo_socket_type = mobo.get("recommended_mobo", {}).get("socket_type")

     gpu = fetch_gpu(mobo_gpu_socket)
     ComCase= fetch_case(mobo_form_factor, input.case_size)
     cooling = fetch_cooling(mobo_socket_type, input.cooling) 
     storage= fetch_storage(input.pref_storage_type,input.pref_storage_size)
     memory= fetch_memory(input.pref_memory_type,input.pref_memory_size)
     


     # to get recommended PSU
     cpu_watts=int(cpu.get("recommended_cpu", {}).get("required_watt"))
     mobo_watts=int(mobo.get("recommended_mobo", {}).get("required_watt"))
     gpu_watts=int(gpu.get("recommended_gpu", {}).get("required_watt"))
     cooling_watts=int(cooling.get("recommended_cooling", {}).get("required_watt"))
     storage_watts=int(storage.get("recommended_storage", {}).get("required_watt"))
     memory_watts=int(memory.get("recommended_memory", {}).get("required_watt"))
    
     required_watts= cpu_watts + mobo_watts + gpu_watts + cooling_watts + storage_watts + memory_watts

     psu= fetch_psu(required_watts)
     
     #to get the name of all the components
     cpu_name=str(cpu.get("recommended_cpu", {}).get("name"))
     mobo_name=str(mobo.get("recommended_mobo", {}).get("name"))
     gpu_name=str(gpu.get("recommended_gpu", {}).get("model"))
     cooling_name=str(cooling.get("recommended_cooling", {}).get("name"))     
     psu_name=str(psu.get("recommended_psu", {}).get("name"))
     case_name=str(ComCase.get("recommended_case", {}).get("name"))

     #need different way of handling it
     storage_name=str(storage.get("recommended_storage", {}).get("storage_type")) + " " + str(storage.get("recommended_storage", {}).get("capacity")) + " GB Storage"
     memory_name=str(memory.get("recommended_memory", {}).get("ram_type")) +" "+ str(memory.get("recommended_memory", {}).get("size")) +" Memory"

     #to get price of all components

     cpu_price=cpu.get("recommended_cpu", {}).get("price")
     mobo_price=mobo.get("recommended_mobo", {}).get("price")
     gpu_price=gpu.get("recommended_gpu", {}).get("price")
     cooling_price=cooling.get("recommended_cooling", {}).get("price")
     storage_price=storage.get("recommended_storage", {}).get("price")
     memory_price=memory.get("recommended_memory", {}).get("price")
     psu_price=psu.get("recommended_psu", {}).get("price")
     case_price=ComCase.get("recommended_case", {}).get("price")

     total_price= cpu_price + mobo_price + gpu_price + cooling_price + storage_price + memory_price + psu_price + case_price
     
     build= RecommendedBuildForUser(recommended_cpu_name= cpu_name, recommended_cpu_price= cpu_price, recommended_gpu_name= gpu_name, recommended_gpu_price= gpu_price, recommended_mobo_name=mobo_name, recommended_mobo_price=mobo_price,recommended_psu_name=psu_name,recommended_psu_price=psu_price,recommended_case_name=case_name,recommended_case_price=case_price,recommended_cooling_name=cooling_name,recommended_cooling_price=cooling_price,recommended_storage_name=storage_name, recommended_storage_price=storage_price, recommended_memory_name=memory_name, recommended_memory_price= memory_price, recommended_total_cost=total_price)

     return{"build":build}
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})



#-------------------to test code thhat interacts with database easily--------------
@app.get("/user_input/cpu/{preferred_cpu}")
def test_fetch_cpu(cpu_model:str):
    try:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
       
       #query
        query = "SELECT * FROM cpus WHERE series LIKE ? "      
        cursor.execute( query, (f"%{cpu_model}%",))
        
      
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
    
#test GPU retrieval
@app.get("/user_input/gpu/{recommeded_gpu}")
def test_gpu_for_mobo(mobo_gpu_socket:str):
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
    

#-------------------to test code thhat interacts with database easily end --------------



#-------------------Uvicorn--------------
# Root endpoint to validate API is running
@app.get("/")
def root():
    return {"message": "PC Builder API is running. Use /recommend endpoint for recommendations."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)