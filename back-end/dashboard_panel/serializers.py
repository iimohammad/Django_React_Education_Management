from rest_framework import serializers
from .models import (
    EnrollmentRequest,
)
class EnrollmentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrollmentRequest
        fields = '__all__'

class EducationalAssistantEnrollmentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrollmentRequest
        fields = '__all__'

class StudentEnrollmentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrollmentRequest
        exclude = ['is_approved']
