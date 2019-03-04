# fellow class is for permission, we use it like authentication component
from app_02.models import User


class AdministratorPermission(object):
    # set display message when requester has no permission, default is set by rest_framework in English
    # message = ""

    def has_permission(self, request, view_instance):
        # user name is in the request
        user_type = User.objects.filter(name=request.user).first().user_type
        if user_type == 2:
            # user is administrator
            return True
        else:
            return False