from django.db import models


class BaseModel(models.Model):

    """An abstract model that provides basic functionality
    """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
