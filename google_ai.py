# import os
# from google.oauth2 import service_account
# from googleapiclient.discovery import build

# import sys
# print("Python Path:", sys.path)
# from google.oauth2 import service_account
# from googleapiclient.discovery import build


# class GoogleAI:
#     def __init__(self):
#         # Load credentials from the service account JSON key
#         key_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_KEY")
#         self.credentials = service_account.Credentials.from_service_account_file(key_path)

#     def get_vision_service(self):
#         # Example: Initialize Google Vision API
#         return build("vision", "v1", credentials=self.credentials)

#     def analyze_image(self, image_uri):
#         # Example: Use Google Vision API to analyze an image
#         service = self.get_vision_service()
#         request = service.images().annotate(body={
#             "requests": [{
#                 "image": {"source": {"imageUri": image_uri}},
#                 "features": [{"type": "LABEL_DETECTION", "maxResults": 10}]
#             }]
#         })
#         response = request.execute()
#         return response
