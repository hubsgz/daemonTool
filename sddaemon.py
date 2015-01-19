#!/bin/sh
#coding=utf-8
import os,datetime,time
import subprocess
import daemonToolBase

"""
    这是一个daemonTool使用示例
"""

class sddaemon(daemonToolBase.daemonToolBase):
    """
        ssh 隧道进程守护
    """
    def p_is_ok(self):
        '''
            判断隧道是否通畅， 不通畅返回False
        '''
        p = subprocess.Popen("ssh root@122.122.122.122 'svn info svn://localhost:23690/www.test.com/index.html | wc -l'", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        timeout = 10
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        while p.poll() is None:
            time.sleep(1)
            if end_time <= datetime.datetime.now():
                self.log('p_is_ok timeout')
                return False
        (stdoutdata , stderrdata) = p.communicate()
        linenum = stdoutdata
            
        linenum = linenum.strip()
        if linenum == '0':
            return False
        else:
            return True

if __name__ == '__main__':

    cmd = 'ssh -o TCPKeepAlive=yes -o ServerAliveInterval=2 -o ServerAliveCountMax=2 -N -R 23690:localhost:3690 root@122.122.122.122'
    sddaemon(cmd.split()).run()
