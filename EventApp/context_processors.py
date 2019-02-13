from .models import *


def add_variable_to_context(request):
    return {
        'testmes': Department.objects.all(),
        'footers': SocialMedia.objects.all()
    }