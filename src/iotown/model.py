import requests
def uploadModel(url, token, epoch, modelID, ext, status, fileurl):
    apiaddr = url + "/api/v1.0/nn/model/train"
    header = {'Token': token}
    filelist = {'model_id':modelID, 'epoch':epoch, 'ext':ext, 'status':status}
    r = requests.post(apiaddr, data=filelist, files={"file":open(fileurl,'rb')}, headers=header)
    if r.status_code == 200:
        return True
    else:
        print(r)
        return False
def downloadModel(url, token, epoch, modelID, ext, fileurl):
    apiaddr = url + f"/api/v1.0/nn/model/train/{modelID}/{epoch}/{ext}"
    header = {'Token': token}
    r = requests.get(apiaddr, headers=header)
    if r.status_code == 200:
        f = open(fileurl,'wb')
        f.write(r.content)
        f.close()
        return True
    else:
        print(r)
        return False
def getModelID(url, token):
    apiaddr = url + f"/api/v1.0/nn/models"
    header = {'Token': token}
    r = requests.get(apiaddr, headers=header)
    if r.status_code == 200:
        return r.json()['models']
    else:
        print("Error", r.status_code)
        return None
def getModelEpochs(url, token, modelID):
    apiaddr = url + f"/api/v1.0/nn/model/trains/{modelID}"
    header = {'Token': token}
    r = requests.get(apiaddr, headers=header)
    if r.status_code == 200:
        return r.json()['trains']
    else:
        print("Error", r.status_code)
        return None 