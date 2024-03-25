from rest_framework import serializers
from .models import *

class ApprovedCourseSerialziers(serializers.ModelSerializer):
    class Meta:
        model = ApprovedCourse
        fields = ['id', 'Title', 'description' , 'teacher' , 'created_at']


class EducationAssistantSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = EducationAssistant
        fields = ['id', 'first_name', 'last_name', 'description', 'semester' , 'created_at' , 'contact_number', ]

class ActionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ['id', 'user', 'action_type', 'timestamp',]