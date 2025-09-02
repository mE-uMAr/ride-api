from datetime import datetime
from typing import List
from fastapi import HTTPException
from sqlmodel import Session, select

from app.models import Ride, RideCreate, RideStatus

class RideService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_ride(self, ride_data: RideCreate, rider_id: int) -> Ride:
        ride = Ride(**ride_data.dict(), rider_id=rider_id)
        self.db.add(ride)
        self.db.commit()
        self.db.refresh(ride)
        return ride
    
    def get_available_rides(self) -> List[Ride]:
        return self.db.exec(
            select(Ride).where(Ride.status == RideStatus.PENDING)
        ).all()
    
    def accept_ride(self, ride_id: int, driver_id: int) -> Ride:
        ride = self.db.exec(select(Ride).where(Ride.id == ride_id)).first()
        
        if not ride:
            raise HTTPException(status_code=404, detail="Ride not found")
        
        if ride.status != RideStatus.PENDING:
            raise HTTPException(status_code=409, detail="Ride already accepted")
        
        if ride.rider_id == driver_id:
            raise HTTPException(status_code=400, detail="Cannot accept your own ride")
        ride.driver_id = driver_id
        ride.status = RideStatus.ACCEPTED
        ride.accepted_at = datetime.utcnow()
        
        try:
            self.db.add(ride)
            self.db.commit()
            self.db.refresh(ride)
            return ride
        except Exception:
            self.db.rollback()
            raise HTTPException(status_code=409, detail="Ride was already accepted")
        
    def complete_ride(self, ride_id: int, driver_id: int) -> Ride:
        ride = self.db.exec(select(Ride).where((Ride.id == ride_id) & (Ride.driver_id == driver_id))).first()
        
        if not ride:
            raise HTTPException(status_code=404, detail="Ride not found for current user")
        
        if ride.status == RideStatus.COMPLETED:
            raise HTTPException(status_code=409, detail="Ride already completed")
        
        if ride.rider_id == driver_id:
            raise HTTPException(status_code=400, detail="Cannot complete your own ride")
        
        ride.driver_id = driver_id
        ride.status = RideStatus.COMPLETED
        ride.accepted_at = datetime.utcnow()
        
        try:
            self.db.add(ride)
            self.db.commit()
            self.db.refresh(ride)
            return ride
        except Exception:
            self.db.rollback()
            raise HTTPException(status_code=409, detail="Ride was already completed")
    
    def get_user_rides(self, user_id: int, user_type: str) -> List[Ride]:
        if user_type == "rider":
            return self.db.exec(select(Ride).where(Ride.rider_id == user_id)).all()
        else:
            return self.db.exec(select(Ride).where(Ride.driver_id == user_id)).all()

def notify_rider(ride_id: int, message: str): #simulattion
    print(f"[NOTIFICATION] Ride {ride_id}: {message}")
