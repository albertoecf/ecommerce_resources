from django import forms
from .models import AccountClass


class RegistrationFormClass(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': "Create Password",
               'class': 'form-control'}))

    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password',
               'class': 'form-control'}))

    class Meta:
        model = AccountClass
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and set placeholder text and CSS class for form fields.
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = "Your Name"
        self.fields['last_name'].widget.attrs['placeholder'] = "Your Last Name"
        self.fields['email'].widget.attrs['placeholder'] = "Your email"
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationFormClass, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password don't match"
            )
