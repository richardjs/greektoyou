from django.urls import path

import greektoyou.views

urlpatterns = [
    path('read/<str:book_id>', greektoyou.views.read),
]
