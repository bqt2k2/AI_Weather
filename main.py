from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()  # <== Thêm dòng này để load file .env
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# Khởi tạo app
app = FastAPI()

# Cấu hình static và templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Cấu hình Gemini API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Khởi tạo model Gemini
model = genai.GenerativeModel("gemini-2.0-flash")


@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "response": ""}
    )


@app.post("/chat", response_class=HTMLResponse)
async def post_chat(request: Request, message: str = Form(...)):
    try:
        response = model.generate_content(message)
        reply = response.text
    except Exception as e:
        reply = f"Lỗi: {e}"
    return templates.TemplateResponse(
        "index.html", {"request": request, "response": reply}
    )
