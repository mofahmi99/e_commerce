from django.contrib.gis.geos import Point

from helpers.models import Timestamps
from django.contrib.gis.db import models


class Address(Timestamps):
    """
    store user location data
    """
    title = models.CharField(max_length=255)
    city = models.ForeignKey('branches.City', on_delete=models.CASCADE)
    location = models.PointField()
    address_info = models.TextField()
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} - {self.user.phone_number}'
