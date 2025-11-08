from app.main import app
from dotenv import load_dotenv
import os

load_dotenv()
os.makedirs("data", exist_ok=True)
if __name__ == "__main__":
    import uvicorn

    print("\n" + "=" * 60)
    print("FastAPI Server Starting...")
    print("=" * 60)
    print("API Documentation: http://localhost:8000/docs")
    print("Alternative Docs:  http://localhost:8000/redoc")
    print("API Base URL:      http://localhost:8000/api")
    print("=" * 60 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)
