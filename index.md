---
layout: single
title: Home
permalink: /
author_profile: true
sidebar:
  nav: "main"
---

<div style="
    background: #111; 
    border-left: 4px solid #3498db; 
    padding: 15px; 
    margin-bottom: 30px; 
    font-family: monospace; 
    color: #bbb;
    font-size: 0.9em;
">
  <p style="margin: 0; margin-bottom: 5px;">
    <strong style="color: #3498db;">root@S3Z4R:~$</strong> whoami
  </p>
  <p style="margin: 0; line-height: 1.5;">
    I am a cybersecurity enthusiast and CTF player focusing on 
    <span style="color: #ccc; font-weight: bold;">Offensive Security</span> and 
    <span style="color: #ccc; font-weight: bold;">Penetration Testing</span>. 
    This portfolio serves as my personal knowledge base and documentation 
    archive for CTF writeups, penetration testing methodologies, and offensive security tools.
  </p>
</div>

<br>

<h2 style="color: #f1c40f; border-bottom: 1px solid #333; padding-bottom: 10px;">
  <i class="fas fa-crown"></i> Hall of Fame
</h2>

{% assign starred_posts = site.pages | where: "starred", true | sort: "date" | reverse %}
{% for post in starred_posts limit: 3 %}
  <div class="starred-item">
    <div style="margin-bottom: 5px;">
      <a href="{{ post.url | relative_url }}" class="starred-title">
        {{ post.title }}
      </a>
    </div>
    
    <div style="font-size: 0.9em; color: #aaa; margin-bottom: 5px;">
      {{ post.tags | join: ", " }}
    </div>
    
    <div style="font-size: 0.85em; color: #f1c40f; font-weight: bold;">
      {{ post.date | date: "%b %Y" }}
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
    <div style="margin-bottom: 5px;">
      <a href="{{ post.url | relative_url }}" style="font-size: 1.1em; font-weight: bold; text-decoration: none; color: #eee;">
        {{ post.title }}
      </a>
    </div>

    <div style="font-size: 0.9em; margin-bottom: 5px; color: #888;">
      <span style="color: #3498db; font-weight: bold;">{{ post.os }}</span>
      {% if post.tags %}
        | {{ post.tags | join: ", " }}
      {% endif %}
    </div>

    <div style="font-size: 0.8em; color: #666;">
      {{ post.date | date: "%d %B %Y" }}
    </div>
  </div>

  {% endif %}
{% endfor %}