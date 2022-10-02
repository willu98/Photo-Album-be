import jwt
from  fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

class AuthHandler():
    security = HTTPBearer()
    pswd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = 'SECRET'

    def get_hashed_password(self, password:str) -> str:
        return self.pswd_context.hash(password)

    def verify_password(self, password: str, hashed_pass: str) ->  bool:
        return self.pswd_context.verify(password, hashed_pass)

    def encode_token(self,  user_id):
        exp = datetime.now(timezone.utc) + timedelta(days = 0, minutes=15)
        payload = {
            'exp': exp,
            'iat': datetime.now(timezone.utc),
            'sub': user_id
        }
        return {
            'token': jwt.encode(
                payload,
                self.secret,
                algorithm='HS256'
            ),
            'exp': exp
        }

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401,detail='Signature has expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)