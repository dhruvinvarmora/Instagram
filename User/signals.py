from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Follow, Room
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=Follow)
def check_mutual_follow_and_create_room(sender, instance, created, **kwargs):
    if not created:
        return

    user1 = instance.user
    user2 = instance.followed

    try:
        reverse_follow = Follow.objects.get(user=user2, followed=user1)

        # Both follow each other
        instance.follow_each_other = True
        reverse_follow.follow_each_other = True
        instance.save(update_fields=["follow_each_other"])
        reverse_follow.save(update_fields=["follow_each_other"])

        # Create room
        slug = f'{min(user1.username, user2.username)}_{max(user1.username, user2.username)}'
        room_name = f'chat_{slug}'
        Room.objects.get_or_create(slug=slug, defaults={'name': room_name})
        print(f"✅ Room created for mutual follow: {room_name}")

    except Follow.DoesNotExist:
        # One-sided follow only
        instance.follow_each_other = False
        instance.save(update_fields=["follow_each_other"])
        print(f"⚠️ One-sided follow: {user1.username} → {user2.username}")