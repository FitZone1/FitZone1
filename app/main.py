from fastapi import FastAPI

app = FastAPI(title="FitZone API", version="1.0.0")

@app.get("/")
def root():
    return {"message": "FitZone API funcionando"}

@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0", "environment": "development"}
