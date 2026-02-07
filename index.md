---
layout: home
title: "MiaadZ (S3Z4R)"
nav_order: 1
sidebar:
  nav: "main"
---

**Offensive Security & Penetration Testing** | **Top 7% @**[TryHackMe](https://tryhackme.com/p/S3Z4R)

---

<div style="margin-bottom: 30px;">
  <a href="https://tryhackme.com/p/S3Z4R"><img src="https://img.shields.io/badge/TryHackMe-S3Z4R-green?logo=tryhackme&logoColor=white"></a>
  <img src="https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black">
  <img src="https://img.shields.io/badge/Kali_Linux-557C94?logo=kali-linux&logoColor=white">
  <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Burp_Suite-FF6633?logo=burpsuite&logoColor=white">
  <img src="https://img.shields.io/badge/Nmap-0D93DA?logo=nmap&logoColor=white">
</div>

## 📡 Recent Activity

<ul>
  {% assign latest_posts = site.pages | sort: "date" | reverse %}
  {% for post in latest_posts limit: 6 %}
    {% if post.title != "Home" and post.title != "Armory & Tools" and post.title != "TryHackMe Operations" and post.title != "HackTheBox Operations" %}
    <li style="margin-bottom: 10px;">
      <a href="{{ post.url | relative_url }}" style="font-weight: bold; font-size: 1.1em;">{{ post.title }}</a> 
      <small style="color: #aaa;">
        — {{ post.date | date: "%Y-%m-%d" }} 
        [{{ post.difficulty }} {{ post.os }}]
      </small>
    </li>
    {% endif %}
  {% endfor %}
</ul>

---

## ⭐ Star of the Month

<style>
  /* Grid Layout */
  .grid__wrapper { display: flex; flex-wrap: wrap; gap: 15px; }
  .grid__item { flex: 1 1 250px; max-width: 350px; }
  
  /* Remove Black Background & Borders */
  .archive__item { 
    background: transparent !important; 
    border: none !important; 
    padding: 0 !important;
  }
  
  /* Fix Title Styling in Grid */
  .archive__item-title { margin-top: 0; font-size: 1.1em; }
  .archive__item-title a { text-decoration: none; }
  
  /* Align Metadata */
  .page__meta { font-size: 0.8em; margin-top: 5px; }
</style>

<div class="grid__wrapper">
  {% assign starred_posts = site.pages | where: "starred", true | sort: "date" | reverse %}
  
  {% for post in starred_posts limit: 3 %}
    <div class="grid__item">
      <article class="archive__item">
        <h3 class="archive__item-title">
          <a href="{{ post.url | relative_url }}">🏆 {{ post.title }}</a>
        </h3>
        
        <p class="page__meta">
           <b>{{ post.date | date: "%B %Y" }}</b><br>
           <span style="color: #3498db;">{{ post.os }}</span> | 
           <span style="color: {% if post.difficulty == 'Easy' %}#2ecc71{% elsif post.difficulty == 'Medium' %}#f1c40f{% else %}#e74c3c{% endif %};">
             {{ post.difficulty }}
           </span>
        </p>
        
        <p style="font-size: 0.85em; opacity: 0.8;">
          {% if post.tags %}
            <i>{{ post.tags | join: ", " }}</i>
          {% endif %}
        </p>
      </article>
    </div>
  {% endfor %}
</div>