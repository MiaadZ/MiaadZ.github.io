---
title: "Armory & Tools"
layout: archive
permalink: /tools/
author_profile: true
sidebar:
  nav: "main"
---

{% assign tags = site.tags | sort %}

{% for tag in tags %}
  <div id="{{ tag[0] | slugify }}" class="tool-section">
    <h3 class="archive__item-title">{{ tag[0] }}</h3>
    <ul>
      {% for post in tag[1] %}
        <li>
          <a href="{{ post.url | relative_url }}">{{ post.title }}</a> 
          <small>({{ post.difficulty }})</small>
        </li>
      {% endfor %}
    </ul>
    <hr>
  </div>
{% endfor %}