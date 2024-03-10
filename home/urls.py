from django.contrib import admin
from django.urls import path, include

from .views import *

urlpatterns = [
    path('', PublicBlog.as_view()),
    path('blog/', BlogView.as_view(), name='blog'),
]