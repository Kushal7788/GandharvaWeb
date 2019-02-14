from .models import *


def add_variable_to_context(request):
    obj = Document_type.objects.get(type='Rule Book')
    return {
        'testmes': Department.objects.all(),
        'footers': SocialMedia.objects.all(),
        'rulebook': Document.objects.get(category = obj)
    }