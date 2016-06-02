## Design Automation in Python
 Design Automation is called AutoCAD IO in the past.

[![ver](https://img.shields.io/badge/language-python-orange.svg)](https://www.python.org/)
 [![ver](https://img.shields.io/badge/AutoCAD.io-2.0.0-blue.svg)](https://developer.autodesk.com/api/autocadio/v2/)
![Platforms](https://img.shields.io/badge/platform-windows%20%7C%20osx%20%7C%20linux-lightgray.svg)
 [![License](http://img.shields.io/:license-mit-red.svg)](http://opensource.org/licenses/MIT)
 
 ## Description
This is a Python sample code for AutoCAD.IO (v2). It is a very short demo at this moment which shows get token and check the status of one existing workitem only. More functions of IO will be added in the future.
 
##Setup/Usage Instructions
* Get your credentials of AutoCAD IO at http://developer.autodesk.com
* Follow the steps on https://developer.autodesk.com/api/autocadio/#sample-codes to create a test codes with full workflow: create activity, create workitem, create app package (if needed) . make a note with the workitem id
* download [Python](https://www.python.org/downloads/). The code can work with old version such as 2.7, but it is recommended to use the new version.
* run acadio.py with the  credentials and workitem id like:
* * acadio.py --consumerKey [you key] --consumerSecret [your secret] --workItem  [your work item id]
* [![](help/testdemo.png)]

 
 ## License
 These samples are licensed under the terms of the [MIT License](http://opensource.org/licenses/MIT). Please see the [LICENSE](LICENSE) file for full details.
