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
    roles_level=False

    if roles_user:
        roles_user = RoleAssignment.objects.get(user=request.user).role.name
        campaign_object = RoleMaster.objects.filter(name="Campaigning Head")[0]
        campaign = campaign_object.level
        # print(campaign)
        roles_level = RoleMaster.objects.filter(name=roles_user)[0].level
        if roles_level >= campaign:
            roles_level = 1
        # print(roles_level)

    if not roles_level :
        roles_level = 0
    global_objects = EventDepartment.objects.filter(department=6)
    event_name = []
    for global_object in global_objects:
        event_name.append(global_object.event.event_name)
    if roles_user == "Event Head":
        event_id = RoleAssignment.objects.get(user=request.user).event.event_id
    else:
        event_id = 0
    return {
        'testmes': Department.objects.all().order_by('rank'),
        'global_events': event_name,
        'footers': SocialMedia.objects.all(),
        'rulebook': rulebook,
        'role': roles_user,
        'level': roles_level,
        'event_id':event_id
    }
