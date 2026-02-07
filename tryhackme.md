---
title: "TryHackMe Writeups"
layout: archive
permalink: /tryhackme/
author_profile: true
sidebar:
  nav: "main"
---

{% assign machines = site.pages | where: "parent", "TryHackMe" | sort: "date" | reverse %}

{% for post in machines %}
<div class="list-item">
  <h2 class="archive__item-title">
    <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
  </h2>
  
  <div class="list-meta">
    <i class="far fa-calendar-alt"></i> {{ post.date | date: "%B %d, %Y" }} | 
    <span style="color: #3498db;">{{ post.os }}</span> | 
    <span style="color: {% if post.difficulty == 'Easy' %}#2ecc71{% elsif post.difficulty == 'Medium' %}#f1c40f{% else %}#e74c3c{% endif %};">
      {{ post.difficulty }}
    </span>
  </div>

  <div class="archive__item-excerpt">
    {% if post.tags %}
      <small>Stack: {{ post.tags | join: ", " }}</small>
    {% endif %}
  </div>
</div>
{% endfor %}