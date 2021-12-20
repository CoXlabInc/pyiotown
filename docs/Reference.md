# **pyiotown Api Reference**
---
---
# *LIST*
## **GET**
### [**downloadAnnotations()**](#downloadannotations-1)
### [**downloadImage()**](#downloadimage-1)
### [**storage()**](#storage-1)
## **POST**
### [**uploadImage()**](#uploadimage-1)
### [**data()**](#data-1)
### [**postprocess()**](#postprocess-1)
### [**postprocess_common()**](#postprocess_common-1)
---
---
# *GET*
## **downloadAnnotations**
download Dataset's Annotations. return Json data ( id, boxinfo )
### *prototype*
```
def downloadAnnotations(url, token, classname):
```
### *parameters*
| name | type| desc| example |
|:------:|:------:|:------:|:------:|
|url|String| IoT.own Server URL|https://192.168.0.5:8888|
|token|String| IoT.own API token| aoijobseij12312oi51o4i6|
|classname|String| image Label Class name | "human"|

### *return*
| value | desc|
|:---:|:---:|
| Json Data | if Download Success, return ( Annotation ) json data |
| None | if Download Fail, return None |
### *Example*
```
from pyiotown import get

url = "https://192.168.0.5:8888"
token = "aoijobseij12312oi51o4i6"
classname = "car"
r = get.downloadAnnotations(url,token,classname)
```     

---
## **downloadImage**
download Image throuht imageID. image will return by Bytearray.
### *prototype*
```
def downloadImage(url, token, imageID):
```
### *parameters*
| name | type| desc| example |
|:------:|:------:|:------:|:------:|
|url|String| IoT.own Server URL|https://192.168.0.5:8888|
|token|String| IoT.own API token| aoijobseij12312oi51o4i6|
|imageID|String| image ID to download | 601023l345oi23uaeior|

### *return*
| value | desc|
|:---:|:---:|
| encoded Byte Image | if Download Success, return encoded byte image |
| None | if Download Fail, return None |
### *Example*
```
from pyiotown import get
from PIL import Image
from io import BytesIO

url = "https://192.168.0.5:8888"
token = "aoijobseij12312oi51o4i6"
imageID = "601023l345oi23uaeior"
r = get.downloadImage(url,token,imageID)
image = Image.open(BytesIO(r))
image.save("test.jpg") # image save
``` 

---
## **storage**
download DB data from IoT.own Server
### *prototype*
```
def storage(url, token, nid, date_from , date_to, lastKey=""):
```
### *parameters*
| name | type| desc| example |
|:------:|:------:|:------:|:------:|
|url|String| IoT.own Server URL|https://192.168.0.5|
|token|String| IoT.own API token| aoijobseij12312oi51o4i6|
|nid|String| data node ID, if "", then search all node | LW1122334455667788|
|date_from|String| UTC date from  | 2021-11-19T00:00:00Z |
|date_to|String| UTC date to | 2021-11-25T23:59:59Z |
|lastKey|String| default is None, but if response data > 5000, lastKey will be returned. next, api call using that lastKey. then next 5000 data will be returned | 601023l345oi23uaei or ""|

### *return*
| value | desc|
|:---:|:---:|
| Dict | if Download Success, return dictionary. data is different from time to time. so print that return value |
| None | if Download Fail, return None |
### *Example*
```
from pyiotown import get

url = "https://192.168.0.5"
token = "aoijobseij12312oi51o4i6"
nodeID = "LW1122334455667788"
date_from = "2021-11-19T00:00:00Z"
date_to = "2021-11-25T23:59:59Z"
r = get.storage(url,token,nodeID,date_from,date_to)
```



# *POST*
## **uploadImage**
upload Image to IoT.own. payload should be encoded base64 
### *prototype*
```
def uploadImage(url, token, payload):
```
### *parameters*
| name | type| desc| example |
|:------:|:------:|:------:|:------:|
|url|String| IoT.own Server URL|https://192.168.0.5:8888|
|token|String| IoT.own API token| aoijobseij12312oi51o4i6|
|payload|dict| Image + Annotation Data|{"image": base64 encoded image ,"type":"jpg","labels":[ {"name":"human","x":0.1,"y":0.2,"w":0.4,"h":0.4}, { ... } , { ... }] }|
```
label exp) "name":classname, "x":centerX, "y":centerY, "w":boxWidth, "h":boxHeight (same YOLO)
```

**Warning : User have to encode Image base64.*
### *return*
| value | desc|
|:---:|:---:|
| True | if send to IoT.own success , return True |
| False | if send to IoT.own Fail, return False and print Error|
### *Example*
```
from pyiotown import post

url = "https://192.168.0.5:8888"
token = "aoijobseij12312oi51o4i6"
f = open("test.jpg","rb")
baseimage = base64/b64encode(f.read()).decode('UTF-8')
payload = {"image":baseimage, "type":"jpg", ...}
r = post.uploadImage(url,token,payload)
```     

---
## **data**
send device data to IoT.own Server

1. send only text
2. send with files ( image, video, binary, ... )
### *prototype*
```
def data(url, token, nid, data, files="")
```

### **1. send only text**
### *parameters*
|name|type|desc|example|
|:---:|:---:|:---:|:---:|
|url|String| IoT.own Server URL|https://192.168.0.5:8888|
|token|String| IoT.own API token| aoijobseij12312oi51o4i6|
|nid|String| registered in IoT.own Node ID | LW140C5BFFFF |
|data| dict | data from device | { "temper":12.5, "class":"timer" , ... } 

### *return*
| value | desc|
|:---:|:---:|
| True | if send to IoT.own success, return True |
| False | if send to IoT.own Fail, return False and print Error|

### *Example*
```
from pyiotown import post
url = "https://192.168.0.5:8888"
token = "aoijobseij12312oi51o4i6"
nodeid = "LW140C5BFFFF"
payload = { "temper":12.5, "class":"timer" }
r = post.data(url,token,nodeid,payload)
```
### **2. send with files ( image, video, binary, ... )**
### *parameters*
|name|type|desc|example|
|:---:|:---:|:---:|:---:|
|url|String| IoT.own Server URL|https://192.168.0.5:8888|
|token|String| IoT.own API token| aoijobseij12312oi51o4i6|
|nid|String| registered in IoT.own Node ID | LW140C5BFFFF |
|data| dict | meta data for explain files | 
{   "input_video": {
        "type": "video",
        file: "video1"
        }, 
    "output_video": {
        "type": "video",
        file: "video2"
        }
    } 
|files| dict | files for send to Server | { "video1": open("1.mp4") ,"video2": open("2.mp4") }

### *return*
| value | desc|
|:---:|:---:|
| True | if send to IoT.own success, return True |
| False | if send to IoT.own Fail, return False and print Error|

### *Example*
```
from pyiotown import post
url = "https://192.168.0.5:8888"
token = "aoijobseij12312oi51o4i6"
nodeid = "LW140C5BFFFF"
meta = {   
    "input_video": {
        "type": "video",
        file: "video1"
        }, 
    "output_video": {
        "type": "video",
        file: "video2"
        }
    } 
files = {
    "video1": open("1.mp4","rb")
    "video2": open("2.mp4","rb")
}
r = post.data(url,token,nodeid,meta,files)
```




---
## **postprocess**
receive Data from IoT.own and send modified data to IoT.own using MQTT
### *prototype*
```
def postprocess(url, token, name, func, username, pw)
```
### *parameters*
|name|type|desc|example|
|:---:|:---:|:---:|:---:|
|url|String| IoT.own Server URL|https://192.168.0.5|
|token|String| IoT.own API token| aoijobseij12312oi51o4i6|
|name|String| post process name | postproc1 |
|func| function | self-made function | postproc | 
|username|String|MQTT ID|admin|
|pw|String|MQTT Password|1234|

### *return*
| value | desc|
|:---:|:---:|
| loop | if postprocess start, then loop start |
| stop | if error occured during operation, then stop function  |

### *function*

```
function consist of one parameter and one return value.
parameter and return data type is dictionary.
user add key and value to the parameter and return it 

refer to example code and change code.
```

### *Example*

0. get topic from IoT.own
1. user subscribe received topic
2. IoT.own receive data from sensor, then publish data to typical topic
3. user made function called by mqtt
4. if user made function return, then publish to mqtt server
5. check IoT.own


```
from pyiotown import post

def postproc(rawdata):
    sensor1 = rawdata['data']['sensor1']
    sensor2 = rawdata['data']['sensor2']
    sensor3 = rawdata['data']['sensor3']
    changedata = {}
    changedata['sensor1'] = sensor1 + 10
    changedata['sensor2'] = sensor2 + 30
    changedata['sensor3'] = sensor3 + 50
    rawdata['data'] = changedata
    return rawdata

url = "https://192.168.0.1/"
token = "aoijobseij12312oi51o4i6"
name = "postproc1"
username = "admin"
password = "1234"
post.postprocess(url,token,name, postproc, username, password)
```

---
## **postprocess_common**
for using common topic postprocess. 
### *prototype*
```
def postprocess_common(url, topic, func, username, pw)
```
### *parameters*
|name|type|desc|example|
|:---:|:---:|:---:|:---:|
|url|String| IoT.own Server URL|https://192.168.0.5|
|topic|String| IoT.own API token| iotown/proc/common/yolo-x |
|func| function | self-made function | postproc_common | 
|username|String|MQTT ID|admin|
|pw|String|MQTT Password|1234|

### *return*
| value | desc|
|:---:|:---:|
| loop | if postprocess start, then loop start |
| stop | if error occured during operation, then stop function  |

### *function*

```
function consist of one parameter and one return value.
parameter and return data type is dictionary.
user add key and value to the parameter and return it 

refer to example code
```

### *Example*

1. user subscribe typical topic
2. IoT.own receive data from sensor, then publish data to typical topic
3. user made function called by mqtt
4. if user made function return, then publish to mqtt server
5. check IoT.own


```
from pyiotown import post

def postproc_common(rawdata):
    encoded_img = rawdata['data']['snap']['raw']
    decoded_img = base64.b64decode(encoded_img)
    nparr = np.frombuffer(decoded_img, np.byte)
    origin_img = cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)

    ###
    Inference Code (skip)
    ###

    rawdata['data']['snap']['detected'] = [{"name":"human" "x":0.2,"y":0.4,"w":0.3,"h":0.3,"score":0.75 }, {"name":"car" "x":0.1,"y":0.1,"w":0.2,"h":0.2,"score":0.8 }]
    return rawdata

url = "https://192.168.0.1/"
topic = "iotown/proc/common/yolo-x"
username = "admin"
password = "1234"
post.postprocess_common(url,topic,postproc_common, username, password)
```