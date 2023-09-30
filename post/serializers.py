from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Post, Job_level, Job_type
from django.db.models import Avg
from review.serializers import CommentSerializer




class Job_levelSerializer(ModelSerializer):
    class Meta:
        model = Job_level
        fields = '__all__'


class Job_typeSerializer(ModelSerializer):
    class Meta:
        model = Job_type
        fields = '__all__'

class PostListSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['company_name','job_type','level','experience','salary', 'pk']
        extra_kwargs = {'user': {'required': False}}



class PostDetailSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {'user': {'required': False}}


    def validate_salary(self, salary):
        if salary <= 0:
            raise ValidationError('Price not be 0 or little')
        return salary


    def to_representation(self, instance):
        repres = super().to_representation(instance)
        repres['rating'] = instance.ratings.all().aggregate(Avg('rating'))['rating__avg']
        repres['likes'] = instance.likes.all().count()
        repres['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        return repres

