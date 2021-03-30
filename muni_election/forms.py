from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, PasswordChangeForm,UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from muni_election.models import voter, voter_migration
from django.contrib.auth import get_user_model
from django import forms

class VoterLoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
        'notVoter': _("You are not a voter."),
    }
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_voter:
            raise  ValidationError(
                self.error_messages['notVoter'],
                code='notVoter',
            )

class userReg(ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        user = get_user_model()
        model = user
        fields = ['username','first_name','last_name','email','phone','password']
        widgets = {
            'password': forms.PasswordInput()
        }
    def clean(self):
        cleaned_data = super(userReg,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if(password != confirm_password):
            raise forms.ValidationError("Both password does not matched")

class voterReg(ModelForm):
    class Meta:
        model = voter
        fields = ['voter_id','area','serial','dob','gender','ward','municipality']
        widgets = {
            'dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class migrateVoter(ModelForm):
    class Meta:
        model = voter_migration
        fields = ['start_date','end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'end_date': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
        }