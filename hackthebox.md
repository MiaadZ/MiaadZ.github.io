---
title: "HackTheBox Writeups"
layout: archive
permalink: /hackthebox/
author_profile: true
sidebar:
  nav: "main"
---

Accessing archived mission logs from the HackTheBox sector.

{% assign entries = site.pages | where: "parent", "HackTheBox" | sort: "date" | reverse %}
{% assign by_year = entries | group_by_exp: "item", "item.date | date: '%Y'" %}

{% for year in by_year %}
  <h2 class="timeline-year">
    {{ year.name }} 
    <span class="year-count">{{ year.items.size }} Writeups</span>
  </h2>

  {% assign current_month = "" %}

  {% for post in year.items %}
    
    {% capture this_month %}{{ post.date | date: "%B" }}{% endcapture %}
    {% if this_month != current_month %}
      <h3 class="timeline-month">{{ this_month }}</h3>
      {% assign current_month = this_month %}
    {% endif %}

    {% if post.starred %}
      <div class="starred-item">
        <div>
          <a href="{{ post.url | relative_url }}" class="starred-title">
            <i class="fas fa-star" style="font-size: 0.8em; margin-right: 5px;"></i> {{ post.title }}
          </a>
          <div style="font-size: 0.9em; opacity: 0.8; margin-top: 4px;">
            <small>Stack: {{ post.tags | join: ", " }}</small>
          </div>
        </div>
        <div class="list-meta">
          <b style="color: #ccc;">{{ post.date | date: "%d" }}</b><br>
          {{ post.difficulty }}
        </div>
      </div>
    {% else %}
      <div class="list-item">
        <h2 class="archive__item-title" style="margin: 0; font-size: 1em;">
          <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
        </h2>
        
        <div class="list-meta">
          {{ post.date | date: "%d" }} | 
          <span style="color: #3498db;">{{ post.os }}</span> | 
          <span style="color: {% if post.difficulty == 'Easy' %}#2ecc71{% elsif post.difficulty == 'Medium' %}#f1c40f{% else %}#e74c3c{% endif %};">
            {{ post.difficulty }}
          </span>
        </div>

        <div class="archive__item-excerpt" style="margin-top: 5px;">
          {% if post.tags %}
            <small style="color: #555;">Stack: {{ post.tags | join: ", " }}</small>
          {% endif %}
        </div>
      </div>
    {% endif %}

  {% endfor %}
{% endfor %}