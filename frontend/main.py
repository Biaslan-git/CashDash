from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from api import router as api_router

app = FastAPI()
app.include_router(api_router)

BACKEND_URL = 'http://localhost:8000'

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
templates.env.globals.update({
    "backend_url": BACKEND_URL,
})


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
    })

@app.get("/transactions", response_class=HTMLResponse)
async def transactions(request: Request):
    return templates.TemplateResponse("transactions.html", {
        "request": request,
    })
