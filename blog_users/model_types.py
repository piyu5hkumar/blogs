from django.db import models


class UserType(models.TextChoices):
    SUPER_ADMIN = "super_admin", "Super Admin"
    ADMIN = "admin", "Admin"
    NORMAL = "normal", "Normal"
