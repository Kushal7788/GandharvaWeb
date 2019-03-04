from django.core.exceptions import PermissionDenied
from EventApp.models import MyUser, RoleMaster, RoleAssignment


def user_Role_head(function):
    def wrap(request, *args, **kwargs):
        entry = RoleAssignment.objects.get(user=request.user.id)
        rolename = RoleMaster.objects.get(name="Department Head")
        if entry.role == rolename:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def user_Campaign_head(function):
    def wrap(request, *args, **kwargs):
        print(request.user)
        entry = RoleAssignment.objects.get(user=request.user)
        print(entry)
        rolename1 = RoleMaster.objects.get(name="Jt Campaigning Head")
        rolename2 = RoleMaster.objects.get(name="Campaigning Head")
        if entry.role == rolename1 or entry.role == rolename2:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def staff_user(function):
    def wrap(request, *args, **kwargs):
        entry = request.user
        if entry.is_staff:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def event_head_present(function):
    def wrap(request, *args, **kwargs):
        entry = RoleAssignment.objects.get(user=request.user.id)
        rolename = RoleMaster.objects.get(name="Event Head")
        if entry.role == rolename:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def executive_incharge(function):
    def wrap(request, *args, **kwargs):
        entry = RoleAssignment.objects.get(user=request.user.id)
        rolename = RoleMaster.objects.get(name="Executive Incharge")
        if entry.role == rolename:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap