# **pyiotown Api Reference**

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
|url|String| IoT.own Server URL|http://192.168.0.5:8888|
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

url = "http://192.168.0.5:8888"
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
|url|String| IoT.own Server URL|http://192.168.0.5:8888|
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

url = "http://192.168.0.5:8888"
token = "aoijobseij12312oi51o4i6"
imageID = "601023l345oi23uaeior"
r = get.downloadImage(url,token,imageID)
image = Image.open(BytesIO(r))
image.save("test.jpg") # image save
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
|url|String| IoT.own Server URL|http://192.168.0.5:8888|
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

url = "http://192.168.0.5:8888"
token = "aoijobseij12312oi51o4i6"
f = open("test.jpg","rb")
baseimage = base64/b64encode(f.read()).decode('UTF-8')
payload = {"image":baseimage, "type":"jpg", ...}
r = post.uploadImage(url,token,payload)
```     

---
## **data**
send device data to IoT.own Server
### *prototype*
```
def data(url, token, nid, data)
```
### *parameters*
|name|type|desc|example|
|:---:|:---:|:---:|:---:|
|url|String| IoT.own Server URL|http://192.168.0.5:8888|
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
url = "http://192.168.0.5:8888"
token = "aoijobseij12312oi51o4i6"
nodeid = "LW140C5BFFFF"
payload = { "temper":12.5, "class":"timer" }
r = post.data(url,token,nodeid,payload)
```