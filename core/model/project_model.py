import uuid
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

# We reuse the Utils to ensure date consistency if needed, 
# but for the model definition, we just expect strings.

class UseCase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    # Optional ID: 
    # - Present? -> Updates existing Use Case
    # - None?    -> Creates new Use Case
    id: Optional[str] = Field(None, alias="_id") 
    name: str
    deadline: str

class Project(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    # Project ID (Only for reading/URL, usually not sent in Body for Edit)
    id: Optional[str] = Field(None, alias="_id")
    
    # Immutable fields (Sent only on Add)
    fid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    
    # Mutable fields
    name: str
    usecases: List[UseCase] = []
    
    # Timestamps
    created_at: str
    updated_at: str
