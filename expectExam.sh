sudo yum install expect
自动输入密码脚本
#!/usr/bin/expect -f  
 set ip [lindex $argv 0 ]     //接收第一个参数,并设置IP  
 set password [lindex $argv 1 ]   //接收第二个参数,并设置密码  
 set timeout 10                   //设置超时时间  
 spawn ssh root@$ip       //发送ssh请滶  
 expect {                 //返回信息匹配  
 "*yes/no" { send "yes\r"; exp_continue}  //第一次ssh连接会提示yes/no,继续  
 "*password:" { send "$password\r" }      //出现密码提示,发送密码  
 }  
 interact          //交互模式,用户会停留在远程服务器上面. 
