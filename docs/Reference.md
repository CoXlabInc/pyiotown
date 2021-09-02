# **pyiotown Api Reference**

## **uploadImage**
### *prototype*
```
def uploadImage(url, token, payload):
```
### *parameters*
| name | type| desc| example |
|:------:|:------:|:------:|:------:|
|url|String| IoT.own Server URL|http://192.168.0.5:8888|
|token|String| IoT.own API token| aoijobseij12312oi51o4i6|
|payload|Json Data| Image + Annotation Data|{"image": base64 encoded image ,"type":"jpg","labels":[ {"name":"human","x":0.1,"y":0.2,"w":0.4,"h":0.4}, { ... } , { ... }] }|

**Warning : User have to encode Image base64.*
### *return*
| value | desc|
|:---:|:---:|
| True | if send to IoT.own server, return True |
| False | if send to IoT.own Fail, return True and print Error|
### *Example*
```
ex) from pyiotown import model

    url = "http://192.168.0.5:8888"
    token = "aoijobseij12312oi51o4i6"
    f = open("test.jpg","rb")
    baseimage = base64/b64encode(f.read()).decode('UTF-8')
    payload = {"image":baseimage, "type":"jpg", ...}
    r = model.uploadImage(url,token,payload)
```     

---
## **downloadAnnotations**
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
ex) from pyiotown import model

    url = "http://192.168.0.5:8888"
    token = "aoijobseij12312oi51o4i6"
    classname = "car"
    r = model.downloadAnnotations(url,token,classname)
```     

---
## **downloadImage**
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
ex) from pyiotown import model
    from PIL import Image
    from io import BytesIO

    url = "http://192.168.0.5:8888"
    token = "aoijobseij12312oi51o4i6"
    imageID = "601023l345oi23uaeior"
    r = model.downloadImage(url,token,imageID)
    image = Image.open(BytesIO(r))
    image.save("test.jpg") # image save
```     

