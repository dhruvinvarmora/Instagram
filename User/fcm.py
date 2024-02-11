# import json

# import google.auth.transport.requests
# import requests
# from django.conf import settings
# from google.oauth2 import service_account


# class FCMClient(object):
#     """FCM Client For Firebase Push Notification"""

#     def __init__(self):

#         self.FCM_URL = "https://fcm.googleapis.com/v1/projects/firpta-solutions/messages:send"
#         self.SCOPES = ["https://www.googleapis.com/auth/firebase.messaging"]

#     def _get_access_token(self):
#         """
#         Retrieve a valid access token that can be used to authorize requests.

#         :return: Access token.
#         """
#         credentials = service_account.Credentials.from_service_account_file(
#             settings.GOOGLE_APPLICATION_CREDENTIALS,
#             scopes=self.SCOPES,
#         )
#         request = google.auth.transport.requests.Request()
#         credentials.refresh(request)
#         return credentials.token

#     def get_headers(self):
#         headers = {
#             "Authorization": "Bearer " + self._get_access_token(),
#             "Content-Type": "application/json; UTF-8",
#         }
#         return headers

#     def _send_fcm_message(self, token, message_title, message_body):
#         """
#         Send HTTP request to FCM with given message.
#         Args:
#             fcm_message: JSON object that will make up the body of the request.
#         """
#         try:
#             headers = self.get_headers()

#             fcm_message = {
#                 "message": {
#                     "token": token,
#                     "notification": {"title": message_title, "body": message_body},
#                     "webpush": {"fcm_options": {"link": settings.APP_URL}},
#                 }
#             }

#             resp = requests.post(
#                 self.FCM_URL, data=json.dumps(fcm_message), headers=headers
#             )

#             if resp.status_code == 200:
#                 print("Message sent to Firebase for delivery, response:")
#                 return resp
#             else:
#                 print("Unable to send message to Firebase")
#         except Exception as e:
#             print("➡ e :", e)


import time
from django.conf import settings
from firebase_admin.messaging import Message, Notification
import firebase_admin

class FCMClient(object):
    """FCM Client For Firebase Push Notification"""

    def __init__(self) -> None:
        try:
            firebase_admin.get_app()
        except Exception:
            cred = firebase_admin.credentials.Certificate(settings.GOOGLE_APPLICATION_CREDENTIALS)
            firebase_admin.initialize_app(cred)
            

    def send_push_notification(self, devices, data):
        try:
            # device = FCMDevice.objects.filter(user__in=user_ids).first()
            # result = devices.send_message(title=data["title"],body=data["message"], sound=True)
            print("---------->>>>>>>>>>>>,,,,,,,,,,")
            time.sleep(5)
            # result = devices.send_message(Message(data=data))
            result = devices.send_message(Message(notification=Notification(title=data["title"], body=data["message"])))
            return result
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            pass