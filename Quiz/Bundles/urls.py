from django.urls import path
from .views import BundleView, SpecificBundle
urlpatterns = [
    path('', BundleView.as_view()),
    path('<int:pk>', SpecificBundle.as_view())
]