from django.db import models


class Menu(models.Model):
    slug = models.SlugField('url', unique=True, max_length=50)
    parent = models.ForeignKey(
        'Menu',
        related_name='children',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self) -> str:
        return self.slug
