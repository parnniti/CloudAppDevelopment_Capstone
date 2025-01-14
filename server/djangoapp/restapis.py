import requests
import json
from requests.auth import HTTPBasicAuth
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from pprint import pprint
from enum import Enum

# import related models here
from .models import CarDealer, DealerReview

COUCH_URL = "https://db3582cc-bf02-4c82-a0fb-ac354b647a59-bluemix.cloudantnosqldb.appdomain.cloud"
IAM_API_KEY = "zRYGmwl5fu4dP_NVCvUd4Vc8lyiBphX4CjSf5bwXvfvr"
COUCH_USERNAME = "db3582cc-bf02-4c82-a0fb-ac354b647a59-bluemix"

authenticator = IAMAuthenticator(IAM_API_KEY)
service = CloudantV1(authenticator=authenticator)
service.set_service_url(COUCH_URL)


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(review, **kwargs):
    response = service.post_document(
        db='reviews',
        document=review,
    ).get_result()
    return response


# Create a get_dealers_from_cf method to get dealers from a cloud function

def dealer_json_to_object(dealer):
    return CarDealer(
        address=dealer["address"], 
        city=dealer["city"], 
        full_name=dealer["full_name"],
        id=dealer["id"], 
        lat=dealer["lat"], 
        long=dealer["long"],
        short_name=dealer["short_name"],
        st=dealer["st"], 
        zip=dealer["zip"],
    )

def get_dealers_from_cf():
    try:
        res = service.post_all_docs(
            db='dealerships',
            include_docs=True,
        ).get_result()['rows']
        return [dealer_json_to_object(_['doc']) for _ in res]

    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    except:
        return {"error": "Something went wrong"}

def get_dealer_by_id(dealer_id=1):
    try:
        res = service.post_find(
            db='dealerships',
            selector={
                "id": dealer_id
            },
        ).get_result()['docs']
        return dealer_json_to_object(res[0])

    except:
        print("Something went wrong with get_dealer_by_id()")

def get_dealers_by_state(state="CA"):
    try:
        res = service.post_find(
            db='dealerships',
            selector={
                "st": state
            },
        ).get_result()['docs']
        return [dealer_json_to_object(dealer) for dealer in res]

    except:
        print("Something went wrong with get_dealer_by_state()")


def review_json_to_object(review_json):
    try:
        review_obj = DealerReview(
            dealership=review_json["dealership"],
            name=review_json["name"],
            review=review_json["review"],
            purchase=review_json["purchase"],
        )
    except:
        print("Error while creating a review object")

    review_obj.sentiment = analyze_review_sentiments(review_obj.review)
    
    if "id" in review_json:
        review_obj.id = review_json["id"]
    if "purchase_date" in review_json:
        review_obj.purchase_date = review_json["purchase_date"]
    if "car_make" in review_json:
        review_obj.car_make = review_json["car_make"]
    if "car_model" in review_json:
        review_obj.car_model = review_json["car_model"]
    if "car_year" in review_json:
        review_obj.car_year = review_json["car_year"]

    return review_obj

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(dealer_id=None):
    try:
        if dealer_id:
            res = service.post_find(
                db='reviews',
                selector={
                    "dealership": dealer_id,
                }
            ).get_result()['docs']

            results = [review_json_to_object(review_json) for review_json in res]
            return results
            
        else:
            res = service.post_all_docs(
                db='reviews',
                include_docs=True,
            ).get_result()['rows']
            return [review_json_to_object(_['doc']) for _ in res]

    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    except:
        return {"error": "Something went wrong with get_dealer_reviews_from_cf()"}

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text

NLU_API_KEY = "8kyJZrl0F6ziUmLLXcFnfkyWx7Jm0lgcOEW8-d_5-Chq"
NLU_URL = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/a78b5af7-0f36-4503-8beb-08652486aaa3"

class NLUmethods(Enum):
    ANALYZE = "/v1/analyze"


def analyze_review_sentiments(text):

    params = {
        "text": text,
        "version": "2022-04-07",
        "features": "sentiment",
    }

    response = requests.get(
        url = NLU_URL + NLUmethods.ANALYZE.value,
        params = params,
        headers = {
            'Content-Type': 'application/json'
        },
        auth=HTTPBasicAuth('apikey', NLU_API_KEY),
    )
    json_text = json.loads(response.text)

    try:
        return json_text['sentiment']['document']['label']
    except:
        return "neutral"


