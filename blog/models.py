from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy
from taggit.managers import TaggableManager


class Post(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts')

    title = models.CharField(max_length=125)
    tags = TaggableManager()

    added = models.ManyToManyField(get_user_model(), related_name='bookmarks', blank=True)

    text = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    main_img = models.ImageField(upload_to='uploads/%Y/%m/%d/', null=True, blank=True)

    ordering=('-created',)

    def __str__(self):
        return f'Post: {self.title}'

    def get_normal_time(self):
        return self.created.strftime('%b %d, %Y')

    def get_absolute_url(self):
        return reverse_lazy('blog:post-detail', args=[self.pk])


class Meet(models.Model):
    title = models.CharField(max_length=100)

    lat = models.FloatField()
    lng = models.FloatField()

    tags = TaggableManager()

    meet_date = models.DateTimeField()
    participants = models.ManyToManyField(get_user_model(), related_name='meets', blank=True)

    ordering = ['-meet_date']

    def __str__(self):
        return f'Meet {self.title}'

    def get_normal_time(self):
        return self.meet_date.strftime('%Y-%m-%d %H:%M')

    def get_absolute_url(self):
        return reverse_lazy('blog:meet-detail', args=[self.pk])
