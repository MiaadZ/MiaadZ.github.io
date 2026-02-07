---
layout: single
title: Home
permalink: /
author_profile: true
sidebar:
  nav: "main"
---

<style>
  .page__title { display: none; }
  
  /* STANDARD LIST STYLE */
  .list-item {
    display: flex; justify-content: space-between; align-items: center;
    border-bottom: 1px solid #333; padding: 10px 0;
  }
  .list-meta { font-size: 0.85em; color: #888; white-space: nowrap; margin-left: 15px; }

  /* FANCIER STARRED STYLE */
  .starred-item {
    background: linear-gradient(90deg, rgba(241, 196, 15, 0.1) 0%, rgba(0,0,0,0) 100%);
    border-left: 4px solid #f1c40f; /* Gold Bar */
    padding: 15px;
    margin-bottom: 10px;
    border-radius: 0 4px 4px 0;
    transition: transform 0.2s;
  }
  .starred-item:hover { transform: translateX(5px); }
  .starred-title { font-size: 1.1em; font-weight: bold; color: #f1c40f !important; }
</style>

<h2 style="color: #f1c40f; border-bottom: 1px solid #333; padding-bottom: 10px;">
  <i class="fas fa-crown"></i> Hall of Fame
</h2>

{% assign starred_posts = site.pages | where: "starred", true | sort: "date" | reverse %}
{% for post in starred_posts limit: 3 %}
  <div class="starred-item">
    <div>
      <a href="{{ post.url | relative_url }}" class="starred-title" style="text-decoration: none;">
        {{ post.title }}
      </a>
      <div style="font-size: 0.9em; opacity: 0.8; margin-top: 4px;">
        {{ post.tags | join: ", " }}
      </div>
    </div>
    
    <div class="list-meta">
      <b style="color: #ccc;">{{ post.date | date: "%b %Y" }}</b><br>
      {{ post.difficulty }}
    </div>
  </div>
{% endfor %}

<br>

<h2>📡 Recent Activity</h2>

{% assign latest_posts = site.pages | sort: "date" | reverse %}
{% for post in latest_posts limit: 6 %}
  {% if post.title != "Home" and post.title != "Armory & Tools" and post.title != "TryHackMe Operations" and post.title != "HackTheBox Operations" %}
  <div class="list-item">
    <a href="{{ post.url | relative_url }}" style="font-weight: bold; text-decoration: none;">{{ post.title }}</a>
    <div class="list-meta">
      {{ post.date | date: "%Y-%m-%d" }} | 
      <span style="color: {% if post.difficulty == 'Easy' %}#2ecc71{% elsif post.difficulty == 'Medium' %}#f1c40f{% else %}#e74c3c{% endif %};">
        {{ post.difficulty }}
      </span>
    </div>
  </div>
  {% endif %}
{% endfor %}