from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.


class AccountManagerClass(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        """ Create and save a user with the given email, first name, last name, and password. The email and username must be unique.
    :param first_name: The first name of the user
    :type first_name: str
    :param last_name: The last name of the user
    :type last_name: str
    :param email: The email of the user
    :type email: str
    :param password: The password of the user (optional)
    :type password: str
    :return: The created user
    :rtype: Account
        """
        if not email:
            raise ValueError('User should have an email')
        if not username:
            raise ValueError('User should have an username')

        new_user = self.model(
            email = self.normalize_email(email),
            username = username ,
            first_name = first_name,
            last_name = last_name
        )

        new_user.set_password(password)
        new_user.save(using=self._db)
        return new_user

    def create_superuser(self, first_name, last_name, email, username, password):
        """ Create and save a superuser with the given email, first name, last name, username, and password.
    The email and username must be unique."""
        superuser = self.create_user(
            email = self.normalize_email(email),
            username = username ,
            password = password,
            first_name = first_name,
            last_name = last_name
        )

        superuser.is_admin = True
        superuser.is_active = True
        superuser.is_staff = True
        superuser.is_superadmin = True
        superuser.save(using=self._db)
        return superuser

class AccountClass(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100, unique=True)

    # Django attributes
    date_joined = models.DateTimeField(auto_now_add = True)
    last_login = models.DateTimeField(auto_now_add = True)
    is_admin = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    is_active = models.BooleanField(default = False)
    is_superadmin = models.BooleanField(default = False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    objects = AccountManagerClass()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
