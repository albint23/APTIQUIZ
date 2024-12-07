from django import forms
from .models import *

class QuizForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = []

    selected_option = forms.CharField(widget=forms.HiddenInput, required=False)

class AddDP_Form(forms.ModelForm):
    class Meta:
        model = UserImages
        fields = ['image']

    def save(self, user, commit=True):
        instance = super(AddDP_Form, self).save(commit=False)
        instance.user = user

        if commit:
            instance.save()

        return instance

class DP_Form(forms.ModelForm):
    class Meta:
        model = UserImages
        fields = ['image']
    
    def clean_image(self):
        image = self.cleaned_data['image']
        return image

class UserEditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class AddQuizForm(forms.ModelForm):
    class Meta:
        model = Quizzes
        fields = ['name', 'category', 'total_questions', 'marks_for_each', 'time_limit']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'display: inline-block; margin-right: 10px;'

class AddQuestionForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['topic', 'question', 'image', 'option_1', 'option_2', 'option_3', 'option_4', 'answer']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs['accept'] = 'image/*'

class EditQuestionForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['topic', 'question', 'image', 'option_1', 'option_2', 'option_3', 'option_4', 'answer']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs['accept'] = 'image/*'