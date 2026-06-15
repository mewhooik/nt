import os
import requests
import time
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

# Caching variables
cached_response = None
last_fetch_time = 0
CACHE_DURATION = 300  # 5 minutes

@app.get("/allbatch")
def get_allbatch():
    global cached_response, last_fetch_time
    
    current_time = time.time()
    
    # Agar cache valid hai (5 minute se kam purana), toh cached data return karo
    if cached_response and (current_time - last_fetch_time) < CACHE_DURATION:
        return JSONResponse(content=cached_response, status_code=200)
    
    # Original API URL
    url = "https://nt.rarestudy.in/api/batches"
    
    # Headers
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://nt.rarestudy.in/",
        "sec-ch-ua": '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
    }
    
    # Cookies
    cookies = {
        "nt_favs": '["179"]',
        "nt_completed": "{}"
    }

    try:
        # Original API se data fetch karna
        response = requests.get(url, headers=headers, cookies=cookies, timeout=15)
        
        # Check karo ki response valid hai ya nahi
        if response.status_code == 200:
            try:
                data = response.json()
                # Cache update karo
                cached_response = data
                last_fetch_time = current_time
                return JSONResponse(content=data, status_code=200)
            except Exception as json_error:
                # JSON parse fail - cached data use karo
                if cached_response:
                    return JSONResponse(content=cached_response, status_code=200)
                return JSONResponse(
                    content={"success": False, "error": "Invalid JSON from upstream", "details": str(json_error)}, 
                    status_code=502
                )
        else:
            # Non-200 status - cached data use karo
            if cached_response:
                return JSONResponse(content=cached_response, status_code=200)
            return JSONResponse(
                content={"success": False, "error": f"Upstream returned status {response.status_code}"}, 
                status_code=502
            )
            
    except requests.exceptions.Timeout:
        if cached_response:
            return JSONResponse(content=cached_response, status_code=200)
        return JSONResponse(
            content={"success": False, "error": "Request timed out"}, 
            status_code=504
        )
    except Exception as e:
        if cached_response:
            return JSONResponse(content=cached_response, status_code=200)
        return JSONResponse(
            content={"success": False, "error": str(e)}, 
            status_code=500
        )

@app.get("/")
def root():
    return {
        "status": "API is running successfully",
        "message": "Hit /allbatch to get batches data from nt.rarestudy.in",
        "cache_info": {
            "has_cache": cached_response is not None,
            "cache_age_seconds": int(time.time() - last_fetch_time) if cached_response else None
        }
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
