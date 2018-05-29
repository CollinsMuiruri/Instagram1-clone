from django.db import models
import datetime as dt
from django.contrib.auth.models import User
from tinymce.models import HTMLField

# Create your models here.


class tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Profile(models.Model):
    profilePic = models.ImageField(upload_to='profile/', null=True, blank=True)
    bio = models.CharField(max_length=60, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.bio

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def get_profile(cls):
        profile = Profile.objects.all()
        return profile

    @classmethod
    def find_profile(cls, search_term):
        profile = cls.objects.filter(user__username__icontains=search_term)
        return profile

    @classmethod
    def update_profile(cls, id, bio):
        updated = Image.objects.filter(id=id).update(bio=bio)
        return updated


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    image_name = models.CharField(max_length=60)
    caption = HTMLField()
    editor = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image

    def save_editor(self):
        self.save()

    class Meta:
        ordering = ['image']

    def delete_profile(self):
        self.delete()

    def change_profile(self):
        self.change()

    def update_profile(self):
        self.update()

    @classmethod
    def get_images(cls):
        image = Image.objects.all()
        return image

    @classmethod
    def todays_images(cls):
        today = dt.date.today()
        images = cls.objects.filter(pub_date__date=today)
        return images

    @classmethod
    def days_images(cls, date):
        images = cls.objects.filter(pub_date__date=date)
        return images

    @classmethod
    def search_by_image_name(cls, search_term):
        images = cls.objects.filter(image_name__icontains=search_term)
        return images


class Comment(models.Model):
    comments = models.CharField(max_length=60, blank=True, null=True)
    comment_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)

    def __str__(self):
        return self.comments

    class Meta:
        ordering = ['-comment_date']

    def save_comment(self):
        return self.save()

    def delete_comment(self):
        self.delete()

    @classmethod
    def get_comment(cls):
        comment = Comment.objects.all()
        return comment
