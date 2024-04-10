from rest_framework import serializers
from accounts.models import User , Student
from education.models import Major

class UserSerializerNameLastname(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name')
    
class MajorSerializerName(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = ['major_name']
        
class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializerNameLastname()
    major = MajorSerializerName()
    class Meta:
        model = Student
        fields = ['id', 'user', 'entry_semester', 'gpa', 'entry_year', 'major',
                    'military_service_status','year_of_study']