# -*- encoding: utf-8 -*-

import logging
import requests
import time

logger = logging.getLogger(__name__)
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
API_WORKER_URL_FORMAT = 'http://{address}:8082'

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


def send_environment_data(environment):
    
    # Get worker
    worker_url = environment.get('worker')
    response = requests.get(worker_url)
    response.raise_for_status()
    worker = response.json()

    # Get worker API URL
    url = API_WORKER_URL_FORMAT.format(
        address=worker.get('address')
    )

    try:

        # Send enviroment data to worker
        response = requests.post(url,data=environment)
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

        response = requests.patch(deployment_url,data=deployment)
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

    except Exception as e:
        logger.warning("API SERVER no available on '%s'",API_SERVER_BASE_URL)

    logger.info("End dispatch...")


if __name__ == '__main__':
    logger.info("Dispatcher started !!")
    while True: 
        time.sleep(SLEEP_SECONDS)
        dispatch()
