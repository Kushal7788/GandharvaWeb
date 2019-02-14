from .models import *


def add_variable_to_context(request):
    return {
        'testmes': Department.objects.all().order_by('rank'),
        'footers': SocialMedia.objects.all()
    }

