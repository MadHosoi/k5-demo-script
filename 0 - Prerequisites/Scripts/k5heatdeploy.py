#!/usr/bin/python


import sys
import json
import pprint
import datetime
import time
import random
import string
import copy
from multiprocessing import Process, Queue
import requests
import getopt

from k5contractsettings import *
from time import sleep

proxies = {
       'http': 'http://10.142.74.132:82',
       'https': 'http://10.142.74.132:82'
    }

def get_scoped_token(adminUser, adminPassword, contract, projectid, region):
    """Ket a K5 project scoped token

    Args:
        adminUser (TYPE): k5 username
        adminPassword (TYPE): K5 password
        contract (TYPE): K5 contract name
        projectid (TYPE): K5 project id to scope to
        region (TYPE): K5 region

    Returns:
        TYPE: K5 token object
    """
    identityURL = 'https://identity.' + region + \
        '.cloud.global.fujitsu.com/v3/auth/tokens'

    try:
        response = requests.post(
            identityURL, 
            headers={'Content-Type': 'application/json','Accept':'application/json'}, 
            json={"auth":{"identity":{"methods":["password"],"password":{"user":{"domain":{"name": contract }, "name": adminUser, "password": adminPassword}}}, "scope": { "project": {"id": projectid}}}}, 
            proxies=proxies)
        token = response.headers['X-Subject-Token']
        print token

        response = requests.post(identityURL,
                                 headers={'Content-Type': 'application/json',
                                          'Accept': 'application/json'},
                                 json={"auth":
                                         {"identity":
                                          {"methods": ["password"], "password":
                                           {"user":
                                           {"domain":
                                               {"name": contract},
                                            "name": adminUser,
                                            "password": adminPassword
                                            }}},
                                          "scope":
                                          {"project":
                                           {"id": projectid
                                            }}}})

        return response
    except:
        return 'Regional Project Token Scoping Failure'

def get_endpoint(k5token, endpoint_type):
    """Extract the appropriate endpoint URL from the K5 token object body
    Args:
        k5token (TYPE): K5 token object
        endpoint_type (TYPE): trype of endpoint required - e.g. compute, network...

    Returns:
        TYPE: string - contain the endpoint url
    """
    # list the endpoints
    
    for ep in k5token.json()['token']['catalog']:
        if len(ep['endpoints'])>0:
            # if this is the endpoint that  I'm looking for return the url
            if endpoint_type == ep['endpoints'][0].get('name'):
                return ep['endpoints'][0].get('url')

def deploy_heat_stack(k5token, stack_name, stack_to_deploy, stack_parameters):
    """Summary


    Returns:
        TYPE: Description
    """
    orchestrationURL = unicode(get_endpoint(k5token, "orchestration")) + unicode("/stacks")
    print(orchestrationURL)
    token = k5token.headers['X-Subject-Token']
    try:
        response = requests.post(orchestrationURL,
                                 headers={
                                     'X-Auth-Token': token, 'Content-Type': 'application/json', 'Accept': 'application/json'},
                                 json={
                                        "files": {},
                                        "disable_rollback": True,
                                        "parameters": stack_parameters,
                                        "stack_name": stack_name,
                                        "template": stack_to_deploy,
                                        "timeout_mins": 60
                                        },
                                 proxies=proxies)
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())

def get_stack_details(k5token, stackName, stackId):
    """Summary


    Returns:
        TYPE: Description
    """
    orchestrationURL = unicode(get_endpoint(k5token, "orchestration")) + unicode("/stacks/")+ unicode(stackName)+ unicode("/")+ unicode(stackId)+ unicode("?resolve_outputs=True")
    print(orchestrationURL)
    token = k5token.headers['X-Subject-Token']
    try:
        response = requests.get(orchestrationURL,
                                 headers={
                                     'X-Auth-Token': token, 
                                     'Content-Type': 'application/json', 
                                     'Accept': 'application/json'},
                                 proxies=proxies)
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())

def list_heat_stacks(k5token):
    """Summary


    Returns:
        TYPE: Description
    """
    orchestrationURL = unicode(get_endpoint(k5token, "orchestration")) + unicode("/stacks")
    print(orchestrationURL)
    token = k5token.headers['X-Subject-Token']
    try:
        response = requests.get(orchestrationURL,
                                 headers={
                                     'X-Auth-Token': token, 
                                     'Content-Type': 'application/json', 
                                     'Accept': 'application/json'},
                                 proxies=proxies)
        return response
    except:
        return ("\nUnexpected error:", sys.exc_info())

def main(argv):
    """Summary

    Returns:
        TYPE: Description
    """
        
    inputfile = ''
    heatname = ''
    try:
        opts, args = getopt.getopt(argv,"hi:n:",["inputfile=","heatname="])
    except getopt.GetoptError:
        print('k5heatdeploy.py -i <inputfile> -n <heatname>')
        sys.exit(2)
    if not opts:
        print('k5heatdeploy.py -i <inputfile> -n <heatname>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('k5heatdeploy.py -i <inputfile> -n <heatname>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-n", "--heatname"):
            container = arg

    print "Authorizing.."
    k5token = get_scoped_token(adminUser, adminPassword, contract, demoProjectA, region)

    print(k5token)
    print "Authorized."
    
    stack_to_deploy = open(inputfile, 'r').read()

    stackName = heatname
    deployresult = deploy_heat_stack(k5token, stackName, stack_to_deploy, "").json()
    print(deployresult)

    stack = deployresult['stack']
    stackId = stack.get('id')
    deployedStacksOnline = False
    deployedStackFailure = False 

    while not deployedStacksOnline:
    	deployedStacksOnline = True
    	for newStack in list_heat_stacks(k5token).json()['stacks']:
    		print("Stack ID & Status > ", newStack.get('stack_name'), newStack.get('stack_status'), "\n")
    		if ('FAIL' or 'ERROR') in newStack.get('stack_status'):
    			deployedStackFailure = True
    		if 'PROGRESS' in newStack.get('stack_status'):
    			deployedStacksOnline = False
    	sleep(5)

    details = get_stack_details(k5token, stackName, stackId).json()

    # print details
    
    # Print Error Warnings
    if deployedStackFailure:
    	print("WARNING: There was a stack deployment failure\n" + details['stack'].get('stack_status_reason') + "\n")
        

    # Deployment Complete
    print("Deployment Complete\n")
    
if __name__ == "__main__":
   main(sys.argv[1:])