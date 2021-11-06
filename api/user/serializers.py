from rest_framework import serializers
from .models import EndUser, Location, Education, Employment


class EndUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EndUser
        fields = ('id', 'name', 'email', 'phone', 'description',
                  'followers', 'following', 'profile_image', 'created_at')


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'location', 'start_year', 'end_year')


class EducationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Education
        fields = ('school', 'degree_type', 'graduation_year')


class EmploymentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employment
        fields = ('position', 'company', 'start_year', 'end_year')
