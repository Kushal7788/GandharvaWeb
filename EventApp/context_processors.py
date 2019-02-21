from .models import *


def add_variable_to_context(request):
    obj = Document.objects.filter(category=Document_type.objects.get(type='Rule Book')).count()
    if obj:
        rulebook = Document.objects.get(category=Document_type.objects.get(type='Rule Book'))
    else:
        rulebook = None
    try:
        roles_user = RoleAssignment.objects.filter(user=request.user).count()
    except:
        roles_user = None

    if roles_user:
        roles_user = RoleAssignment.objects.get(user=request.user).role.name

    global_objects = EventDepartment.objects.filter(department=6)
    event_name = []
    for global_object in global_objects:
        event_name.append(global_object.event.event_name)

    return {
        'testmes': Department.objects.all().order_by('rank'),
        'global_events': event_name,
        'footers': SocialMedia.objects.all(),
        'rulebook': rulebook,
        'role': roles_user,
    }
