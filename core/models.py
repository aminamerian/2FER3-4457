from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from utils.models import BaseModel


class Advertisement(BaseModel):
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="advertisements",
        verbose_name=_("Created by"),
    )

    class Meta:
        verbose_name = _("Advertisement")
        verbose_name_plural = _("Advertisements")

    def __str__(self):
        return self.title


class Comment(BaseModel):
    advertisement = models.ForeignKey(
        Advertisement,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("Advertisement"),
    )
    text = models.TextField(verbose_name=_("Text"))
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("Created by"),
    )

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        unique_together = ("advertisement", "created_by")

    def __str__(self):
        return self.text
