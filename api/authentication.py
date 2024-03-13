from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from datetime import datetime, timedelta


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise AuthenticationFailed('User inactive or deleted')

        if datetime.now() - token.created > timedelta(minutes=10):
            token.delete()
            raise AuthenticationFailed('Token has expired')

        token.created = datetime.now()
        token.save()

        return token.user, token
