#!/bin/sh
#coding=utf-8
import os,datetime,time
import subprocess
import daemonToolBase


if __name__ == '__main__':
    shfile = '/root/bin/python/daemonTool/mei-ssh-d.sh'
    cmd = '/usr/bin/expect -f %s' % shfile
    daemonToolBase.daemonToolBase(cmd.split()).run(daemon=False)
