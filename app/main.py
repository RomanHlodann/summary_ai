from __future__ import annotations

import logging

from contextlib import asynccontextmanager
from fastapi import Depends, BackgroundTasks, UploadFile, FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.services.openai import OpenAIClient
from app.services.container import Container, get_container

from dotenv import load_dotenv


load_dotenv()

templates = Jinja2Templates(directory="app/templates")

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.openai_client = OpenAIClient()
    yield


app = FastAPI(title="PDF Summarizer", lifespan=lifespan)


@app.post("/summarize")
async def summarize_pdf(
    file: UploadFile,
    background_tasks: BackgroundTasks,
    container: Container = Depends(get_container),
):
    inspection = await container.inspector.inspect(file)

    record = await container.repo.create(
        file_name=inspection["filename"],
        file_size=inspection["file_size"],
    )

    background_tasks.add_task(
        container.processor.process,
        record.id,
        inspection["content"],
        inspection["filename"],
    )

    return RedirectResponse(url="/", status_code=303)


@app.get("/", response_class=HTMLResponse)
async def ui(
    request: Request,
    container: Container = Depends(get_container),
):
    history = await container.repo.get_last(limit=5)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "history": history,
        },
    )


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
