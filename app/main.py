from fastapi import FastAPI

app = FastAPI(title="PDF Summary AI")


@app.get("/")
def health():
    return {"status": "ok"}
