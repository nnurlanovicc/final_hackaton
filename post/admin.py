from django.contrib import admin
from .models import Post, Job_type, Job_level
from review.models import Comment

class CommentInLine(admin.TabularInline):
    model = Comment

class PostAdmin(admin.ModelAdmin):
    list_filter = ['vacancy', 'salary']
    search_fields = ['vacancy', 'description']
    inlines = [CommentInLine]


admin.site.register(Post, PostAdmin)
admin.site.register(Job_type)
admin.site.register(Job_level)

