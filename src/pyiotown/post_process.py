from .post import post_files
import json
from urllib.parse import urlparse
import paho.mqtt.client as mqtt
import sys
import ssl

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        name = userdata['name']
        print(f"Post process '{name}' Connect OK! Subscribe Start")
    else:
        print("Bad connection Reason",rc)

def on_message(client, userdata, msg):
    message = json.loads((msg.payload).decode('utf-8'))

    if userdata['group'] == 'common':
        # Common post process
        data = message
    else:
        # User-specific post process
        data = { 'gid': message['gid'],
                 'nid': message['nid'],
                 'data': message['data'],
                 'ntype': message['ntype'],
                 'ndesc': message['ndesc'] }
        if 'lora_meta' in message.keys():
            data['lora_meta'] = message['lora_meta']
    
    try:
        result = userdata['func'](data)
    except Exception as e:
        print(f'Error on calling the user-defined function', file=sys.stderr)
        print(e, file=sys.stderr)
        client.publish('iotown/proc-done', msg.payload, 1)
        return

    if type(result) is dict and 'data' in result.keys():
        result = post.post_files(result, userdata['url'], userdata['token'])
        message['data'] = result['data']
        client.publish('iotown/proc-done', json.dumps(message), 1)
    elif result is None:
        print(f"Discard the message")
    else:
        print(f"CALLBACK FUNCTION TYPE ERROR {type(result)} must [ dict ]", file=sys.stderr)
        client.publish('iotown/proc-done', msg.payload, 1)

    
def updateExpire(url, token, name, verify=True, timeout=60):
    apiaddr = url + "/api/v1.0/pp/proc"
    header = {'Accept':'application/json', 'token':token}
    payload = { 'name' : name}
    try:
        r = requests.post(apiaddr, json=payload, headers=header, verify=verify, timeout=timeout)
        if r.status_code != 200 and r.status_code != 403:
            print(f"update Expire Fail! {r}")
    except Exception as e:
        print(f"update Expire Fail! reason: {e}")
    timer = threading.Timer(60, updateExpire, [url, token, name, verify, timeout])
    timer.start()

def getTopic(url, token, name, verify=True, timeout=60):
    apiaddr = url + "/api/v1.0/pp/proc"
    header = {'Accept':'application/json', 'token':token}
    payload = {'name':name}    
    try:
        r = requests.post(apiaddr, json=payload, headers=header, verify=verify, timeout=timeout)
        if r.status_code == 200:
            topic = json.loads((r.content).decode('utf-8'))['topic']
            #print(f"Get Topic From IoT.own Success: {topic}")
            return topic
        elif r.status_code == 403:
            topic = json.loads((r.content).decode('utf-8'))['topic']
            #print(f"process already in use. please restart after 1 minute later.: {topic}")
            return topic
        else:
            print(r)
            return None
    except Exception as e:
        print(e)
        return None

def connect(url, name, func, username, pw, mqtt_host=None, port=8883, verify=True):
    # get Topic From IoTown
    topic = getTopic(url, pw, name, verify)

    if topic == None:
        raise Exception("IoT.own returned none")

    try:
        group = topic.split('/')[2]
    except Exception as e:
        raise Exception(f"Invalid topic {topic}")
    
    updateExpire(url, pw, name, verify)
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(username, pw)
    client.user_data_set({
        "url": url,
        "token": pw,
        "func": func,
        "group": group,
        "name": name,
    })

    if mqtt_host is None:
      mqtt_server = urlparse(url).hostname
    else:
      mqtt_server = urlparse(mqtt_url).hostname
      
    print(f"Post process '{name}' is trying to connect to {mqtt_server}:{port}")
    client.tls_set(cert_reqs=ssl.CERT_NONE)
    client.tls_insecure_set(True)
    client.connect(mqtt_server, port=port)
    client.subscribe(topic, 1)
    return client

def connect_common(url, topic, func, username, pw, mqtt_host=None, port=8883):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(username, pw)
    client.user_data_set({
        "url": url,
        "token": pw,
        "func": func,
        "group": "common",
        "name": topic,
    })

    if mqtt_host is None:
      mqtt_server = urlparse(url).hostname
    else:
      mqtt_server = urlparse(mqtt_url).hostname

    print(f"Post process '{topic}' is trying to Connect to {mqtt_server}:{port}")
    client.tls_set(cert_reqs=ssl.CERT_NONE)
    client.tls_insecure_set(True)
    client.connect(mqtt_server, port=port)
    client.subscribe(f'iotown/proc/common/{topic}', 1)
    return client

def loop_forever(clients):
    if isinstance(clients, list) == False:
        clients = [ clients ]

    while True:
        for c in clients:
            c.loop(timeout=0.01)