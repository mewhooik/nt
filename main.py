from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok"}

@app.get("/allbatch")
def allbatch():
    try:
        url = "https://examcrushers.in/NT/proxy.php?endpoint=all-course"

        r = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=30
        )

        return {
            "status_code": r.status_code,
            "content_type": r.headers.get("content-type"),
            "response": r.text[:1000]
        }

    except Exception as e:
        return {
            "error": str(e)
        }
