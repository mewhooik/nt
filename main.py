from fastapi import FastAPI
import requests

app = FastAPI(
    title="ExamCrushers API",
    version="1.0"
)

SOURCE_URL = "https://examcrushers.in/NT/proxy.php?endpoint=all-course"


@app.get("/")
def root():
    return {
        "status": "online",
        "message": "API Running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.get("/allbatch")
def allbatch():
    try:
        response = requests.get(
            SOURCE_URL,
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
