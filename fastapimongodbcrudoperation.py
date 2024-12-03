from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

app = FastAPI()

# Step 1: Connect to MongoDB
# MongoDB is a NoSQL database, and we connect to it using motor, an async MongoDB client.
client = AsyncIOMotorClient("mongodb://localhost:27017")  # The default MongoDB address
db = client["crud_example"]  # The database we are working with
collection = db["users"]  # The collection (table) where we store user data

# Step 2: Create a Pydantic model for user input validation
# This defines the structure of the data we expect for each user (name and age)
class User(BaseModel):
    name: str  # The user's name
    age: int   # The user's age

# Step 3: Create User (POST) - Insert a new user into the collection
@app.post("/create-user")
async def create_user(user: User):
    # Insert the user into the collection. 'user.dict()' converts the Pydantic model to a dictionary.
    result = await collection.insert_one(user.dict())
    return {"message": "User created successfully", "id": str(result.inserted_id)}  # Return success message with the new user ID

# Step 4: Get User (GET) - Fetch a user by their name
@app.get("/get-user/{name}")
async def get_user(name: str):
    # Look for the user by name in the collection
    user = await collection.find_one({"name": name})
    if user:
        user["_id"] = str(user["_id"])  # Convert the ObjectId (MongoDB's ID format) to a string for easy reading
        return user  # Return the user data if found
    return {"error": "User not found"}  # Return error if no user is found with the given name

# Step 5: Update User (PUT) - Update a user's age by name
@app.put("/update-user/{name}")
async def update_user(name: str, age: int):
    # Update the user's age where the name matches
    result = await collection.update_one({"name": name}, {"$set": {"age": age}})
    if result.matched_count:  # Check if the user was found and updated
        return {"message": f"User {name} updated successfully"}  # Return success message
    return {"error": "User not found"}  # Return error if no user is found

# Step 6: Delete User (DELETE) - Remove a user by their name
@app.delete("/delete-user/{name}")
async def delete_user(name: str):
    # Delete the user from the collection by name
    result = await collection.delete_one({"name": name})
    if result.deleted_count:  # Check if a user was deleted
        return {"message": f"User {name} deleted successfully"}  # Return success message
    return {"error": "User not found"}  # Return error if no user is found

# Step 7: Get All Users (GET) - Fetch all users in the collection
@app.get("/get-all-users")
async def get_all_users():
    users = []  # Initialize an empty list to store the users
    async for user in collection.find():  # Fetch all users in the collection
        user["_id"] = str(user["_id"])  # Convert ObjectId to string
        users.append(user)  # Add each user to the list
    return {"users": users}  # Return the list of users

# Step 8: Count Users (GET) - Get the total number of users
@app.get("/count-users")
async def count_users():
    count = await collection.count_documents({})  # Count the total number of documents (users) in the collection
    return {"user_count": count}  # Return the user count

# uvicorn fastapimongodbcrudoperation:app --reload