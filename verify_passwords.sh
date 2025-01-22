#!/usr/bin/expect -f
#!/bin/bash

set ip [lindex $argv 0];
set linus_password [lindex $argv 1];
set toc_password [lindex $argv 2];
set root_password [lindex $argv 3];
set timeout 2

spawn ssh linus@$ip

expect "password:" { send "$linus_password\r" }

if { "$toc_password" != "None" } {
    expect " linus>" { send "toc installer $toc_password PSMF\r" }
    expect "TOC>" { send "exit\r" }
}

expect " linus>" { send "su -\r" }
expect "Password:" { send "$root_password\r" }
expect "#" { send "exit\r" }

expect eof

