#####################################################################
## Copyright (c) Autodesk, Inc. All rights reserved
## Written by Forge Partner Development
##
## Permission to use, copy, modify, and distribute this software in
## object code form for any purpose and without fee is hereby granted,
## provided that the above copyright notice appears in all copies and
## that both that copyright notice and the limited warranty and
## restricted rights notice below appear in all supporting
## documentation.
##
## AUTODESK PROVIDES THIS PROGRAM "AS IS" AND WITH ALL FAULTS.
## AUTODESK SPECIFICALLY DISCLAIMS ANY IMPLIED WARRANTY OF
## MERCHANTABILITY OR FITNESS FOR A PARTICULAR USE.  AUTODESK, INC.
## DOES NOT WARRANT THAT THE OPERATION OF THE PROGRAM WILL BE
## UNINTERRUPTED OR ERROR FREE.
#####################################################################

import os
import sys
import requests  
import argparse
import re
import json
import base64
import datetime 
from pathlib import Path
import six 
import urllib
import hashlib, hmac 
import boto3 

config = __import__('config')
utility = __import__('utility') 


Forge_CLIENT_ID = config.Forge_CLIENT_ID
Forge_CLIENT_SECRET = config.Forge_CLIENT_SECRET
Forge_BASE_URL = config.Forge_BASE_URL
DA_BASE_URL = config.DA_BASE_URL
APP_BUNDDLE_URL = config.APP_BUNDDLE_URL
 
def getToken():
    """Obtain Forge token given a client id & secret"""
    req = { 'client_id' : Forge_CLIENT_ID, 'client_secret': Forge_CLIENT_SECRET, 'grant_type' : 'client_credentials','scope':'code:all bucket:create bucket:read data:read data:write'}
    resp = requests.post(Forge_BASE_URL+'/authentication/v1/authenticate', req)
    if resp.status_code == 200:
        config.token = resp.json()['token_type'] + " " + resp.json()['access_token']
        return config.token
    else:
        print('Get Token Failed! status = {0} ; message = {1}'.format(resp.status_code,resp.text) )
        return None

def getNickName():
    resp = requests.get(Forge_BASE_URL+DA_BASE_URL+'/forgeapps/me', headers={'Authorization': config.token})
    if resp.status_code == 200:
        return resp.json()
    else:
        print('Get Nick Name of Design Automation Failed! status = {0} ; message = {1}'.format(resp.status_code,resp.text ) )
        return None

def deleteNickName(name):
    resp = requests.delete(Forge_BASE_URL+DA_BASE_URL+'/forgeapps/me', headers={'Authorization': config.token})
    if resp.status_code == 200:
        return resp.text
    else:
        print('Delete Nick Name of Design Automation Failed! status = {0} ; message = {1}'.format(resp.status_code,resp.text ) )
        return None

def setNickName(name):
    resp = requests.patch(Forge_BASE_URL+DA_BASE_URL+'/forgeapps/me', headers={'Authorization': config.token},json={"nickname": name})
    if resp.status_code == 200:
        return resp.text
    else:
        print('Set Nick Name of Design Automation Failed! status = {0} ; message = {1}'.format(resp.status_code,resp.text ) )
        return None

def dumpEngines():
    #now /engines endpoint returns engines in pages, so dump all engines page by page
    pageToken = None
    resp = requests.get(Forge_BASE_URL+DA_BASE_URL+'/engines', headers={'Authorization': config.token})
    
    if(resp.status_code==200):
        engines = resp.json()['data'] 
        while(resp.json()['paginationToken']!=''): 
            pageToken = resp.json()['paginationToken']
            engines.extend(resp.json()['data'])
            resp = requests.get(Forge_BASE_URL+DA_BASE_URL+'/engines?page='+str(pageToken), headers={'Authorization': config.token})
            if(resp.status_code!=200):
                print('Get Engines of Design Automation Failed in one page! status ={0} ; message = {1}'.format(resp.status_code,resp.text ) )
                return engines 
        return engines
    else:
        print('Get Engines of Design Automation Failed! status ={0} ; message = {1}'.format(resp.status_code,resp.text ) )
        return None

def getEngineAttributes(engine):
    data = {}
    if re.search('3dsMax', engine, re.IGNORECASE):
        data['commandLine'] = "$(engine.path)\\3dsmaxbatch.exe -sceneFile \"$(args[inputFile].path)\" \"$(settings[script].path)\""
        data['extension'] = "max"
        data['script'] = "da = dotNetClass(\"Autodesk.Forge.Sample.DesignAutomation.Max.RuntimeExecute\")\nda.ModifyWindowWidthHeight()\n"
    if re.search('AutoCAD', engine, re.IGNORECASE):
        data['commandLine'] = "$(engine.path)\\accoreconsole.exe /i \"$(args[inputFile].path)\" /al \"$(appbundles[{0}].path)\" /s \"$(settings[script].path)\""
        data['extension'] = "dwg"
        data['script'] = "UpdateParam\n" 
    if re.search('Inventor', engine, re.IGNORECASE):
        data['commandLine'] = "$(engine.path)\\InventorCoreConsole.exe /i \"$(args[inputFile].path)\" /al \"$(appbundles[{0}].path)\""
        data['extension'] = "ipt"
        data['script'] = ""  
    if re.search('Revit', engine, re.IGNORECASE):
        data['commandLine'] =  "$(engine.path)\\revitcoreconsole.exe /i \"$(args[inputFile].path)\" /al \"$(appbundles[{0}].path)\""
        data['extension'] = "rvt"
        data['script'] = ""    
    return data 

def getDefinedAppbundles():
    resp = requests.get(Forge_BASE_URL+DA_BASE_URL+'/appbundles', headers={'Authorization': config.token})
    if resp.status_code == 200:
        return resp.json()['data']  
    else:
        print('Get Appbundles of Design Automation Failed! status ={0} ; message = {1}'.format(resp.status_code,resp.text ) )
        return None

#####
#   Define a new appbundle
####
def createAppBundle(enginename,appname): 
    #engineAttributes = getEngineAttributes(enginename)
    #commandLine = engineAttributes['commandLine'].format(appname) 
    appBundleSpec = {}
    appBundleSpec['id'] = appname
    appBundleSpec['engine'] = enginename
    appBundleSpec['description'] = 'Description for {0}'.format(appname)

    resp = requests.post(Forge_BASE_URL+DA_BASE_URL+'/appbundles', headers={'Authorization': config.token},json=appBundleSpec)
    if resp.status_code == 200:
        return resp.json()
    else:
        print('Create AppBundle of Design Automation Failed! status ={0} ; message = {1}'.format(resp.status_code,resp.text ) )
        return None

#####
#   create a new appbundle version
####
def createAppBundleVersion(enginename,appname): 
    #engineAttributes = getEngineAttributes(enginename)
    #commandLine = engineAttributes['commandLine'].format(appname) 
    appBundleSpec = {}
    appBundleSpec['engine'] = enginename
    appBundleSpec['description'] = 'Description for {0}'.format(appname)

    resp = requests.post(Forge_BASE_URL+DA_BASE_URL+'/appbundles/'+appname+'/versions', headers={'Authorization': config.token},json=appBundleSpec)
    if resp.status_code == 200:
        return resp.json()
    else:
        print('Create AppBundle of Design Automation Failed! status ={0} ; message = {1}'.format(resp.status_code,resp.text ) )
        return None

####
# Create appbundle alias
###
def createAppBundleAlias(appname,alias,version):
    aliasSpec ={'version':version,'id':alias}
    resp = requests.post(Forge_BASE_URL+DA_BASE_URL+'/appbundles/'+appname+'/aliases', headers={'Authorization': config.token},json=aliasSpec)
    if resp.status_code == 200:
        return resp.json() 
    else:
        print('Create AppBundle Alias of Design Automation Failed! status ={0} ; message = {1}'.format(resp.status_code,resp.text ) )
        return None

####
# Update appbundle alias
###
def updateAppBundleAlias(appname,alias,version):
    aliasSpec ={'version':version}
    resp = requests.patch(Forge_BASE_URL+DA_BASE_URL+'/appbundles/'+appname+'/aliases/'+alias, headers={'Authorization': config.token},json=aliasSpec)
    if resp.status_code == 200:
        return resp.json() 
    else:
        print('Create AppBundle Alias of Design Automation Failed! status ={0} ; message = {1}'.format(resp.status_code,resp.text ) )
        return None

def uploadZip(appPackagePath,appname,zipname,appFormData):
    my_file = Path(appPackagePath + zipname)
    #the package file (*.zip) exists
    if my_file.is_file():
        if sys.version_info[0] < 3:
            payload = appFormData
            files = {'file': open(appPackagePath + zipname,'rb')}
            resp = requests.post(APP_BUNDDLE_URL,files=files, data=payload)
        else:
            appFormData['file'] = (zipname,open(appPackagePath + zipname,'rb')) 
            resp = requests.post(APP_BUNDDLE_URL,files=appFormData) 

        if resp.status_code == 200:
            return resp.text
        else:
            print('UploadZip of Design Automation Failed! status ={0} ; message = {1}'.format(resp.status_code,resp.text ) )
            return None
    else:
        print(' ' + zipname + ' does not exist')
        return None
 

def getDefinedActivities():
    resp = requests.get(Forge_BASE_URL+DA_BASE_URL+'/activities', headers={'Authorization': config.token})
    if resp.status_code == 200:
        return resp.json()['data']  
    else:
        print('Get Activities of Design Automation = {0} ; message = {1}'.format(resp.status_code,resp.text ) )
        return None

#####
#   Define a new activity
####
def createActivity(enginename,appname,qualifiedAppBundleId,actname): 
    engineAttributes = getEngineAttributes(enginename)
    commandLine = engineAttributes['commandLine'].format(appname) 
    activitySpec = {}
    activitySpec['id'] = actname
    activitySpec['engine'] = enginename
    activitySpec['commandLine'] = [commandLine]
    activitySpec['appbundles'] = [qualifiedAppBundleId]
    activitySpec['description'] = 'Description for {0}'.format(actname) 
      
    activitySpec['Parameters'] = {}
    activitySpec['Parameters']["inputFile"] = {"verb":"get","description":"","localName":"$(inputFile)","zip":False,"ondemand":False} 
    activitySpec['Parameters']["inputJson"] = {"verb":"get","description":"","localName":"params.json","zip":False,"ondemand":False} 
    activitySpec['Parameters']["outputFile"] = {"verb":"put","description":"","localName":"outputFile." + engineAttributes["extension"],"zip":False,"ondemand":False,"required":True} 

    activitySpec['Settings'] ={}
    activitySpec['Settings']["script"] ={"Value":engineAttributes["script"]}


    resp = requests.post(Forge_BASE_URL+DA_BASE_URL+'/activities', headers={'Authorization': config.token},json=activitySpec)
    if resp.status_code == 200:
        return resp.json() 
    else:
        print('Create Activity of Design Automation Failed! status ={0} ; message = {1}'.format(resp.status_code,resp.text ) )
        return None

####
# Create activity alias
###
def createActivityAlias(actname,alias):
    aliasSpec ={'version':1,'id':alias}
    resp = requests.post(Forge_BASE_URL+DA_BASE_URL+'/activities/'+actname+'/aliases', headers={'Authorization': config.token},json=aliasSpec)
    if resp.status_code == 200:
        return resp.json() 
    else:
        print('Create Activity Alias of Design Automation Failed! status ={0} ; message = {1}'.format(resp.status_code,resp.text ) )
        return None

####
# Create Bucket
###
def createBucket(bucketname):
    payload = {'bucketKey' : bucketname,'policyKey' : 'transient'}
    resp = requests.post(Forge_BASE_URL+'/oss/v2/buckets', headers={'Authorization': config.token,'Content-Type':'application/json'},json=payload)
    if resp.status_code == 200 or resp.status_code == 409:
        return resp.json() 
    else:
        print('Create Bucket of Data Management Failed! status ={0} ; message = {1}'.format(resp.status_code,resp.text ) )
        return None

####
# Upload Source File to Bucket
###
def uploadFileToBucket(modelfilePath,bucketname,filename):
    my_file = Path(modelfilePath + filename)
    #check package file (*.zip) exists
    if my_file.is_file():
        filesize = os.path.getsize( modelfilePath + filename )
        # encoding the file name
        if sys.version_info[0] < 3:
            encodedfilename= urllib.pathname2url(filename)
        else:
            encodedfilename= urllib.parse.quote(filename) 
        resp = requests.put(Forge_BASE_URL+'/oss/v2/buckets/'+bucketname+'/objects/'+encodedfilename, headers={'Authorization': config.token,'Content-Type' : 'application/octet-stream','Content-Length' : str(filesize)},data= open(modelfilePath + filename, 'rb'))
        if resp.status_code == 200:
            return resp.json()
        else:
            print('Upload File to Bucket of Data Management Failed! status ={0} ; message = {1}'.format(resp.status_code,resp.text ) )
            return None
    else:
        print(' ' + filename + ' does not exist')
        return None

####
# Create WorkItem
###
def createWorkItem(qualifiedActivityId,param):
    workItemSpec = {}
    workItemSpec['activityId'] = qualifiedActivityId
    workItemSpec['arguments'] = {}

    inputFileArgument = {}
    inputFileArgument['url'] = "https://developer.api.autodesk.com/oss/v2/buckets/{0}/objects/{1}".format(param['bucketKey'],param['inputFileNameOSS'])
    inputFileArgument['headers'] = {}
    inputFileArgument['headers']['Authorization'] = config.token
    
    inputJsonArgument = {}
    inputJsonArgument['url'] = 'data:application/json,'+ str(param['jsonInput'])

    dateStr = str(datetime.datetime.now())
    dateStr = dateStr.replace(':','.') ### : is not accepted as file name
    outputFileNameOSS = '{0}_output_{1}'.format(dateStr,param['inputFileNameOSS'])
    ossOutputUrl = "https://developer.api.autodesk.com/oss/v2/buckets/{0}/objects/{1}".format(param['bucketKey'],outputFileNameOSS)
    outputFileArgument = {}
    outputFileArgument['url'] = ossOutputUrl
    outputFileArgument['headers'] = {} 
    outputFileArgument['headers']['Authorization'] = config.token
    outputFileArgument['verb'] = 'put'

    workItemSpec['arguments']['inputFile'] = inputFileArgument
    workItemSpec['arguments']['inputJson'] = inputJsonArgument
    workItemSpec['arguments']['outputFile'] = outputFileArgument

    resp = requests.post(Forge_BASE_URL+DA_BASE_URL+'/workitems', headers={'Authorization': config.token},json=workItemSpec)
    if resp.status_code == 200:
        copyResJson = resp.json()
        #for download the output file. append two elements of json
        copyResJson['outputFileNameOSS'] = outputFileNameOSS 
        copyResJson['ossOutputUrl'] = ossOutputUrl
        return copyResJson
    else:
        print('Create WorkItem of Design Automation Failed! status ={0} ; message = {1}'.format(resp.status_code,resp.text ) )
        return None

def getWorkItemStatus(wid):
    resp = requests.get(Forge_BASE_URL+DA_BASE_URL+'/workitems/'+wid , headers={'Authorization': config.token})
    if resp.status_code == 200:
        return resp.json() 
    else:
        print('Get WorkItem Status of Design Automation = {0} ; message = {1}'.format(resp.status_code,resp.text ) )
        return None


##other user scenarios ###

## output to personal AWS bucket
def createWorkItem_outputPersonalAWSBucket(qualifiedActivityId,inputparam):

    #prepare input parameters of Forge DA
    workItemSpec = {}
    workItemSpec['activityId'] = qualifiedActivityId
    workItemSpec['arguments'] = {}

    inputFileArgument = {}
    inputFileArgument['url'] = "https://developer.api.autodesk.com/oss/v2/buckets/{0}/objects/{1}".format(inputparam['bucketKey'],inputparam['inputFileNameOSS'])
    inputFileArgument['headers'] = {}
    inputFileArgument['headers']['Authorization'] = config.token
    
    inputJsonArgument = {}
    inputJsonArgument['url'] = 'data:application/json,'+ str(inputparam['jsonInput'])

    #prepare output parameters of Forge DA (for personal AWS bucket)
    dateStr = str(datetime.datetime.now())
    dateStr = dateStr.replace(':','.') ### : is not accepted as file name
    outputFileNameOSS = '{0}_output_{1}'.format(dateStr,inputparam['inputFileNameOSS']) 

    #Begin: generate AWS credentials

    #check key, secret, token.. 
    if config.Personal_AWS_Key is None or config.Personal_AWS_Secret is None or config.Personal_AWS_Token is None:
        print('No AWS key / secret / token is available.')
        return None 
    #get aws credentials by Boto3 
    s3_client = boto3.client('s3',aws_access_key_id=config.Personal_AWS_Key,aws_secret_access_key=config.Personal_AWS_Secret, aws_session_token=config.Personal_AWS_Token)
    if s3_client==None:
        print("S3 client is none...")
        return None   
    #call generate_presigned_post of Boto3 to get upload url and fields params 
    signed_parts = s3_client.generate_presigned_post(Bucket=config.Personal_AWS_Bucket_Key,Key=outputFileNameOSS)
    print('---signed_parts----\n{0}'.format(signed_parts))
    signed_url = signed_parts['url'] 
    
    awsOutputUrl = signed_url
    outputFileArgument = {}
    outputFileArgument['verb'] = 'post'
    outputFileArgument['url'] = awsOutputUrl  
    outputFileArgument['multiparts'] = {} 
    outputFileArgument['multiparts']['key'] = outputFileNameOSS  
    outputFileArgument['multiparts']['AWSAccessKeyId'] = signed_parts['fields']['AWSAccessKeyId'] #the same to config.Personal_AWS_Key
    outputFileArgument['multiparts']['x-amz-security-token'] = signed_parts['fields']['x-amz-security-token']
    outputFileArgument['multiparts']['policy'] = signed_parts['fields']['policy'] 
    outputFileArgument['multiparts']['signature'] = signed_parts['fields']['signature']

    ##End generate AWS credentials #######

    workItemSpec['arguments']['inputFile'] = inputFileArgument
    workItemSpec['arguments']['inputJson'] = inputJsonArgument
    workItemSpec['arguments']['outputFile'] = outputFileArgument

    resp = requests.post(Forge_BASE_URL+DA_BASE_URL+'/workitems', headers={'Authorization': config.token},json=workItemSpec)
    if resp.status_code == 200:
        copyResJson = resp.json()
        #for download the output file. append elements of json 
        copyResJson['outputFileNameOSS'] = outputFileNameOSS 
        return copyResJson
    else:
        print('Create WorkItem of Design Automation, output to personal AWS bucket Failed! status ={0} ; message = {1}'.format(resp.status_code,resp.text ) )
        return None 

#####
