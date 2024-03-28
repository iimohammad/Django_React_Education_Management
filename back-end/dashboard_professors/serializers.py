from rest_framework import serializers
from education.models import Course, Semester


class ShowSemestersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['id', 'name', 'start_semester', 'end_semester', 'semester_type']
