from django.contrib.auth.models import AbstractUser # AbstractUser is Django's base user class that provides core user functionality
from django.db import models # This provides Django's ORM (Object-Relational Mapping) functionality

class User(AbstractUser):
    # This creates a custom User model that inherits all the basic fields and functionality from Django's AbstractUser
    # So the User inherits several fields from AbstractBaseUser, including username, first_name, password, last_login, is_active, and is_staff, is_superuser, date_joined
    email = models.EmailField(unique=True) # Default email field of AbstractBaseUser is not unique, so we need to specify that it should be unique
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email' # This tells Django to use the email field for authentication instead of the default username
    REQUIRED_FIELDS = ['username'] # This specifies the fields that are required when creating a new user.