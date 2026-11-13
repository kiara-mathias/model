from fastapi import FastAPI

app = FastAPI(title="FitModel API")

@app.get("/health")
def health():
    return {"status": "ok"}
