#!/bin/sh
#coding=utf-8
import subprocess,time,os,sys,signal

class daemonToolBase(object):
    """
        进程守护基类, 适用于守护长期运行的程序, 类似linux下的 daemontools, 提供如下功能
        1.   当程序挂掉时自动启动
        2.   运行时，每隔10秒运行一次自定义方法 p_is_ok 判断进程是否处于正常运行状态, 连续三次返回False, 将自动重启进程
    """
    p = None
    notoknum = 0
    cmd = ''
    logfile = ''
    islog = False
    _stop = False

    def __init__(self, cmd, logfile='log/log.log', islog=False): 
        self.islog = islog
        self.cmd = cmd
        self.logfile = "%s/%s" % (os.path.abspath('.'), logfile)

    def on_signal(self, signal_num, stack):
        self.stop()
        self.log('signal_num [%d]' % (signal_num))

    def run(self, daemon=True):
        if daemon:
            signal.signal(signal.SIGTERM, self.on_signal)
            signal.signal(signal.SIGINT, self.on_signal)
            
            daemonize(stderr="%s/log/ProcessMonitorError.log" % os.path.abspath('.'))            

            self.prun()           
        else:
            self.prun()

    def prun(self):

        self.p_start()
        while True:
            time.sleep(10)
            if self._stop:
                self.p_stop()
                self.log('stoped')
                break

            if self.p.poll() != None:
                self.log("progress[%d] is finish" % self.p.pid)

                #启动
                self.p_start()
            else:
                self.log("progress[%d] is runing" % self.p.pid)

                #检测程序是否正常运行, 3次后重启进程
                if not self.p_is_ok():
                    self.notoknum = self.notoknum + 1
                    if self.notoknum > 3:
                        self.p_restart()
                        self.notoknum=0
                else:
                    self.notoknum=0


    def p_is_ok(self):
        '''
            判断程序是否正常运行
        '''
        return True

    def p_restart(self):
        '''
            重启进程
        '''
        self.p_stop()
        self.p_start()

    def p_stop(self):
        '''
            停止进程
        '''
        self.log('progress[%d] stop' % self.p.pid)
        self.p.terminate()

    def p_start(self):    
        '''
            启动进程
        '''    
        self.log('progress start ...')
        self.p = subprocess.Popen(self.cmd, shell=False, stdout=subprocess.PIPE)
        self.log('progress[%d] start ok' % self.p.pid)

    def stop(self):
        self._stop = True

    def log(self, sstr):
        '''
            记录日志
        '''
        if not self.islog:
            return 0
        f = open(self.logfile, 'a+')
        st = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        f.write("[%s] %s\n" % (st, sstr))
        f.close()
        
def daemonize(stdin='/dev/null',stdout= '/dev/null', stderr= 'dev/null'):
    '''Fork当前进程为守护进程，重定向标准文件描述符
        （默认情况下定向到/dev/null）
    '''
    #Perform first fork.
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  #first parent out
    except OSError, e:
        sys.stderr.write("fork #1 failed: (%d) %s\n" %(e.errno, e.strerror))
        sys.exit(1)

    #从母体环境脱离
    os.chdir("/")
    os.umask(022)
    os.setsid()
    #执行第二次fork
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0) #second parent out
    except OSError, e:
        sys.stderr.write("fork #2 failed: (%d) %s]n" %(e.errno,e.strerror))
        sys.exit(1)
    
    #进程已经是守护进程了，重定向标准文件描述符
    for f in sys.stdout, sys.stderr: f.flush()
    si = file(stdin, 'r')
    so = file(stdout,'a+')
    se = file(stderr,'a+',0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())
    
    
