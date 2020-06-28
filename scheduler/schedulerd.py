# -*- encoding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s : %(name)s : %(levelname)s : %(message)s')
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)


class Schedulerd(object):
    """docstring for Deployd"""

    def __init__(self,api_base_url):
        self._base_url = api_base_url


    def _get_available_nodes(self):

        url = self._base_url + '/workernodes/'
        nodes = None

        logger.info("Getting available nodes from '%s'" % url)
        response = requests.get(url)

        # Check if something when wrong
        response.raise_for_status()

        nodes = response.json()
        logger.info("Number of available nodes retrieved '%s'" % len(nodes))

        return nodes

    def _get_peding_deployments(self):
        url = self._base_url + '/executionenvironments/?status=Pending' 
        deployments = None

        logger.info("Getting pending deployments from '%s'" % url)
        response = requests.get(url)

        # Check if something when wrong
        response.raise_for_status()
        
        deployments = response.json()
        logger.info(
            "Number of pending deployments retrieved '%s'" % len(deployments)
        )

        return deployments

    def _fit_deployment_into_node(self,deployment,node):
        required_cpus = deployment.get('cpus')
        required_memory = deployment.get('memory')

        available_cpus = node.get('cpus')
        available_memory = node.get('memory')

        fits_cpu = required_cpus < available_cpus
        fits_memory = required_memory < available_memory

        return =  fits_cpu and fits_memory

    def _asign_node_to_deployment(self,node,deployment):

    def _schedule_pending_deployment(self,deployment,nodes):

        # sort by cpu capacity, more cpus avaiable first
        sorted_nodes = sorted(
            data, key=lambda k: k['available_cpus'], reverse=True
        )

        for node in sorted_nodes:
            if self._fit_deployment_into_node(deployment,node):


    def schedule_pending_desployments(self):
        deployments = self._get_peding_deployments()
        for deployment in deployments:
            nodes = self._get_available_nodes()
            self._schedule_pending_deployment(deployment,nodes)


    def run(self):
        self._deploy_manifests()