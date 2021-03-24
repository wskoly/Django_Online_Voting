from django.utils.translation import gettext, gettext_lazy as _
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from muni_election.models import *


class adminUser(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email','phone')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_voter', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

class MayorAdmin(admin.ModelAdmin):
    exclude = ('vote_count',)

class CouncilorAdmin(admin.ModelAdmin):
    exclude = ('vote_count',)

class ReCouncilorAdmin(admin.ModelAdmin):
    exclude = ('vote_count',)

class vote_st(admin.ModelAdmin):
    readonly_fields = ['voter_hash','election_id', 'mayor_candidate', 'councilor_candidate', 're_councilor_candidate']
class voted(admin.ModelAdmin):
    readonly_fields = ['election_id','user']
#change admin panel
admin.site.site_header = "Online Voting Administration"
admin.site.site_title = "Online Voting Admin"
admin.site.index_title = "Online Voting Administration"
# Register your models here.
admin.site.register(user, adminUser)
admin.site.register(voter)
admin.site.register(voter_area)
admin.site.register(election_staff)
admin.site.register(election)
admin.site.register(mayor_candidate, MayorAdmin)
admin.site.register(councilor_candidate,CouncilorAdmin)
admin.site.register(re_councilor_candidate,ReCouncilorAdmin)
admin.site.register(vote_store,vote_st)
admin.site.register(is_voted,voted)
