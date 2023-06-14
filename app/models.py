from django.db import models

# Create your models here.
class image_storage(models.Model):

    img = models.ImageField(upload_to="imgs", null=True)
    img_input = models.ImageField(upload_to="imgs/input", null=True)
    date_time = models.DateTimeField(auto_now=True)
    ocr_output = models.CharField(max_length=20,null=True)

    def __str__(self):
        return self.ocr_output