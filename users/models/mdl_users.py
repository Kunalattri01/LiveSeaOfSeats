from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    email = models.EmailField(unique=True, db_column='EMAIL_ID')
    phone_number = models.CharField(max_length=15, blank=True, null=True, db_column='PHONE_NUMBER')

    profile_picture = models.ImageField(upload_to="users/profile/", blank=True, null=True, db_column='PROFILE_PICTURE')
    date_of_birth = models.DateField(blank=True, null=True, db_column='DATE_OF_BIRTH')

    GENDER_CHOICES = (
        ("MALE", "MALE"),
        ("FEMALE", "FEMALE"),
        ("OTHER", "OTHER"),
    )
    
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True, db_column='GENDER')

    address = models.TextField(blank=True, null=True, db_column='ADDRESS')
    city = models.CharField(max_length=100, blank=True, null=True, db_column='CITY')
    state = models.CharField(max_length=100, blank=True, null=True, db_column='STATE')
    country = models.CharField(max_length=100, blank=True, null=True, db_column='COUNTRY')
    zip_code = models.CharField(max_length=10, blank=True, null=True, db_column='ZIP_CODE')

    ROLE_CHOICES = (
        ("USER", "USER"),
        ("ORGANIZER", "ORGANIZER"),
        ("ADMIN", "ADMIN"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="USER", db_column='ROLE')

    is_email_verified = models.BooleanField(default=False, db_column='IS_EMAIL_VERIFIED')
    is_phone_verified = models.BooleanField(default=False, db_column='IS_PHONE_VERIFIED')

    created_at = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')
    updated_at = models.DateTimeField(auto_now=True, db_column='UPDATED_AT')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    class Meta:
        db_table = "USER_MT"
        ordering = ["-created_at"]