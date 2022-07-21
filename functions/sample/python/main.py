#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#

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

    try:
        if params['']
        res = service.post_all_docs(
            db='reviews',
            include_docs=True,
        ).get_result()['rows']
        return [e['doc'] for e in res]


    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}

    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return 

main()