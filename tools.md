---
title: "Armory & Tools"
layout: archive
permalink: /tools/
author_profile: true
sidebar:
  nav: "main"
---

{% assign rawtags = "" %}
{% for page in site.pages %}
  {% if page.tags %}
    {% assign ttags = page.tags | join: '|' | append: '|' %}
    {% assign rawtags = rawtags | append: ttags %}
  {% endif %}
{% endfor %}
{% assign rawtags = rawtags | split: '|' | uniq | sort %}

<div style="margin-bottom: 30px;">
  {% for tag in rawtags %}
    <a href="#{{ tag }}" class="tool-badge">{{ tag }}</a>
  {% endfor %}
</div>

{% for tag in rawtags %}

<h3 id="{{ tag }}" style="margin-top: 30px; border-bottom: 2px solid #3498db; display: inline-block;">
  {{ tag }}
</h3>

<div style="margin-bottom: 20px;">
{% for mypage in site.pages %}
  {% if mypage.tags contains tag %}
  <div class="tool-item">
    <a href="{{ mypage.url | relative_url }}" style="font-weight: bold; text-decoration: none;">
      {{ mypage.title }}
    </a>
    
    <div class="tool-meta">
      {{ mypage.date | date: "%Y-%m-%d" }} | 
      <span style="color: #3498db;">{{ mypage.os }}</span> | 
      <span style="color: {% if mypage.difficulty == 'Easy' %}#2ecc71{% elsif mypage.difficulty == 'Medium' %}#f1c40f{% else %}#e74c3c{% endif %};">
        {{ mypage.difficulty }}
      </span>
    </div>
  </div>
  {% endif %}
{% endfor %}
</div>

{% endfor %}