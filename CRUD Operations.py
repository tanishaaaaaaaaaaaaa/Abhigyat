from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["crud_database"]
collection = db["crud_collection"]

async def crud_operations():
    # Create
    result = await collection.insert_one({"name": "Charlie", "age": 22})
    print("Created Document ID:", result.inserted_id)

    # Read
    document = await collection.find_one({"name": "Charlie"})
    print("Fetched Document:", document)

    # Update
    await collection.update_one({"name": "Charlie"}, {"$set": {"age": 23}})
    updated_document = await collection.find_one({"name": "Charlie"})
    print("Updated Document:", updated_document)

    # Delete
    await collection.delete_one({"name": "Charlie"})
    print("Deleted Document")

# Run the operations
asyncio.run(crud_operations())
