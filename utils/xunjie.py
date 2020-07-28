import requests
import os
import uuid
import json
import time
import datetime
import subprocess


def videoToText(videoPath):
    text = ""
    audioPath = videoToAudio(videoPath)
    if audioPath != None:
        text = audioToText(audioPath)
    return text


def netVideoToText(videoUrl):
    text = ""
    videoPath = download(videoUrl)
    audioPath = videoToAudio(videoPath)
    if audioPath != None:
        text = audioToText(audioPath)
    return text


def videoToAudio(videoPath):
    videoDir = videoPath[:videoPath.rindex(os.sep) + 1]
    audioPath = videoDir + str(uuid.uuid1()).replace("-", "") + ".m4a"

    #视频抽成音频
    command = "ffmpeg -i {} -vn -y -acodec copy {}".format(videoPath, audioPath)
    try:
        resCode = subprocess.call(command, shell=True)
        if resCode == 0:
            print("videoToAudio success")
            return audioPath
        else:
            print("videoToAudio filed")

    except Exception as e:
        print("videoToAudio error:", e)

    return None


def netVideoToAudio(videoUrl):

    videoPath = download(videoUrl)
    return videoToAudio(videoPath)


def audioToText(audioPath):

    originalFileName =  "1_" + str(uuid.uuid1()).replace("-", "") + ".mp3"
    md5 = str(uuid.uuid1()).replace("-", "")
    fileName  = str(uuid.uuid1()).replace("-", "") + "_" + originalFileName;

    url = "https://user.api.hudunsoft.com/v1/alivoice/uploadaudiofile?r=0.14161597935633452"
    url2 = "https://user.api.hudunsoft.com/v1/alivoice/md5Totext"
    header = {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) voicedesktop/1.5.1 Chrome/66.0.3359.181 Electron/3.0.13 Safari/537.36",
        "Accept-Encoding": "gzip",
        "charset": "utf-8",
        "Connection": "Keep-Alive"
    }

    header2 = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) voicedesktop/1.5.1 Chrome/66.0.3359.181 Electron/3.0.13 Safari/537.36",
        "Accept-Encoding": "gzip",
        "charset": "utf-8",
        "Connection": "Keep-Alive"
    }

    data1 = {
        "action": "Begin",
        "fileName": fileName,
        "md5": md5
    }

    files = {'file': open(audioPath, 'rb')}

    data2 = {
        "action": "Store",
        "pos": 0,
        "size": os.path.getsize(audioPath),
        "md5": md5
    }

    data3 = {
        "action": "End",
        "fileName": fileName,
        "md5": md5
    }

    data = {
        "client": "mac",
        "source": "335",
        "soft_version": "V1.5.0",
        "device_id": "824744e1f51647ba9e91b4b5719a6aa0",
        "md5": md5,
        "fileName": originalFileName,
        "title": originalFileName,
        "language": "zh"
    }

    response = requests.post(url, verify=False, headers = header, data = data1)
    response.encoding = 'utf-8'
    html = response.text
    print(html)

    response = requests.post(url, verify=False, headers = header2, data = data2, files = files)
    response.encoding='utf-8'
    html = response.text
    print(html)

    response = requests.post(url, verify=False, headers = header, data = data3)
    response.encoding = 'utf-8'
    html = response.text
    print(html)

    text = ""
    i = 0
    while i < 30:
        i = i + 1
        time.sleep(10)
        response = requests.post(url2, verify=False, headers=header, data=data)
        response.encoding = 'utf-8'
        html = response.text
        result = json.loads(html)
        if(result['code'] == 0):
            datas = result['data']
            for data in datas:
                text = text + data['text']
            break

    return text


def download(videoUrl, localFileDir):

    fileName = str(uuid.uuid1()).replace("-", "")
    filePath = localFileDir

    # 增加日期文件夹
    os.chdir(filePath)
    date = datetime.datetime.now().strftime('%Y%m%d')
    if not os.path.exists(date):
        os.makedirs(date)

    filePath = filePath + os.sep + date
    filePath = filePath + os.sep + fileName + ".mp4"

    down_res = requests.get(videoUrl, verify=False)
    with open(filePath, "wb") as code:
        code.write(down_res.content)

    return filePath


if __name__ == "__main__":

    # audioPath = videoToAudio("/Users/chenyaozong/xigua/20200715/54岁林志炫大病后狂举杠铃，胳膊和腿一样细，骨瘦如柴似纸片人.mp4")
    # if audioPath != None:
    #     text = audioToText(audioPath)
    #     print(text)

    text = audioToText("/Users/chenyaozong/Downloads/wKg5Hl8eKX-xjK0LACstKJLJAso686.m4a")
    print(text)