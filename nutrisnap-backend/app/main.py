from fastapi import FastAPI

app = FastAPI(title="NutriSnap API")


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
