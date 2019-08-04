from django.urls import path

import greektoyou.views

urlpatterns = [
    path('read/<str:book_id>', greektoyou.views.read),
    path('api/info/<str:word_code>', greektoyou.views.api_info),
]
