from fastapi import FastAPI
import requests

app = FastAPI(
    title="Exam Crushers API",
    version="1.0.0"
)

BASE_URL = "https://examcrushers.in/NT/proxy.php"


@app.get("/")
def home():
    return {
        "status": "online",
        "message": "Railway API Running"
    }


@app.get("/allbatch")
def allbatch():
    try:
        r = requests.get(
            f"{BASE_URL}?endpoint=all-course",
            timeout=30
        )

        return r.json()

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@app.get("/health")
def health():
    return {"status": "ok"}