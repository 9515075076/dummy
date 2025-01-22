#!/usr/bin/expect -f
#!/bin/bash

set ip [lindex $argv 0];
set linus_password [lindex $argv 1];
set timeout 2

log_user 0;
spawn ssh linus@$ip
expect "password:" { send "$linus_password\r"}

expect " linus>" { send "sqlminus -l pfmconfig@PSMF \"set colsep ,\" \"select service.name||','||service.ri||','||host.hostname||','||parttion.smf_ref FROM service INNER JOIN parttion ON service.ri=parttion.serv_ref INNER JOIN host ON host.ri=parttion.host_ref where service.grp_bep is not NULL and service.name NOT LIKE 'pfm%' ORDER BY parttion.host_ref\"\r" }
expect "parttion.host_ref\""
log_user 1;

expect "SQL>" { send "exit\r" }
expect " linus>"
log_user 0;
expect eof