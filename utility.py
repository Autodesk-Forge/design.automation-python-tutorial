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
 
import requests 
from pathlib import Path  

def downloadResults(params):
    if params['report'] is not None:
        print('---downloading report file:'+ params['workItemId'] +'.log' )  
        res = requests.get(params['report']['url'])  
        if res.status_code == 200: 
            with open('./report/' +params['workItemId']+'.log' , 'wb') as f:
                f.write(res.content)
                print('get log file succeeded: '+ './report/' + params['workItemId'] +'.log') 
        else:
            print('get log file failed! workItemId:'+ params['workItemId'])

    if params['output'] is not None: 
        print('---downloading output file:'+ params['output']['fileName'])  
        res = requests.get(params['output']['url'],headers=params['output']['header']) 
        if res.status_code == 200:  
            with open('./output/' + params['output']['fileName'] , 'wb') as f:
                f.write(res.content)
                print('get output file succeeded: '+ './output/' + params['output']['fileName']) 
        else:
            print('get output file failed! workItemId:'+ params['workItemId'] )
            return  

#from https://docs.aws.amazon.com/code-samples/latest/catalog/python-s3-s3_basics-presigned_url.py.html
####preserve####
def generate_aws_presigned_url(s3_client, client_method, method_parameters, expires_in):
    try:
        url = s3_client.generate_presigned_url(
            ClientMethod=client_method,
            Params=method_parameters,
            ExpiresIn=expires_in
        )
        print("Got presigned URL")
    except :
        print("Couldn't get a presigned URL for client method '%s'.", client_method)
        raise
    return url