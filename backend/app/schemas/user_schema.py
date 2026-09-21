from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


class UserResponse(BaseModel):
    # print("(UserResponse) userschema-->")
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
# This tells Pydantic that it can create this schema from an object’s attributes, not only from a dictionary.That works because values are accessed like:

# data["id"]
# data["name"]
# data["email"]
# But in FastAPI with SQLAlchemy, you often have a database object:

# user.id
# user.name
# user.email