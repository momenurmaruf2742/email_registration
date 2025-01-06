from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.json_formator import format_response
from app.database import async_session, init_db
from app.schemas import UserCreate
from app.email_sender import send_welcome_email
import app.crud

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.on_event("startup")
async def on_startup():
    await init_db()

# Dependency for database session
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

@app.post("/register", status_code=201)
async def register_user(user: UserCreate, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_session)):
    # Check if email already exists
    existing_user = await crud.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create a new user
    new_user = await crud.create_user(db, user)

    # Send welcome email in the background
    background_tasks.add_task(send_welcome_email, new_user.email, new_user.first_name)

    # # JSON response with the new user details
    # return {
    #     "id": new_user.id,
    #     "first_name": new_user.first_name,
    #     "last_name": new_user.last_name,
    #     "email": new_user.email,
    #     "message": "User registered successfully!"
    # }

    # Use the format_response function
    response_data = {
        "id": new_user.id,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "email": new_user.email,
    }
    return format_response(data=response_data, message="User registered successfully!")

@app.get("/users/{user_id}", status_code=200)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    user = await crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    response_data = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
    }
    return format_response(data=response_data, message="User details fetched successfully")

