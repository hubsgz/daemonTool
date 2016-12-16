#!/usrlbin/python
#coding=utf-8
import urllib
import urllib2
import cookielib
import re,os
import daemonToolBase
from random import choice

class app(daemonToolBase.daemonToolBase):

    def p_start(self):    
        '''
            启动进程
        '''    
        pre_start()
        super(app, self).p_start()
        #self.log('progress start ...')
        #self.p = subprocess.Popen(self.cmd, shell=False, stdout=subprocess.PIPE)
        #self.log('progress[%d] start ok' % self.p.pid)


"""
#获取Cookiejar对象（存在本机的cookie消息）
cj = cookielib.CookieJar()
#自定义opener,并将opener跟CookieJar对象绑定
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)')]
#安装opener,此后调用urlopen()时都会使用安装过的opener对象
urllib2.install_opener(opener)
url = "http://sde.snnu.edu.cn/pubclass/zszq/loadright.ashx"
req = urllib2.Request(url, urllib.urlencode({"parentID":"40"}))
req.add_header("Referer","http://xxoo.com")
resp = urllib2.urlopen(req)
print resp.read()
"""

def pre_start():

    header = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
        "Connection":"keep-alive",
        "Cookie":"PHPSESSID=g0slanheoi5defiv481u636nm1; hm_t_vis_5434=0; Hm_lvt_11ed59c7dea4b08cc9bcbee9548cb74c=1421586335; Hm_lpvt_11ed59c7dea4b08cc9bcbee9548cb74c=1421586335",
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }

    url = 'http://boafanx.tabboa.com/free/'
    req = urllib2.Request(url, headers=header)
    webpage = urllib2.urlopen(req)

    html = webpage.read()


    p = re.compile('<pre><code>(.*?)</code></pre>', re.I | re.M | re.S )
    rs = p.findall(html)
    print rs

    if rs:
        servers = [1,3]
        cnum = choice(servers)
        ls = rs[cnum].strip().split('\n')
        
        data = []
        num = 0
        for r in ls:
            num = num + 1
            tmp =  r.split('：')
            data.append(tmp[1])
        print data

        cmd = r"""#!/usr/bin/expect -f 

    set ip %s 
    set password eyo3     
    set timeout 10        
    spawn ssh -p%s -o TCPKeepAlive=yes -o ServerAliveInterval=5 -o ServerAliveCountMax=5 -N -D *:37070 boa@$ip         
    expect {                 
    "*yes/no" { send "yes\r"; exp_continue}  
    "*password:" { send "$password\r\r\n" }      
    }  
    interact 
        """ % (data[0], data[1])
        
        shfile = '/tmp/sd.sh'
        f = open(shfile, 'w+')
        f.write(cmd)
        f.close()
        os.system('chmod +x %s' % shfile)
        
    else:
        print 'no match'

if __name__ == '__main__':
    shfile = '/tmp/sd.sh'
    cmd = '/usr/bin/expect -f %s' % shfile
    app(cmd.split()).run(daemon=False)
    #os.system('/usr/bin/expect -f %s' % shfile)

