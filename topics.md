---
layout: default
title: Topics
permalink: /topics/
nav_section: topics
---
<section class="archive">
  <header class="page-header"><p class="eyebrow">Browse the notebook</p><h1>Topics</h1><p>Explore writeups, notes and projects by subject.</p></header>
  {% assign topics = site.notebook_topics %}
  {% include topic-links.html topics=topics %}
  <p class="index-link"><a href="{{ '/tools/' | relative_url }}">Browse tools and tags</a></p>
</section>
