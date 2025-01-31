from django.contrib.auth.forms import UserCreationForm
from core.models import User


class CreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
