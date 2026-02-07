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

<style>
  .tool-index-container {
    background: #111;
    border: 1px solid #333;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 40px;
    text-align: center;
  }
  .tool-badge {
    display: inline-block;
    background: #1e1e1e;
    color: #ccc;
    padding: 5px 12px;
    margin: 4px;
    border-radius: 4px;
    font-size: 0.85em;
    text-decoration: none;
    border: 1px solid #333;
    transition: all 0.2s ease;
  }
  .tool-badge:hover {
    background: #3498db; /* Blue hover */
    color: white;
    border-color: #3498db;
    text-decoration: none;
  }
</style>

<div class="tool-index-container">
  <p style="margin-top: 0; color: #666; font-size: 0.8em; text-transform: uppercase; letter-spacing: 1px;">// Tool Index // Access Vector</p>
  {% for tag in rawtags %}
    <a href="#{{ tag }}" class="tool-badge">{{ tag }}</a>
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