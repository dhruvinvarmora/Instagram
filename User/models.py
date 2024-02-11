from django.db import models
from django.contrib.auth.models import AbstractUser
from crum import get_current_user


class MyUser(AbstractUser):
    username=models.CharField(max_length=30,unique=True)
    Gender=(('Male','Male'),
            ('Female','Female'))
    Bio=models.CharField(max_length=200) 
    Gender=models.CharField(choices=Gender,default='Male',max_length=20)
    DP=models.ImageField(upload_to="DP/",max_length=250,null=True,default=None)

    @property
    def follower_count(self):
        count=self.follow_follower.count()
        return count
    @property
    def following_count(self):
        count=self.follow_followed.count()
        return count
    
    @property
    def postcount(self):
        count=self.userpost.count()
        return count



class Follow(models.Model):
    user=models.ForeignKey(MyUser,related_name="follow_follower",on_delete=models.CASCADE)
    followed=models.ForeignKey(MyUser,related_name="follow_followed",on_delete=models.CASCADE)
    is_follow=models.BooleanField(default=True)
    followed_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} --> {self.followed}"
    
    def save(self,*args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user=None
        if not self.pk:
            self.user = user
        super(Follow,self).save(*args,**kwargs)




class Notification(models.Model):
    """User Notification Model"""

    user = models.ForeignKey(
        MyUser,
        on_delete=models.SET_NULL,
        related_name="user_notification",
        null=True,
        blank=True,
    )
    notification_title = models.CharField(null=True, blank=True, max_length=255)
    notification_body = models.CharField(null=True, blank=True, max_length=255)
    is_read = models.BooleanField(default=False)