# Design Automation API workflow sample in Python
(Formely <Desktop Product> I/O).

[![ver](https://img.shields.io/badge/language-python-orange.svg)](https://www.python.org/)
[![tls1.2](https://img.shields.io/badge/TLS-1.2-green.svg)](https://www.ietf.org/rfc/rfc5246.txt)
![Platforms](https://img.shields.io/badge/Web-Windows%20%7C%20MacOS%20%7C%20Linux-lightgray.svg)
[![Data-Management](https://img.shields.io/badge/Data%20Management-v1-green.svg)](https://forge.autodesk.com/en/docs/data/v2/developers_guide/overview/)
[![Design-Automation](https://img.shields.io/badge/Design%20Automation-v3-green.svg)](https://forge.autodesk.com/en/docs/design-automation/v3/reference/http/)

[![oAuth2](https://img.shields.io/badge/oAuth2-v1-green.svg)](http://developer.autodesk.com/)
[![Data-Management](https://img.shields.io/badge/Data%20Management-v1-green.svg)](http://developer.autodesk.com/)
[![OSS](https://img.shields.io/badge/OSS-v2-green.svg)](http://developer.autodesk.com/)

[![License](http://img.shields.io/:license-mit-blue.svg)](http://opensource.org/licenses/MIT)
 

## Description
This is a Python sample code for <b>Design Automation API (DA)</b> (v3). It demos the workflow on updating the width and height param of DWG Dynamic Block (using AutoCAD), RVT Window Family instance (using Revit), IPT Part parameters (using Inventor) and 3DS ... (using 3dsMax). The source demo files and plugin projects are cloned from  [learn.forge.designautomation](https://github.com/Autodesk-Forge/learn.forge.designautomation)

## Thumbnail
![thumbnail](/thumbnail.png)  

### Dependencies
* **Python**: Download [Python](https://www.python.org/downloads/). The code can work with old version such as 2.7.9, but it requires to have TLS1.2 supported. It is recommended to use Python > 3. 
* **Forge Account**: Learn how to create a Forge Account, activate subscription and create an app at [this tutorial](http://learnforge.autodesk.io/#/account/). Make sure to select the service **Design Automation API V3 (beta)**. Make a note with the credentials (client id and client secret) of the app. 
* **Plugin**: Build the the plugin in [Plugins](/plugins) folder by corresponding version of _Visual Studio_ and refererences of correspoinding Autodesk products. The app bundle zip will be put to [bundles folder](/plugins/bundles) by post-build event
* Install dependencies via pip:
```
    pip install -r requirements.txt
```

## Running locally
1. input the credentials (client_id and client_secret) [config.py](/config.py). Input desired nickname and alais. 
```
    #Forge Client Id
    Forge_CLIENT_ID = ''
    #Forge Client Secret
    Forge_CLIENT_SECRET =''
    #desired nick name
    desired_nickname = 'xiaodonglikename'   
    #Alias
    alias = 'dev' 
```
2. run main.py with width and height value:
* * python main.py --height [height value] --width [width value]  

3. Follow the note of command line to select: bundle, app engines. The code will re-use the name of bundle name as the appBundle name and activity name of DA. Ensure to select the suitable engines for the corresponding bundle. 

4. The code will create a new activity or appbundle if they do not exist. If they exist, one new version will be generated. 

5. Before posting workitem, the code will upload the demo source file to OSS bucket of your Forge account. The updated model file will also be put to OSS bucket, with a new name. 

6. Wait for the response about work item status. If it success, the output model file (model with the updated parameters) will be downloaded to [output folder](/output). Try with other tool (such as https://viewer.autodesk.com ) to verify if the model is valid and parameters are updated. If it fails, the log file will be downloaded to [report folder](/report). 

## Demo Video
Click the image below to check the demo video:
[![Forge Design Automation Python Workflow](/demo.png)](https://www.youtube.com/embed/YvzBaArFbfQ) 

## Troubleshooting

1. When installing depencencies, for such similar error as below, try to upgrade [pip](https://pip.pypa.io/en/stable/installing/)
```
Could not fetch URL https://pypi.python.org/simple/pathlib/: There was a problem confirming the ssl certificate: [SSL: TLSV1_ALERT_PROTOCOL_VERSION] tlsv1 alert protocol version (_ssl.c:661)
```

2. When running the code, it failed with such error below,  check if TLS1.2 and above is supported with SSL request with this Python enviroment. 
```
requests.exceptions.SSLError: HTTPSConnectionPool(host='developer.api.autodesk.com', port=443): Max retries exceeded with url: /authentication/v1/authenticate (Caused by SSLError(SSLEOFError(8, u'EOF occurred in violation of protocol (_ssl.c:590)'),))
```
The best is to upgrade Python to version which > 3. Or try to install **requests** by security if in old version of Python, e.g.
```
pip install requests[security]
```

## Further Reading
* [Design Automation API help](https://forge.autodesk.com/en/docs/design-automation/v3/developers_guide/overview/)
* [Blogs on Python & Forge](https://forge.autodesk.com/categories/python)

## License
These samples are licensed under the terms of the [MIT License](http://opensource.org/licenses/MIT). Please see the [LICENSE](LICENSE) file for full details.

### Authors

Autodesk Forge Support

- Xiaodong Liang [@coldwood](https://twitter.com/coldwood)

See more at [Forge blog](https://forge.autodesk.com/blog).
