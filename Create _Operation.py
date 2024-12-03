from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
from fastapi.responses import JSONResponse

# Initialize FastAPI app
app = FastAPI()

# MongoDB client setup (update the connection string as needed)
client = MongoClient("mongodb://localhost:27017/")
db = client["your_database_name"]
collection = db["your_collection_name"]

# Define the Item model
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    quantity: int

# Custom JSONResponse to handle ObjectId serialization
class CustomJSONResponse(JSONResponse):
    def render(self, content: dict) -> bytes:
        if "_id" in content:
            content["_id"] = str(content["_id"])
        return super().render(content)

@app.post("/items/", response_class=CustomJSONResponse)
async def create_item(item: Item):
    document = item.dict()
    result = await collection.insert_one(document)
    return CustomJSONResponse(content={"id": str(result.inserted_id)})

# You can run the FastAPI app using: uvicorn Create_Operation:app --reload