# Design Automation API sample in Python
(Formely <Desktop Product> I/O).

[![ver](https://img.shields.io/badge/language-python-orange.svg)](https://www.python.org/)
[![Design Automation](https://img.shields.io/badge/Design%20Automation-v2-green.svg)](http://developer.autodesk.com/)
![Platforms](https://img.shields.io/badge/platform-windows%20%7C%20osx%20%7C%20linux-lightgray.svg)
![Python](https://img.shields.io/badge/Python-2.7%2F3.3-green.svg)
 [![License](http://img.shields.io/:license-mit-red.svg)](http://opensource.org/licenses/MIT)
 
## Description
This is a Python sample code for <b>Design Automation API</b> (v2). It is a very short demo at this moment which shows getting token and checking the status of one existing workitem only. More functions will be added in the future.
 
## Thumbnail
![thumbnail](/thumbnail.png) 


## Setup

### Dependencies
* Download [Python](https://www.python.org/downloads/). The code can work with old version such as 2.7, but it is recommended to use the new version.

### Prerequisites
1. **Forge Account**: Learn how to create a Forge Account, activate subscription and create an app at [this tutorial](http://learnforge.autodesk.io/#/account/). Make sure to select the service **Design Automation**.
2. Make a note with the credentials (client id and client secret) of the app. 
3. Follow the steps on [API Basic](https://forge.autodesk.com/en/docs/design-automation/v2/developers_guide/basics/) to create a test codes with full workflow: create activity, create workitem, create app package (if needed). Make a note with the workitem id. Another choice is to check some samples (prefix with "design automation") on [Autodesk-Forge Github Repository](https://github.com/Autodesk-Forge/) such as [design.automation-workflow-winform-sample](https://github.com/Autodesk-Forge/design.automation-workflow-winform-sample). Build the sample and get a workitem id.


## Running locally
1. run acadio.py with the  credentials and workitem id like:
* * acad-da.py --client_id [you client id] --client_secret [your client secret] --workitem_id  [your work item id]
2. wait for the response about work item status. It will also download the log file

![thumbnail](/demo.png) 

## Further Reading
* [Design Automation API help](https://forge.autodesk.com/en/docs/design-automation/v2/developers_guide/overview/)

* [Blogs on Python & Forge](https://forge.autodesk.com/categories/python)

### Limitation
* as of writing, only AutoCAD Design Automation is released. While the skeleton of this sample could apply with other products (such as Revit, Inventor) after replacing the endpoints.

 ## License
 These samples are licensed under the terms of the [MIT License](http://opensource.org/licenses/MIT). Please see the [LICENSE](LICENSE) file for full details.
