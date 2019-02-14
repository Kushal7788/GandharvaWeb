from .models import *


def add_variable_to_context(request):
    obj = Document_type.objects.get(type='Rule Book')
    global_objects = EventDepartment.objects.filter(department=6)
    event_name = []
    for global_object in global_objects:
        event_name.append(global_object.event.event_name)


    return {
        'testmes': Department.objects.all(),
        'global_events': event_name,
        'footers': SocialMedia.objects.all(),
        'rulebook': Document.objects.get(category = obj)
    }