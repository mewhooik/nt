import os
import requests
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/allbatch")
def get_allbatch():
    url = "https://examcrushers.in/NT/proxy.php?endpoint=all-course"
    
    # Original API ke headers
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
    
    # Original API ke cookies (Cloudflare bypass ke liye)
    cookies = {
        "PHPSESSID": "b1566a4220426b26964bc18bd776eb6c",
        "examcrushers_user_id": "user_6a2f9885427ab_808218b3051618dd53d51e8f0bd4d941",
        "__test": "12317a504a1abe5f0c137a0158ef1807",
        "cf_clearance": "c1HZhL.yDbYhkvx7_NwwflzdbUPZMjNGV1.rMDkCNHM-1781519258-1.2.1.1-v8pNgvEZrAviT4HqAm18zb1urkKaVd6IQl84BzkhD0dfahbBDwC.eO1rjzBlwvEBu7E9Hv2Y.oxWAfTTuhMsA4f54qqRSKpZsk0jvy3XiPvzxsV76Na.FrPuvVQ0TeUT6k4aCHFczgB6Wpx.YWyxIetCfV7xT36P0I9RCPwJ5rA.tgLV9Q2n_G5CvDXpzOW27MxLSfULCn_lGiuK.f1VcJIsUilKrNNX53wPG4n6lJRDIHy9KETFVS1RhOQQaf.SlpqHtD4SHNFg_ZQhMFtyoBuaTtGZXzmv9qgSVOy9IXimrNWB_gvCA1shZPAEFndzte9i792.2HRNeYx7.4W.QA"
    }

    try:
        # Original API se data fetch karna
        response = requests.get(url, headers=headers, cookies=cookies, timeout=15)
        # Same JSON response return karna
        return JSONResponse(content=response.json(), status_code=response.status_code)
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)

# Root endpoint (Check karne ke liye ki API chal rahi hai)
@app.get("/")
def root():
    return {"status": "API is running successfully", "message": "Hit /allbatch to get course data."}

if __name__ == "__main__":
    import uvicorn
    # Railway automatically PORT environment variable set karta hai
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
