#################################################################
# the process of authentication:
#     1、 send request with token parameter
# 2、if it's partial authentication, we just write a class that is to authenticate, overwrite "authenticate" function
# and set the variable "authentication_classes" in the View class


# but if we want authentication works in the all of the views, we can directly set following digest in the setting.py
#                   REST_FRAMEWORK = {
#                       "DEFAULT_AUTHENTICATION_CLASSES": (
#                           "app02.utils.authentication.TokenAuthentication"
#                       )
#                   }

# if we set "DEFAULT_AUTHENTICATION_CLASSES" in the setting.py, each view will be authenticated.
# we can then set "authentication_classes = []" in the view that we want it not to be authenticated.
# For example, login view
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from app_02.models import Token


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # the request here is not ordinating request, it's from rest_framework
        token = request.GET.get("token")
        token_obj = Token.objects.filter(token=token).first()
        if token_obj is not None:
            # if it's authenticated
            return token_obj.user.name, token_obj.token
        else:
            raise AuthenticationFailed(detail="token is not valid!")



#################################################################