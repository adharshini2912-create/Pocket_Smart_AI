import json
from fastapi import APIRouter,Depends,File,Form,HTTPException,Request,UploadFile
from ..database import get_db
from ..models.schemas import HomeRequest,PartyRequest,JewelryRequest
from ..security import decode_token
from ..services.gemini_service import generate
router=APIRouter(prefix='/api',tags=['planners'])
def current_user(request:Request):
    uid=decode_token(request.cookies.get('access_token',''))
    if not uid: raise HTTPException(401,'Please login first')
    return uid
def save(uid,planner,data,result):
    c=get_db(); c.execute('INSERT INTO recommendations(user_id,planner,request_json,response_json) VALUES(?,?,?,?)',(uid,planner,json.dumps(data),json.dumps(result))); c.commit(); c.close()
@router.post('/generate-home')
def home(d:HomeRequest,uid:int=Depends(current_user)):
    x=generate('home',d.model_dump()); save(uid,'home',d.model_dump(),x); return {'planner':'home','budget':d.budget,'currency':'INR',**x}
@router.post('/generate-party')
def party(d:PartyRequest,uid:int=Depends(current_user)):
    x=generate('party',d.model_dump()); save(uid,'party',d.model_dump(),x); return {'planner':'party','budget':d.budget,'currency':'INR',**x}
@router.post('/generate-jewelry')
async def jewelry(request:Request,uid:int=Depends(current_user),budget:float=Form(...),occasion:str=Form(...),style:str=Form('elegant'),outfit_color:str=Form('not specified'),preferences:str=Form(''),outfit_image:UploadFile|None=File(None)):
    if budget<=0 or budget>10000000: raise HTTPException(422,'Invalid budget')
    b=None; mime=None
    if outfit_image:
        if outfit_image.content_type not in {'image/jpeg','image/png','image/webp'}: raise HTTPException(400,'Use JPG, PNG or WEBP image')
        b=await outfit_image.read()
        if len(b)>5*1024*1024: raise HTTPException(413,'Image must be 5 MB or smaller')
        mime=outfit_image.content_type
    d=JewelryRequest(budget=budget,occasion=occasion,style=style,outfit_color=outfit_color,preferences=preferences); x=generate('jewelry',d.model_dump(),b,mime); save(uid,'jewelry',d.model_dump(),x); return {'planner':'jewelry','budget':budget,'currency':'INR',**x}
@router.get('/history')
def history(uid:int=Depends(current_user)):
    c=get_db(); rows=c.execute('SELECT id,planner,request_json,response_json,created_at FROM recommendations WHERE user_id=? ORDER BY id DESC',(uid,)).fetchall(); c.close(); return [{'id':r['id'],'planner':r['planner'],'request':json.loads(r['request_json']),'response':json.loads(r['response_json']),'created_at':r['created_at']} for r in rows]
@router.get('/recommendations-details/{rid}')
def details(rid:int,uid:int=Depends(current_user)):
    c=get_db(); r=c.execute('SELECT * FROM recommendations WHERE id=? AND user_id=?',(rid,uid)).fetchone(); c.close()
    if not r: raise HTTPException(404,'Recommendation not found')
    return {'id':r['id'],'planner':r['planner'],'request':json.loads(r['request_json']),'response':json.loads(r['response_json']),'created_at':r['created_at']}
