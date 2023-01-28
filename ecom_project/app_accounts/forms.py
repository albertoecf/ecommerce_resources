from django import forms
from .models import AccountClass, UserProfileClass


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

class UserFormClass(forms.ModelForm):
    """
    A form class that inherits from Django's ModelForm and is used to handle user input for the AccountClass model.
    """
    class Meta:
        """
        Meta options for the UserFormClass.
        """
        model = AccountClass
        fields = ('first_name','last_name')
    def __init__(self,*args,**kwargs):
        """
        Initialization of the form, calls the superclass constructor and loops through the fields to add a 'form-control' class to the widget for styling.
        """
        super(UserFormClass, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-cont'


class UserProfileFormClass(forms.ModelForm):
    """
    A form class for creating or updating user's profile information.
    """

    profile_picture = forms.ImageField(required=False, error_messages={'invalid':('Only img files')}, widget=forms.FileInput )
    class Meta:
        """
        A nested class inside UserProfileFormClass that specifies the model and fields for the form.
        """
        model = UserProfileClass
        fields = ('address_line_1','address_line_2','city','state','country','profile_picture')

    def __init__(self,*args, **kwargs):
        """
        Initialize the form and set the class attribute of each widget to 'form-control'
        """
        super(UserProfileFormClass , self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
