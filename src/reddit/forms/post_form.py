from django import forms
from reddit.models import Post


class PostForm(forms.ModelForm):
    post_title = forms.CharField(label='', widget=forms.Textarea(attrs={"placeholder":"Post Title", "rows":3, "cols":60}))
    post_text  = forms.CharField(label='',
                        required=False,
                        widget=forms.Textarea(
                                attrs={
                                    "rows": 20,
                                    "cols":60,
                                    "placeholder": "Post Text"
                                    }
                                ))

    class Meta:
        model = Post
        fields = [
            "post_title",
            "post_text"
        ]
