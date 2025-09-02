from typing import List
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlmodel import Session

from app.database import get_db
from app.models import User, Ride, RideCreate, RideResponse, UserType
from app.auth import get_current_user
from app.services import RideService, notify_rider

router = APIRouter()

@router.post("/", response_model=RideResponse, status_code=201)
def create_ride(ride_data: RideCreate,background_tasks: BackgroundTasks,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    if current_user.user_type != UserType.RIDER:
        raise HTTPException(status_code=403, detail="Only riders can create rides")
    
    ride_service = RideService(db)
    ride = ride_service.create_ride(ride_data, current_user.id)

    background_tasks.add_task(
        notify_rider, 
        ride.id, 
        f"Ride request created successfully"
    )
    
    return ride

@router.get("/available", response_model=List[RideResponse])
def get_available_rides(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.user_type != UserType.DRIVER:
        raise HTTPException(status_code=403, detail="Only drivers can view available rides")
    ride_service = RideService(db)
    return ride_service.get_available_rides()

@router.post("/{ride_id}/accept", response_model=RideResponse)
def accept_ride(ride_id: int,background_tasks: BackgroundTasks,current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.user_type != UserType.DRIVER:
        raise HTTPException(status_code=403, detail="Only drivers can accept rides")
    ride_service = RideService(db)
    ride = ride_service.accept_ride(ride_id, current_user.id)

    background_tasks.add_task(
        notify_rider,
        ride.id,
        f"Your ride has been accepted by driver {current_user.full_name}"
    )
    return ride

@router.post("/{ride_id}/compltte", response_model=RideResponse)
def complete_ride(ride_id: int,background_tasks: BackgroundTasks,current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.user_type != UserType.DRIVER:
        raise HTTPException(status_code=403, detail="Only drivers can complete rides")
    ride_service = RideService(db)
    ride = ride_service.complete_ride(ride_id, current_user.id)

    background_tasks.add_task(
        notify_rider,
        ride.id,
        f"Your ride has been complted"
    )
    return ride

@router.get("/my-rides", response_model=List[RideResponse])
def get_my_rides(current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    ride_service = RideService(db)
    return ride_service.get_user_rides(current_user.id, current_user.user_type)
