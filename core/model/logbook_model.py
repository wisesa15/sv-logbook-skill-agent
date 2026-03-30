import uuid
from datetime import datetime
from typing import List, Optional, Literal, Any, Union
from pydantic import BaseModel, Field, ConfigDict, field_validator

# --- 1. Enums & Helpers ---
WorkModeType = Literal["WFH", "WFO", "WFA", "Workshop", "Leave (Cuti)", "Leave (Sakit)"]

# --- 2. Inner Value Objects (No IDs) ---

class Progress(BaseModel):
    """
    Represents the progress inside an activity.
    Matches JSON: { "type": "...", "value": "...", "percentage": "..." }
    """
    type: str
    value: Union[str, int]  # JSON allows string "1" or int 1, this handles both
    percentage: Union[str, int]

class UsecaseInfo(BaseModel):
    name: str
    deadline: str  # CHANGED: datetime -> str

# --- 3. Entity Objects (Have Optional IDs) ---

class Tool(BaseModel):
    """
    Matches items in the 'tools' list.
    """
    model_config = ConfigDict(populate_by_name=True)
    
    id: Optional[str] = Field(None, alias="_id")
    fid: str
    name: str

class Activity(BaseModel):
    """
    Matches items in the 'detail[].activity' list.
    """
    model_config = ConfigDict(populate_by_name=True)
    
    id: Optional[str] = Field(None, alias="_id")
    description: str = Field(..., alias="value") # Maps JSON 'value' to 'description'
    progress: Progress

class LogbookDetail(BaseModel):
    """
    Matches items in the 'detail' list. 
    The ID here belongs to this container, NOT the inner usecase object.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: Optional[str] = Field(None, alias="_id")
    usecase: UsecaseInfo
    activity: List[Activity]
    next_activity: List[str] = []

# --- 4. User Profile (For Read/Edit context) ---

class UserTeam(BaseModel):
    name: str
    project_manager: Optional[str] = None
    team_lead: Optional[str] = None

class UserWorkplace(BaseModel):
    name: str
    fid: str

class UserProfile(BaseModel):
    """
    Only present in the 'Edit' / DB version (second.json).
    Made optional in the root so 'Add' (first.json) doesn't fail.
    """
    name: str
    email: str
    team: UserTeam
    role: str
    workplace: UserWorkplace

# --- 5. The Master Model ---    
class LogbookEntry(BaseModel):
    """
    The Single Source of Truth.
    Parses both first.json (Add) and second.json (Edit).
    """
    model_config = ConfigDict(populate_by_name=True)

    id: Optional[str] = Field(None, alias="_id")
    fid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    
    # Metadata
    created_at: Optional[str] = None  # CHANGED: datetime -> str
    updated_at: Optional[str] = None  # CHANGED: datetime -> str
    current_team: str
    
    # Core Data
    work_mode: str
    selected_date: str  # CHANGED: datetime -> str
    project: str
    
    detail: List[LogbookDetail]
    tools: List[Tool]
    
    user: Optional[UserProfile] = None