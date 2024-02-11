from django.db import IntegrityError
from crum import get_current_user
from django.dispatch import Signal, receiver
from django.db.models.signals import pre_save,post_delete,pre_delete,post_save
from User.models import Follow, MyUser
from post.views import Notificitons
from post.models import Comment, Post

post_liked = Signal()
post_unliked = Signal()

@receiver(pre_delete, sender=Follow)
def activity_log_create_update(sender, instance, **kwargs):
    user=get_current_user()
    new_data = (instance.__dict__).copy()
    send_user = new_data["followed_id"]
    receiver = MyUser.objects.filter(pk=send_user).first()
    sender = get_current_user()
    Notificitons.objects.create(
        receiver=receiver,
        sender=sender,
        type=Notificitons.UNFOLLOW
    )

@receiver(pre_save, sender=Follow)
def activity_log_create_update(sender, instance, **kwargs):
    new_data = (instance.__dict__).copy()

    if instance.pk:
        old_data = Follow.objects.get(pk=instance.pk).__dict__.copy()
        
        user = get_current_user()

        Notificitons.objects.create(
            receiver=user,
        )
    else:
        user = new_data["user_id"]
        send_user = new_data["followed_id"]
        receiver = MyUser.objects.filter(pk=send_user).first()

        sender = get_current_user()
        
        Notificitons.objects.create(
            receiver=receiver,
            sender=sender,
            type=Notificitons.FOLLOW
        )

@receiver(post_liked)
def handle_post_liked(sender, **kwargs):
    receiver_user = kwargs['post']
    user = kwargs['user']
    post=Post.objects.get(pk=receiver_user.pk)
    Notificitons.objects.create(
        receiver=receiver_user.user,
        sender=user,
        post=post,
        type=Notificitons.LIKE
    )

@receiver(post_unliked)
def handle_post_unliked(sender, **kwargs):
    receiver_user = kwargs['post']
    user = kwargs['user']
    post=Post.objects.get(pk=receiver_user.pk)
    Notificitons.objects.create(
        receiver=receiver_user.user,
        sender=user,
        post=post,
        type=Notificitons.UNLIKE
    )

@receiver(post_save, sender=Post)
def activity_log_create_update(sender, instance, created, **kwargs):
    new_data = (instance.__dict__).copy()
    print('new_data--------------------------------------: ', new_data)
    if created:
        print('_________________kwargs',kwargs)
        uploader = get_current_user()
        Notificitons.objects.create(
            sender=uploader,
            post=instance,
            type=Notificitons.UPLOADED
        )


@receiver(post_save, sender=Comment)
def activity_log_create_update(sender, instance, **kwargs):
    new_data = (instance.__dict__).copy()
    unrequired_fields = ["_state", "created_on", "updated_on"]

    for field in unrequired_fields:
        del new_data[field]
    print('-------------',instance)
    print('-------------',kwargs)
    user = new_data["user_id"]
    send_user = Post.objects.get(id=new_data["post_id"])
    receiver = MyUser.objects.filter(username=send_user.user).first()
    post_instance = Post.objects.get(id=new_data["post_id"])
    sender = get_current_user()
    print('------new_data-------',new_data['text'])
    comment=Comment.objects.filter(text = new_data['text']).first()
    print('comment-----------------------------: ', comment)
    Notificitons.objects.create(
        post=post_instance,
        receiver=receiver,
        sender=sender,
        comment=comment,
        type=Notificitons.COMMENT
    )