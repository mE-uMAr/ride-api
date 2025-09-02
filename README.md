# Riding app backend

A simple FastAPI application for ride-hailing services where riders can request rides and drivers can accept them.

## Features

- User registration and JWT authentication
- Ride creation by riders
- Available rides listing for drivers
- Ride acceptance with concurrency control
- Background notifications
- Input validation for coordinates and pricing

## Setup

1. Install dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

2. Run the application:
\`\`\`bash
python main.py
\`\`\`

3. Access the API documentation at: http://localhost:8000/docs

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token

### Rides
- `POST /rides/` - Create ride request (riders only)
- `GET /rides/available` - Get available rides (drivers only)
- `POST /rides/{ride_id}/accept` - Accept a ride (drivers only)
- `GET /rides/my-rides` - Get user's rides
- `POST /rides/{ride_id}/complete` Mark ide completed

## Usage

1. Register as a rider or driver
2. Login to get access token
3. Use token in Authorization header: `Bearer <token>`
4. Riders can create rides, drivers can view and accept them

## Database

Uses SQLite database (`rides.db`) with automatic table creation.
