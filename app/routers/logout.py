from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils

router = APIRouter(tags=['Authentication'])

# OAuth2 scheme for token validation
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post('/logout')
def logout(current_user: schemas.User = Depends(utils.get_current_user)):
    """
    Endpoint to logout user by invalidating the token.
    """
    # Here, you can implement specific logic to invalidate the token or session
    return {"message": "Successfully logged out"}

# Example of protected route
@router.get('/protected')
def protected_route(current_user: schemas.User = Depends(utils.get_current_user)):
    """
    Example of a protected route that requires authentication.
    """
    return {"message": "This is a protected route"}
