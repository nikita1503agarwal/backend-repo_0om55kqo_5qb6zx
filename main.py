import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from database import db, create_document, get_documents

app = FastAPI(title="Nautical School Admin API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Nautical School Admin Backend Running"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response

# -----------------------------
# Admin API for Courses
# -----------------------------
class CourseCreate(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    modality: Optional[str] = None
    duration_hours: Optional[int] = None
    price: float
    seats: Optional[int] = 8
    is_published: bool = True
    tags: List[str] = []

class CourseOut(CourseCreate):
    id: str

@app.post("/api/courses", response_model=dict)
def create_course(course: CourseCreate):
    try:
        new_id = create_document("course", course.model_dump())
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/courses", response_model=List[dict])
def list_courses():
    try:
        items = get_documents("course")
        # Normalize ObjectId to string
        for it in items:
            it["id"] = str(it.pop("_id"))
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------
# Admin API for Enrollments
# -----------------------------
class EnrollmentCreate(BaseModel):
    course_id: str
    student_name: str
    email: str
    phone: Optional[str] = None
    preferred_dates: Optional[str] = None
    status: str = "pending"
    notes: Optional[str] = None

@app.post("/api/enrollments", response_model=dict)
def create_enrollment(enrollment: EnrollmentCreate):
    try:
        new_id = create_document("enrollment", enrollment.model_dump())
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/enrollments", response_model=List[dict])
def list_enrollments():
    try:
        items = get_documents("enrollment")
        for it in items:
            it["id"] = str(it.pop("_id"))
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
