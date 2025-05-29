from django import forms
from .models import *
from django import forms
from .models import RewardApplication


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']


class RewardForm(forms.ModelForm):
    class Meta:
        model = Reward
        fields = ['title', 'description', 'category', 'reward_amount']


class RewardApplicationForm(forms.ModelForm):
    class Meta:
        model = RewardApplication
        fields = ['reward', 'is_accepted']