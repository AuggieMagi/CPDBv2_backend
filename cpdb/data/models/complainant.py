from django.contrib.gis.db import models
from django_bulk_update.manager import BulkUpdateManager

from data.constants import GENDER_DICT
from data.validators import validate_race
from .common import TimeStampsModel


class Complainant(TimeStampsModel):
    allegation = models.ForeignKey('data.Allegation', on_delete=models.CASCADE, null=True)
    gender = models.CharField(max_length=1, blank=True)
    race = models.CharField(max_length=50, default='Unknown', validators=[validate_race])
    age = models.IntegerField(null=True)
    birth_year = models.IntegerField(null=True)

    objects = BulkUpdateManager()

    @property
    def gender_display(self):
        try:
            return GENDER_DICT[self.gender]
        except KeyError:
            return self.gender
