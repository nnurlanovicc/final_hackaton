from django.db import models
from django.contrib.auth import get_user_model
from post.models import Post

User = get_user_model()



class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes',verbose_name='автор')
    post = models.ForeignKey( Post, on_delete=models. CASCADE, related_name='likes',verbose_name='пост')
    
    

class Comment(models.Model):
    body = models.TextField(verbose_name='Содержимое комментария')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments',verbose_name='пост')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments',verbose_name='автор')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='дата создания')


    

class Rating(models.Model):
    rating = models.PositiveSmallIntegerField(default=1,blank=False,verbose_name='рейтинг')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='ratings',verbose_name='пост')
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='ratings',verbose_name='автор')



class FavoriteItem(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favorites',verbose_name='пост')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites',verbose_name='автор')


    class Meta:
        ordering: ('-pk',)
        constraints = [models.UniqueConstraint(fields=['author', 'post'], name='unique_author_post'),]
        indexes = [models.Index(fields=['author','post'], name='idx_auth_post'),]


    def __str__(self):
        return f'{self.author}->{self.post}'
    
    


    


