from fastapi import (
	status,

	HTTPException, 
	UploadFile, 
	FastAPI,
	Depends, 
	File,
	Body
)

from app.schemas.user import (
	CreateUserSchema, 
	UserLoginSchema,
	UserSchema
)

from app.schemas.user import (
	CreateUserSchema, 
	UserLoginSchema,
	UserSchema
)

from sqlalchemy.orm import Session

from db_init import get_db

from app.models import user as user_model

from app.services import user as user_db_services

app = FastAPI()

@app.post('/signup', response_model=UserSchema)
def signup(
	payload: CreateUserSchema = Body(), 
	session:Session=Depends(get_db)
):
	"""Processes request to register user account."""
	payload.hashed_password = user_model.User.hash_password(payload.hashed_password)
	return user_db_services.create_user(session, user=payload)
