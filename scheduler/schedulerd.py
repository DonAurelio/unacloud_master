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
API_BASE_URL = 'http://localhost:8081/api'

# Wait time for next iteration (seconds)
SLEEP_SECONDS = 5


def get_available_workers():
    endpoint = '/worker/workers/'
    url = API_BASE_URL + endpoint
    workers = None

    logger.info("Getting available workers from '%s'" % url)
    response = requests.get(url)

    # Check if something when wrong
    response.raise_for_status()

    workers = response.json()
    logger.info("Number of available workers retrieved '%s'" % len(workers))

    return workers


def get_peding_environments():
    endpoint = '/environment/environments/'
    query = '?deployment__status=Pending'
    url = API_BASE_URL + endpoint + query

    environments = None

    logger.info("Getting pending environments from '%s'" % url)
    response = requests.get(url)

    # Check if something when wrong
    response.raise_for_status()
    
    environments = response.json()
    logger.info(
        "Number of pending environments retrieved '%s'" % len(environments)
    )

    return environments


def fits_environment_into_worker(environment,worker):
    required_cpus = environment.get('cpus')
    required_memory = environment.get('memory')

    available_cpus = worker.get('cpus')
    available_memory = worker.get('memory')

    fits_cpu = required_cpus < available_cpus
    fits_memory = required_memory < available_memory

    return fits_cpu and fits_memory


def get_first_fit(environment,workers):

    # sort by cpu capacity, more cpus avaiable first
    workers = sorted(
        workers, key=lambda k: k['available_cpus'], reverse=True
    )

    index = 0 
    selected_worker = None
    while index < len(workers):
        current_worker = workers[index]
        condition = fits_environment_into_worker(
            environment,current_worker
        )

        if condition:
            selected_worker = current_worker
            index = len(workers)
        else:
            index += 1

    return selected_worker


def report_scheduling_decision(environment,worker):

    if worker is None:
        logger.warning(
            "No nodes available for environment (id='%s',name='%s')",
            environment.get('id'),environment.get('name')
        )
        # Change deployment status to scheduled
        url = environment.get('deployment')

        data = {
            'status': 'Pending',
            'details': 'No nodes aviable for this environment !!'
        }
        response = requests.patch(url,data=data)

        response.raise_for_status()   

    else:
        # Assinng worker to environment
        url = environment.get('url')

        data = {
            'worker': worker.get('url')
        }
        response = requests.patch(url,data=data)

        response.raise_for_status()

        # Change deployment status to scheduled
        url = environment.get('deployment')

        data = {
            'status': 'Scheduled'
        }
        response = requests.patch(url,data=data)

        response.raise_for_status()

        logger.info(
            "Environment (id='%s',name='%s') was assigned to node '%s'",
            environment.get('id'),environment.get('name'),worker.get('id')
        )


def schedule():
    logger.info("Scheduling...")
    environments = get_peding_environments()
    for environment in environments:
        try: 
            workers = get_available_workers()
            worker = get_first_fit(environment,workers)
            report_scheduling_decision(environment,worker)
        except requests.exceptions.ConnectionError as e:
            logger.exception(e)
        except Exception as e:
            logger.exception(e)


    logger.info("End scheduling...")


if __name__ == '__main__':
    logger.info("Scheduler started !!")
    while True:
        time.sleep(SLEEP_SECONDS)
        schedule()
