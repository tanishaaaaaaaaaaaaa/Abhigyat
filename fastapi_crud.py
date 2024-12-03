from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.testclient import TestClient
import asyncio

app = FastAPI()
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["crud_api"]
collection = db["users"]

# Create user
@app.post("/create-user")
async def create_user(name: str, age: int):
    result = await collection.insert_one({"name": name, "age": age})
    return {"id": str(result.inserted_id)}

# Get user
@app.get("/get-user/{name}")
async def get_user(name: str):
    user = await collection.find_one({"name": name})
    return user or {"error": "User not found"}

# Update user
@app.put("/update-user/{name}")
async def update_user(name: str, age: int):
    result = await collection.update_one({"name": name}, {"$set": {"age": age}})
    return {"modified_count": result.modified_count}

# Delete user
@app.delete("/delete-user/{name}")
async def delete_user(name: str):
    result = await collection.delete_one({"name": name})
    return {"deleted_count": result.deleted_count}

# Testing the endpoints using TestClient
if __name__ == "__main__":
    # Use TestClient to make requests to the FastAPI application
    client_test = TestClient(app)

    # 1. Create a new user
    response = client_test.post("/create-user", json={"name": "Alice", "age": 30})
    print("Create User Response:", response.json())

    # 2. Get the created user
    response = client_test.get("/get-user/Alice")
    print("Get User Response:", response.json())

    # 3. Update the user age
    response = client_test.put("/update-user/Alice", json={"age": 35})
    print("Update User Response:", response.json())

    # 4. Get the updated user
    response = client_test.get("/get-user/Alice")
    print("Get Updated User Response:", response.json())

    # 5. Delete the user
    response = client_test.delete("/delete-user/Alice")
    print("Delete User Response:", response.json())

    # 6. Try to get the deleted user
    response = client_test.get("/get-user/Alice")
    print("Get Deleted User Response:", response.json())
