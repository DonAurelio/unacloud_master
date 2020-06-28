# -*- encoding: utf-8 -*-

import logging
import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s : %(name)s : %(levelname)s : %(message)s')
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)


API_BASE_URL = 'localhost:8081'


def get_available_workers():
    endpoint = '/worker/workers/'
    url = API_BASE_URL + endpoint
    nodes = None

    logger.info("Getting available nodes from '%s'" % url)
    response = requests.get(url)

    # Check if something when wrong
    response.raise_for_status()

    nodes = response.json()
    logger.info("Number of available nodes retrieved '%s'" % len(nodes))

    return nodes


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


def get_report_scheduling_decision(environment,worker):
    # Change execution environment and deployemnt to scheduled
    # write some info
    pass
