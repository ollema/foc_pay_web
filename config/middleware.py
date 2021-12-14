import functools

from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import get_supported_language_variant


@functools.lru_cache()
def get_languages():
    """
    Cache of settings.LANGUAGES in a dictionary for easy lookups by key.
    """
    return dict(settings.LANGUAGES)


class SimpleLocaleMiddleware(MiddlewareMixin):
    """
    Parse a request and decide what translation object to install in the
    current thread context. This allows pages to be dynamically translated to
    the language the user desires (if the language is available).
    """

    response_redirect_class = HttpResponseRedirect

    def process_request(self, request):
        # default lang from settings
        language = settings.LANGUAGE_CODE

        # get language/lang_code from cookies
        lang_code = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
        if lang_code:
            if lang_code in get_languages():
                language = lang_code
            else:
                try:
                    language = get_supported_language_variant(lang_code)
                except LookupError:
                    pass

        # always use english on admin site
        if request.path.lstrip("/").startswith(settings.ADMIN_URL.lstrip("/")):
            language = "en-US"

        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        language = translation.get_language()
        response.headers.setdefault("Content-Language", language)
        return response
