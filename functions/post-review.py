
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from pprint import pprint
import requests

COUCH_URL = "https://db3582cc-bf02-4c82-a0fb-ac354b647a59-bluemix.cloudantnosqldb.appdomain.cloud"
IAM_API_KEY = "zRYGmwl5fu4dP_NVCvUd4Vc8lyiBphX4CjSf5bwXvfvr"
COUCH_USERNAME = "db3582cc-bf02-4c82-a0fb-ac354b647a59-bluemix"


def main(params=None):
    authenticator = IAMAuthenticator(IAM_API_KEY)
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(COUCH_URL)
    res = service.post_document(
        db='reviews',
        document=params['review'],
    ).get_result()
    return res
