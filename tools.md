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

<div style="background: #1a1a1a; padding: 15px; border-radius: 5px; margin-bottom: 30px;">
  <strong>Quick Index:</strong><br>
  {% for tag in rawtags %}
    <a href="#{{ tag }}" style="margin-right: 10px; text-decoration: none; color: #3498db;">{{ tag }}</a>
  {% endfor %}
</div>

{% for tag in rawtags %}

<div id="{{ tag }}" style="margin-bottom: 40px;">
  <h2 style="border-bottom: 2px solid #333; padding-bottom: 5px;">
    <i class="fas fa-terminal"></i> {{ tag }}
  </h2>
  <ul>
  {% for mypage in site.pages %}
    {% if mypage.tags contains tag %}
    <li>
      <a href="{{ mypage.url | relative_url }}"><strong>{{ mypage.title }}</strong></a> 
      <small style="color: #888;">({{ mypage.difficulty }} {{ mypage.os }})</small>
    </li>
    {% endif %}
  {% endfor %}
  </ul>
</div>

{% endfor %}