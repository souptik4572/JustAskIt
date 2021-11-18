from rest_framework import serializers

from .models import Education, Employment, EndUser, Follow, Location


class EndUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EndUser
        fields = ('id', 'name', 'email', 'phone',
                  'description',  'profile_image', 'created_at')


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'location', 'start_year', 'end_year')


class EducationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Education
        fields = ('id', 'school', 'degree_type', 'graduation_year')


class EmploymentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employment
        fields = ('id', 'position', 'company', 'start_year', 'end_year')


class FollowSerializer(serializers.HyperlinkedModelSerializer):
    follower = EndUserSerializer(read_only=True)
    followee = EndUserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ('follower', 'followee')
