---
title: "TryHackMe Writeups"
layout: archive
permalink: /tryhackme/
author_profile: true
sidebar:
  nav: "main"
---

<div class="terminal-card">
  <p style="margin: 0; margin-bottom: 5px;">
    <span class="cmd-prompt">root@S3Z4R:</span><span class="cmd-path">~</span>$ cd tryhackme
  </p>
  <p style="margin: 0; line-height: 1.5;">
    Accessing mission logs...<br>
    Listing detailed walkthroughs and flag captures from the <span style="color: #fff;">TryHackMe</span> sector.
  </p>
</div>

{% assign entries = site.pages | where: "parent", "TryHackMe" | sort: "date" | reverse %}
{% assign by_year = entries | group_by_exp: "item", "item.date | date: '%Y'" %}

{% for year in by_year %}
<h2 class="timeline-year">
{{ year.name }} 
<span class="year-count">{{ year.items.size }} Writeups</span>
</h2>

{% assign months = year.items | group_by_exp: "item", "item.date | date: '%m'" %}

{% for month in months %}
<h3 class="timeline-month">{{ month.items[0].date | date: "%B" }}</h3>

{% assign stars = month.items | where: "starred", true %}
{% assign norms = month.items | where: "starred", false %}

{% for post in stars %}
<div class="starred-item">
<div style="margin-bottom: 5px;">
<a href="{{ post.url | relative_url }}" class="starred-title">
<i class="fas fa-star" style="font-size: 0.8em; margin-right: 5px;"></i> {{ post.title }}
</a>
</div>
<div class="list-meta" style="margin-bottom: 5px;">
<span style="color: #3498db;">{{ post.os }}</span> | 
<span style="color: {% if post.difficulty == 'Easy' %}#2ecc71{% elsif post.difficulty == 'Medium' %}#f1c40f{% else %}#e74c3c{% endif %};">
{{ post.difficulty }}
</span>
</div>
<div class="archive__item-excerpt">
{% if post.tags %}
<small style="color: #aaa;">Stack: {{ post.tags | join: ", " }}</small>
{% endif %}
</div>
</div>
{% endfor %}

{% for post in norms %}
<div class="list-item">
<div style="margin-bottom: 5px;">
<h2 class="archive__item-title" style="margin: 0; font-size: 1em;">
<a href="{{ post.url | relative_url }}">{{ post.title }}</a>
</h2>
</div>
<div class="list-meta" style="margin-bottom: 5px;">
<span style="color: #3498db;">{{ post.os }}</span> | 
<span style="color: {% if post.difficulty == 'Easy' %}#2ecc71{% elsif post.difficulty == 'Medium' %}#f1c40f{% else %}#e74c3c{% endif %};">
{{ post.difficulty }}
</span>
</div>
<div class="archive__item-excerpt">
{% if post.tags %}
<small style="color: #555;">Stack: {{ post.tags | join: ", " }}</small>
{% endif %}
</div>
</div>
{% endfor %}

{% endfor %}
{% endfor %}