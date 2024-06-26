from django import forms 
from .models import Users

class SignupForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'username_validate', 'placeholder': 'Enter Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'email_validate', 'placeholder': 'Enter Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))

    class Meta:
        model = Users
        fields = ['username','email', 'password']
        
    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        if commit:
            user.save()

        return user

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'email_validate', 'placeholder': 'Enter Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))
 
    class Meta:
        model = Users
        field = ['email', 'password']