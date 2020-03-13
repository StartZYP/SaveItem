# encoding=utf8
import requests
import time
import Utils
import json
import imaplib
import base64
import random
import os
import commands
import re
from urllib import unquote
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
def Sessionrequests(getorpost, Session, url, params, data, header):
    while True:  # 一直循环，知道访问站点成功
        if getorpost == "get":
            try:
                # 以下except都是用来捕获当requests请求出现异常时，
                # 通过捕获然后等待网络情况的变化，以此来保护程序的不间断运行
                response = Session.get(url, params=params, headers=header, timeout=20)
                break
            except requests.exceptions.ConnectionError:
                print('ConnectionError -- please wait 3 seconds')
                time.sleep(3)
            except requests.exceptions.ChunkedEncodingError:
                print('ChunkedEncodingError -- please wait 3 seconds')
                time.sleep(3)
            except:
                print('Unfortunitely -- An Unknow Error Happened, Please wait 3 seconds')
                time.sleep(3)
        else:
            try:
                response = Session.post(url, params=params, data=data, headers=header, timeout=20)
                break
            except requests.exceptions.ConnectionError:
                print('ConnectionError -- please wait 3 seconds')
                time.sleep(3)
            except requests.exceptions.ChunkedEncodingError:
                print('ChunkedEncodingError -- please wait 3 seconds')
                time.sleep(3)
            except:
                print('Unfortunitely -- An Unknow Error Happened, Please wait 3 seconds')
                time.sleep(3)
    return response

def regmcbbs(url,username,password):
    url = url.replace('http://sctrack.sc.gg/track/click/','').replace('.html','')
    newurl = unquote(json.loads(base64.b64decode(url))['link']).encode('unicode-escape').decode('string_escape')
    print(newurl)
    session = requests.session()
    hashcode = unquote(Utils.getmidstring(newurl,"hash=","&email")).encode('unicode-escape').decode('string_escape')
    email = Utils.getmidstring(newurl,"email=",".com")+".com"
    getregisterparams = {
        'mod': 'register',
        'hash': hashcode,
        'email': email
    }
    getregisterheard = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        'Referer': 'https://www.mcbbs.net/member.php?mod=register&hash=bf50xZYCbLuiy8qUDtyOamLwExkQ%2F%2FwfBcxXIY3KE9nHMV%2B4l7s6q4Tv5Cc%2Bfz6YEr7%2Ff3SIj70u6A&email=id5jboj6x@21cn.com'
    }
    response = Sessionrequests('get', session, 'https://www.mcbbs.net/member.php', params= getregisterparams,header= getregisterheard,data=None)
    idhash = Utils.getHash(response.text)
    agreebbrule = Utils.getagreebbrule(response.text)
    print(idhash)
    print(agreebbrule)
    registerparams = {
        'mod': 'register',
        'inajax': '1'
    }
    registerheard = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Referer': 'https://www.mcbbs.net/member.php?mod=register',
        'upgrade-insecure-requests':'1',
    }
    jsonlate = GetGeetest1(session,newurl)
    readregister = {
        'regsubmit': 'yes',
        'formhash': idhash,
        'referer': 'https://www.mcbbs.net/',
        'mcbbsemail': email,
        'mcbbsusername': username,
        'mcbbspassword': password,
        'mcbbspasswordreset': password,
        'geetest_challenge': jsonlate['data']['challenge'],
        'geetest_validate': jsonlate['data']['validate'],
        'geetest_seccode': jsonlate['data']['validate'] + '|jordan',
        'agreebbrule': agreebbrule,
        'activationauth': '',
        'hash': hashcode
    }
    print(readregister)
    response = Sessionrequests('post', session, 'https://www.mcbbs.net/member.php', registerparams, readregister, registerheard)
    print(response.text)
    return session




def SendEmail(EmailAddress):
    session = requests.session()
    getregisterparams = {
        'mod': 'register'
    }
    getregisterheard = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        'Referer': 'https://www.mcbbs.net/member.php?mod=register&hash=bf50xZYCbLuiy8qUDtyOamLwExkQ%2F%2FwfBcxXIY3KE9nHMV%2B4l7s6q4Tv5Cc%2Bfz6YEr7%2Ff3SIj70u6A&email=id5jboj6x@21cn.com'
    }
    response = Sessionrequests('get', session, 'https://www.mcbbs.net/member.php', params= getregisterparams,header= getregisterheard,data=None)
    idhash = Utils.getHash(response.text)
    agreebbrule = Utils.getagreebbrule(response.text)
    print(idhash)
    print(agreebbrule)
    jsonlate = GetGeetest(session)

    registerheard = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Referer': 'https://www.mcbbs.net/member.php?mod=register',
        'upgrade-insecure-requests':'1',
    }

    registerparams = {
        'mod': 'register',
        'inajax': '1'
    }
    # readregister = {
    #     'regsubmit': 'yes',
    #     'formhash': idhash,
    #     'referer': 'https://www.mcbbs.net/portal.php',
    #     'mcbbsemail': EmailAddress,
    #     'handlekey': 'sendregister',
    #     'agreebbrule': agreebbrule,
    #     'activationauth': '',
    #     'hash':''
    # }
    readregister = {
        'regsubmit': 'yes',
        'formhash': idhash,
        'referer': 'https://www.mcbbs.net/portal.php',
        'mcbbsemail': EmailAddress,
        'handlekey': 'sendregister',
        'geetest_challenge': jsonlate['data']['challenge'],
        'geetest_validate': jsonlate['data']['validate'],
        'geetest_seccode': jsonlate['data']['validate'] + '|jordan',
        'agreebbrule': agreebbrule,
        'activationauth': '',
        'hash':''
    }
    print(readregister)
    # response = session.post('https://www.mcbbs.net/member.php', params=registerparams, data=readregister, headers=registerheard)
    response = Sessionrequests('post', session, 'https://www.mcbbs.net/member.php', registerparams, readregister, registerheard)
    print(response.text)


def GetGeetest(session):
    count = 0
    inflag = 0
    while (inflag == 0):
        count += 1
        geetestparmas = {
            'id': 'geetest3',
            'model': 'start',
            't': str(time.time())
        }
        response = session.get('https://www.mcbbs.net/plugin.php', params=geetestparmas)
        jsonobj = json.loads(response.text)
        challengecodeparmas = {
            'gt': jsonobj['gt'],
            'challenge': jsonobj['challenge'],
            'referer': 'https://www.mcbbs.net/member.php?mod=register',
            'secretkey': '289c3c9aaa064ea9896a0af6deaf7510',
            'devCode': '900ec168b8ae4b57997e2e681508b4ce',
            'wtype': 'geetest'
        }
        temptext = Sessionrequests('get', session, 'http://api.ddocr.com/api/gateway.jsonp', challengecodeparmas, None,
                                   header=None)
        print(str(count) + "正在识别验证")
        # print(temptext.text)
        if len(temptext.text) > 100:
            jsonobj = json.loads(temptext.text)
            print(jsonobj['data']['challenge'])
            print(jsonobj['data']['validate'])
            return jsonobj
        if count == 20:
            exit()


def GetGeetest1(session,newurl):
    count = 0
    inflag = 0
    while (inflag == 0):
        count += 1
        geetestparmas = {
            'id': 'geetest3',
            'model': 'start',
            't': str(time.time())
        }
        response = session.get('https://www.mcbbs.net/plugin.php', params=geetestparmas)
        jsonobj = json.loads(response.text)
        challengecodeparmas = {
            'gt': jsonobj['gt'],
            'challenge': jsonobj['challenge'],
            'referer': newurl,
            'secretkey': '289c3c9aaa064ea9896a0af6deaf7510',
            'devCode': '900ec168b8ae4b57997e2e681508b4ce',
            'wtype': 'geetest'
        }
        temptext = Sessionrequests('get', session, 'http://api.ddocr.com/api/gateway.jsonp', challengecodeparmas, None,
                                   header=None)
        print(str(count) + "正在识别验证")
        # print(temptext.text)
        if len(temptext.text) > 100:
            jsonobj = json.loads(temptext.text)
            print(jsonobj['data']['challenge'])
            print(jsonobj['data']['validate'])
            return jsonobj
        if count == 20:
            exit()

def getmidstring(html, start_str, end):
    #print(html)
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()

def read_email_from_gmail(Email , password):
        mail = imaplib.IMAP4_SSL('imap-mail.outlook.com', 993)
        mail.login(Email, password)
        mail.select('Junk')
        (retcode, messages) = mail.search(None, 'all')
        print(str(messages[0]))
        if messages[0] != b'1':
            mail.select('inbox')
            (retcode, messages) = mail.search(None, 'all')
            print(messages)
        result, email_data = mail.fetch('1', '(RFC822)')
        msg = str(email_data[0][1].decode('utf-8')).split('MIME-Version: 1.0')[1].encode('utf-8')
        msg = str(base64.b64decode(msg))
        msg = getmidstring(msg, 'download" href="', '"')
        print(msg)
        with open('url.txt', 'a') as f:
            f.write(msg+'\n')
            f.close()

def getusername():
    getregisterparams = {
        'mod': 'space',
        'uid': random.randint(100000, 3007075)
    }
    session = requests.session()
    response = Sessionrequests('get', session, 'https://www.mcbbs.net/home.php', params= getregisterparams,header= None,data=None)
    #print(response.text)
    username = Utils.getmidstring(response.text,'class="mt">','</h2>')
    randomstr = [
        'Rz','Bq','qq','Pz','Lc','11','zs','32','、c','5c','7q','_9','Me','O_','帅','_、','_c'
    ]
    if username==None:
        print("空")
        getusername()
    #print(len(randomstr))
    #print(randomstr[random.randint(0,len(randomstr)-1)])
    print(username)
    username = username[:-2]+randomstr[random.randint(0,len(randomstr)-1)]
    return username

def ChangeIp():
    print("Ip 正在更换")
    os.system("/sbin/ifdown ppp0")
    os.system("/sbin/ifup ppp0")
    # global ip
    hostip = commands.getstatusoutput("curl icanhazip.com")[1].split('\n')[-1]
    print(hostip)
    flag = re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", hostip)
    while not flag:
        print("Ip 正在更换")
        print("出问题中")
        os.system("/sbin/ifdown ppp0")
        os.system("/sbin/ifup ppp0")
        # global ip
        hostip = commands.getstatusoutput("curl icanhazip.com")[1].split('\n')[-1]
        flag = re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", hostip)
        print(hostip)

def TaskDo(session):
    Taskparams = {
        'mod': 'task'
    }
    response = Sessionrequests('get', session, 'https://www.mcbbs.net/home.php', params= Taskparams,header= None,data=None)
    taskhash = Utils.getHash(response.text)
    # 新人徽章
    Taskparams = {
        'mod': 'task',
        'do': 'apply',
        'id': '6',
        'hash': taskhash
    }
    Sessionrequests('get', session, 'https://www.mcbbs.net/home.php', params= Taskparams,header= None,data=None)
    Taskparams = {
        'mod': 'task',
        'do': 'draw',
        'id': '6',
        'hash': taskhash
    }
    Sessionrequests('get', session, 'https://www.mcbbs.net/home.php', params= Taskparams,header= None,data=None)
    # 新手升级礼包7
    Taskparams = {
        'mod': 'task',
        'do': 'apply',
        'id': '7',
        'hash': taskhash
    }
    Sessionrequests('get', session, 'https://www.mcbbs.net/home.php', params= Taskparams,header= None,data=None)
    Taskparams = {
        'mod': 'task',
        'do': 'draw',
        'id': '7',
        'hash': taskhash
    }
    Sessionrequests('get', session, 'https://www.mcbbs.net/home.php', params= Taskparams,header= None,data=None)
    # 每日活跃得钻石
    Taskparams = {
        'mod': 'task',
        'do': 'apply',
        'id': '3',
        'hash': taskhash
    }
    Sessionrequests('get', session, 'https://www.mcbbs.net/home.php', params= Taskparams,header= None,data=None)
    Taskparams = {
        'mod': 'task',
        'do': 'draw',
        'id': '3',
        'hash': taskhash
    }
    Sessionrequests('get', session, 'https://www.mcbbs.net/home.php', params= Taskparams,header= None,data=None)
    # 50金初来
    Taskparams = {
        'mod': 'task',
        'do': 'apply',
        'id': '26',
        'hash': taskhash
    }
    Sessionrequests('get', session, 'https://www.mcbbs.net/home.php', params= Taskparams,header= None,data=None)
    Taskparams = {
        'mod': 'task',
        'do': 'draw',
        'id': '26',
        'hash': taskhash
    }
    Sessionrequests('get', session, 'https://www.mcbbs.net/home.php', params= Taskparams,header= None,data=None)
    # 周人气
    Taskparams = {
        'mod': 'task',
        'do': 'apply',
        'id': '23',
        'hash': taskhash
    }
    Sessionrequests('get', session, 'https://www.mcbbs.net/home.php', params= Taskparams,header= None,data=None)
    Taskparams = {
        'mod': 'task',
        'do': 'draw',
        'id': '23',
        'hash': taskhash
    }
    Sessionrequests('get', session, 'https://www.mcbbs.net/home.php', params= Taskparams,header= None,data=None)


def SendEmailfun():
    with open('./email.txt') as f:
        for line in f.readlines():
            info = line.split("----")
            SendEmail(info[0])
            print("SendEmail:"+info[0], info[1])
def GetEmail():
    with open('./email.txt') as f:
        for line in f.readlines():
            info = line.split("----")
            print("GetEmailUrl:"+info[0], info[1])
            read_email_from_gmail(info[0],info[1])
def Reg():
    with open('./url.txt') as f:
        for line in f.readlines():
            username = getusername()
            ChangeIp()
            session = regmcbbs(line,username,'asd123456')
            print("DonewTask")
            TaskDo(session)
            with open('newpassword.txt', 'a') as f:
                f.write(username+'----asd123456'+'\n')
                f.close()


if __name__ == '__main__':
    SendEmailfun()
    with open('./email.txt') as f:
        for line in f.readlines():
            info = line.split("----")
            print("GetEmailUrl:"+info[0], info[1])
            read_email_from_gmail(info[0],info[1])
    with open('./url.txt') as f:
        for line in f.readlines():
            username = getusername()
            ChangeIp()
            session = regmcbbs(line,username,'asd123456')
            print("DonewTask")
            TaskDo(session)
            with open('newpassword.txt', 'a') as f:
                f.write(username+'----asd123456'+'\n')
                f.close()
    print("全部完成")

