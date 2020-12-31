from botocore.exceptions import ClientError
from chalice import Chalice, CORSConfig, NotFoundError, BadRequestError, Response, AuthResponse, AuthRoute, \
    CognitoUserPoolAuthorizer
from basicauth import decode
import logging
import boto3
from hashlib import blake2b
import json

app = Chalice(app_name='backendservice')

app = Chalice(app_name='lasalle_serverlessbackend')

app.log.setLevel(logging.DEBUG)

cors_config = CORSConfig(allow_origin="*")

default_news = [
    {
        'firstNew': True,
        'title': "ESA formally adopts Ariel, the exoplanet explorer",
        'imageSrc': "https://s3-eu-west-1.amazonaws.com/ieec.cat/uploads/PR_Image2.webp",
        'date': "2020-11-13 11:50:00",
        'description': "The European Space Agency (ESA) has formally adopted the " +
                       "mission " +
                       "Ariel into the program of future missions for implementation.",
        'link': "content/58/news/detail/880/esa-formally-adopts-ariel-the-exoplanet-explorer"
    },
    {
        'firstNew': False,
        'title': "NewSpace Strategy of Catalonia, a new step towards the democratization" +
                 " of space",
        'imageSrc': "https://s3-eu-west-1.amazonaws.com/ieec.cat/uploads/PR_Image1.webp",
        'date': "2020-11-10 12:50:00",
        'description': "The Catalan Government has promoted the development and " +
                       "implementation of this initiative, which seeks that new private " +
                       "agents find commercial opportunities in the exploration and use of space.",
        'link': "content/58/news/detail/878/newspace-strategy-of-catalonia-a-new-step-towards-the-" +
                "democratization-of-space"
    },
    {
        'firstNew': False,
        'title': "New research on light flashes in the night sky may improve astronomical data",
        'imageSrc': "https://s3-eu-west-1.amazonaws.com/ieec.cat/uploads/PR_Image1.gif",
        'date': "2020-11-09 15:25:00",
        'description': "A team that includes a researcher from Institute of Space Studies of " +
                       "Catalonia (IEEC) at Institute of Cosmos Science (ICC-UB) measured flashes of light, " +
                       "often mistaken for stars, reflecting off satellites and space trash in Earth&#39;s orbit",
        'link': "content/58/news/detail/877/new-research-on-light-flashes-in-the-night-sky-may-improve-" +
                "astronomical-data"
    },
    {
        'firstNew': False,
        'title': "A technologically viable model for a Mars city, as imagined by a Catalan-led team",
        'imageSrc': "https://s3-eu-west-1.amazonaws.com/ieec.cat/uploads/" +
                    "Nuwa%2BCliff%2Band%2BValley%2BCover%2BImage.webp",
        'date': "2020-10-19 12:00:00",
        'description': "A proposal for a city on planet Mars by a Catalan-led team was presented on Saturday," +
                       " 17 October 2020, in the final of the Mars Society competition",
        'link': "content/58/news/detail/875/a-technologically-viable-model-for-a-mars-city-" +
                "as-imagined-by-a-catalan-led-team"
    },
    {
        'firstNew': False,
        'title': "IEEC researchers lead project selected among the finalists of the Mars Society competition to develop a city on the red planet",
        'imageSrc': "https://s3-eu-west-1.amazonaws.com/ieec.cat/uploads/Nuwa%2BCliff%2Band%2BValley%2BCover%2BImage.webp",
        'date': "2020-10-13 14:00:00",
        'description': "The Mars city proposal is led by researchers from the Institute of" +
                       " Space Studies of Catalonia (IEEC) at the Institute of Space Sciences (ICE, CSIC), the Polytechnic " +
                       "University of Catalonia (UPC) and the Institute of Cosmos Sciences of the University of " +
                       "  Barcelona (ICCUB).",
        'link': "content/58/news/detail/871/ieec-researchers-lead-project-selected-among-the-finalists-of-the-mars-society-competition-to-develop-a-city-on-the-red-planet"
    }
]

users_new_dictionary = {
    "testkey": []
}


@app.route('/', cors=cors_config)
def index():
    return {'hello': 'world'}


# /news?key=127H3267
@app.route('/news', methods=['GET'], cors=cors_config)
def news():
    global users_new_dictionary
    app.log.debug("GET Call app.route/news")
    key = ''
    try:
        key = app.current_request.query_params.get('key')
    except AttributeError:
        key = ''

    if len(key) == 0:
        return json.dumps(default_news)

    if key in users_new_dictionary:
        return json.dumps(users_new_dictionary[key])
    return json.dumps([])


# /news?key=127H3267
@app.route('/news', methods=['POST'], cors=cors_config)
def create_news():
    global users_new_dictionary
    try:
        key = app.current_request.query_params.get('key')
    except AttributeError:
        key = ''

    if key in users_new_dictionary:
        app.log.debug("POST found key in app.route/new: " + key)
    else:
        users_new_dictionary[key] = []

    post_json = app.current_request.json_body
    users_new_dictionary[key].append(post_json)
    return json.dumps(users_new_dictionary[key])


# /news?key=127H3267
@app.route('/news', methods=['DELETE'], cors=cors_config)
def delete_news():
    global users_new_dictionary
    try:
        key = app.current_request.query_params.get('key')
    except AttributeError:
        raise NotFoundError("You have to pass a key: /news?key=127H3267")

    if key in users_new_dictionary:
        users_new_dictionary[key] = []
    else:
        raise NotFoundError("key: " + key + " not found")

    return {"deleted": True}


@app.route('/allnews', methods=['GET'], cors=cors_config)
def news():
    global users_new_dictionary
    return json.dumps(users_new_dictionary)
