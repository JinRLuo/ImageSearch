from django.db import models
from django.utils.timezone import now


# Create your models here.
class Image(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    image = models.ImageField(upload_to="images/")
    update_time = models.DateTimeField('更新日期', default=now)

    class Meta:
        db_table = "external_image"
