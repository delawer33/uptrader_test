from django.db import models
from django.urls import reverse, NoReverseMatch
from django.core.exceptions import ValidationError


class MenuItem(models.Model):
    name = models.CharField(max_length=100)

    menu_name = models.CharField(max_length=100)

    order = models.IntegerField(default=0)

    url = models.CharField(max_length=250, blank=True)

    named_url = models.CharField(max_length=100, blank=True)

    parent = models.ForeignKey(
        "MenuItem",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ["order"]

    def get_url(self):
        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                return self.url or "#"
        return self.url or "#"

    def clean(self):
        super().clean()
        if not self.url and not self.named_url:
            raise ValidationError(
                "Должно быть указано хотя бы одно из полей: url или named_url."
            )

    def __str__(self):
        return self.name
