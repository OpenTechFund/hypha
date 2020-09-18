from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.fields import RichTextField


@register_setting
class CookieConsentSettings(BaseSetting):
    class Meta:
        verbose_name = 'Cookie consent settings'

    cookieconsent_active = models.BooleanField(
        "Activate cookie concent feature",
        default=False,
    )

    cookieconsent_title = models.CharField(
        max_length=255,
        default='Your cookie settings',
    )

    cookieconsent_message = RichTextField(
        default='This website deploys cookies for basic functionality and to keep it secure. These cookies are strictly necessary. Optional analysis cookies which provide us with statistical information about the use of the website may also be deployed, but only with your consent. Please review our <a href="/data-privacy-policy/">Privacy & Data Policy</a> for more information.',
    )

    panels = [
        MultiFieldPanel([
            FieldPanel('cookieconsent_active'),
            FieldPanel('cookieconsent_title'),
            FieldPanel('cookieconsent_message'),
        ], 'cookie banner'),
    ]
