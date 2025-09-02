from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum
from pydantic import EmailStr, validator

class UserType(str, Enum):
    RIDER = "rider"
    DRIVER = "driver"

class RideStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    COMPLETED = "completed"
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True)
    full_name: str = Field(min_length=2, max_length=100)
    user_type: UserType

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    rider_rides: List["Ride"] = Relationship(
        back_populates="rider",
        sa_relationship_kwargs={"foreign_keys": "[Ride.rider_id]"}
    )
    driver_rides: List["Ride"] = Relationship(
        back_populates="driver", 
        sa_relationship_kwargs={"foreign_keys": "[Ride.driver_id]"}
    )

class UserCreate(UserBase):
    password: str = Field(min_length=6)

class UserResponse(UserBase):
    id: int
    created_at: datetime
class RideBase(SQLModel):
    pickup_latitude: float = Field(ge=-90, le=90)
    pickup_longitude: float = Field(ge=-180, le=180)
    dropoff_latitude: float = Field(ge=-90, le=90)
    dropoff_longitude: float = Field(ge=-180, le=180)
    price: float = Field(gt=0)
    
    @validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return round(v, 2)

class Ride(RideBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    rider_id: int = Field(foreign_key="user.id")
    driver_id: Optional[int] = Field(default=None, foreign_key="user.id")
    status: RideStatus = Field(default=RideStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    accepted_at: Optional[datetime] = Field(default=None)
    rider: Optional[User] = Relationship(
        back_populates="rider_rides",
        sa_relationship_kwargs={"foreign_keys": "[Ride.rider_id]"}
    )
    driver: Optional[User] = Relationship(
        back_populates="driver_rides",
        sa_relationship_kwargs={"foreign_keys": "[Ride.driver_id]"}
    )

class RideCreate(RideBase):
    pass

class RideResponse(RideBase):
    id: int
    rider_id: int
    driver_id: Optional[int]
    status: RideStatus
    created_at: datetime
    accepted_at: Optional[datetime]
class LoginRequest(SQLModel):
    email: EmailStr
    password: str

class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
