from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth import password_validation
from django.forms import SelectDateWidget

from Student.models import Student, Post
from django.conf import settings
import re


class StudentRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    username = forms.CharField(widget=forms.HiddenInput())
    accept = forms.BooleanField(required=True, label="<a href='/guidelines/'>Agree with guidelines</a>")

    class Meta():
        model = Student
        fields = ('email', 'password', 'username', 'accept')

    def is_valid(self):
        if super().is_valid():
            if re.match(settings.STUDENT_EMAIL_REGEX, self.cleaned_data['email']):
                return super(StudentRegisterForm, self).is_valid()
            else:
                self._errors['email'] = ["Please Enter your KSU Email Address."]
                return False
        else:
            return False


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('email',)


class StudentLoginForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('email', 'password')
        widgets = {
            'password': forms.PasswordInput(),
        }


class StudentPasswordChangeForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': ('The two password fields didn’t match.'),
        'password_incorrect': ("Your old password was entered incorrectly. Please enter it again."),
    }

    new_password1 = forms.CharField(
        label=("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    old_password = forms.CharField(
        label=("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
    )
    field_order = ['old_password', 'new_password1', 'new_password2']

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.student.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password

    def __init__(self, student, *args, **kwargs):
        self.student = student
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.set_password(password)
        if commit:
            self.save()
        return self

    class Meta():
        model = Student
        widgets = {
            'old_password': forms.PasswordInput(),
            'new_password1': forms.PasswordInput(),
            'new_password2': forms.PasswordInput()
        }
        fields = ('old_password', 'new_password1', 'new_password2')


class StudentPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'file', 'file_type', 'student', 'course')
        error_messages = {
            'student': {
                'invalid_choice': "Post Student Error Message.",
            },
            'file_type': {
                'invalid_choice': "Post FileType Error Message.",
            },
            'course': {
                'invalid_choice': "Post Course Error Message.",
            },
            'file': {
                'required': "Post File Error Message.",
                'invalid_choice': "Post File Error Message."
            }
        }