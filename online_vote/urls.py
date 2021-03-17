"""online_vote URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from muni_election import views
from django.contrib.auth.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('vote/', views.vote, name='vote'),
    path('standings/', views.standings, name='standings'),
    path('logout/', views.voter_logout, name='logout'),
    path('password_change/', PasswordChangeView.as_view(success_url ='done', template_name= 'muni_election/change_pw.html'), name='change_password'),
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name= 'muni_election/pw_change_done.html'), name='change_password_done'),
    path('password_reset/', PasswordResetView.as_view(html_email_template_name = 'muni_election/pw_reset_email.html',subject_template_name ='muni_election/pw_reset_subject.txt'), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('voter_reg', views.voter_reg, name='voter_reg'),
    path('voter_reg/done/', views.voter_reg_complete, name='voter_reg_done'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
