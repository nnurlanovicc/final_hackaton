from rest_framework.serializers import ModelSerializer,ReadOnlyField,ValidationError,PrimaryKeyRelatedField
from .models import Comment, Like, Rating,FavoriteItem
from post.models import Post
# from post.serializers import PostListSerializer



class CommentSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.email')
    post = ReadOnlyField(source='')

    class Meta:
        model = Comment
        fields = '__all__'


    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        post = validated_data.get('post')
        comment = Comment.objects.create(**validated_data)
        return comment        

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if instance.author != user:
            raise ValidationError('Вы не можете изменить комментарии другого автора')
        if 'author' in validated_data:
            raise ValidationError('Вы не можете изменить автора')
        instance.body = validated_data.get('body', instance.body)
        instance.save()
        return instance



class RatingSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.email')
    post = ReadOnlyField(source='')

    class Meta:
        model = Rating
        fields = '__all__'


    def validate_rating(self, rating):
        if rating in range(1,6):
            return rating
        raise ValidationError('Рейтинг должен быть от 1 до 5')


    def create(self, validated_data):
        user = self.context['request'].user
        post = validated_data.get('post')
        if not post:
            raise ValidationError('Поле "post" обязательно')
        if Rating.objects.filter(post=post, author=user).exists():
            raise ValidationError('Вы уже оставляли рейтинг для этого поста')
        return Rating.objects.create(post=post, author=user, **validated_data)

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if instance.author != user:
            raise ValidationError('Вы не можете изменить рейтинг другого автора')
        if 'author' in validated_data:
            raise ValidationError('Вы не можете изменить автора')
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        return instance

class LikeSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.email')
    post = ReadOnlyField(source='')


    class Meta:
        model = Like
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        return self.Meta.model.objects.create(author=user, **validated_data)
    


class FavoriteListSerializer(ModelSerializer):
    # post = PostListSerializer

    class Meta:
        model = FavoriteItem
        fields = '__all__'


class FavoriteCreateSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.email')

    class Meta:
        model = FavoriteItem
        fields = ('post', 'author')


