from rest_framework import serializers
from accounts.models import Student , User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','first_name' ,'last_name','email' , 'user_number', 
                  'national_code', 'birthday', 'profile_image', 'phone', 'address', 'gender']

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer() 
    class Meta:
        model = Student
        fields = ['id', 'user', 'entry_semester', 'gpa', 'entry_year', 'major'
                  , 'advisor', 'military_service_status', 'year_of_study']