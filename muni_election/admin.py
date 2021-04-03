from django.utils.translation import gettext, gettext_lazy as _
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from muni_election.models import *
from django.urls import path
from muni_election.views import voter_migrate

@admin.register(user)
class adminUser(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email','phone')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_voter', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(voter_area)
class areaAdmin(admin.ModelAdmin):
    list_display = ['code','name','subDist','dist','div']

@admin.register(voter)
class voterAdmin(admin.ModelAdmin):
    list_display = ['user', 'voter_id','get_name','get_email','get_phone', 'area', 'serial', 'dob', 'gender', 'ward', 'municipality']

@admin.register(election)
class electionAdmin(admin.ModelAdmin):
    list_display = ['name', 'num_of_ward', 'area_names', 'is_open', 'is_res_published']

@admin.register(mayor_candidate)
class MayorAdmin(admin.ModelAdmin):
    exclude = ('vote_count',)
    list_display = ['election_id','name', 'symbol', 'vote_count']

@admin.register(councilor_candidate)
class CouncilorAdmin(admin.ModelAdmin):
    exclude = ('vote_count',)
    list_display = ['election_id', 'name', 'symbol', 'ward_no', 'vote_count']

@admin.register(re_councilor_candidate)
class ReCouncilorAdmin(admin.ModelAdmin):
    exclude = ('vote_count',)
    list_display = ['election_id', 'name', 'symbol', 'reserve_ward_1', 'reserve_ward_2', 'reserve_ward_3', 'vote_count']

class vote_st(admin.ModelAdmin):
    readonly_fields = ['voter_hash','election_id', 'mayor_candidate', 'councilor_candidate', 're_councilor_candidate']


class voted(admin.ModelAdmin):
    readonly_fields = ['election_id','user']

@admin.register(election_staff)
class staffAdmin(admin.ModelAdmin):
    list_display = ['user','staff_name','role']

@admin.register(voter_migration)
class voterMigrateAdmin(admin.ModelAdmin):
    model = voter_migration

    def get_urls(self):
        view_name = '{}_{}_changelist'.format(
            self.model._meta.app_label, self.model._meta.model_name)
        return [
            path('', voter_migrate, name=view_name),
        ]


#change admin panel
admin.site.site_header = _("Online Election Administration")
admin.site.site_title = _("Online Election Admin")
admin.site.index_title = _("Online Election Administration")
# Register your models here.
'''admin.site.register(voter_migration, voterMigrateAdmin)
admin.site.register(user, adminUser)
admin.site.register(voter,voterAdmin)
admin.site.register(voter_area,areaAdmin)
admin.site.register(election_staff,staffAdmin)
admin.site.register(election,electionAdmin)
admin.site.register(mayor_candidate, MayorAdmin)
admin.site.register(councilor_candidate,CouncilorAdmin)
admin.site.register(re_councilor_candidate,ReCouncilorAdmin)
admin.site.register(vote_store,vote_st)
admin.site.register(is_voted,voted)'''
