import base64,hashlib,hmac,os,time,jwt
from .config import settings
ALG='HS256'; EXP=60*60*8
def hash_password(p):
    salt=os.urandom(16); dk=hashlib.pbkdf2_hmac('sha256',p.encode(),salt,210000); return 'pbkdf2_sha256$210000$'+base64.b64encode(salt).decode()+'$'+base64.b64encode(dk).decode()
def verify_password(p,e):
    try:
        _,n,s,h=e.split('$'); salt=base64.b64decode(s); expected=base64.b64decode(h); actual=hashlib.pbkdf2_hmac('sha256',p.encode(),salt,int(n)); return hmac.compare_digest(actual,expected)
    except Exception:return False
def create_token(uid):
    now=int(time.time()); return jwt.encode({'sub':str(uid),'iat':now,'exp':now+EXP},settings.secret_key,algorithm=ALG)
def decode_token(t):
    try:return int(jwt.decode(t,settings.secret_key,algorithms=[ALG])['sub'])
    except Exception:return None
