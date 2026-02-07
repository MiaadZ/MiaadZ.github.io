---
layout: home
title: "CTF Portfolio: MiaadZ (S3Z4R)"
nav_order: 1
sidebar:
  nav: "main"
---

<style>
  .archive__item-title a { text-decoration: none; }
  .list-item {
    border-bottom: 1px solid #333;
    padding-bottom: 10px;
    margin-bottom: 10px;
  }
  .list-meta { font-size: 0.8em; color: #888; }
  /* HIDE THE AUTOMATIC RECENT POSTS AT BOTTOM */
  .entries-grid, .entries-list, .archive { display: none !important; }
  /* But bring back our custom sections */
  #my-custom-content .archive { display: block !important; }
</style>

<div id="my-custom-content">

**Offensive Security & Penetration Testing** | **Top 7% @** [TryHackMe](https://tryhackme.com/p/S3Z4R)

---

<div style="margin-bottom: 30px;">
  <a href="https://tryhackme.com/p/S3Z4R"><img src="https://img.shields.io/badge/TryHackMe-S3Z4R-green?logo=tryhackme&logoColor=white"></a>
  <img src="https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black">
  <img src="https://img.shields.io/badge/Kali_Linux-557C94?logo=kali-linux&logoColor=white">
  <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Burp_Suite-FF6633?logo=burpsuite&logoColor=white">
</div>

## 📡 Recent Activity

{% assign latest_posts = site.pages | sort: "date" | reverse %}
{% for post in latest_posts limit: 5 %}
  {% if post.title != "Home" and post.title != "Armory & Tools" and post.title != "TryHackMe Operations" and post.title != "HackTheBox Operations" %}
  <div class="list-item">
    <h3 class="archive__item-title" style="margin-top: 0; font-size: 1.1em;">
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
    </h3>
    <div class="list-meta">
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

## ⭐ Star of the Month

<style>
  .grid__wrapper { display: flex; flex-wrap: wrap; gap: 15px; }
  .grid__item { flex: 1 1 250px; max-width: 350px; }
  .archive__item { background: transparent !important; border: none !important; padding: 0 !important; }
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
      </article>
    </div>
  {% endfor %}
</div>

</div>