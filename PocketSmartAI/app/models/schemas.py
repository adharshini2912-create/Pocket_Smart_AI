from pydantic import BaseModel,Field
from typing import Optional
class RegisterRequest(BaseModel): username:str=Field(min_length=3,max_length=40); email:str; password:str=Field(min_length=6,max_length=128)
class LoginRequest(BaseModel): email:str; password:str
class HomeRequest(BaseModel): budget:float=Field(gt=0,le=10000000); rooms:str=Field(min_length=1,max_length=500); items:str=Field(min_length=1,max_length=1000); style:str='modern'; priorities:str='value for money'
class PartyRequest(BaseModel): budget:float=Field(gt=0,le=10000000); guests:int=Field(gt=0,le=10000); event_type:str=Field(min_length=1,max_length=100); venue:str='flexible'; food_preference:str='mixed'; date:Optional[str]=None
class JewelryRequest(BaseModel): budget:float=Field(gt=0,le=10000000); occasion:str=Field(min_length=1,max_length=100); style:str='elegant'; outfit_color:str='not specified'; preferences:str=''
