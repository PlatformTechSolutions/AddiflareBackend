from django.contrib import admin
from .models import Profile, Blog
from django.contrib.admin import AdminSite
from .login import CustomLoginForm
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect


class CustomLoginAdminSite(AdminSite):
    site_title = _('Addiflare||push the addiction to flame')
    site_header = _('Administration')
    index_title = _('Admin Login')
    #registering Custom login form for the Login interface
    #this login form uses CustomBackend
    login_form = CustomLoginForm


#create a Admin_site object to register models
admin_site = CustomLoginAdminSite()


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ['get_username', 'fullname', 'city', 'state', 'country', 'occupation',
                    'shortdescription', 'verified', 'emailverified', 'is2fa', 'issuspended']

    def get_username(self, obj):
        if not obj.user.is_superuser:
            return obj.user.username
    #get_username.admin_order_field  = 'author'  #Allows column order sorting
    get_username.short_description = 'Username'  # Renames column head

    #Filtering on side - for some reason, this works
    #list_filter = ['title', 'author__name']


class BlogAdmin(admin.ModelAdmin):
    model = Blog


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Blog, BlogAdmin)
