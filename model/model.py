from pydantic import BaseModel

class Blog(BaseModel):
    username:str
    email:str
    password:str
    title:str
    description:str
    content:str
    author:str
class LinkID(BaseModel):
    user_id:str
    linked_id:str