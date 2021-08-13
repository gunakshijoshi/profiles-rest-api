from django.db import models
"""abstract base user and PermissionsMixin -> for overriding or customising default django user model"""
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
"""Default manager model that comes with django(for UserProfileManager)"""
from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    """manager for user profiles"""

    def create_user(self, email, name, password:None):
        """Create a new user profile"""
        """CLI will use when creating users with command line tool"""
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password) #hashed password
        user.save(using=self._db)    #to support multiple database in future (using=self.db)

        return user

    def create_superuser(self,email,name,password):
        """Create and save a new superuser with given details(it will use create_user to create a new user)"""
        user = self.create_user(email, name, password)

        user.is_superuser = True  #we ahven't specified in model(like is_staff) since it is automatically created by PermissionsMixin"""
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser,PermissionsMixin):
    """Database model for users in system"""
    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    #to work with django admin or authentication
    USERNAME_FIELD = 'email'                #"""required by default"""
    REQUIRED_FIELDS = ['name']              #"""user must specify the email and name"""

    """django to interect with custom user model"""
    def get_full_name(self):
        """retrieve full name of user"""
        return self.name

    def get_short_name(self):
        """retrieve short name for user"""
        return self.name

    """String representation of a model - this we return when we convert the user profile object to a string in python"""
    def __str__(self):
        return self.email
