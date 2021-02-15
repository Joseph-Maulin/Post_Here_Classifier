from django import forms
from reddit.models import User


class UserForm(forms.ModelForm):
    user_name = forms.CharField(label='', widget=forms.Textarea(attrs={"placeholder":"Username", "rows":3, "cols":60}))


    class Meta:
        model = User
        fields = [
            "user_name"
        ]
