#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests #http://requests.readthedocs.org/en/latest/
import datetime
import json

from Credentials import Credentials

ApiCredentials = None

_authEntryPoint = 'https://developer.api.autodesk.com/authentication/v1/authenticate'
_apiEntryPoint = 'https://developer.api.autodesk.com/autocad.io/us-east/v2/'

_token = {'token': None, 'expires': None}

class Unauthorized(ValueError):
    pass
class NotFound(ValueError):
    pass
class ServerError(ValueError):
    pass

def getToken():
    """Obtain Apiggee token given a consumer key/secret 
    reusing a previously gotten one while still valid"""
    if _token['token'] is None or \
            _token['expires'] is None or \
            datetime.datetime.utcnow() >= _token['expires']:
        req = {
            'client_id' : ApiCredentials.clientId,
            'client_secret': ApiCredentials.clientSecret,
            'grant_type' : 'client_credentials',
        }
        resp = requests.post(_authEntryPoint, req).json();
        if resp.has_key('errorCode'):
            raise Unauthorized(
                resp['errorCode'],
                resp.get('developerMessage', u'Wrong ApiCredentials'),
                resp.get('more info', '')
            )
        _token['expires'] = \
            datetime.datetime.utcnow() + datetime.timedelta(seconds = (resp['expires_in'] * 2)/3)
        _token['token'] = resp['token_type'] + " " + resp['access_token']
    return _token['token']
    
def _authorizedGet(url):
    return requests.get(url, headers = {'Authorization': getToken()})
def _authorizedPost(url, payload):
    headers = {
        'Authorization': getToken(),
    # POST as application/x-www-form-urlencoded doesn't seem to be working
        'Content-Type': 'application/json'
    }
    return requests.post(url, data = json.dumps(payload), headers = headers)

def getWorkItem(workItemId):
    """Get WorkItem"""
    token = getToken()
    resp = _authorizedGet("{0}/WorkItems('{1}')".format(
        _apiEntryPoint, workItemId)
    )
    if resp.status_code == 404:
        raise NotFound(u"WorkItem '{0}' does not exist".format(workItemId))
    resp = resp.json()
    return resp

def printReport(workItemId):
    """Download and print the AutoCAD.IO report for a given workitem"""
    resp = getWorkItem(workItemId)
    url = resp['StatusDetails']['Report']
    if url is None:
        print("WorkItem('{0}') is: {1}".format(workItemId, resp['Status']))
    else:
        resp = requests.get(url)
        print(resp.text)

def submitWorkItem(ActivityId = "PlotToPDF",
        InputArguments = None,
        OutputArguments = None):
    """"Create a WorkItem based on given arguments.
    Returns the Id of the newly created WorkItem.
    Defaults create the WorkItem described in the API docs:
    https://developer.autodesk.com/api/autocadio/#to-create-a-workitem"""
    if InputArguments is None:
        InputArguments = [{
            "Resource":"https://s3.amazonaws.com/AutoCAD-Core-Engine-Services/TestDwg/makeall.dwg",
            "Name":"HostDwg","StorageProvider":"Generic"
        }]
    if OutputArguments is None:
        OutputArguments = [{
            "Name":"Result","StorageProvider":"Generic","HttpVerb":"POST"
        }]
    req = {
      "@odata.type":"#ACES.Models.WorkItem","Arguments":{
           "InputArguments": InputArguments,
           "OutputArguments": OutputArguments,
       },"ActivityId": ActivityId, "Id":""
    }
    resp = _authorizedPost('{0}WorkItems'.format(_apiEntryPoint), req)
    if resp.status_code == 401:
        raise Unauthorized('Unauthorized to create a WorkItem')
    if resp.status_code == 500:
        print resp.json()
        print resp.json()['error']['innererror']['stacktrace']
        raise ServerError('Remote server error')
    resp = resp.json()
    return resp['Id']

#TODO: add support for other operations (query activities etc.)
if __name__ == '__main__':
    import argparse, time
    parser = argparse.ArgumentParser(description='Get error report from AutoCAD.IO for a work item.')
    parser.add_argument('--clientId', required=True);
    parser.add_argument('--clientSecret', required=True);
    
    args = parser.parse_args()
    
    ApiCredentials = Credentials(
        clientId = args.clientId,
        clientSecret = args.clientSecret
    )
    
    # Create a default WorkItem
    workItemId = submitWorkItem()
    print("Created WorkItem('{0}')".format(workItemId))
    # Wait until WorkItem is done
    while True:
        workItem = getWorkItem(workItemId)
        if workItem['Status'] not in ['Pending', 'InProgress']:
            break
        else:
            print("WorkItem is {0}".format(workItem['Status']))
        time.sleep(2)
    # Print the report of that WorkItem
    printReport(workItemId)
    workItem = getWorkItem(workItemId)
    print('OutputArguments')
    print(workItem['Arguments']['OutputArguments'])
    