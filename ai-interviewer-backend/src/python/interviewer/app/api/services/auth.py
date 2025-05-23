from datetime import datetime, timedelta
from jose import JWTError, jwt
from interviewer.app.api.schemas.user import User


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
            "id": user.user_id,
            "exp": expire
        }
        encoded_jwt = jwt.encode(data, self.SECRET_KEY, algorithm=self.ALGORITHM)
        print(f"Jwt type is {type(encoded_jwt)}")
        return encoded_jwt

    def validate_token_and_get_user_id(self, token: str) -> int:
        """
        Validate a JWT token and return the user ID if valid.

        :param token: JWT token as string
        :return: user ID (int)
        :raises: JWTError if token is invalid or expired
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            user_id: int = payload.get("id")
            if user_id is None:
                raise JWTError("Missing user ID in token payload.")
            return user_id
        except JWTError as e:
            raise JWTError(f"Token validation failed: {e}")
