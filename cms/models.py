from django.db import models
from utils.abstract_models import BaseModel


class Toggle(BaseModel):
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

