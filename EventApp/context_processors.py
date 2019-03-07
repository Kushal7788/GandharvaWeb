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
    #uncomment lines when you assign levels to all campaign heads
    if roles_user:
        roles_user = RoleAssignment.objects.get(user=request.user).role.name
        # campaign_object = RoleAssignment.objects.filter(role__name="Campaigning Head")[0]
        # print(campaign_object.user)
        # campaign = campaign_object.level
        roles_level = RoleAssignment.objects.get(user=request.user).level
        # if roles_level >= campaign:
        #     roles_level = 1
        # print(campaign)
        # print(roles_level)

    if not roles_level :
        roles_level = 0
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
        'level': roles_level
    }
