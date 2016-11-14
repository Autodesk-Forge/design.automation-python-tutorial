import requests #http://requests.readthedocs.org/en/latest/
import argparse

def getToken(consumerKey, consumerSecret):
    """Obtain Apiggee token given a consumer key/secret"""
    req = { 'client_id' : consumerKey, 'client_secret': consumerSecret, 'grant_type' : 'client_credentials','scope':'code:all'}
    resp = requests.post('https://developer.api.autodesk.com/authentication/v1/authenticate', req).json();
    return resp['token_type'] + " " + resp['access_token']

def printReport(args):
    """Download and print the AutoCAD.IO report for a given workitem"""
    token = getToken(args.consumerKey, args.consumerSecret)
    target = 'https://developer.api.autodesk.com/autocad.io/us-east/v2/'
    resp = requests.get("{0}/WorkItems('{1}')".format(target, args.workItem), headers={'Authorization': token}).json();
    resp = requests.get(resp['StatusDetails']['Report']);
    print(resp.text)

#TODO: add support for other operations (submit workitem, query activities etc.)
parser = argparse.ArgumentParser(description='Get error report from AutoCAD.IO for a work item.')
parser.add_argument('--consumerKey', required=True);
parser.add_argument('--consumerSecret', required=True);
parser.add_argument('--workItem', required=True);

args = parser.parse_args()

#For now, the only supported operation is printing the report of a workitem.
printReport(args)
