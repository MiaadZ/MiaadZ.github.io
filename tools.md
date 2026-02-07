---
title: "Armory & Tools"
layout: archive
permalink: /tools/
author_profile: true
sidebar:
  nav: "main"
toc: true
toc_sticky: true
toc_label: "Tool Index"
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

## {{ tag }}
{% for mypage in site.pages %}
  {% if mypage.tags contains tag %}
  * [**{{ mypage.title }}**]({{ mypage.url | relative_url }}) <small class="text-muted">({{ mypage.difficulty }})</small>
  {% endif %}
{% endfor %}

---
{% endfor %}