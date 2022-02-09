from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

from attendant.models import Student, School, Absent, Like, Document


class StudentApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = (
            'id', 'student_name', 'school', 'studyfield_code', 'studyfield_name', 'input_date', 'parent_mobile',
            'student_level',)


class SchoolApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = (
            'id', 'school_name', 'school_phone', 'school_address', 'studyfield_code_list', 'studyfield_name_list',
            'school_admin', 'school_sms_api', 'school_sms_username', 'school_sms_password')


class AbsentApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Absent
        fields = (
            'student', 'absent_date', 'sent', 'absent_type',)


class LikeApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = (
            'student', 'date_send',)


class DocumentApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = (
            'docfile',)


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid Details.")
