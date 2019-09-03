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
import sys 
import time
import os
import requests  
import argparse

print(requests.get('https://www.howsmyssl.com/a/check', verify=False).json()['tls_version'])

forge_da = __import__('forge_da')
config = __import__('config')

appPackagePath = './plugins/bundles/'
modelfilePath = './sample files/' 

#desired nick name
desired_nickname = config.desired_nickname
#Alias
alias = config.alias

# time out max 2when get workitem status
TIMEOUT = 10 * 60  # 10min

#default width
width = 100
#default height
height = 100

parser = argparse.ArgumentParser(description='Demo Workflow of Design Automation. Input Updated Height and Width:')
parser.add_argument('--height', required=True)
parser.add_argument('--width', required=True) 

#read height and width from arguments
args = parser.parse_args()
width = args.width
height = args.height

### 0. get bundle
file_list=os.listdir(appPackagePath)
index = 0
for bundle in file_list: 
    print ('[' + str(index) + '] ' + bundle)
    index+=1

variable = input('select bundle: ')
#app package zip name 
zip_name = file_list[int(variable)]
print(zip_name)

#app bundle name 
appboundle_name = os.path.splitext(zip_name)[0]
#activity  name
activity_name = appboundle_name

file_list=os.listdir(modelfilePath)
index = 0
for demofile in file_list: 
    print ('[' + str(index) + '] ' + demofile)
    index+=1
variable = input('select demo file: ')

#demo file name
demo_file_name = file_list[int(variable)]
print(demo_file_name)

### 1. get token
print('---Getting token...')
token = forge_da.getToken()
if token == None:
    quit() 

### 2. check nick name
print('---Check nick name...')

nickname = forge_da.getNickName()
print('nick name: ' + nickname) 
if nickname == None:
    quit()   
if nickname == config.Forge_CLIENT_ID :
    #set desired nick name
    if forge_da.deleteNickName(nickname) == None:
        quit()
    if forge_da.setNickName(desired_nickname) == None:
        quit()

nickname = forge_da.getNickName()
if nickname == None:
    quit()  
print('current nick name: ' + nickname) 


### 3. list engines
print('---List engines...')

engines = forge_da.dumpEngines()
if engines == None:
    quit()  

index = 0
print('***engine list***')
for eng in engines: 
    print(' ['+str(index) + ']' + eng) 
    index+=1
variable = input('select product: ')
enginename = engines[int(variable)]
print(enginename)
#print(engineAttributes(engine)) 

### 4. create/update app bundle 
print('---Creating App Bundle...')

qualifiedAppBundleId = '{0}.{1}+{2}'.format(nickname, appboundle_name, alias)
findApp = False
print('***appbundle list***')
appbubdles = forge_da.getDefinedAppbundles()
for app in appbubdles: 
    print(' '+ app)
    if qualifiedAppBundleId == app:
        findApp = True  

if findApp :
    print('---App bundle already defined:' +qualifiedAppBundleId)  
    print('---Creating new version of app bundle...')  
    newAppVersionRes = forge_da.createAppBundleVersion(enginename,appboundle_name)
    if newAppVersionRes == None:
        quit()
    print('---Uploading bundle zip...') 
    uploadRes = forge_da.uploadZip(appPackagePath,appboundle_name,zip_name,newAppVersionRes['uploadParameters']['formData'] )
    if uploadRes == None:
        quit()
    print('---Updating app bundle alias...')
    alaisRes = forge_da.updateAppBundleAlias(appboundle_name,alias,newAppVersionRes['version'])
    if alaisRes == None:
        quit()
    print('***New app bundle version is created...' + str(qualifiedAppBundleId) + ' version=' + str(newAppVersionRes['version'])) 
else:
    print('---Creating new app bundle...')   
    newAppRes = forge_da.createAppBundle(enginename,appboundle_name)
    print(newAppRes)
    if newAppRes == None:
        quit()
    uploadRes = forge_da.uploadZip(appPackagePath,appboundle_name,zip_name,newAppRes['uploadParameters']['formData'] )
    if uploadRes == None:
        quit()
    print('---Creating app bundle alias...')
    alaisRes = forge_da.createAppBundleAlias(appboundle_name,alias,1)
    if alaisRes == None:
        quit() 
    print('***New app bundle is created...{0}'.format(qualifiedAppBundleId)) 



### 5. create activity 
qualifiedActivityId = '{0}.{1}+{2}'.format(nickname, activity_name, alias)
findAct = False
print('***activity list***') 
activities = forge_da.getDefinedActivities()
for act in activities: 
    print(' ' + act) 
    if qualifiedActivityId == act:
        findAct = True 

if findAct :
     # as this activity points to a AppBundle "dev" alias (which points to the last version of the bundle)
    # there is no need to update it (for this sample), but this may be extended for different contexts
    print('***Activity already defined:' +qualifiedActivityId) 
else:
    print('---Creating activity...')  
    res = forge_da.createActivity(enginename,appboundle_name,qualifiedAppBundleId,activity_name)
    if res == None:
        quit()
    print('---Creating activity alias...')  
    res = forge_da.createActivityAlias(activity_name,alias)
    if res == None:
        quit()
    print('***New activity  is created...{0}'.format(qualifiedActivityId)) 


### 6. prepare source file in Forge bucket
print('---Prepare source file in Forge bucket...')  

bucketKey = nickname.lower() + "_designautomation"
res = forge_da.createBucket(bucketKey)
if res == None:
    quit()
res = forge_da.uploadFileToBucket(modelfilePath,bucketKey,demo_file_name)
if res == None:
    quit()
inputFileNameOSS = res['objectKey']

### 7. create workitem
print('---Create workitem...')  

param={}
param['bucketKey'] = bucketKey
param['inputFileNameOSS'] = inputFileNameOSS
param['jsonInput'] ={}
param['jsonInput']['width'] = width
param['jsonInput']['height'] = height
res = forge_da.createWorkItem(qualifiedActivityId,param)
if res == None:
     quit()
#work item ID
workItemId = res['id']
#url of output file on Forge OSS bucket
ossOutputUrl = res['ossOutputUrl']
outputFileNameOSS = res['outputFileNameOSS']


### 8. check workitem status and download result/report
status = 'pending'
print('---work item running!')
start_time = time.time()
while status == 'pending' or status == 'inprogress':
    statusRes = forge_da.getWorkItemStatus(workItemId)
    if statusRes == None:
        quit()
    status = statusRes['status']
    if status != 'pending' and status != 'inprogress':
        break
    elapsed_time = time.time() - start_time
    if elapsed_time > TIMEOUT:
        print('     get work item status timeout!') 
        break

print('****work item status:' + status)


### 9. get output file or log file 

if status == 'success':
    # #successful job. download the output file from Forge OSS bucket
    print('---downloading output file:'+ outputFileNameOSS ) 

    res = requests.get(ossOutputUrl,headers={'Authorization': config.token})  
    if res.status_code == 200:  
        with open('./output/' + outputFileNameOSS , 'wb') as f:
            f.write(res.content)
            print('get output file succeeded: '+ './output/' + outputFileNameOSS) 
    else:
        print('get output file failed!')
   
else:
    print('---downloading report file:'+ workItemId +'.log' )  
    #failed job. download the report file
    reportUrl = statusRes['reportUrl'] 
    res = requests.get(reportUrl)  
    if res.status_code == 200: 
        with open('./report/' +workItemId +'.log' , 'wb') as f:
            f.write(res.content)
            print('get log file succeeded: '+ './output/' +workItemId +'.log') 
    else:
        print('get log file failed!')


