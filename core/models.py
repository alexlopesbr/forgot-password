from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from .exceptions import ForgotPasswordInvalidParams, ForgotPasswordExpired
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if(not email):
            raise ValueError('Users must have an email')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email,
                                password=password,
                                )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    forgot_password_hash = models.CharField(
        max_length=255, null=True, blank=True)
    forgot_password_expire = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin

    @classmethod
    def change_password(cls, email, forgot_password_hash, new_password):
        try:
            user = cls.objects.get(
                email=email, forgot_password_hash=forgot_password_hash)
        except cls.DoesNotExist:
            raise ForgotPasswordInvalidParams

        now = timezone.now()

        if user.forgot_password_expire < now:
            raise ForgotPasswordExpired

        user.set_password(new_password)
        user.forgot_password_expire = now
        user.save()
