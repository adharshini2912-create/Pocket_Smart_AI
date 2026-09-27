from fastapi import APIRouter,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
router=APIRouter(); templates=Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent/'templates'))
@router.get('/',response_class=HTMLResponse)
def home(request:Request): return templates.TemplateResponse('index.html',{'request':request})
@router.get('/login',response_class=HTMLResponse)
def login(request:Request): return templates.TemplateResponse('login.html',{'request':request})
@router.get('/register',response_class=HTMLResponse)
def register(request:Request): return templates.TemplateResponse('register.html',{'request':request})
@router.get('/dashboard',response_class=HTMLResponse)
def dashboard(request:Request): return templates.TemplateResponse('dashboard.html',{'request':request})
@router.get('/planner/{planner}',response_class=HTMLResponse)
def planner(request:Request,planner:str):
    if planner not in {'home','party','jewelry'}: return templates.TemplateResponse('404.html',{'request':request},status_code=404)
    return templates.TemplateResponse(f'{planner}.html',{'request':request})
@router.get('/history',response_class=HTMLResponse)
def history(request:Request): return templates.TemplateResponse('history.html',{'request':request})
