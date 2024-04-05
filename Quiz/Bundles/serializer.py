from rest_framework import serializers
from .models import  Bundle


class BundleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bundle
        fields = ['id', 'name', 'price', 'no_of_questions','no_of_quizzes']