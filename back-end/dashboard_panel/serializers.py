from rest_framework import serializers
from accounts.models import Teacher, EducationalAssistant

class TeacherSerializers(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class EducationalAssistantSerializers(serializers.ModelSerializer):
    class Meta:
        Model = EducationalAssistant
        fields = '__all__'


    
