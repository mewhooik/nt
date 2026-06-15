from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok"}

@app.get("/allbatch")
def allbatch():
    return requests.get(
        "https://examcrushers.in/NT/proxy.php?endpoint=all-course"
    ).json()
