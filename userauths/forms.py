from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile
from django.contrib.auth import authenticate

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password confirmation'}))
    class Meta:
        model = User
        fields = ['username', 'email']
        
class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('User is not a valid user')
            if not user.check_password(password):
                raise forms.ValidationError('Password is incorrect')
            if not user.is_active:
                raise forms.ValidationError('User is inactive')
        
        return super(UserLoginForm, self).clean()
    
    
class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    bio = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    # image = forms.CharField(widget=forms.ImageField(attrs={'class': 'form-control'}))
    # image = forms.CharField(widget=forms.ImageField(attrs={'class': 'form-control'}))
    # image = forms.CharField(widget=forms.ImageField(attrs={'class': 'form-control'}))
    # image = forms.CharField(widget=forms.ImageField(attrs={'class': 'form-control'}))
    # image = forms.CharField(widget=forms.ImageField(attrs={'class': 'form-control'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['full_name', 'image', 'bio', 'phone']