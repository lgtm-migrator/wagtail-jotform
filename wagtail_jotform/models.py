from django.conf import settings
from django.db import models
from django.forms.widgets import Select
from django.shortcuts import render

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page

from .utils import JotFormAPI


def jot_form_choices():
    jot_form_data = []
    if settings.JOTFORM_API_URL and settings.JOTFORM_API_KEY:
        data = JotFormAPI()
        data.fetch_from_api()
        data = data.get_data()

        if data and "content" in data:
            for item in data["content"]:
                jot_form_data.append((item["id"], item["title"]))
    return jot_form_data


class EmbededFormPage(RoutablePageMixin, Page):
    thank_you_template = "wagtail_jotform/thank_you.html"
    subpage_types = []

    introduction = models.TextField(blank=True)
    form = models.CharField(max_length=1000)
    thank_you_text = RichTextField(
        blank=True,
        help_text="Text displayed to the user on successful submission of the form",
    )

    @route(r"^thank-you/$", name="embeded_form_thank_you")
    def thank_you_page(self, request, *args, **kwargs):
        return render(request, self.thank_you_template, {"page": self})

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("form", widget=Select(choices=jot_form_choices())),
        FieldPanel("thank_you_text"),
    ]