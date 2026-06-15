import os
import requests
import time
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

# Caching variables
cached_response = None
last_fetch_time = 0
CACHE_DURATION = 300  # 5 minutes (300 seconds)

@app.get("/allbatch")
def get_allbatch():
    global cached_response, last_fetch_time
    
    current_time = time.time()
    
    # Agar cache valid hai (5 minute se kam purana), toh cached data return karo
    if cached_response and (current_time - last_fetch_time) < CACHE_DURATION:
        return JSONResponse(content=cached_response, status_code=200)
    
    # Naya data fetch karna hai
    url = "https://examcrushers.in/NT/proxy.php?endpoint=all-course"
    
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://examcrushers.in/NT/",
        "sec-ch-ua": '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
    }
    
    cookies = {
        "PHPSESSID": "b1566a4220426b26964bc18bd776eb6c",
        "examcrushers_user_id": "user_6a2f9885427ab_808218b3051618dd53d51e8f0bd4d941",
        "__test": "12317a504a1abe5f0c137a0158ef1807",
        "cf_clearance": "c1HZhL.yDbYhkvx7_NwwflzdbUPZMjNGV1.rMDkCNHM-1781519258-1.2.1.1-v8pNgvEZrAviT4HqAm18zb1urkKaVd6IQl84BzkhD0dfahbBDwC.eO1rjzBlwvEBu7E9Hv2Y.oxWAfTTuhMsA4f54qqRSKpZsk0jvy3XiPvzxsV76Na.FrPuvVQ0TeUT6k4aCHFczgB6Wpx.YWyxIetCfV7xT36P0I9RCPwJ5rA.tgLV9Q2n_G5CvDXpzOW27MxLSfULCn_lGiuK.f1VcJIsUilKrNNX53wPG4n6lJRDIHy9KETFVS1RhOQQaf.SlpqHtD4SHNFg_ZQhMFtyoBuaTtGZXzmv9qgSVOy9IXimrNWB_gvCA1shZPAEFndzte9i792.2HRNeYx7.4W.QA"
    }

    try:
        response = requests.get(url, headers=headers, cookies=cookies, timeout=15)
        
        # Check karo ki response valid hai ya nahi
        if response.status_code == 200:
            try:
                data = response.json()
                # Agar data mein "success": true hai, toh cache update karo
                if data.get("success"):
                    cached_response = data
                    last_fetch_time = current_time
                    return JSONResponse(content=data, status_code=200)
                else:
                    # Agar success false hai, toh cached data use karo
                    if cached_response:
                        return JSONResponse(content=cached_response, status_code=200)
                    return JSONResponse(content=data, status_code=200)
            except Exception as json_error:
                # JSON parse fail ho gaya (empty ya HTML response)
                # Cached data return karo agar available hai
                if cached_response:
                    return JSONResponse(content=cached_response, status_code=200)
                return JSONResponse(
                    content={"success": False, "error": "Invalid JSON response from upstream", "details": str(json_error)}, 
                    status_code=502
                )
        else:
            # Non-200 status code
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
            content={"success": False, "error": "Request to upstream API timed out"}, 
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
        "message": "Hit /allbatch to get course data.",
        "cache_info": {
            "has_cache": cached_response is not None,
            "cache_age_seconds": int(time.time() - last_fetch_time) if cached_response else None
        }
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
