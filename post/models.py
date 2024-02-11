from django.db import models
from django.contrib.auth.models import AbstractUser
from crum import get_current_user
from User.models import MyUser

class Post(models.Model):
   like=models.ManyToManyField(MyUser,default=None,blank=True,related_name="likes")
   captions=models.CharField(max_length=200)
   user=models.ForeignKey(MyUser,on_delete=models.CASCADE,related_name="userpost")
   created_on=models.DateTimeField(auto_now_add=True)
   updated_on=models.DateTimeField(auto_now=True)

# is_active=
   class Meta:
       ordering=['-created_on']
       
   def __str__(self):
        return self.pk
   
   def save(self,*args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user=None
        if not self.pk:
            self.user = user
        super(Post,self).save(*args,**kwargs)

   @property
   def like_count(self):
       count=self.like.count()
       return count

class PostImage(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="user_post")
    post_img=models.FileField(upload_to="Post/",max_length=250,null=True,default=None)


class Comment(models.Model):
    text=models.CharField(max_length=240,blank=True,null=True)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE)
    commented_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
    @property
    def comment_count(self):
        count=self.text.count()
        return count

class ArchivePost(models.Model):
    archive_post=models.ForeignKey(Post,on_delete=models.CASCADE)
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE)
   
class Story(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    story = models.FileField(upload_to="Story/", max_length=250, default=None, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)