from rest_framework import serializers

from .models import Course, Enrollment

from useraccount.serializers import UserDetailSerializer


class CoursesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            'id',
            'title',
            'image_url',
        )


class CoursesDetailSerializer(serializers.ModelSerializer):
    instructor = UserDetailSerializer(read_only=True, many=False)

    class Meta:
        model = Course
        fields = (
            'id',
            'title',
            'description',
            'image_url',
            'instructor'
        )


class EnrollmentsListSerializer(serializers.ModelSerializer):
    course = CoursesListSerializer(read_only=True, many=False)
    
    class Meta:
        model = Enrollment
        fields = (
            'id',  'course'
        )