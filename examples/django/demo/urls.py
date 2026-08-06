from django.http import HttpResponse, JsonResponse
from django.urls import include, path

from scalekit.frameworks.django import login_required


def home(request):
    return HttpResponse(
        '<a href="/login">Login</a> | <a href="/account">Account</a> | <a href="/logout">Logout</a>'
    )


@login_required
def account(request):
    return JsonResponse(request.scalekit_user)


urlpatterns = [
    path("", home),
    path("account", account),
    path("", include("scalekit.frameworks.django")),
]
