from django.urls import path
from .views import QuizMakerAPIView,QuizAPIView,SpecificQuiz
urlpatterns = [
    path('create/', QuizMakerAPIView.as_view()),
    path('teacher/<int:fk>', QuizAPIView.as_view()),
    path('<int:pk>', SpecificQuiz.as_view()),
]