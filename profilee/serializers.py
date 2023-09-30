from rest_framework.serializers import ModelSerializer
from .models import ProfileUser, ProfileRecruiter


class ProfileUserSerializer(ModelSerializer):
    
    class Meta:
        model = ProfileUser
        fields = '__all__'
        extra_kwargs = {'user': {'required': False}}



class ProfileRecruiterSerializer(ModelSerializer):
    
    class Meta:
        model = ProfileRecruiter
        fields = '__all__'
        extra_kwargs = {'user': {'required': False}}
