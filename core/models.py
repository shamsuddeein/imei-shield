from django.db import models
from django.core.validators import RegexValidator
from .validators import validate_imei

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)  # mark admin 
    
    def __str__(self):
        return self.username


class Report(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("verified", "Verified"),
        ("resolved", "Resolved"),
    ]

    imei = models.CharField(
        max_length=15,
        unique=True,
        validators=[
            RegexValidator(r"^\d{15}$", "IMEI must be 15 digits"),
            validate_imei,
        ],
        help_text="15-digit IMEI number",
    )
    owner_name = models.CharField(max_length=100, help_text="Name of the phone owner")
    phone_model = models.CharField(max_length=100, help_text="Brand and model")
    last_seen_location = models.CharField(max_length=255, blank=True)
    contact_info = models.CharField(max_length=150, help_text="Phone or email")
    proof_of_ownership = models.FileField(
        upload_to="reports/proofs/",
        blank=True,
        null=True,
        help_text="Receipt, photo, or proof of ownership",
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.imei} - {self.phone_model}"


class ImeiCheckLog(models.Model):
    imei = models.CharField(max_length=15, validators=[RegexValidator(r"^\d{15}$")])
    checked_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"Check {self.imei} at {self.checked_at}"
