from rest_framework import serializers
from .models import ContactInfo, University,Comment

class ContactInfoSerialziers(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = ['id', 'email', 'phone_number' , 'mobile_number' , 'address']


class UniversitySerializers(serializers.ModelSerializer):
 
    class Meta:
        model = University
        fields = ['id', 'name', 'description', 'contentInfo', 'website_url' , 'social_media_links']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'university', 'content', 'author']

class AdminCommentSerializers(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'post', 'content', 'author', 'is_active' , 'created_at']