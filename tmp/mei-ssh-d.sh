#!/usr/bin/expect -f 

#set ip 45.33.111.169 
set ip 45.32.95.172 
set username zsgqixi
set password ssh789     
set timeout 10        
spawn ssh -o TCPKeepAlive=yes -o ServerAliveInterval=10 -o ServerAliveCountMax=3 -p22 -N -D *:17070 $username@$ip         
expect {                 
"*yes/no" { send "yes\r"; exp_continue}  
"*password:" { send "$password\r" }      
}  
interact   
