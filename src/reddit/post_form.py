from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    post_title = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder":"Post Title"}))
    post_text  = forms.CharField(label='',
                        required=False,
                        widget=forms.Textarea(
                                attrs={
                                    "rows": 20,
                                    "cols":40,
                                    "placeholder": "Post Text"
                                    }
                                ))

    class Meta:
        model = Post
        fields = [
            "post_title",
            "post_text"
        ]
