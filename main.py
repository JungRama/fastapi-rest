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

from typing import Dict


from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm


from sqlalchemy.orm import Session

from db_init import get_db

from app.models import user as user_model

from app.services import user as user_db_services

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@app.post('/login', response_model=Dict)
def login(
		payload: OAuth2PasswordRequestForm = Depends(),
		session: Session = Depends(get_db)
	):
	"""Processes user's authentication and returns a token
	on successful authentication.

	request body:

	- username: Unique identifier for a user e.g email, 
				phone number, name

	- password:
	"""
	try:
		user:user_model.User = user_db_services.get_user(
			session=session, email=payload.username
		)
	except:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid user credentials"
		)

	is_validated:bool = user.validate_password(payload.password)
	if not is_validated:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid user credentials"
		)

	return user.generate_token()

@app.post('/signup', response_model=UserSchema)
def signup(
	payload: CreateUserSchema = Body(), 
	session:Session=Depends(get_db)
):
	"""Processes request to register user account."""
	payload.hashed_password = user_model.User.hash_password(payload.hashed_password)
	return user_db_services.create_user(session, user=payload)

@app.get("/profile/{id}", response_model=UserSchema)
def profile(
	id:int, 
	session:Session=Depends(get_db),
	token: str = Depends(oauth2_scheme),
):
	"""Processes request to retrieve the requesting user
	profile 
	"""
	return user_db_services.get_user_by_id(session=session, id=id)