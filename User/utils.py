# from fcm_django.models import FCMDevice
# from .fcm import FCMClient
# from User.models import Notification

# def send_notification(user, token, message_title, message_body):
#     resp = FCMClient()._send_fcm_message(
#         token=token,
#         message_title=message_title,
#         message_body=message_body,
#     )
#     if resp is not None:
#         if resp.status_code == 200:
#             Notification.objects.create(
#                 user=user,
#                 notification_title=message_title,
#                 notification_body=message_body,
#                 is_read=False,
#             )
#         else:
#             pass
#     else:
#         pass
#     return "success"

import traceback
from fcm_django.models import FCMDevice
from User.fcm import FCMClient

def send_firebase_push_notification(user_ids, data):
    """Celery task to send fcm push notification on passed notification with message."""

    try:
        devices = FCMDevice.objects.filter(user__id__in=user_ids)
        if devices:
            FCMClient().send_push_notification(
                devices,
                data,
            )
    except Exception as e:
        print(traceback.format_exc())
        print(e)    

