from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db
init_db()
client=TestClient(app)
def test_health():
    r=client.get('/health'); assert r.status_code==200 and r.json()['status']=='ok'
def test_register_and_home():
    import uuid
    email=uuid.uuid4().hex[:10]+'@example.com'
    r=client.post('/api/auth/register',json={'username':'tester'+uuid.uuid4().hex[:5],'email':email,'password':'secret123'}); assert r.status_code==200
    r=client.post('/api/generate-home',json={'budget':50000,'rooms':'Living room','items':'Sofa, lights','style':'modern','priorities':'value'}); assert r.status_code==200 and r.json()['planner']=='home' and r.json()['recommendations']
