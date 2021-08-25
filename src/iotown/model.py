import requests

def uploadModel(url, token, epoch, modelID, ext, status, file):
    apiaddr = url + "/api/v1.0/nn/model/train"
    header = {'Token': token}
    filelist = {'model_id':modelID, 'epoch':epoch, 'ext':ext, 'status':status, 'file':file}
    r = requests.post(apiaddr, files=filelist, headers=header)
    print(r)
def downloadModel(url, token, epoch, modelID, ext):
    apiaddr = url + f"/api/v1.0/nn/model/{modelID}/{epoch}/{ext}"
    header = {'Token': token}
    r = requests.get(apiaddr, headers=header)
    print(r)
def getModelID(url, token):
    apiaddr = url + f"/api/v1.0/nn/models"
    header
    r = requests.get(apiaddr, headers=header)
    print(r)
def getModelEpochs(url, token, modelID):
    apiaddr = url + f"/api/v1.0/nn/model/trains/{modelID}"
    header = {'Token': token}
    r = requests.get(apiaddr, headers=header)
    print(r)