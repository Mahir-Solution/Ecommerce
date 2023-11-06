from typing import Any
from django import forms
from .models import Registation

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))
    class Meta:# it contain the additional info about the registrationform class
        model = Registation
        fields = ['first_name','last_name','phone_number','email']#these filed are display in the html form


    
    def clean(self):
        cleaned_data = super(RegistrationForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("passwored not match")
        
        # return cleaned_data

    # the below init is a constructor that assigrn all field to css class form control 
    def __init__(self, *args, **kwargs):# this line accept any number of positional and keyword argument and this is constructor name __init__
        super(RegistrationForm,self).__init__(*args, **kwargs)#this line call to paraennt class(forms.ModelFrom) constructor
        # the below four line set the place holder on different field
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter You Email'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Your Mobile Number'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'# this line app to all field css class form control


