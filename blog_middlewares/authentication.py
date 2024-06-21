from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from blog_users.models import User
from django.conf import settings
from utils.helper import decipher
import jwt
from cryptography.fernet import InvalidToken


class TokenAuthentication(BaseAuthentication):
    @staticmethod
    def authenticate(request):
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                raise Exception('Authorization header missing')

            auth_token = decipher(auth_header)
            decoded_jwt = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=["HS256"])

            return (User.objects.get(pk=decoded_jwt['user_id']), None)

        except InvalidToken:
            raise AuthenticationFailed('Compromised Token')
        except User.DoesNotExist:
            raise AuthenticationFailed('No such user')
        except Exception as e:
            raise AuthenticationFailed(str(e))



class TokenAuthenticationNo403(BaseAuthentication):
    def authenticate(self, request):
        try:
            return TokenAuthentication.authenticate(request)
        except:
            return (None, None)
