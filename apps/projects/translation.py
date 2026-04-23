from modeltranslation.translator import TranslationOptions, register

from .models import CaseStudy


@register(CaseStudy)
class CaseStudyTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "client",
        "industry",
        "challenge",
        "solution",
        "results",
        "meta_description",
    )
