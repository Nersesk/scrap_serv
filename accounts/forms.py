from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

from scraping.models import Language, City

User=get_user_model()

class UserLoginForm(forms.Form):
    email=forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control'}),label='Email')
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),label='Password')

    def clean(self,*args,**kwargs):
        email=str(self.cleaned_data.get('email')).strip()
        password=self.cleaned_data.get('password')

        if email and password:
            qs=User.objects.filter(email=email)
            if not qs.exists():
                raise forms.ValidationError("We cannot find an account with that email address")
            if not check_password(password,qs[0].password):
                raise forms.ValidationError("Wrong password")
            user=authenticate(email=email,password=password)
            if not user:
                raise forms.ValidationError("Account out of use")
        return super(UserLoginForm,self).clean()

class UserRegistrationForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label='Enter your email')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Enter Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Confirm Password')
    class Meta:
        model=User
        fields=('email',)

    def clean_password2(self):
        data=self.cleaned_data
        if data.get('password')!=data.get('password2'):
            raise forms.ValidationError("Passwords don't match")
        return data['password2']

class UserUpdateForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(), to_field_name='slug', required=True,
                                  widget=forms.Select(attrs={"class": "form-control"}),
                                  label='City')
    language = forms.ModelChoiceField(queryset=Language.objects.all(), to_field_name='slug', required=True,
                                      widget=forms.Select(attrs={"class": "form-control"}),
                                      label="Profession")
    send_email=forms.BooleanField(required=False,widget=forms.CheckboxInput(),label="Do you want to receive emails?")

    class Meta:
        model=User
        fields=('city','language','send_email')



class ContactForm(forms.Form):
    city = forms.CharField(required=True,
                                  widget=forms.TextInput(attrs={"class": "form-control"}),
                                  label='City')

    language = forms.CharField(required=True,
                           widget=forms.TextInput(attrs={"class": "form-control"}),
                           label='Language')

    email=forms.EmailField(required=True,
                           widget=forms.EmailInput(attrs={"class": "form-control"}),
                           label='Email')