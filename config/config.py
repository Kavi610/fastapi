from passlib.context import CryptContext
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://kaviyarasuramesh610:Kaviyarasu610@cluster0.mfocfdd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db=client.myblogs #appname=myblogs
blogsCollection=db['blogs']
userCollection=db['users']
client=MongoClient("mongodb://localhost:27017")
db=client["user_database"]
pwt_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)