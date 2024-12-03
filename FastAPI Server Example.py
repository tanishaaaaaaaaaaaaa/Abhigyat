from fastapi import FastAPI
from fastapi.testclient import TestClient  # Import TestClient for testing

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI server!"}

@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello, {name}!"}

# Use TestClient for testing the endpoints
if __name__ == "__main__":
    client = TestClient(app)

    # Test the root endpoint
    response = client.get("/")
    print("Root Endpoint Response:", response.json())

    # Test the hello endpoint
    name = "Tanisha"
    response = client.get(f"/hello/{name}")
    print(f"Hello Endpoint Response for {name}:", response.json())

