from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("quiz/<str:quiz_url>/", views.getQuiz, name="quizInfo")
]
