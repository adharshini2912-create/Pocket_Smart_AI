from fastapi import APIRouter,HTTPException,Response,Request
from ..database import get_db
from ..models.schemas import RegisterRequest,LoginRequest
from ..security import hash_password,verify_password,create_token,decode_token
router=APIRouter(prefix='/api/auth',tags=['auth'])
@router.post('/register')
def register(d:RegisterRequest,response:Response):
    c=get_db()
    try: cur=c.execute('INSERT INTO users(username,email,password_hash) VALUES(?,?,?)',(d.username,d.email.lower(),hash_password(d.password))); c.commit(); uid=cur.lastrowid
    except Exception: raise HTTPException(400,'Username or email already exists')
    finally:c.close()
    response.set_cookie('access_token',create_token(uid),httponly=True,samesite='lax'); return {'message':'Registered successfully','user_id':uid,'username':d.username}
@router.post('/login')
def login(d:LoginRequest,response:Response):
    c=get_db(); r=c.execute('SELECT * FROM users WHERE email=?',(d.email.lower(),)).fetchone(); c.close()
    if not r or not verify_password(d.password,r['password_hash']): raise HTTPException(401,'Invalid email or password')
    response.set_cookie('access_token',create_token(r['id']),httponly=True,samesite='lax'); return {'message':'Login successful','username':r['username'],'user_id':r['id']}
@router.post('/logout')
def logout(response:Response): response.delete_cookie('access_token'); return {'message':'Logged out'}
@router.get('/session-info')
def info(request:Request):
    uid=decode_token(request.cookies.get('access_token',''))
    if not uid:return {'authenticated':False}
    c=get_db(); r=c.execute('SELECT id,username,email FROM users WHERE id=?',(uid,)).fetchone(); c.close(); return {'authenticated':bool(r),'user':dict(r) if r else None}
