from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from accounts.models import EducationalAssistant, Student, Teacher, User

from .models import EducationalAssistant, Student, User,AdminUser



class UserProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['profile_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and not request.user.is_staff:
            self.fields['profile_image'].queryset = User.objects.filter(id=request.user.id)

class EditTeacherProfileSerializers(serializers.ModelSerializer):
    class Meta: 
        model = Teacher
        fields = '__all__'
        read_only_fields = ['rank']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password_confirm', 'email', 'phone')
        extra_kwargs = {
            'phone_number': {'required': False}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class TeacherSerializers(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'



class EmailUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class PasswordResetActionSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    class Meta:
        model = User
        fields = ['email']

    def save(self):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return user

class PasswordResetLoginSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def save(self):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return user


class AdminSerializers(serializers.Serializer):
    class Meta:
        model = AdminUser
        fields = '__all__'



class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['profile_image', 'birthday']

    def update(self, instance, validated_data):
        profile_image = validated_data.get('profile_image', instance.profile_image)
        birthday = validated_data.get('birthday', instance.birthday)
        
        instance.profile_image = profile_image
        instance.birthday = birthday
        instance.save()
        
        return instance

class TeacherSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer()

    class Meta:
        model = Teacher
        fields = ['id', 'user', 'expertise', 'rank', 'department', 'can_be_advisor']
        read_only_fields = ['id','user','can_be_advisor','expertise', 'rank', 'department']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        profile_image = user_data.get('profile_image', None)
        birthday = user_data.get('birthday', None)

        # Update user profile image and birthday
        if profile_image is not None:
            instance.user.profile_image = profile_image
        if birthday is not None:
            instance.user.birthday = birthday
        instance.user.save()

        return instance
class StudentSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer()

    class Meta:
        model = Student
        fields = ['id', 'user', 'entry_semester', 'gpa', 'entry_year', 'major', 'advisor', 'military_service_status', 'year_of_study']

class EducationalAssistantSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer()

    class Meta:
        model = EducationalAssistant
        fields = ['id', 'user', 'field']



