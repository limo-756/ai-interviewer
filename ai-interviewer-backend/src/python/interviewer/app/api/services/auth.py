from datetime import datetime, timedelta
from jose import JWTError, jwt
from interviewer.schemas import User

class Authenticator:
    SECRET_KEY = "your-secret-key"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 40

    def create_access_token(self, user: User, expires_delta: timedelta | None = None):
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)  # Default to 15 minutes

        data = {
            "id": user.id,
            "exp": expire
        }
        encoded_jwt = jwt.encode(data, self.SECRET_KEY, algorithm=self.ALGORITHM)
        print(f"Jwt type is {type(encoded_jwt)}")
        return encoded_jwt
