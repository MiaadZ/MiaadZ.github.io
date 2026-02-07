---
layout: single
title: Home
permalink: /
author_profile: true
sidebar:
  nav: "main"
---

<style>
  /* Remove the default page title since we have a custom header */
  .page__title { display: none; }
  
  /* List View Styling */
  .list-item {
    border-bottom: 1px solid #333;
    padding-bottom: 10px;
    margin-bottom: 10px;
  }
  .archive__item-title a { text-decoration: none; }
</style>

# CTF Portfolio: MiaadZ (S3Z4R)
**Offensive Security & Penetration Testing** | **Top 7% @** [TryHackMe](https://tryhackme.com/p/S3Z4R)

---

<div style="margin-bottom: 30px;">
  <a href="https://tryhackme.com/p/S3Z4R"><img src="https://img.shields.io/badge/TryHackMe-S3Z4R-green?logo=tryhackme&logoColor=white"></a>
  <img src="https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black">
  <img src="https://img.shields.io/badge/Kali_Linux-557C94?logo=kali-linux&logoColor=white">
  <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Burp_Suite-FF6633?logo=burpsuite&logoColor=white">
</div>

## Recent Activity

{% assign latest_posts = site.pages | sort: "date" | reverse %}
{% for post in latest_posts limit: 5 %}
  {% if post.title != "Home" and post.title != "Armory & Tools" and post.title != "TryHackMe Operations" and post.title != "HackTheBox Operations" %}
  <div class="list-item">
    <h3 class="archive__item-title" style="margin-top: 0; font-size: 1.1em;">
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
    </h3>
    <div style="font-size: 0.8em; color: #888;">
      <i class="far fa-calendar-alt"></i> {{ post.date | date: "%Y-%m-%d" }} | 
      <span style="color: #3498db;">{{ post.os }}</span> | 
      <span style="color: {% if post.difficulty == 'Easy' %}#2ecc71{% elsif post.difficulty == 'Medium' %}#f1c40f{% else %}#e74c3c{% endif %};">
        {{ post.difficulty }}
      </span>
    </div>
  </div>
  {% endif %}
{% endfor %}

---

## Star of the Month

<style>
  /* HALL OF FAME GRID FIX */
  .grid__wrapper {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
  }
  
  /* On mobile, stack them nicely */
  @media (max-width: 768px) {
    .grid__wrapper { grid-template-columns: 1fr; }
  }

  /* Remove Black Background & Borders */
  .archive__item { 
    background: transparent !important; 
    border: none !important; 
    padding: 0 !important;
  }
  
  /* Fix Title Styling */
  .archive__item-title { margin-top: 0; font-size: 1.1em; }
  .archive__item-title a { text-decoration: none; }
  
  /* HIDE FEED IN FOOTER */
  .page__footer-follow { display: none !important; } 
  .page__footer .fas.fa-rss { display: none !important; }
</style>

<div class="grid__wrapper">
  {% assign starred_posts = site.pages | where: "starred", true | sort: "date" | reverse %}
  {% for post in starred_posts limit: 3 %}
    <div class="grid__item">
      <article class="archive__item">
        <h3 class="archive__item-title">
          <a href="{{ post.url | relative_url }}">🏆 {{ post.title }}</a>
        </h3>
        <p class="page__meta" style="font-size: 0.8em;">
           <b>{{ post.date | date: "%B %Y" }}</b><br>
           <span style="color: #3498db;">{{ post.os }}</span> | 
           <span style="color: {% if post.difficulty == 'Easy' %}#2ecc71{% elsif post.difficulty == 'Medium' %}#f1c40f{% else %}#e74c3c{% endif %};">
             {{ post.difficulty }}
           </span>
        </p>
      </article>
    </div>
  {% endfor %}
</div>