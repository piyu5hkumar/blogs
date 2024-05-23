from django.db import models


class UserType(models.TextChoices):
    SUPER_ADMIN = "super_admin", "Super Admin"
    ADMIN = "admin", "Admin"
    OPS = "ops", "Operations"
    TENANT_SUPER_ADMIN = "tenant_super_admin", "Tenant Super Admin"
    TENANT_ADMIN = "tenant_admin", "Tenant Admin"
    TENANT_OPS = "tenant_ops", "Tenant Operations"
