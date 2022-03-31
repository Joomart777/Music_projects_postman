from django.db import models


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


COUNTRY = (
    ('KG', 'Кыргызстан'),
    ('KZ', 'Казахстан')
)


class Music(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    duration = models.IntegerField(default=3)
    country = models.CharField(max_length=50, choices=COUNTRY)
    category = models.ForeignKey(Category, related_name='music', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} - {self.country}'

    class Meta:
        verbose_name_plural = 'Музыка'
        verbose_name = 'Музыка**'