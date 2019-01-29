from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
import random

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(random.randint(5000,9000)) +
                six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()
