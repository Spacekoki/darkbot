#!/usr/bin/env python3
# -*- coding: utf-8 -*
import collections as cl
import datetime
import requests
import json
from icecream import ic
import subprocess
import os


def detect():
    now = datetime.datetime.now()
    jsnpath = 'result/{0:%Y%m%d_%H%M%S}.json'.format(now)
    picpath = 'camera/{0:%Y%m%d_%H%M%S}.jpg'.format(now)

    cheese=['fswebcam','-p','MJPEG','-r','1280x1024','--no-banner','--rotate=90','-D','1']
    cheese.append(picpath)

    try:
        subprocess.check_call(cheese)
        print ("Command finished.")
    except:
        return "Command envailed."

    try:
        f1={'file':open(picpath,'rb')}
        print ("file read.")
    except:
        return "file doesn't exists."

    f2=open(jsnpath,'w')

    try:
        r=requests.post("http://localhost:9300/detect",files=f1)
    except :
        return "Server error."
        sys.exit()
    if r.status_code is not 200:
            data=json.loads(r.content)
            ic(data)
            f2.close()
            return "f**k you"
    print ("detected")
    #print(r.status_code,r.text)
    f2.write(r.text)
    f2.close()
    return r.text,now


def clear():
    path=['camera/', 'result/', 'json/']
    try:
        for n in range(3):
            for root, dirs, files in os.walk(path[n], topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
    except:
        return "Error."
    return "all cleared"



def think(time):
    #A---D
    #|   |
    #B---C
    t=[
        [[185,390],[255,450],[530,410],[460,350]], 
        [[255,450],[355,550],[715,475],[605,400]],
        [[545,510],[665,650],[1024,545],[875,440]] 
    ]
    try:
        path1 = 'result/{0:%Y%m%d_%H%M%S}.json'.format(time)
    except ValueError:
        return "I am busy, so try again."

    path2 = 'json/td_{0:%Y%m%d_%H%M%S}.json'.format(time)
    res=[0,0,0]

    key=['table1','table2','table3','timing']
    #d={}
    d=cl.OrderedDict()

    if path1=='i':
        return "I am busy, so try again."
    f1=open(path1,'r')
    f2=open(path2,'w')
    dict=json.load(f1)
    for data in dict.get('result'):
        print(data['obj_name'])
        if data['obj_name']=='person' :
            bd=data['bounding_box']
            x=bd['x_min']+bd['width']/2
            y=bd['y_min']+bd['height']/2
            print(x,y)
            for a in range(3):
                p=0
                m=0
                for b in range(4):
                    if b==3 :
                        c=0
                    else :
                        c=b+1
                    cp = (t[a][c][0]-t[a][b][0])*(y-t[a][b][1])-(t[a][c][1]-t[a][b][1])*(x-t[a][b][0])
                    if cp>0:
                        p+=1
                    elif cp<0:
                        m+=1
                    else:
                        m+=1
                        p+=1
                print(p,m)
                if m==4 or p ==4 :
                    res[a]+=1
                    #d[key[0]]=x
                    #d[key[1]]=y
                    #d[key[2]]=a+1
                    #json.dump(d,f2,indent=4)
    for n in range(3):
        d[key[n]]=res[n]
    d[key[3]]='{0:%Y%m%d_%H%M%S}'.format(time)
    json.dump(d,f2,indent=4)
    f1.close()
    f2.close()
    return res

def upload(time):
    path='json/td_{0:%Y%m%d_%H%M%S}.json'.format(time)
    decoder = json.JSONDecoder(object_pairs_hook=cl.OrderedDict)
    with open(path) as json_file:
        json_dict = decoder.decode(json_file.read())
    json_str=json.dumps(json_dict)
    print(json_str)
    d = [('json',json_str),]
    try:
        requests.post('http://localhost:8888/td.darknet.darknet', data=d)
    except:
        return "Upload error."
    return "Uploaded to TD"

'''
def predict(time):
    picpath = 'file=@/home/pi/darkbot/camera/{0:%Y%m%d_%H%M%S}.jpg'.format(time)
    respath = 'p_{0:%Y%m%d_%H%M%S}.jpg'.format(time)
    print(picpath,respath)
    cmd=['curl''-XPOST' '-F' 'http://142.93.244.194:9300/get_predict_image' '>']
    cmd.insert(3,picpath)
    cmd.append(respath)
    try:
        subprocess.check_call(cmd)
        print ("Command finished.")
    except:
        return "Command envailed."
    return respath
'''
