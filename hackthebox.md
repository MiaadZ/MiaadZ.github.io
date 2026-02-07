---
title: "HackTheBox Operations"
layout: archive
permalink: /HackTheBox/
author_profile: true
sidebar:
  nav: "main"
---

Accessing archived mission logs from the HackTheBox sector.

<div class="grid__wrapper">
  {% assign machines = site.pages | where: "parent", "HackTheBox" | sort: "date" | reverse %}
  
  {% for post in machines %}
    <div class="grid__item">
      <article class="archive__item" itemscope itemtype="https://schema.org/CreativeWork">
        
        <h2 class="archive__item-title" itemprop="headline">
          <a href="{{ post.url | relative_url }}" rel="permalink">{{ post.title }}</a>
        </h2>
        
        <p class="page__meta">
          <span style="color: #3498db; font-weight: bold;">{{ post.os }}</span> &nbsp;
          <span style="color: {% if post.difficulty == 'Easy' %}#2ecc71{% elsif post.difficulty == 'Medium' %}#f1c40f{% else %}#e74c3c{% endif %}; font-weight: bold;">
            {{ post.difficulty }}
          </span>
          <br>
          <span style="font-size: 0.8em; color: #aaa;">
            <i class="far fa-calendar-alt" aria-hidden="true"></i> {{ post.date | date: "%Y-%m-%d" }}
          </span>
        </p>

        <p class="archive__item-excerpt" itemprop="description">
          {% if post.tags %}
            Tools: <i>{{ post.tags | join: ", " }}</i>
          {% else %}
             Mission log unavailable.
          {% endif %}
        </p>
        
        <p><a href="{{ post.url | relative_url }}" class="btn btn--primary btn--small">Access Log</a></p>
        
      </article>
    </div>
  {% endfor %}
</div>