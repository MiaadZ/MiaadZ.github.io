---
title: "HackTheBox Operations"
layout: archive
permalink: /hackthebox/
author_profile: true
sidebar:
  nav: "main"
---

All captured flags and mission logs from the HackTheBox platform.

{% assign machines = site.pages | where: "parent", "HackTheBox" | sort: "date" | reverse %}

| Mission Name | Difficulty | OS | Date |
|:-------------|:-----------|:---|:-----|
{% for post in machines %}
| [**{{ post.title }}**]({{ post.url }}) | {{ post.difficulty }} | {{ post.os }} | {{ post.date | date: "%Y-%m-%d" }} |
{% endfor %}
