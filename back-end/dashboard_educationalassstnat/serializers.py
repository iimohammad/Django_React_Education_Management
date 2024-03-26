from rest_framework import serializers
from .models import *

class ApprovedCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovedCourse
        fields = ['id', 'Title', 'description' , 'teacher' , 'created_at']


class SemesterCourseSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = SemesterCourse
        fields = ['id', 'Title', 'description', 'Teacher', 'semester' , 'created_at' , 'week_day_course', 'exam_location' , 'exam_time' ]

class EducationAssistantSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = EducationAssistant
        fields = ['id', 'first_name', 'last_name', 'description', 'semester' , 'created_at' , 'contact_number', ]


class ActionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ['id', 'user', 'action_type', 'timestamp',]