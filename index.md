---
layout: single
title: Home
permalink: /
author_profile: true
sidebar:
  nav: "main"
---

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

<h2 style="color: #3498db; border-bottom: 1px solid #333; padding-bottom: 10px;">
  <i class="fas fa-satellite-dish"></i> Recent Activity
</h2>

{% assign latest_posts = site.pages | sort: "date" | reverse %}
{% for post in latest_posts limit: 6 %}
  {% if post.title != "Home" and post.title != "Armory & Tools" and post.title != "TryHackMe Writeups" and post.title != "HackTheBox Writeups" %}
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