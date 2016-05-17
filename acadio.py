#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests #http://requests.readthedocs.org/en/latest/
from Credentials import Credentials

ApiCredentials = None

_authEntryPoint = 'https://developer.api.autodesk.com/authentication/v1/authenticate'
_apiEntryPoint = 'https://developer.api.autodesk.com/autocad.io/us-east/v2/'

class Unauthorized(ValueError):
    pass
class NotFound(ValueError):
    pass

def getToken():
    """Obtain Apiggee token given a consumer key/secret"""
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
    return resp['token_type'] + " " + resp['access_token']

def printReport(args):
    """Download and print the AutoCAD.IO report for a given workitem"""
    token = getToken()
    resp = requests.get("{0}/WorkItems('{1}')".format(
        _apiEntryPoint, args.workItem),
        headers={'Authorization': token}
    )
    if resp.status_code == 404:
        raise NotFound(u"WorkItem '{0}' does not exist".format(args.workItem))
    resp = resp.json()
    resp = requests.get(resp['StatusDetails']['Report']);
    print(resp.text)

#TODO: add support for other operations (submit workitem, query activities etc.)
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Get error report from AutoCAD.IO for a work item.')
    parser.add_argument('--consumerKey', required=True);
    parser.add_argument('--consumerSecret', required=True);
    parser.add_argument('--workItem', required=True);
    
    args = parser.parse_args()
    
    ApiCredentials = Credentials(
        clientId = args.consumerKey,
        clientSecret = args.consumerSecret
    )
    
    #For now, the only supported operation is printing the report of a workitem.
    printReport(args)