---
layout: default
title: Tools and tags
permalink: /tools/
nav_section: topics
---
<section class="archive">
<h1>Tools and tags</h1>
<p>This legacy tag index links to existing writeups. Reviewed knowledge routes will live under <a href="{{ '/topics/' | relative_url }}">Topics</a>.</p>
<ul class="tag-index">
{% for tag in site.notebook_tags %}<li><a href="#{{ tag | slugify }}">{{ tag | escape }}</a></li>{% endfor %}
</ul>
{% for tag in site.notebook_tags %}
<section>
{% assign slug = tag | slugify %}
{% if tag != slug %}{% unless tag contains ' ' %}<span class="legacy-anchor" id="{{ tag | escape }}"></span>{% endunless %}{% endif %}
<h2 id="{{ slug }}">{{ tag | escape }}</h2>
{% assign tagged = site.notebook_entries | where_exp: 'entry', 'entry.tags contains tag' %}
{% include content-list.html entries=tagged %}
</section>
{% endfor %}
</section>
