from django.urls import path, re_path

from .views import EchoView, FibonacciView

urlpatterns = [
    re_path(r'^tutorial/?$', EchoView.as_view()),
    re_path(r'^fibonacci/?$', FibonacciView.as_view()),
    re_path(r'^logs/?$', FibonacciView.as_view()),
]
