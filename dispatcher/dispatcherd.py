# -*- encoding: utf-8 -*-

import logging
import requests
import time

logger = logging.getLogger('dispatcherd')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s : %(name)s : %(levelname)s : %(message)s')
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)


# Base API url without the ending slash
API_SERVER_BASE_URL = 'http://localhost:8081/api'

# Worker API port
API_WORKER_URL_FORMAT = 'http://{address}:8082/{endpoint}/'

# Wait time for next iteration (seconds)
SLEEP_SECONDS = 5


def get_scheduled_environments():
    endpoint = '/environment/environments/'
    query = '?deployment__status=Scheduled'
    url = API_SERVER_BASE_URL + endpoint + query

    environments = None

    logger.info("Getting scheduled environments from '%s'" % url)
    response = requests.get(url)

    # Check if something when wrong
    response.raise_for_status()
    
    environments = response.json()
    logger.info(
        "Number of scheduled environments retrieved '%s'" % len(environments)
    )

    return environments

def get_scheduled_actions():
    endpoint = '/environment/actions/'
    query = '?environment__deployment__status=Success&status=Scheduled'
    url = API_SERVER_BASE_URL + endpoint + query

    logger.info("Getting scheduled actions from '%s'" % url)
    response = requests.get(url)

    # Check if something when wrong
    response.raise_for_status()
    
    actions = response.json()
    logger.info(
        "Number of scheduled actions retrieved '%s'" % len(actions)
    )

    return actions

def send_environment_data(environment):
    
    # Get worker
    worker_url = environment.get('worker')
    response = requests.get(worker_url)
    response.raise_for_status()
    worker = response.json()

    # Get worker API URL
    url = API_WORKER_URL_FORMAT.format(
        address=worker.get('address'),
        endpoint='environments'

    )

    try:

        # Send enviroment data to worker (flask receives data when json is used)
        response = requests.post(url,json=environment)
        response.raise_for_status()

        # Resport to api serve that the deployemnt 
        # was dispatched
        deployment_url = environment.get('deployment')
        deployment = {
            'status': 'Dispatched',
            'detail': 'successfully dispatched'
        }

        response = requests.patch(deployment_url,data=deployment)
        response.raise_for_status()
    except Exception as e:
        logger.error(
            "Worker '%s' not available, so enviroment '%s' not dispatched",
            worker.get('address'),
            environment.get('id')
        )
        # Resport to api serve that the deployemnt 
        # was dispatched
        deployment_url = environment.get('deployment')
        deployment = {
            'status': 'Failed',
            'detail': "Worker '%s' not available, so enviroment not dispatched" % (
                worker.get('address')
            )
        }

        logger.exception(e)

        response = requests.patch(deployment_url,data=deployment)
        response.raise_for_status()

def send_action_data(action):
    
    # Get environment
    environment_url = action.get('environment')
    response = requests.get(environment_url)
    response.raise_for_status()
    environment = response.json()

    # Get worker
    worker_url = environment.get('worker')
    response = requests.get(worker_url)
    response.raise_for_status()
    worker = response.json()

    # Get worker API URL
    url = API_WORKER_URL_FORMAT.format(
        address=worker.get('address'),
        endpoint='actions'

    )

    try:
        data = {
            'action_id': action.get('id'),
            'environment_id': environment.get('id'),
            'provider': environment.get('provider'),
            'action': action.get('action')
        }

        # Send enviroment data to worker (flask receives data when json is used)
        response = requests.post(url,json=data)
        response.raise_for_status()

        # Resport to api serve that the deployemnt 
        # was dispatched
        action_url = action.get('url')
        action = {
            'status': 'Dispatched',
            'detail': 'successfully dispatched'
        }

        response = requests.patch(action_url,data=action)
        response.raise_for_status()
    except Exception as e:
        logger.error(
            "Worker '%s' not available, so action '%s' not dispatched",
            worker.get('address'),
            action.get('id')
        )
        # Resport to api serve that the deployemnt 
        # was dispatched
        action_url = action.get('url')
        action = {
            'status': 'Failed',
            'detail': "Worker '%s' not available, so action not dispatched" % (
                worker.get('address')
            )
        }

        logger.exception(e)

        response = requests.patch(action_url,data=action)
        response.raise_for_status()

def dispatch():
    logger.info("Dispactchig ...")

    try:
        environments = get_scheduled_environments()
        for environment in environments:

            try:
                send_environment_data(environment)
            except requests.exceptions.ConnectionError as e:
                logger.exception(e)
            except Exception as e:
                logger.exception(e)

        actions = get_scheduled_actions()
        for action in actions:

            try:
                send_action_data(action)
            except requests.exceptions.ConnectionError as e:
                logger.exception(e)
            except Exception as e:
                logger.exception(e)

    except Exception as e:
        logger.warning("API SERVER no available on '%s'",API_SERVER_BASE_URL)
        logger.exception(e)

    logger.info("End dispatch...")


if __name__ == '__main__':
    logger.info("Dispatcher started !!")
    while True: 
        time.sleep(SLEEP_SECONDS)
        dispatch()
