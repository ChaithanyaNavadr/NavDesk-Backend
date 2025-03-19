from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.role import Role  # Import Role model
from app.core.config import settings
from typing import List

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"

# ✅ Extract user_id and tenant_id from token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        tenant_id: str = payload.get("tenant_id")
        if not user_id or not tenant_id:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # ✅ Fetch user with `user_id` and `tenant_id`
    user = db.query(User).filter(User.user_id == user_id, User.tenant_id == tenant_id).first()
    if not user:
        raise credentials_exception

    return user  # ✅ Returns the authenticated user object



def role_required(allowed_roles: List[str]):
    """
    Dependency to enforce role-based access control using role names.

    Args:
        allowed_roles (List[str]): List of role names allowed to access the route.

    Returns:
        function: A dependency that checks if the user has the required role.
    """
    def check_role(user: User = Depends(get_current_user)):
        if not user.role or user.role.name not in allowed_roles:  # ✅ Handle missing role
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )
        return user
    return check_role
