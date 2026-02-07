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

{% for tag in rawtags %}
  <div class="tool-section">
    <h2 id="{{ tag | slugify }}" style="border-bottom: 2px solid #333; padding-bottom: 5px;">
      <i class="fas fa-terminal"></i> {{ tag }}
    </h2>
    <ul>
      {% for mypage in site.pages %}
        {% if mypage.tags contains tag %}
          <li>
            <a href="{{ mypage.url | relative_url }}"><strong>{{ mypage.title }}</strong></a>
            <small>({{ mypage.difficulty }} {{ mypage.os }})</small>
          </li>
        {% endif %}
      {% endfor %}
    </ul>
  </div>
{% endfor %}