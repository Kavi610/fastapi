
from django import db
from fastapi import APIRouter
from pymongo import MongoClient
from model.model import Blog, LinkID
from serializer.serializer import convertBlog,convertBlogs
from config.config import blogsCollection,userCollection,pwt_context
from bson import ObjectId
endPoints=APIRouter()
@endPoints.get("/")
async def home():
    return {
        'status':'ck',
        'message':'my first api is running'
    }
    
@endPoints.post("/new/blog")
def newBlog(blog:Blog):
    blogsCollection.insert_one(dict(blog))
    return{
        'status':'ok',
        'message':'Data inserted'
    }
    
@endPoints.get("/all/blog")
def getAllBlogs():
    blogs=blogsCollection.find()
    convertedBlogs=convertBlogs(blogs)
    return{
        'ststus':'ok',
        'data':convertedBlogs
    }
    
@endPoints.get("/blog/{id}")
async def getBlog(id:str):
    blog=blogsCollection.find_one({"_id":ObjectId(id)})
    convertedblog=convertBlog(blog)
    return{
        'status':'OK',
        'data':convertedblog
    }
#register
@endPoints.post("/register")
async def register_user(user: Blog):
    # Check if user already exists
    if db.users.find_one({"email": user.email}):
        return {"error": "User already exists"}

    # Hash the password
    hashed_password = pwt_context.hash(user.password)

    # Insert user into database
    user_id = db.users.insert_one({
        "username": user.username,
        "email": user.email,
        "password": hashed_password
    }).inserted_id

    return {"msg": "User registered successfully", "user_id": str(user_id)}
#update mongodb 
@endPoints.get("/update/{id}")
async def updateBlog(id:str,blog:Blog):
    blogsCollection.find_one_and_update(
    {"_id":ObjectId(id)},
    {'set':dict(blog)}
    )
    return{
        "status":"Ok",
        "message":"data havee been update"
    }
    
#delete
@endPoints.get("/delete/{id}")
async def deleteDoc(id:str):
    blogsCollection.find_one_and_delete(
        {'_id':ObjectId(id)}
    )
    return {
        "status":"Ok",
        "message":"Document have beenn delete"
    }
#login
@endPoints.delete("/delete_user/{user_id}")
async def delete_user(user_id: str):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return {"error": "User not found"}

    # Delete related data across collections
    db.users.delete_one({"_id": ObjectId(user_id)})
    db.orders.delete_many({"user_id": user_id})  # Example for deleting related orders

    return {"msg": "User and associated data deleted successfully"}
#linking ID API
@endPoints.post("/link_id")
async def link_id(link: LinkID):
    user = db.users.find_one({"_id": ObjectId(link.user_id)})
    if user:
        db.users.update_one({"_id": ObjectId(link.user_id)}, {"$set": {"linked_id": link.linked_id}})
        return {"msg": "ID linked successfully"}
    return {"error": "User not found"}
#join
@endPoints.get("/user_details/{user_id}")
async def get_user_details(user_id: str):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return {"error": "User not found"}

    # Join with another collection (e.g., 'orders')
    orders = list(db.orders.find({"user_id": user_id}))
    return {"user": user, "orders": orders}