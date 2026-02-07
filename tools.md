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

<style>
  .tool-badge {
    display: inline-block; background: #151515; color: #ccc;
    padding: 4px 8px; margin: 3px; border-radius: 4px; font-size: 0.8em;
    text-decoration: none; border: 1px solid #333;
  }
  .tool-badge:hover { background: #3498db; color: white; border-color: #3498db; }
  
  /* NEW LIST STYLING */
  .tool-item {
    display: flex;
    justify-content: space-between; /* Pushes meta to the right */
    align-items: center;
    border-bottom: 1px solid #222;
    padding: 8px 0;
  }
  .tool-meta {
    font-size: 0.8em;
    font-family: monospace;
    color: #666;
    white-space: nowrap; /* Prevents wrapping */
    margin-left: 10px;
  }
</style>

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