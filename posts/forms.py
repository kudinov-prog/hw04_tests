from django import forms
from .models import Group, Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['group', 'text']
        labels = {'group': 'Группа', 'text': 'Текст'}
        help_texts = {
            'group': 'Если знаете тематику, то выберите группу!',
            'text': 'Постарайтесь выкладывать годный контент!'
            }
