from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, PasswordChangeForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
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