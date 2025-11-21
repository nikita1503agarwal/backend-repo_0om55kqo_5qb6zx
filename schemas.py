"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Example schemas (you can keep for reference):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# --------------------------------------------------
# Nautical School Admin Schemas
# --------------------------------------------------

class Course(BaseModel):
    """
    Courses offered by the nautical school
    Collection name: "course"
    """
    name: str = Field(..., description="Course name")
    code: str = Field(..., description="Short code, e.g., PER, PNB")
    description: Optional[str] = Field(None, description="Course details")
    modality: Optional[str] = Field(None, description="Sailing, Motor, Theory, Mixed")
    duration_hours: Optional[int] = Field(None, ge=0, description="Duration in hours")
    price: float = Field(..., ge=0, description="Course price in EUR")
    seats: Optional[int] = Field(8, ge=0, description="Available seats")
    is_published: bool = Field(True, description="Visible on website")
    tags: List[str] = Field(default_factory=list, description="Search tags")

class Enrollment(BaseModel):
    """
    Student enrollments for courses
    Collection name: "enrollment"
    """
    course_id: str = Field(..., description="Reference to course _id")
    student_name: str = Field(..., description="Full name of student")
    email: str = Field(..., description="Contact email")
    phone: Optional[str] = Field(None, description="Contact phone")
    preferred_dates: Optional[str] = Field(None, description="Preferred dates or schedule notes")
    status: str = Field("pending", description="pending, confirmed, cancelled")
    notes: Optional[str] = Field(None, description="Internal notes")

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
