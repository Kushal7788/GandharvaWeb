# inluce the models to be viewed here
from django.contrib import admin
from .models import *

# register here after creating new models to view at back end

admin.site.register(RoleAssignment)
admin.site.register(RoleMaster)
admin.site.register(MyUser)
admin.site.register(EventMaster)
admin.site.register(EventDepartment)
admin.site.register(Department)
admin.site.register(SponsorMaster)
admin.site.register(Carousel)
admin.site.register(ContactUs)
admin.site.register(GandharvaHome)
admin.site.register(College)
admin.site.register(Document)
admin.site.register(Document_type)
