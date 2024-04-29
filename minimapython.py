# post: title draft lang url date last_modified_at id feed.excerpt_only content author authors category categories tags description image.path image excerpt 
# page: url collection category tags
# site: time title lang  description author author.uri show_drafts feed.excerpt_only
# TODO: put in ctx page/post pages/posts

import os
import json
import html
import argparse
import xml.dom.minidom

post_list_html = '''
<li>
    <span class="post-meta">{{ post__date__date_format }}</span>
    <h3>
      <a class="post-link" href="{{ post__url__relative_url }}">
        {{ post__title__escape }}
      </a>
    </h3>
<!--site__show_excerpts
      {{ post__excerpt }}
site__show_excerpts-->
</li>
'''

page_author_html = '''
<span itemprop="author" itemscope itemtype="http://schema.org/Person"><span class="p-author h-card" itemprop="name">{{ author }}</span></span>
'''

site_header_pages_html = '''
<a class="page-link" href="{{ page__url__relative_url }}">{{ page__title__escape }}</a>
'''

home_html = '''
<div class="home">
<!--page__title
    <h1 class="page-heading">{{ page__title }}</h1>
page__title-->

  {{ content }}


<!--page__list_title
      <h2 class="post-list-heading">{{ page__list_title }}</h2>
page__list_title-->
    <ul class="post-list">
<!--post_list_html
      {{ post_list_html }}
post_list_html-->
    </ul>

      <div class="pager">
        <ul class="pagination">
<!--paginator__previous_page
          <li><a href="{{ paginator__previous_page_path__relative_url }}" class="previous-page">{{ paginator__previous_page }}</a></li>
paginator__previous_page-->
<!--paginator__previous_page__is_none
          <li><div class="pager-edge">•</div></li>
paginator__previous_page__is_none-->
          <li><div class="current-page">{{ paginator__page }}</div></li>
<!--paginator__next_page
          <li><a href="{{ paginator__next_page_path__relative_url }}" class="next-page">{{ paginator__next_page }}</a></li>
paginator__next_page-->
<!--paginator__next_page__is_none
          <li><div class="pager-edge">•</div></li>
paginator__next_page__is_none-->
        </ul>
      </div>

</div>
'''

post_html = '''
<!-- https://github.com/jekyll/minima/blob/master/_layouts/post.html -->
<article class="post h-entry" itemscope itemtype="http://schema.org/BlogPosting">

  <header class="post-header">
    <h1 class="post-title p-name" itemprop="name headline">{{ page__title__escape }}</h1>
    <p class="post-meta">
      <time class="dt-published" datetime="{{ page__date__date_to_xmlschema }}" itemprop="datePublished">
        {{ page__date__date_format }}
      </time>
<!--page__modified_date__date_to_xmlschema
        ~
        <time class="dt-modified" datetime="{{ page__modified_date__date_to_xmlschema }}" itemprop="dateModified">
          {{ page__modified_date__date_format }}
        </time>
page__modified_date__date_to_xmlschema-->

<!--page_author_html
        • {{ page_author_html }}
page_author_html-->
    </p>
  </header>

  <div class="post-content e-content" itemprop="articleBody">
    {{ content }}
  </div>

  {{ comments_html }}

  <a class="u-url" href="{{ page__url__relative_url }}" hidden></a>
</article>
'''

page_html = '''
<!-- https://github.com/jekyll/minima/blob/master/_layouts/page.html -->
<article class="post">

  <header class="post-header">
    <h1 class="post-title">{{ page__title__escape }}</h1>
  </header>

  <div class="post-content">
    {{ content }}
  </div>

</article>
'''

base_html = '''
<!DOCTYPE html>
<html lang="{{ page__lang }}">
  <!-- https://github.com/jekyll/minima/blob/master/_layouts/base.html -->

  {{ head_html }}

  <body>

    {{ header_html }}

    <main class="page-content" aria-label="Content">
      <div class="wrapper">
        {{ content_base }}
      </div>
    </main>

    {{ footer_html }}

  </body>

</html>
'''

googleanalytics_html = '''
<script async src="https://www.googletagmanager.com/gtag/js?id={{ site__google_analytics }}"></script>
<script>
  window['ga-disable-{{ site__google_analytics }}'] = window.doNotTrack === "1" || navigator.doNotTrack === "1" || navigator.doNotTrack === "yes" || navigator.msDoNotTrack === "1";
  window.dataLayer = window.dataLayer || [];
  function gtag(){window.dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', '{{ site__google_analytics }}');
</script>

'''

comments_html = '''
<!-- comments_html -->
'''

seo_html = '''
<!-- https://github.com/jekyll/jekyll-seo-tag/blob/master/lib/template.html -->
<!--seo_tag__title
  <title>{{ seo_tag__title }}</title>
seo_tag__title-->

<meta name="generator" content="minimapython" />

<!--seo_tag__page_title
  <meta property="og:title" content="{{ seo_tag__page_title }}" />
seo_tag__page_title-->

<!--seo_tag__author__name
  <meta name="author" content="{{ seo_tag__author__name }}" />
seo_tag__author__name-->

<meta property="og:locale" content="{{ seo_tag__page_locale }}" />

<!--seo_tag__description
  <meta name="description" content="{{ seo_tag__description }}" />
  <meta property="og:description" content="{{ seo_tag__description }}" />
  <meta property="twitter:description" content="{{ seo_tag__description }}" />
seo_tag__description-->

<!--seo_tag__canonical_url
  <link rel="canonical" href="{{ seo_tag__canonical_url }}" />
  <meta property="og:url" content="{{ seo_tag__canonical_url }}" />
seo_tag__canonical_url-->

<!--seo_tag__site_title
  <meta property="og:site_name" content="{{ seo_tag__site_title }}" />
seo_tag__site_title-->

<!--seo_tag__image__path
  <meta property="og:image" content="{{ seo_tag__image__path }}" />
seo_tag__image__path-->
<!--seo_tag__image__height
    <meta property="og:image:height" content="{{ seo_tag__image__height }}" />
seo_tag__image__height-->
<!--seo_tag__image__width
    <meta property="og:image:width" content="{{ seo_tag__image__width }}" />
seo_tag__image__width-->
<!--seo_tag__image__alt
    <meta property="og:image:alt" content="{{ seo_tag__image__alt }}" />
seo_tag__image__alt-->

<!--page__date__date_to_xmlschema
  <meta property="og:type" content="article" />
  <meta property="article:published_time" content="{{ page__date__date_to_xmlschema }}" />
page__date__date_to_xmlschema-->
<!--page__date__is_none
  <meta property="og:type" content="website" />
page__date__is_none-->

<!--paginator__previous_page_path__absolute_url
  <link rel="prev" href="{{ paginator__previous_page_path__absolute_url }}" />
paginator__previous_page_path__absolute_url-->
<!--paginator__next_page_path__absolute_url
  <link rel="next" href="{{ paginator__next_page_path__absolute_url }}" />
paginator__next_page_path__absolute_url-->

<!--page__twitter__card
  <meta name="twitter:card" content="{{ page__twitter__card }}" />
  <meta property="twitter:image" content="{{ seo_tag__image__path }}" />
page__twitter__card-->
<!--seo_tag__image__is_none
  <meta name="twitter:card" content="summary" />
seo_tag__image__is_none-->

<!--seo_tag__image__alt
  <meta name="twitter:image:alt" content="{{ seo_tag__image__alt }}" />
seo_tag__image__alt-->

<!--seo_tag__page_title
  <meta property="twitter:title" content="{{ seo_tag__page_title }}" />
seo_tag__page_title-->

<!--site__twitter__username__removeATSIGN
  <meta name="twitter:site" content="@{{ site__twitter__username__removeATSIGN }}" />
site__twitter__username__removeATSIGN-->

<!--seo_tag__author__twitter__removeATSIGN
    <meta name="twitter:creator" content="@{{ seo_tag__author__twitter__removeATSIGN }}" />
seo_tag__author__twitter__removeATSIGN-->

<!--site__facebook__admins
    <meta property="fb:admins" content="{{ site__facebook__admins }}" />
site__facebook__admins-->

<!--site__facebook__publisher
    <meta property="article:publisher" content="{{ site__facebook__publisher }}" />
site__facebook__publisher-->

<!--site__facebook__app_id
    <meta property="fb:app_id" content="{{ site__facebook__app_id }}" />
site__facebook__app_id-->

<!--site__webmaster_verifications__google
    <meta name="google-site-verification" content="{{ site__webmaster_verifications__google }}" />
site__webmaster_verifications__google-->
<!--site__webmaster_verifications__bing
    <meta name="msvalidate.01" content="{{ site__webmaster_verifications__bing }}" />
site__webmaster_verifications__bing-->
<!--site__webmaster_verifications__alexa
    <meta name="alexaVerifyID" content="{{ site__webmaster_verifications__alexa }}" />
site__webmaster_verifications__alexa-->
<!--site__webmaster_verifications__yandex
    <meta name="yandex-verification" content="{{ site__webmaster_verifications__yandex }}" />
site__webmaster_verifications__yandex-->
<!--site__webmaster_verifications__baidu
    <meta name="baidu-site-verification" content="{{ site__webmaster_verifications__baidu }}" />
site__webmaster_verifications__baidu-->
<!--site__webmaster_verifications__facebook
    <meta name="facebook-domain-verification" content="{{ site__webmaster_verifications__facebook }}" />
site__webmaster_verifications__facebook-->

<script type="application/ld+json">
  {{ seo_tag__json_ld__jsonify }}
</script>

<!-- End Jekyll SEO tag -->
'''


customhead_html = '''
<!-- customhead_html -->
'''

head_html = '''
<!-- https://github.com/jekyll/minima/blob/master/_includes/head.html -->
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  {{ seo_html }}
  <style>
  {{ style_css }}
  </style>
  <!-- <link rel="stylesheet" href="style_css__relative_url"> -->

  {{ googleanalytics_html }}

  {{ customhead_html }}

</head>
'''

header_html = '''
<!-- https://github.com/jekyll/minima/blob/master/_includes/header.html -->
<header class="site-header">

  <div class="wrapper">
    <a class="site-title" rel="author" href="{{ root__relative_url }}">{{ site__title__escape }}</a>

<!--site_header_pages_html
      <nav class="site-nav">
        <input type="checkbox" id="nav-trigger" class="nav-trigger" />
        <label for="nav-trigger">
          <span class="menu-icon">
            <svg viewBox="0 0 18 15" width="18px" height="15px">
              <path d="M18,1.484c0,0.82-0.665,1.484-1.484,1.484H1.484C0.665,2.969,0,2.304,0,1.484l0,0C0,0.665,0.665,0,1.484,0 h15.032C17.335,0,18,0.665,18,1.484L18,1.484z M18,7.516C18,8.335,17.335,9,16.516,9H1.484C0.665,9,0,8.335,0,7.516l0,0 c0-0.82,0.665-1.484,1.484-1.484h15.032C17.335,6.031,18,6.696,18,7.516L18,7.516z M18,13.516C18,14.335,17.335,15,16.516,15H1.484 C0.665,15,0,14.335,0,13.516l0,0c0-0.82,0.665-1.483,1.484-1.483h15.032C17.335,12.031,18,12.695,18,13.516L18,13.516z"/>
            </svg>
          </span>
        </label>

        <div class="trigger">
          {{ site_header_pages_html }}
        </div>
      </nav>
site_header_pages_html-->
  </div>
</header>
'''

footer_html = '''
<!-- https://github.com/jekyll/minima/blob/master/_includes/footer.html -->
<footer class="site-footer h-card">
    <data class="u-url" href="{{ root__relative_url }}"></data>

    <div class="wrapper">

    <div class="footer-col-wrapper">
      <div class="footer-col">

<!--site__feed__path__absolute_url
        <p class="feed-subscribe">
          <a href="{{ site__feed__path__absolute_url }}">
            <svg id="rss" class="svg-icon orange" fill-rule="evenodd" clip-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="1.414" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                <path d="M12.8 16C12.8 8.978 7.022 3.2 0 3.2V0c8.777 0 16 7.223 16 16h-3.2zM2.194 11.61c1.21 0 2.195.985 2.195 2.196 0 1.21-.99 2.194-2.2 2.194C.98 16 0 15.017 0 13.806c0-1.21.983-2.195 2.194-2.195zM10.606 16h-3.11c0-4.113-3.383-7.497-7.496-7.497v-3.11c5.818 0 10.606 4.79 10.606 10.607z"/>
            </svg><span>Subscribe</span>
          </a>
        </p>
site__feed__path__absolute_url-->

        <ul class="contact-list">
            <li class="p-name">{{ site__author__name__escape }}</li>
            <li><a class="u-email" href="mailto:{{ site__author__email }}">{{ site__author__email }}</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <p>{{ site__description__escape }}</p>
      </div>
    </div>

    <div class="social-links">
      <ul class="social-media-list">

<!--site__minima__social_links__devto
          <li>
            <a href="{{ site__minima__social_links__devto }}" target="_blank" title="devto">
              <svg id="devto" class="svg-icon grey" fill-rule="evenodd" clip-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="1.414" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><path d="M4.548,6.415C4.419,6.318,4.29,6.271,4.161,6.271h-0.58v3.471h0.58c0.129,0,0.258-0.049,0.387-0.145 C4.677,9.5,4.742,9.355,4.742,9.163V6.85C4.741,6.656,4.676,6.511,4.548,6.415z M13.981,0.559H2.016 c-0.804,0-1.457,0.65-1.458,1.455v11.973c0.002,0.805,0.655,1.455,1.458,1.455h11.968c0.805,0,1.457-0.65,1.459-1.455V2.014 C15.438,1.209,14.786,0.559,13.981,0.559z M5.68,9.169c0,0.625-0.386,1.572-1.605,1.569H2.532V5.242h1.573 c1.179,0,1.573,0.945,1.574,1.57V9.169z M9.024,6.225h-1.77V7.5h1.082v0.982H7.255v1.275h1.771v0.982H6.959 c-0.371,0.009-0.679-0.283-0.688-0.654V5.931c-0.008-0.37,0.285-0.679,0.655-0.688h2.099V6.225z M12.47,10.055 c-0.438,1.021-1.226,0.817-1.576,0l-1.28-4.812h1.081l0.988,3.778l0.981-3.778h1.082L12.47,10.055z"/></svg>
            </a>
          </li>
site__minima__social_links__devto-->

<!--site__minima__social_links__dribbble
          <li>
            <a href="{{ site__minima__social_links__dribbble }}" target="_blank" title="dribbble">
              <svg id="dribbble" class="svg-icon grey" fill-rule="evenodd" clip-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="1.414" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><path d="M8 16c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm6.747-6.905c-.234-.074-2.115-.635-4.257-.292.894 2.456 1.258 4.456 1.328 4.872 1.533-1.037 2.624-2.68 2.93-4.58zM10.67 14.3c-.102-.6-.5-2.688-1.46-5.18l-.044.014C5.312 10.477 3.93 13.15 3.806 13.4c1.158.905 2.614 1.444 4.194 1.444.947 0 1.85-.194 2.67-.543zm-7.747-1.72c.155-.266 2.03-3.37 5.555-4.51.09-.03.18-.056.27-.08-.173-.39-.36-.778-.555-1.16-3.413 1.02-6.723.977-7.023.97l-.003.208c0 1.755.665 3.358 1.756 4.57zM1.31 6.61c.307.005 3.122.017 6.318-.832-1.132-2.012-2.353-3.705-2.533-3.952-1.912.902-3.34 2.664-3.784 4.785zM6.4 1.368c.188.253 1.43 1.943 2.548 4 2.43-.91 3.46-2.293 3.582-2.468C11.323 1.827 9.736 1.176 8 1.176c-.55 0-1.087.066-1.6.19zm6.89 2.322c-.145.194-1.29 1.662-3.816 2.694.16.325.31.656.453.99.05.117.1.235.147.352 2.274-.286 4.533.172 4.758.22-.015-1.613-.59-3.094-1.543-4.257z"/></svg>
            </a>
          </li>
site__minima__social_links__dribbble-->

<!--site__minima__social_links__flickr
          <li>
            <a href="{{ site__minima__social_links__flickr }}" target="_blank" title="flickr">
              <svg id="flickr" class="svg-icon grey" fill-rule="evenodd" clip-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="1.414" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><path d="M0 8c0 2.05 1.662 3.71 3.71 3.71 2.05 0 3.713-1.66 3.713-3.71S5.76 4.29 3.71 4.29C1.663 4.29 0 5.95 0 8zm8.577 0c0 2.05 1.662 3.71 3.712 3.71C14.33 11.71 16 10.05 16 8s-1.662-3.71-3.71-3.71c-2.05 0-3.713 1.66-3.713 3.71z"/></svg>
            </a>
          </li>
site__minima__social_links__flickr-->

<!--site__minima__social_links__gitlab
          <li>
            <a href="{{ site__minima__social_links__gitlab }}" target="_blank" title="gitlab">
              <svg id="gitlab" class="svg-icon grey" fill-rule="evenodd" clip-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="1.414" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><path d="M1.07,6.337L8,15.219L0.405,9.706C0.3,9.63,0.227,9.529,0.186,9.404c-0.041-0.125-0.041-0.25,0-0.372L1.07,6.337z M5.112,6.337h5.775L8,15.219L5.112,6.337z M3.38,0.982l1.732,5.355H1.07l1.732-5.355c0.047-0.134,0.143-0.201,0.289-0.201 S3.333,0.848,3.38,0.982z M14.93,6.337l0.884,2.695c0.041,0.123,0.041,0.247,0,0.372S15.7,9.63,15.595,9.706L8,15.219L14.93,6.337z M14.93,6.337h-4.042l1.733-5.355c0.046-0.134,0.143-0.201,0.288-0.201c0.146,0,0.243,0.067,0.289,0.201L14.93,6.337z"/></svg>
            </a>
          </li>
site__minima__social_links__gitlab-->

<!--site__minima__social_links__google_scholar
          <li>
            <a href="{{ site__minima__social_links__google_scholar }}" target="_blank" title="google_scholar">
              <svg id="google_scholar" class="svg-icon grey" fill-rule="evenodd" clip-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="1.414" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><circle opacity="0.7" cx="8.036" cy="11.08" r="4.3"/><path opacity="0.75" d="M0.585,6.505l7.42-5.885L8.03,6.582 C5.305,6.632,4.139,8.729,3.913,9.13L0.585,6.505z"/><path d="M15.415,6.509l-7.42-5.886L7.97,6.585c2.725,0.05,3.891,2.147,4.117,2.548L15.415,6.509z"/></svg>
            </a>
          </li>
site__minima__social_links__google_scholar-->

<!--site__minima__social_links__keybase
          <li>
            <a href="{{ site__minima__social_links__keybase }}" target="_blank" title="keybase">
              <svg id="keybase" class="svg-icon grey" fill-rule="evenodd" clip-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="1.414" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><path d="M10.34,13.58c-0.298,0-0.54,0.242-0.54,0.54s0.242,0.54,0.54,0.54c0.298,0,0.54-0.242,0.54-0.54S10.638,13.58,10.34,13.58 L10.34,13.58z M6.38,13.58c-0.298,0-0.54,0.242-0.54,0.54s0.242,0.54,0.54,0.54c0.298,0,0.54-0.242,0.54-0.54 S6.678,13.58,6.38,13.58z"/><path fill="none" stroke="#000000" stroke-width="0.72" stroke-linecap="round" stroke-miterlimit="10" d="M1.58,13.22 c0.104,0.771,0.344,1.497,0.688,2.16 M5.93,3.86H4.31c-0.149,0-0.27-0.121-0.27-0.27V1.97c0-0.149,0.121-0.27,0.27-0.27h1.62 c0.149,0,0.27,0.121,0.27,0.27v1.08"/><path d="M8.18,7.46c-1.489,0-2.7-1.211-2.7-2.7c0-2.471,2.012-4.329,2.098-4.407c0.125-0.113,0.309-0.125,0.447-0.029 s0.191,0.273,0.129,0.429C8,1.142,7.861,1.791,8.002,1.999C8.015,2.018,8.044,2.06,8.18,2.06c1.489,0,2.7,1.211,2.7,2.7 C10.88,6.249,9.669,7.46,8.18,7.46z"/><path d="M15.178,11.759c-0.174-2.216-1.372-4.173-3.196-5.341c-0.015-0.009-0.029-0.02-0.044-0.029 c-0.121-0.076-0.245-0.147-0.371-0.217c-0.044-0.024-0.088-0.049-0.133-0.073c-0.029-0.016-0.061-0.029-0.09-0.043 c-0.228,0.551-0.594,1.03-1.056,1.394l1.206,1.207c0.141,0.141,0.141,0.368,0,0.509c-0.07,0.07-0.162,0.105-0.254,0.105 s-0.185-0.035-0.255-0.105l-0.301-0.301l-0.65,0.651C9.963,9.585,9.871,9.62,9.779,9.62c-0.092,0-0.184-0.035-0.254-0.105 c-0.141-0.141-0.141-0.369,0-0.509l0.651-0.651L9.8,7.979L9.334,8.445c-0.07,0.07-0.162,0.105-0.254,0.105S8.896,8.516,8.826,8.445 C8.74,8.36,8.714,8.245,8.73,8.135C8.552,8.164,8.368,8.18,8.18,8.18c-1.452,0-2.692-0.911-3.188-2.19 C2.318,7.245,0.8,10.089,0.8,13.94v1.08l0.648-0.864c0.669-0.893,1.483-1.789,2.256-2.502c-0.19,0.508-0.318,1.016-0.381,1.521 l-0.113,0.905l0.701-0.585c0.021-0.017,2.087-1.716,4.449-1.716c1.159,0,1.792,0.107,2.352,0.202 c0.479,0.081,0.931,0.157,1.609,0.157c1.115,0,1.727-0.57,1.993-1.254c0.071,0.304,0.121,0.614,0.146,0.931 c0.013,0.167,0.021,0.334,0.021,0.504c0,1.015-0.238,1.987-0.709,2.895c-0.092,0.176-0.022,0.394,0.154,0.485 c0.053,0.027,0.109,0.04,0.165,0.04c0.13,0,0.256-0.07,0.32-0.194c0.523-1.01,0.789-2.095,0.789-3.226 C15.2,12.132,15.192,11.944,15.178,11.759z"/></svg>
            </a>
          </li>
site__minima__social_links__keybase-->

<!--site__minima__social_links__mastodon
          <li>
            <a href="{{ site__minima__social_links__mastodon }}" target="_blank" title="mastodon">
              <svg id="mastodon" class="svg-icon grey" fill-rule="evenodd" clip-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="1.414" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><path d="M15.195,5.352c0-3.347-2.193-4.328-2.193-4.328c-1.104-0.508-3.004-0.721-4.977-0.737H7.977 c-1.973,0.016-3.87,0.229-4.976,0.737c0,0-2.193,0.981-2.193,4.328c0,0.766-0.015,1.683,0.009,2.654c0.08,3.272,0.6,6.499,3.626,7.3 c1.396,0.369,2.594,0.446,3.559,0.394c1.75-0.097,2.732-0.624,2.732-0.624l-0.058-1.27c0,0-1.25,0.395-2.655,0.346 c-1.391-0.047-2.86-0.149-3.085-1.857c-0.021-0.15-0.031-0.312-0.031-0.479c0,0,1.365,0.334,3.096,0.413 c1.059,0.049,2.051-0.062,3.059-0.182c1.934-0.231,3.616-1.422,3.828-2.51C15.224,7.821,15.195,5.352,15.195,5.352z M12.609,9.664 h-1.606V5.73c0-0.83-0.349-1.25-1.047-1.25c-0.772,0-1.158,0.5-1.158,1.486V8.12H7.202V5.966c0-0.987-0.387-1.486-1.158-1.486 c-0.698,0-1.046,0.421-1.046,1.25v3.933H3.391V5.611c0-0.829,0.211-1.487,0.634-1.974c0.437-0.487,1.009-0.736,1.719-0.736 c0.822,0,1.444,0.315,1.855,0.947L8,4.519l0.4-0.67c0.412-0.632,1.033-0.947,1.855-0.947c0.71,0,1.282,0.25,1.72,0.736 c0.423,0.487,0.635,1.145,0.635,1.974V9.664z"/></svg>
            </a>
          </li>
site__minima__social_links__mastodon-->

<!--site__minima__social_links__microdotblog
          <li>
            <a href="{{ site__minima__social_links__microdotblog }}" target="_blank" title="microdotblog">
              <svg id="microdotblog" class="svg-icon grey" fill-rule="evenodd" clip-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="1.414" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><path d="M13.778,12.215c-0.102,0.218-0.171,0.385-0.212,0.498c-0.143,0.399-0.188,0.719-0.202,0.922 c-0.068,1.015,0.388,1.615,0.496,1.776c0.16,0.239,0.227,0.373,0.195,0.404c-0.059,0.104-0.241,0.104-0.546,0 c-0.457-0.157-1.72-0.647-2.196-1.338c-0.191-0.28-0.313-0.398-0.389-0.44C10.021,14.372,9.034,14.556,8,14.556 c-4.33,0-7.84-3.234-7.84-7.224c0-3.99,3.51-7.225,7.84-7.225s7.84,3.234,7.84,7.225C15.84,9.214,15.059,10.929,13.778,12.215z M7.944,9.692c1.542,0.999,2.38,1.439,2.513,1.322c0.133-0.117-0.027-1.051-0.479-2.799c1.436-1.092,2.114-1.753,2.033-1.981 c-0.082-0.229-1.018-0.365-2.81-0.408C8.607,4.13,8.188,3.28,7.944,3.28c-0.244,0-0.663,0.85-1.256,2.546 c-1.795,0.053-2.731,0.188-2.81,0.408c-0.078,0.219,0.6,0.88,2.033,1.981c-0.491,1.689-0.65,2.622-0.48,2.799 C5.602,11.19,6.44,10.75,7.944,9.692z"/></svg>
            </a>
          </li>
site__minima__social_links__microdotblog-->

<!--site__minima__social_links__pinterest
          <li>
            <a href="{{ site__minima__social_links__pinterest }}" target="_blank" title="pinterest">
              <svg id="pinterest" class="svg-icon grey" fill-rule="evenodd" clip-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="1.414" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><path d="M8 0C3.582 0 0 3.582 0 8c0 3.39 2.108 6.285 5.084 7.45-.07-.633-.133-1.604.028-2.295.146-.625.938-3.977.938-3.977s-.24-.48-.24-1.188c0-1.11.646-1.943 1.448-1.943.683 0 1.012.513 1.012 1.127 0 .687-.436 1.713-.662 2.664-.19.797.4 1.445 1.185 1.445 1.42 0 2.514-1.498 2.514-3.662 0-1.91-1.376-3.25-3.342-3.25-2.276 0-3.61 1.71-3.61 3.47 0 .69.263 1.43.593 1.83.066.08.075.15.057.23-.06.25-.196.8-.223.91-.035.15-.115.18-.268.11C3.516 10.46 2.89 9 2.89 7.82c0-2.52 1.834-4.84 5.287-4.84 2.774 0 4.932 1.98 4.932 4.62 0 2.76-1.74 4.98-4.16 4.98-.81 0-1.57-.42-1.84-.92l-.5 1.9c-.18.698-.67 1.57-1 2.1.75.23 1.54.357 2.37.357 4.41 0 8-3.58 8-8s-3.59-8-8-8z"/></svg>
            </a>
          </li>
site__minima__social_links__pinterest-->

<!--site__minima__social_links__stackoverflow
          <li>
            <a href="{{ site__minima__social_links__stackoverflow }}" target="_blank" title="stackoverflow">
              <svg id="stackoverflow" class="svg-icon grey" fill-rule="evenodd" clip-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="1.414" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><path d="M12.566,14.12v-4.08h1.359v5.44H1.686v-5.44h1.36v4.08H12.566z M10.336,0.52L9.269,1.315l3.978,5.358l1.068-0.803 L10.336,0.52z M4.406,12.76h6.8V11.4h-6.8V12.76z M12.158,7.945L7.03,3.675l0.851-1.02l5.128,4.271L12.158,7.945z M5.357,6.646 l6.053,2.815l0.558-1.21L5.916,5.437L5.357,6.64V6.646z M11.227,10.91L4.494,9.774l0.272-1.306l6.549,1.306L11.227,10.91z"/></svg>
            </a>
          </li>
site__minima__social_links__stackoverflow-->

<!--site__minima__social_links__x
          <li>
            <a href="{{ site__minima__social_links__x }}" target="_blank" title="x">
              <svg id="x" class="svg-icon grey" fill-rule="evenodd" clip-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="1.414" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><path d="M 9.5237333,6.7756869 15.481067,0 h -1.4112 L 8.8949333,5.8820316 4.7648,0 H 0 L 6.2469333,8.8955204 0,16 H 1.4112 L 6.8725333,9.7870441 11.2352,16 H 16 M 1.9205333,1.0412656 h 2.168 L 14.0688,15.009892 h -2.168533" style="stroke-width:0.0533111"/></svg>
            </a>
          </li>
site__minima__social_links__x-->

<!--site__minima__social_links__github
          <li>
            <a href="{{ site__minima__social_links__github }}" target="_blank" title="github">
              <svg id="github" class="svg-icon grey" fill-rule="evenodd" clip-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="1.414" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><path d="M8 0C3.58 0 0 3.582 0 8c0 3.535 2.292 6.533 5.47 7.59.4.075.547-.172.547-.385 0-.19-.007-.693-.01-1.36-2.226.483-2.695-1.073-2.695-1.073-.364-.924-.89-1.17-.89-1.17-.725-.496.056-.486.056-.486.803.056 1.225.824 1.225.824.714 1.223 1.873.87 2.33.665.072-.517.278-.87.507-1.07-1.777-.2-3.644-.888-3.644-3.953 0-.873.31-1.587.823-2.147-.09-.202-.36-1.015.07-2.117 0 0 .67-.215 2.2.82.64-.178 1.32-.266 2-.27.68.004 1.36.092 2 .27 1.52-1.035 2.19-.82 2.19-.82.43 1.102.16 1.915.08 2.117.51.56.82 1.274.82 2.147 0 3.073-1.87 3.75-3.65 3.947.28.24.54.73.54 1.48 0 1.07-.01 1.93-.01 2.19 0 .21.14.46.55.38C13.71 14.53 16 11.53 16 8c0-4.418-3.582-8-8-8"/></svg>
            </a>
          </li>
site__minima__social_links__github-->

<!--site__minima__social_links__facebook
          <li>
            <a href="{{ site__minima__social_links__facebook }}" target="_blank" title="facebook">
              <svg id="facebook" class="svg-icon grey" fill-rule="evenodd" clip-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="1.414" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><path d="M15.117 0H.883C.395 0 0 .395 0 .883v14.234c0 .488.395.883.883.883h7.663V9.804H6.46V7.39h2.086V5.607c0-2.066 1.262-3.19 3.106-3.19.883 0 1.642.064 1.863.094v2.16h-1.28c-1 0-1.195.48-1.195 1.18v1.54h2.39l-.31 2.42h-2.08V16h4.077c.488 0 .883-.395.883-.883V.883C16 .395 15.605 0 15.117 0"/></svg>
            </a>
          </li>
site__minima__social_links__facebook-->
          
<!--site__minima__social_links__instagram
          <li>
            <a href="{{ site__minima__social_links__instagram }}" target="_blank" title="instagram">
              <svg id="instagram" class="svg-icon grey" fill-rule="evenodd" clip-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="1.414" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><path d="M8 0C5.827 0 5.555.01 4.702.048 3.85.088 3.27.222 2.76.42c-.526.204-.973.478-1.417.923-.445.444-.72.89-.923 1.417-.198.51-.333 1.09-.372 1.942C.008 5.555 0 5.827 0 8s.01 2.445.048 3.298c.04.852.174 1.433.372 1.942.204.526.478.973.923 1.417.444.445.89.72 1.417.923.51.198 1.09.333 1.942.372.853.04 1.125.048 3.298.048s2.445-.01 3.298-.048c.852-.04 1.433-.174 1.942-.372.526-.204.973-.478 1.417-.923.445-.444.72-.89.923-1.417.198-.51.333-1.09.372-1.942.04-.853.048-1.125.048-3.298s-.01-2.445-.048-3.298c-.04-.852-.174-1.433-.372-1.942-.204-.526-.478-.973-.923-1.417-.444-.445-.89-.72-1.417-.923-.51-.198-1.09-.333-1.942-.372C10.445.008 10.173 0 8 0zm0 1.44c2.136 0 2.39.01 3.233.048.78.036 1.203.166 1.485.276.374.145.64.318.92.598.28.28.453.546.598.92.11.282.24.705.276 1.485.038.844.047 1.097.047 3.233s-.01 2.39-.05 3.233c-.04.78-.17 1.203-.28 1.485-.15.374-.32.64-.6.92-.28.28-.55.453-.92.598-.28.11-.71.24-1.49.276-.85.038-1.1.047-3.24.047s-2.39-.01-3.24-.05c-.78-.04-1.21-.17-1.49-.28-.38-.15-.64-.32-.92-.6-.28-.28-.46-.55-.6-.92-.11-.28-.24-.71-.28-1.49-.03-.84-.04-1.1-.04-3.23s.01-2.39.04-3.24c.04-.78.17-1.21.28-1.49.14-.38.32-.64.6-.92.28-.28.54-.46.92-.6.28-.11.7-.24 1.48-.28.85-.03 1.1-.04 3.24-.04zm0 2.452c-2.27 0-4.108 1.84-4.108 4.108 0 2.27 1.84 4.108 4.108 4.108 2.27 0 4.108-1.84 4.108-4.108 0-2.27-1.84-4.108-4.108-4.108zm0 6.775c-1.473 0-2.667-1.194-2.667-2.667 0-1.473 1.194-2.667 2.667-2.667 1.473 0 2.667 1.194 2.667 2.667 0 1.473-1.194 2.667-2.667 2.667zm5.23-6.937c0 .53-.43.96-.96.96s-.96-.43-.96-.96.43-.96.96-.96.96.43.96.96z"/></svg>
            </a>
          </li>
site__minima__social_links__instagram-->

<!--site__minima__social_links__linkedin
          <li>
            <a href="{{ site__minima__social_links__linkedin }}" target="_blank" title="linkedin">
              <svg id="linkedin" class="svg-icon grey" fill-rule="evenodd" clip-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="1.414" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><path d="M13.632 13.635h-2.37V9.922c0-.886-.018-2.025-1.234-2.025-1.235 0-1.424.964-1.424 1.96v3.778h-2.37V6H8.51v1.04h.03c.318-.6 1.092-1.233 2.247-1.233 2.4 0 2.845 1.58 2.845 3.637v4.188zM3.558 4.955c-.762 0-1.376-.617-1.376-1.377 0-.758.614-1.375 1.376-1.375.76 0 1.376.617 1.376 1.375 0 .76-.617 1.377-1.376 1.377zm1.188 8.68H2.37V6h2.376v7.635zM14.816 0H1.18C.528 0 0 .516 0 1.153v13.694C0 15.484.528 16 1.18 16h13.635c.652 0 1.185-.516 1.185-1.153V1.153C16 .516 15.467 0 14.815 0z"/></svg>
            </a>
          </li>
site__minima__social_links__linkedin-->
    
<!--site__minima__social_links__telegram
          <li>
            <a href="{{ site__minima__social_links__telegram }}" target="_blank" title="telegram">
              <svg id="telegram" class="svg-icon grey" fill-rule="evenodd" clip-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="1.414" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><path d="M10.563,11.596l1.286-6.063c0.053-0.256,0.022-0.44-0.092-0.551c-0.113-0.111-0.264-0.131-0.45-0.061l-7.56,2.914 C3.579,7.897,3.463,7.971,3.402,8.052C3.34,8.134,3.333,8.211,3.38,8.284s0.14,0.13,0.28,0.171l1.934,0.604l4.489-2.826 c0.123-0.082,0.216-0.099,0.28-0.053c0.041,0.029,0.029,0.073-0.035,0.131L6.696,9.592l-0.14,1.996c0.134,0,0.265-0.064,0.394-0.193 l0.945-0.91l1.96,1.444C10.229,12.139,10.465,12.027,10.563,11.596z M15.84,8c0,1.062-0.207,2.077-0.621,3.045 c-0.414,0.969-0.972,1.803-1.671,2.503c-0.7,0.699-1.534,1.257-2.503,1.671C10.077,15.633,9.062,15.84,8,15.84 s-2.077-0.207-3.045-0.621c-0.969-0.414-1.803-0.972-2.502-1.671c-0.7-0.7-1.257-1.534-1.671-2.503C0.367,10.077,0.16,9.062,0.16,8 s0.207-2.077,0.621-3.045c0.414-0.969,0.971-1.803,1.671-2.502c0.7-0.7,1.534-1.257,2.502-1.671C5.923,0.367,6.938,0.16,8,0.16 s2.077,0.207,3.045,0.621c0.969,0.414,1.803,0.971,2.503,1.671c0.699,0.7,1.257,1.534,1.671,2.502C15.633,5.923,15.84,6.938,15.84,8 z"/></svg>
            </a>
          </li>
site__minima__social_links__telegram-->
    
<!--site__minima__social_links__twitter
          <li>
            <a href="{{ site__minima__social_links__twitter }}" target="_blank" title="twitter">
              <svg id="twitter" class="svg-icon grey" fill-rule="evenodd" clip-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="1.414" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><path d="M16 3.038c-.59.26-1.22.437-1.885.517.677-.407 1.198-1.05 1.443-1.816-.634.37-1.337.64-2.085.79-.598-.64-1.45-1.04-2.396-1.04-1.812 0-3.282 1.47-3.282 3.28 0 .26.03.51.085.75-2.728-.13-5.147-1.44-6.766-3.42C.83 2.58.67 3.14.67 3.75c0 1.14.58 2.143 1.46 2.732-.538-.017-1.045-.165-1.487-.41v.04c0 1.59 1.13 2.918 2.633 3.22-.276.074-.566.114-.865.114-.21 0-.41-.02-.61-.058.42 1.304 1.63 2.253 3.07 2.28-1.12.88-2.54 1.404-4.07 1.404-.26 0-.52-.015-.78-.045 1.46.93 3.18 1.474 5.04 1.474 6.04 0 9.34-5 9.34-9.33 0-.14 0-.28-.01-.42.64-.46 1.2-1.04 1.64-1.7z"/></svg>
            </a>
          </li>
site__minima__social_links__twitter-->
    
<!--site__minima__social_links__youtube
          <li>
            <a href="{{ site__minima__social_links__youtube }}" target="_blank" title="youtube">
              <svg id="youtube" class="svg-icon grey" fill-rule="evenodd" clip-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="1.414" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><path d="M0 7.345c0-1.294.16-2.59.16-2.59s.156-1.1.636-1.587c.608-.637 1.408-.617 1.764-.684C3.84 2.36 8 2.324 8 2.324s3.362.004 5.6.166c.314.038.996.04 1.604.678.48.486.636 1.588.636 1.588S16 6.05 16 7.346v1.258c0 1.296-.16 2.59-.16 2.59s-.156 1.102-.636 1.588c-.608.638-1.29.64-1.604.678-2.238.162-5.6.166-5.6.166s-4.16-.037-5.44-.16c-.356-.067-1.156-.047-1.764-.684-.48-.487-.636-1.587-.636-1.587S0 9.9 0 8.605v-1.26zm6.348 2.73V5.58l4.323 2.255-4.32 2.24z"/></svg>
            </a>
          </li>
site__minima__social_links__youtube-->
              
      </ul>
    </div>
    </div>
  </div>

</footer>
'''

minimacss_classic_css = '''/* css from https://github.com/vadimkantorov/minimacss and https://github.com/jekyll/minima */

@media (prefers-color-scheme: light) and (max-width: 1000000px), (min-width: 0px) {
  :root {
    --minima-brand-color:                       var(--minima-light-brand-color);
    --minima-brand-color-light:                 var(--minima-light-brand-color-light);
    --minima-brand-color-dark:                  var(--minima-light-brand-color-dark );
    --minima-site-title-color:                  var(--minima-light-site-title-color);
    --minima-text-color:                        var(--minima-light-text-color);
    --minima-background-color:                  var(--minima-light-background-color);
    --minima-code-background-color:             var(--minima-light-code-background-color);
    --minima-link-base-color:                   var(--minima-light-link-base-color);
    --minima-link-visited-color:                var(--minima-light-link-visited-color);
    --minima-link-hover-color:                  var(--minima-light-link-hover-color);
    --minima-border-color-01:                   var(--minima-light-border-color-01);
    --minima-border-color-02:                   var(--minima-light-border-color-02);
    --minima-border-color-03:                   var(--minima-light-border-color-03);
    --minima-table-text-color:                  var(--minima-light-table-text-color);
    --minima-table-zebra-color:                 var(--minima-light-table-zebra-color);
    --minima-table-header-bg-color:             var(--minima-light-table-header-bg-color);
    --minima-table-header-border:               var(--minima-light-table-header-border);
    --minima-table-border-color:                var(--minima-light-table-border-color);
    --minima-highlight-c-color:                 var(--minima-light-highlight-c-color);
    --minima-highlight-c-font-style:            var(--minima-light-highlight-c-font-style);
    --minima-highlight-err-color:               var(--minima-light-highlight-err-color);
    --minima-highlight-err-background-color:    var(--minima-light-highlight-err-background-color);
    --minima-highlight-k-font-weight:           var(--minima-light-highlight-k-font-weight);
    --minima-highlight-o-font-weight:           var(--minima-light-highlight-o-font-weight);
    --minima-highlight-cm-color:                var(--minima-light-highlight-cm-color);
    --minima-highlight-cm-font-style:           var(--minima-light-highlight-cm-font-style);
    --minima-highlight-cp-color:                var(--minima-light-highlight-cp-color);
    --minima-highlight-cp-font-weight:          var(--minima-light-highlight-cp-font-weight);
    --minima-highlight-c1-color:                var(--minima-light-highlight-c1-color);
    --minima-highlight-c1-font-style:           var(--minima-light-highlight-c1-font-style);
    --minima-highlight-cs-color:                var(--minima-light-highlight-cs-color);
    --minima-highlight-cs-font-weight:          var(--minima-light-highlight-cs-font-weight);
    --minima-highlight-cs-font-style:           var(--minima-light-highlight-cs-font-style);
    --minima-highlight-gd-color:                var(--minima-light-highlight-gd-color);
    --minima-highlight-gd-background-color:     var(--minima-light-highlight-gd-background-color);
    --minima-highlight-gdx-color:               var(--minima-light-highlight-gdx-color);
    --minima-highlight-gdx-background-color:    var(--minima-light-highlight-gdx-background-color);
    --minima-highlight-ge-font-style:           var(--minima-light-highlight-ge-font-style);
    --minima-highlight-gr-color:                var(--minima-light-highlight-gr-color);
    --minima-highlight-gh-color:                var(--minima-light-highlight-gh-color);
    --minima-highlight-gi-color:                var(--minima-light-highlight-gi-color);
    --minima-highlight-gi-background-color:     var(--minima-light-highlight-gi-background-color);
    --minima-highlight-gix-color:               var(--minima-light-highlight-gix-color);
    --minima-highlight-gix-background-color:    var(--minima-light-highlight-gix-background-color);
    --minima-highlight-go-color:                var(--minima-light-highlight-go-color);
    --minima-highlight-gp-color:                var(--minima-light-highlight-gp-color);
    --minima-highlight-gs-font-weight:          var(--minima-light-highlight-gs-font-weight);
    --minima-highlight-gu-color:                var(--minima-light-highlight-gu-color);
    --minima-highlight-gt-color:                var(--minima-light-highlight-gt-color);
    --minima-highlight-kc-font-weight:          var(--minima-light-highlight-kc-font-weight);
    --minima-highlight-kd-font-weight:          var(--minima-light-highlight-kd-font-weight);
    --minima-highlight-kp-font-weight:          var(--minima-light-highlight-kp-font-weight);
    --minima-highlight-kr-font-weight:          var(--minima-light-highlight-kr-font-weight);
    --minima-highlight-kt-color:                var(--minima-light-highlight-kt-color);
    --minima-highlight-kt-font-weight:          var(--minima-light-highlight-kt-font-weight);
    --minima-highlight-m-color:                 var(--minima-light-highlight-m-color );
    --minima-highlight-s-color:                 var(--minima-light-highlight-s-color );
    --minima-highlight-na-color:                var(--minima-light-highlight-na-color);
    --minima-highlight-nb-color:                var(--minima-light-highlight-nb-color);
    --minima-highlight-nc-color:                var(--minima-light-highlight-nc-color);
    --minima-highlight-nc-font-weight:          var(--minima-light-highlight-nc-font-weight);
    --minima-highlight-no-color:                var(--minima-light-highlight-no-color);
    --minima-highlight-ni-color:                var(--minima-light-highlight-ni-color);
    --minima-highlight-ne-color:                var(--minima-light-highlight-ne-color);
    --minima-highlight-ne-font-weight:          var(--minima-light-highlight-ne-font-weight);
    --minima-highlight-nf-color:                var(--minima-light-highlight-nf-color);
    --minima-highlight-nf-font-weight:          var(--minima-light-highlight-nf-font-weight);
    --minima-highlight-nn-color:                var(--minima-light-highlight-nn-color);
    --minima-highlight-nt-color:                var(--minima-light-highlight-nt-color);
    --minima-highlight-nv-color:                var(--minima-light-highlight-nv-color);
    --minima-highlight-ow-font-weight:          var(--minima-light-highlight-ow-font-weight);
    --minima-highlight-w-color:                 var(--minima-light-highlight-w-color );
    --minima-highlight-mf-color:                var(--minima-light-highlight-mf-color);
    --minima-highlight-mh-color:                var(--minima-light-highlight-mh-color);
    --minima-highlight-mi-color:                var(--minima-light-highlight-mi-color);
    --minima-highlight-mo-color:                var(--minima-light-highlight-mo-color);
    --minima-highlight-sb-color:                var(--minima-light-highlight-sb-color);
    --minima-highlight-sc-color:                var(--minima-light-highlight-sc-color);
    --minima-highlight-sd-color:                var(--minima-light-highlight-sd-color);
    --minima-highlight-s2-color:                var(--minima-light-highlight-s2-color);
    --minima-highlight-se-color:                var(--minima-light-highlight-se-color);
    --minima-highlight-sh-color:                var(--minima-light-highlight-sh-color);
    --minima-highlight-si-color:                var(--minima-light-highlight-si-color);
    --minima-highlight-sx-color:                var(--minima-light-highlight-sx-color);
    --minima-highlight-sr-color:                var(--minima-light-highlight-sr-color);
    --minima-highlight-s1-color:                var(--minima-light-highlight-s1-color);
    --minima-highlight-ss-color:                var(--minima-light-highlight-ss-color);
    --minima-highlight-bp-color:                var(--minima-light-highlight-bp-color);
    --minima-highlight-vc-color:                var(--minima-light-highlight-vc-color);
    --minima-highlight-vg-color:                var(--minima-light-highlight-vg-color);
    --minima-highlight-vi-color:                var(--minima-light-highlight-vi-color);
    --minima-highlight-il-color:                var(--minima-light-highlight-il-color); } }

@media (prefers-color-scheme: dark) and (max-width: 0px), (min-width: 1000000px) {
  :root {
    --minima-brand-color:                       var(--minima-dark-brand-color);
    --minima-brand-color-light:                 var(--minima-dark-brand-color-light);
    --minima-brand-color-dark:                  var(--minima-dark-brand-color-dark );
    --minima-site-title-color:                  var(--minima-dark-site-title-color);
    --minima-text-color:                        var(--minima-dark-text-color);
    --minima-background-color:                  var(--minima-dark-background-color);
    --minima-code-background-color:             var(--minima-dark-code-background-color);
    --minima-link-base-color:                   var(--minima-dark-link-base-color);
    --minima-link-visited-color:                var(--minima-dark-link-visited-color);
    --minima-link-hover-color:                  var(--minima-dark-link-hover-color);
    --minima-border-color-01:                   var(--minima-dark-border-color-01);
    --minima-border-color-02:                   var(--minima-dark-border-color-02);
    --minima-border-color-03:                   var(--minima-dark-border-color-03);
    --minima-table-text-color:                  var(--minima-dark-table-text-color);
    --minima-table-zebra-color:                 var(--minima-dark-table-zebra-color);
    --minima-table-header-bg-color:             var(--minima-dark-table-header-bg-color);
    --minima-table-header-border:               var(--minima-dark-table-header-border);
    --minima-table-border-color:                var(--minima-dark-table-border-color);
    --minima-highlight-c-color:                 var(--minima-dark-highlight-c-color);
    --minima-highlight-c-font-style:            var(--minima-dark-highlight-c-font-style);
    --minima-highlight-err-color:               var(--minima-dark-highlight-err-color);
    --minima-highlight-err-background-color:    var(--minima-dark-highlight-err-background-color);
    --minima-highlight-k-font-weight:           var(--minima-dark-highlight-k-font-weight);
    --minima-highlight-o-font-weight:           var(--minima-dark-highlight-o-font-weight);
    --minima-highlight-cm-color:                var(--minima-dark-highlight-cm-color);
    --minima-highlight-cm-font-style:           var(--minima-dark-highlight-cm-font-style);
    --minima-highlight-cp-color:                var(--minima-dark-highlight-cp-color);
    --minima-highlight-cp-font-weight:          var(--minima-dark-highlight-cp-font-weight);
    --minima-highlight-c1-color:                var(--minima-dark-highlight-c1-color);
    --minima-highlight-c1-font-style:           var(--minima-dark-highlight-c1-font-style);
    --minima-highlight-cs-color:                var(--minima-dark-highlight-cs-color);
    --minima-highlight-cs-font-weight:          var(--minima-dark-highlight-cs-font-weight);
    --minima-highlight-cs-font-style:           var(--minima-dark-highlight-cs-font-style);
    --minima-highlight-gd-color:                var(--minima-dark-highlight-gd-color);
    --minima-highlight-gd-background-color:     var(--minima-dark-highlight-gd-background-color);
    --minima-highlight-gdx-color:               var(--minima-dark-highlight-gdx-color);
    --minima-highlight-gdx-background-color:    var(--minima-dark-highlight-gdx-background-color);
    --minima-highlight-ge-font-style:           var(--minima-dark-highlight-ge-font-style);
    --minima-highlight-gr-color:                var(--minima-dark-highlight-gr-color);
    --minima-highlight-gh-color:                var(--minima-dark-highlight-gh-color);
    --minima-highlight-gi-color:                var(--minima-dark-highlight-gi-color);
    --minima-highlight-gi-background-color:     var(--minima-dark-highlight-gi-background-color);
    --minima-highlight-gix-color:               var(--minima-dark-highlight-gix-color);
    --minima-highlight-gix-background-color:    var(--minima-dark-highlight-gix-background-color);
    --minima-highlight-go-color:                var(--minima-dark-highlight-go-color);
    --minima-highlight-gp-color:                var(--minima-dark-highlight-gp-color);
    --minima-highlight-gs-font-weight:          var(--minima-dark-highlight-gs-font-weight);
    --minima-highlight-gu-color:                var(--minima-dark-highlight-gu-color);
    --minima-highlight-gt-color:                var(--minima-dark-highlight-gt-color);
    --minima-highlight-kc-font-weight:          var(--minima-dark-highlight-kc-font-weight);
    --minima-highlight-kd-font-weight:          var(--minima-dark-highlight-kd-font-weight);
    --minima-highlight-kp-font-weight:          var(--minima-dark-highlight-kp-font-weight);
    --minima-highlight-kr-font-weight:          var(--minima-dark-highlight-kr-font-weight);
    --minima-highlight-kt-color:                var(--minima-dark-highlight-kt-color);
    --minima-highlight-kt-font-weight:          var(--minima-dark-highlight-kt-font-weight);
    --minima-highlight-m-color:                 var(--minima-dark-highlight-m-color );
    --minima-highlight-s-color:                 var(--minima-dark-highlight-s-color );
    --minima-highlight-na-color:                var(--minima-dark-highlight-na-color);
    --minima-highlight-nb-color:                var(--minima-dark-highlight-nb-color);
    --minima-highlight-nc-color:                var(--minima-dark-highlight-nc-color);
    --minima-highlight-nc-font-weight:          var(--minima-dark-highlight-nc-font-weight);
    --minima-highlight-no-color:                var(--minima-dark-highlight-no-color);
    --minima-highlight-ni-color:                var(--minima-dark-highlight-ni-color);
    --minima-highlight-ne-color:                var(--minima-dark-highlight-ne-color);
    --minima-highlight-ne-font-weight:          var(--minima-dark-highlight-ne-font-weight);
    --minima-highlight-nf-color:                var(--minima-dark-highlight-nf-color);
    --minima-highlight-nf-font-weight:          var(--minima-dark-highlight-nf-font-weight);
    --minima-highlight-nn-color:                var(--minima-dark-highlight-nn-color);
    --minima-highlight-nt-color:                var(--minima-dark-highlight-nt-color);
    --minima-highlight-nv-color:                var(--minima-dark-highlight-nv-color);
    --minima-highlight-ow-font-weight:          var(--minima-dark-highlight-ow-font-weight);
    --minima-highlight-w-color:                 var(--minima-dark-highlight-w-color );
    --minima-highlight-mf-color:                var(--minima-dark-highlight-mf-color);
    --minima-highlight-mh-color:                var(--minima-dark-highlight-mh-color);
    --minima-highlight-mi-color:                var(--minima-dark-highlight-mi-color);
    --minima-highlight-mo-color:                var(--minima-dark-highlight-mo-color);
    --minima-highlight-sb-color:                var(--minima-dark-highlight-sb-color);
    --minima-highlight-sc-color:                var(--minima-dark-highlight-sc-color);
    --minima-highlight-sd-color:                var(--minima-dark-highlight-sd-color);
    --minima-highlight-s2-color:                var(--minima-dark-highlight-s2-color);
    --minima-highlight-se-color:                var(--minima-dark-highlight-se-color);
    --minima-highlight-sh-color:                var(--minima-dark-highlight-sh-color);
    --minima-highlight-si-color:                var(--minima-dark-highlight-si-color);
    --minima-highlight-sx-color:                var(--minima-dark-highlight-sx-color);
    --minima-highlight-sr-color:                var(--minima-dark-highlight-sr-color);
    --minima-highlight-s1-color:                var(--minima-dark-highlight-s1-color);
    --minima-highlight-ss-color:                var(--minima-dark-highlight-ss-color);
    --minima-highlight-bp-color:                var(--minima-dark-highlight-bp-color);
    --minima-highlight-vc-color:                var(--minima-dark-highlight-vc-color);
    --minima-highlight-vg-color:                var(--minima-dark-highlight-vg-color);
    --minima-highlight-vi-color:                var(--minima-dark-highlight-vi-color);
    --minima-highlight-il-color:                var(--minima-dark-highlight-il-color); } }

'''
minimacss_auto_css = '''

/* begin skins/auto.scss */
:root {
  /* Light mode */
  --minima-light-brand-color-hue: 0;
  --minima-light-brand-color-saturation: 0%;
  --minima-light-brand-color-lightness: 51%;
  --minima-light-text-color-hue: 0;
  --minima-light-text-color-saturation: 0%;
  --minima-light-text-color-lightness: 7%;
  --minima-light-link-base-color-hue: 214;
  --minima-light-link-base-color-saturation: 76%;
  --minima-light-link-base-color-lightness: 53%;
  --minima-light-brand-color:          hsl(var(--minima-light-brand-color-hue), var(--minima-light-brand-color-saturation), var(--minima-light-brand-color-lightness));
  --minima-light-brand-color-light:    hsl(var(--minima-light-brand-color-hue), var(--minima-light-brand-color-saturation), calc(var(--minima-light-brand-color-lightness) + 40%));
  --minima-light-brand-color-dark:    hsl(var(--minima-light-brand-color-hue), var(--minima-light-brand-color-saturation), calc(var(--minima-light-brand-color-lightness) - 25%));
  --minima-light-site-title-color:     var(--minima-light-brand-color-dark);
  --minima-light-text-color:           hsl(var(--minima-light-text-color-hue), var(--minima-light-text-color-saturation), var(--minima-light-text-color-lightness));
  --minima-light-background-color:     #fdfdfd;
  --minima-light-code-background-color:#eeeeff;
  --minima-light-link-base-color:      hsl(var(--minima-light-link-base-color-hue), var(--minima-light-link-base-color-saturation), var(--minima-light-link-base-color-lightness)) ;
  --minima-light-link-visited-color:   hsl(var(--minima-light-link-base-color-hue), var(--minima-light-link-base-color-saturation), calc(var(--minima-light-link-base-color-lightness) - 15%)) ;
  --minima-light-link-hover-color:     var(--minima-light-text-color) ;
  --minima-light-border-color-01:      var(--minima-light-brand-color-light) ;
  --minima-light-border-color-02:      hsl(var(--minima-light-brand-color-hue), var(--minima-light-brand-color-saturation), calc(var(--minima-light-brand-color-lightness) + 35%)) ;
  --minima-light-border-color-03:      var(--minima-light-brand-color-dark) ;
  --minima-light-table-text-color:     hsl(var(--minima-light-text-color-hue), var(--minima-light-text-color-saturation), calc(var(--minima-light-text-color-lightness) + 18%)) ;
  --minima-light-table-zebra-color:    hsl(var(--minima-light-brand-color-hue), var(--minima-light-brand-color-saturation), calc(var(--minima-light-brand-color-lightness) + 46%)) ;
  --minima-light-table-header-bg-color:hsl(var(--minima-light-brand-color-hue), var(--minima-light-brand-color-saturation), calc(var(--minima-light-brand-color-lightness) + 43%)) ;
  --minima-light-table-header-border:  hsl(var(--minima-light-brand-color-hue), var(--minima-light-brand-color-saturation), calc(var(--minima-light-brand-color-lightness) + 37%)) ;
  --minima-light-table-border-color:   var(--minima-light-border-color-01) ;
  /* Dark mode */
  --minima-dark-brand-color-hue: 0;
  --minima-dark-brand-color-saturation: 0%;
  --minima-dark-brand-color-lightness: 60%;
  --minima-dark-background-color-hue: 0;
  --minima-dark-background-color-saturation: 0%;
  --minima-dark-background-color-lightness: 9%;
  --minima-dark-brand-color:           hsl(var(--minima-dark-brand-color-hue), var(--minima-dark-brand-color-saturation), var(--minima-dark-brand-color-lightness));
  --minima-dark-brand-color-light:     hsl(var(--minima-dark-brand-color-hue), var(--minima-dark-brand-color-saturation), calc(var(--minima-dark-brand-color-lightness) + 5%));
  --minima-dark-brand-color-dark:      hsl(var(--minima-dark-brand-color-hue), var(--minima-dark-brand-color-saturation), calc(var(--minima-dark-brand-color-lightness) - 35%));
  --minima-dark-site-title-color:      var(--minima-dark-brand-color-lightt);
  --minima-dark-text-color:            #bbbbbb;
  --minima-dark-background-color:      hsl(var(--minima-dark-background-color-hue), var(--minima-dark-background-color-saturation), var(--minima-dark-background-color-lightness));
  --minima-dark-code-background-color: #212121;
  --minima-dark-link-base-color:       #79b8ff ;
  --minima-dark-link-visited-color:    var(--minima-dark-link-base-color);
  --minima-dark-link-hover-color:      var(--minima-dark-text-color);
  --minima-dark-border-color-01:       var(--minima-dark-brand-color-dark);
  --minima-dark-border-color-02:       var(--minima-dark-brand-color-light);
  --minima-dark-border-color-03:       var(--minima-dark-brand-color);
  --minima-dark-table-text-color:      var(--minima-dark-text-color);
  --minima-dark-table-zebra-color:     hsl(var(--minima-dark-background-color-hue), var(--minima-dark-background-color-saturation), calc(var(--minima-dark-background-color-lightness) + 4%));
  --minima-dark-table-header-bg-color: hsl(var(--minima-dark-background-color-hue), var(--minima-dark-background-color-saturation), calc(var(--minima-dark-background-color-lightness) + 10%));
  --minima-dark-table-header-border:   hsl(var(--minima-dark-background-color-hue), var(--minima-dark-background-color-saturation), calc(var(--minima-dark-background-color-lightness) + 21%));
  --minima-dark-table-border-color:    var(--minima-dark-border-color-01); }

/*
// Syntax highlighting styles should be adjusted appropriately for every "skin"
// ----------------------------------------------------------------------------
*/
/* .lm-highlight */
:root {
  --minima-light-highlight-c-color: #998;
  /*Comment*/
  --minima-light-highlight-c-font-style: italic ;
  /*Comment*/
  --minima-light-highlight-err-color: #a61717;
  /*Error*/
  --minima-light-highlight-err-background-color: #e3d2d2 ;
  /*Error*/
  --minima-light-highlight-k-font-weight: bold ;
  /*Keyword*/
  --minima-light-highlight-o-font-weight: bold ;
  /*Operator*/
  --minima-light-highlight-cm-color: #998;
  /*Comment.Multiline*/
  --minima-light-highlight-cm-font-style: italic ;
  /*Comment.Multiline*/
  --minima-light-highlight-cp-color: #999;
  /*Comment.Preproc*/
  --minima-light-highlight-cp-font-weight: bold ;
  /*Comment.Preproc*/
  --minima-light-highlight-c1-color: #998;
  /*Comment.Single*/
  --minima-light-highlight-c1-font-style: italic ;
  /*Comment.Single*/
  --minima-light-highlight-cs-color: #999;
  /*Comment.Special*/
  --minima-light-highlight-cs-font-weight: bold;
  /*Comment.Special*/
  --minima-light-highlight-cs-font-style: italic ;
  /*Comment.Special*/
  --minima-light-highlight-gd-color: #000;
  /*Generic.Deleted*/
  --minima-light-highlight-gd-background-color: #fdd ;
  /*Generic.Deleted*/
  --minima-light-highlight-gdx-color: #000;
  /*Generic.Deleted.Specific*/
  --minima-light-highlight-gdx-background-color: #faa ;
  /*Generic.Deleted.Specific*/
  --minima-light-highlight-ge-font-style: italic ;
  /*Generic.Emph*/
  --minima-light-highlight-gr-color: #a00 ;
  /*Generic.Error*/
  --minima-light-highlight-gh-color: #999 ;
  /*Generic.Heading*/
  --minima-light-highlight-gi-color: #000;
  /*Generic.Inserted*/
  --minima-light-highlight-gi-background-color: #dfd ;
  /*Generic.Inserted*/
  --minima-light-highlight-gix-color: #000;
  /*Generic.Inserted.Specific*/
  --minima-light-highlight-gix-background-color: #afa ;
  /*Generic.Inserted.Specific*/
  --minima-light-highlight-go-color: #888 ;
  /*Generic.Output*/
  --minima-light-highlight-gp-color: #555 ;
  /*Generic.Prompt*/
  --minima-light-highlight-gs-font-weight: bold ;
  /*Generic.Strong*/
  --minima-light-highlight-gu-color: #aaa ;
  /*Generic.Subheading*/
  --minima-light-highlight-gt-color: #a00 ;
  /*Generic.Traceback*/
  --minima-light-highlight-kc-font-weight: bold ;
  /*Keyword.Constant*/
  --minima-light-highlight-kd-font-weight: bold ;
  /*Keyword.Declaration*/
  --minima-light-highlight-kp-font-weight: bold ;
  /*Keyword.Pseudo*/
  --minima-light-highlight-kr-font-weight: bold ;
  /*Keyword.Reserved*/
  --minima-light-highlight-kt-color: #458;
  /*Keyword.Type */
  --minima-light-highlight-kt-font-weight: bold ;
  /*Keyword.Type*/
  --minima-light-highlight-m-color: #099 ;
  /*Literal.Number*/
  --minima-light-highlight-s-color: #d14 ;
  /*Literal.String*/
  --minima-light-highlight-na-color: #008080 ;
  /*Name.Attribute*/
  --minima-light-highlight-nb-color: #0086B3 ;
  /*Name.Builtin*/
  --minima-light-highlight-nc-color: #458;
  /*Name.Class*/
  --minima-light-highlight-nc-font-weight: bold ;
  /*Name.Class*/
  --minima-light-highlight-no-color: #008080 ;
  /*Name.Constant*/
  --minima-light-highlight-ni-color: #800080 ;
  /*Name.Entity*/
  --minima-light-highlight-ne-color: #900;
  /*Name.Exception*/
  --minima-light-highlight-ne-font-weight: bold ;
  /*Name.Exception*/
  --minima-light-highlight-nf-color: #900;
  /*Name.Function*/
  --minima-light-highlight-nf-font-weight: bold ;
  /*Name.Function*/
  --minima-light-highlight-nn-color: #555;
  /*Name.Namespace*/
  --minima-light-highlight-nt-color: #000080;
  /*Name.Tag*/
  --minima-light-highlight-nv-color: #008080;
  /*Name.Variable*/
  --minima-light-highlight-ow-font-weight: bold ;
  /*Operator.Word*/
  --minima-light-highlight-w-color: #bbb;
  /*Text.Whitespace*/
  --minima-light-highlight-mf-color: #099;
  /*Literal.Number.Float*/
  --minima-light-highlight-mh-color: #099;
  /*Literal.Number.Hex*/
  --minima-light-highlight-mi-color: #099;
  /*Literal.Number.Integer*/
  --minima-light-highlight-mo-color: #099;
  /*Literal.Number.Oct*/
  --minima-light-highlight-sb-color: #d14;
  /*Literal.String.Backtick*/
  --minima-light-highlight-sc-color: #d14;
  /*Literal.String.Char*/
  --minima-light-highlight-sd-color: #d14;
  /*Literal.String.Doc*/
  --minima-light-highlight-s2-color: #d14;
  /*Literal.String.Double*/
  --minima-light-highlight-se-color: #d14;
  /*Literal.String.Escape*/
  --minima-light-highlight-sh-color: #d14;
  /*Literal.String.Heredoc*/
  --minima-light-highlight-si-color: #d14;
  /*Literal.String.Interpol*/
  --minima-light-highlight-sx-color: #d14;
  /*Literal.String.Other*/
  --minima-light-highlight-sr-color: #009926;
  /*Literal.String.Regex*/
  --minima-light-highlight-s1-color: #d14;
  /*Literal.String.Single*/
  --minima-light-highlight-ss-color: #990073;
  /*Literal.String.Symbol*/
  --minima-light-highlight-bp-color: #999;
  /*Name.Builtin.Pseudo*/
  --minima-light-highlight-vc-color: #008080;
  /*Name.Variable.Class*/
  --minima-light-highlight-vg-color: #008080;
  /*Name.Variable.Global*/
  --minima-light-highlight-vi-color: #008080;
  /*Name.Variable.Instance*/
  --minima-light-highlight-il-color: #099;
  /*Literal.Number.Integer.Long*/ }

/* .dm-highlight */
:root {
  --minima-dark-highlight-c-color: #545454;
  /*Comment*/
  --minima-dark-highlight-c-font-style: italic ;
  /*Comment*/
  --minima-dark-highlight-err-color: #f07178;
  /*Error*/
  --minima-dark-highlight-err-background-color: #e3d2d2 ;
  /*Error*/
  --minima-dark-highlight-k-color: #89DDFF;
  /*Keyword*/
  --minima-dark-highlight-k-font-weight: bold ;
  /*Keyword*/
  --minima-dark-highlight-o-font-weight: bold ;
  /*Operator*/
  --minima-dark-highlight-cm-color: #545454;
  /*Comment.Multiline*/
  --minima-dark-highlight-cm-font-style: italic ;
  /*Comment.Multiline*/
  --minima-dark-highlight-cp-color: #545454;
  /*Comment.Preproc*/
  --minima-dark-highlight-cp-font-weight: bold ;
  /*Comment.Preproc*/
  --minima-dark-highlight-c1-color: #545454;
  /*Comment.Single*/
  --minima-dark-highlight-c1-font-style: italic ;
  /*Comment.Single*/
  --minima-dark-highlight-cs-color: #545454;
  /*Comment.Special*/
  --minima-dark-highlight-cs-font-weight: bold;
  /*Comment.Special*/
  --minima-dark-highlight-cs-font-style: italic ;
  /*Comment.Special*/
  --minima-dark-highlight-gd-color: #000;
  /*Generic.Deleted*/
  --minima-dark-highlight-gd-background-color: #fdd;
  /*Generic.Deleted*/
  --minima-dark-highlight-gdx-color: #000;
  /*Generic.Deleted.Specific*/
  --minima-dark-highlight-gdx-background-color: #faa ;
  /*Generic.Deleted.Specific*/
  --minima-dark-highlight-ge-font-style: italic ;
  /*Generic.Emph*/
  --minima-dark-highlight-gr-color: #f07178 ;
  /*Generic.Error*/
  --minima-dark-highlight-gh-color: #999 ;
  /*Generic.Heading*/
  --minima-dark-highlight-gi-color: #000;
  /*Generic.Inserted*/
  --minima-dark-highlight-gi-background-color: #dfd ;
  /*Generic.Inserted*/
  --minima-dark-highlight-gix-color: #000;
  /*Generic.Inserted.Specific*/
  --minima-dark-highlight-gix-background-color: #afa ;
  /*Generic.Inserted.Specific*/
  --minima-dark-highlight-go-color: #888 ;
  /*Generic.Output*/
  --minima-dark-highlight-gp-color: #555 ;
  /*Generic.Prompt*/
  --minima-dark-highlight-gs-font-weight: bold ;
  /*Generic.Strong*/
  --minima-dark-highlight-gu-color: #aaa ;
  /*Generic.Subheading*/
  --minima-dark-highlight-gt-color: #f07178 ;
  /*Generic.Traceback*/
  --minima-dark-highlight-kc-font-weight: bold ;
  /*Keyword.Constant*/
  --minima-dark-highlight-kd-font-weight: bold ;
  /*Keyword.Declaration*/
  --minima-dark-highlight-kp-font-weight: bold ;
  /*Keyword.Pseudo*/
  --minima-dark-highlight-kr-font-weight: bold ;
  /*Keyword.Reserved*/
  --minima-dark-highlight-kt-color: #FFCB6B;
  /*Keyword.Type*/
  --minima-dark-highlight-kt-font-weight: bold ;
  /*Keyword.Type*/
  --minima-dark-highlight-m-color: #F78C6C ;
  /*Literal.Number*/
  --minima-dark-highlight-s-color: #C3E88D ;
  /*Literal.String*/
  --minima-dark-highlight-na-color: #008080 ;
  /*Name.Attribute*/
  --minima-dark-highlight-nb-color: #EEFFFF ;
  /*Name.Builtin*/
  --minima-dark-highlight-nc-color: #FFCB6B;
  /*Name.Class*/
  --minima-dark-highlight-nc-font-weight: bold ;
  /*Name.Class*/
  --minima-dark-highlight-no-color: #008080 ;
  /*Name.Constant*/
  --minima-dark-highlight-ni-color: #800080 ;
  /*Name.Entity*/
  --minima-dark-highlight-ne-color: #900;
  /*Name.Exception*/
  --minima-dark-highlight-ne-font-weight: bold ;
  /*Name.Exception*/
  --minima-dark-highlight-nf-color: #82AAFF;
  /*Name.Function*/
  --minima-dark-highlight-nf-font-weight: bold ;
  /*Name.Function*/
  --minima-dark-highlight-nn-color: #555 ;
  /*Name.Namespace*/
  --minima-dark-highlight-nt-color: #FFCB6B ;
  /*Name.Tag*/
  --minima-dark-highlight-nv-color: #EEFFFF ;
  /*Name.Variable*/
  --minima-dark-highlight-ow-font-weight: bold ;
  /*Operator.Word*/
  --minima-dark-highlight-w-color: #EEFFFF ;
  /*Text.Whitespace*/
  --minima-dark-highlight-mf-color: #F78C6C ;
  /*Literal.Number.Float*/
  --minima-dark-highlight-mh-color: #F78C6C ;
  /*Literal.Number.Hex*/
  --minima-dark-highlight-mi-color: #F78C6C ;
  /*Literal.Number.Integer*/
  --minima-dark-highlight-mo-color: #F78C6C ;
  /*Literal.Number.Oct*/
  --minima-dark-highlight-sb-color: #C3E88D ;
  /*Literal.String.Backtick*/
  --minima-dark-highlight-sc-color: #C3E88D ;
  /*Literal.String.Char*/
  --minima-dark-highlight-sd-color: #C3E88D ;
  /*Literal.String.Doc*/
  --minima-dark-highlight-s2-color: #C3E88D ;
  /*Literal.String.Double*/
  --minima-dark-highlight-se-color: #EEFFFF ;
  /*Literal.String.Escape*/
  --minima-dark-highlight-sh-color: #C3E88D ;
  /*Literal.String.Heredoc*/
  --minima-dark-highlight-si-color: #C3E88D ;
  /*Literal.String.Interpol*/
  --minima-dark-highlight-sx-color: #C3E88D ;
  /*Literal.String.Other*/
  --minima-dark-highlight-sr-color: #C3E88D ;
  /*Literal.String.Regex*/
  --minima-dark-highlight-s1-color: #C3E88D ;
  /*Literal.String.Single*/
  --minima-dark-highlight-ss-color: #C3E88D ;
  /*Literal.String.Symbol*/
  --minima-dark-highlight-bp-color: #999 ;
  /*Name.Builtin.Pseudo*/
  --minima-dark-highlight-vc-color: #FFCB6B ;
  /*Name.Variable.Class*/
  --minima-dark-highlight-vg-color: #EEFFFF ;
  /*Name.Variable.Global*/
  --minima-dark-highlight-vi-color: #EEFFFF ;
  /*Name.Variable.Instance*/
  --minima-dark-highlight-il-color: #F78C6C ;
  /*Literal.Number.Integer.Long*/ }

.highlight {
  /* Comment*/
  /* Error*/
  /* Keyword*/
  /* Operator*/
  /* Comment.Multiline*/
  /* Comment.Preproc*/
  /* Comment.Single*/
  /* Comment.Special*/
  /* Generic.Deleted*/
  /* Generic.Deleted.Specific*/
  /* Generic.Emph*/
  /* Generic.Error*/
  /* Generic.Heading*/
  /* Generic.Inserted*/
  /* Generic.Inserted.Specific*/
  /* Generic.Output*/
  /* Generic.Prompt*/
  /* Generic.Strong*/
  /* Generic.Subheading*/
  /* Generic.Traceback*/
  /* Keyword.Constant*/
  /* Keyword.Declaration*/
  /* Keyword.Pseudo*/
  /* Keyword.Reserved*/
  /* Keyword.Type*/
  /* Literal.Number*/
  /* Literal.String*/
  /* Name.Attribute*/
  /* Name.Builtin*/
  /* Name.Class*/
  /* Name.Constant*/
  /* Name.Entity*/
  /* Name.Exception*/
  /* Name.Function*/
  /* Name.Namespace*/
  /* Name.Tag*/
  /* Name.Variable*/
  /* Operator.Word*/
  /* Text.Whitespace*/
  /* Literal.Number.Float*/
  /* Literal.Number.Hex*/
  /* Literal.Number.Integer*/
  /* Literal.Number.Oct*/
  /* Literal.String.Backtick*/
  /* Literal.String.Char*/
  /* Literal.String.Doc*/
  /* Literal.String.Double*/
  /* Literal.String.Escape*/
  /* Literal.String.Heredoc*/
  /* Literal.String.Interpol*/
  /* Literal.String.Other*/
  /* Literal.String.Regex*/
  /* Literal.String.Single*/
  /* Literal.String.Symbol*/
  /* Name.Builtin.Pseudo*/
  /* Name.Variable.Class*/
  /* Name.Variable.Global*/
  /* Name.Variable.Instance*/
  /* Literal.Number.Integer.Long*/ }
  .highlight .c {
    color: var(--minima-highlight-c-color);
    background-color: var(--minima-highlight-c-background-color);
    font-style: var(--minima-highlight-c-font-style);
    font-weight: var(--minima-highlight-c-font-weight); }
  .highlight .err {
    color: var(--minima-highlight-err-color);
    background-color: var(--minima-highlight-err-background-color);
    font-style: var(--minima-highlight-err-font-style);
    font-weight: var(--minima-highlight-err-font-weight); }
  .highlight .k {
    color: var(--minima-highlight-k-color);
    background-color: var(--minima-highlight-k-background-color);
    font-style: var(--minima-highlight-k-font-style);
    font-weight: var(--minima-highlight-k-font-weight); }
  .highlight .o {
    color: var(--minima-highlight-o-color);
    background-color: var(--minima-highlight-o-background-color);
    font-style: var(--minima-highlight-o-font-style);
    font-weight: var(--minima-highlight-o-font-weight); }
  .highlight .cm {
    color: var(--minima-highlight-cm-color);
    background-color: var(--minima-highlight-cm-background-color);
    font-style: var(--minima-highlight-cm-font-style);
    font-weight: var(--minima-highlight-cm-font-weight); }
  .highlight .cp {
    color: var(--minima-highlight-cp-color);
    background-color: var(--minima-highlight-cp-background-color);
    font-style: var(--minima-highlight-cp-font-style);
    font-weight: var(--minima-highlight-cp-font-weight); }
  .highlight .c1 {
    color: var(--minima-highlight-c1-color);
    background-color: var(--minima-highlight-c1-background-color);
    font-style: var(--minima-highlight-c1-font-style);
    font-weight: var(--minima-highlight-c1-font-weight); }
  .highlight .cs {
    color: var(--minima-highlight-cs-color);
    background-color: var(--minima-highlight-cs-background-color);
    font-style: var(--minima-highlight-cs-font-style);
    font-weight: var(--minima-highlight-cs-font-weight); }
  .highlight .gd {
    color: var(--minima-highlight-gd-color);
    background-color: var(--minima-highlight-gd-background-color);
    font-style: var(--minima-highlight-gd-font-style);
    font-weight: var(--minima-highlight-gd-font-weight); }
  .highlight .gd .x {
    color: var(--minima-highlight-gdx-color);
    background-color: var(--minima-highlight-gdx-background-color);
    font-style: var(--minima-highlight-gdx-font-style);
    font-weight: var(--minima-highlight-gdx-font-weight); }
  .highlight .ge {
    color: var(--minima-highlight-ge-color);
    background-color: var(--minima-highlight-ge-background-color);
    font-style: var(--minima-highlight-ge-font-style);
    font-weight: var(--minima-highlight-ge-font-weight); }
  .highlight .gr {
    color: var(--minima-highlight-gr-color);
    background-color: var(--minima-highlight-gr-background-color);
    font-style: var(--minima-highlight-gr-font-style);
    font-weight: var(--minima-highlight-gr-font-weight); }
  .highlight .gh {
    color: var(--minima-highlight-gh-color);
    background-color: var(--minima-highlight-gh-background-color);
    font-style: var(--minima-highlight-gh-font-style);
    font-weight: var(--minima-highlight-gh-font-weight); }
  .highlight .gi {
    color: var(--minima-highlight-gi-color);
    background-color: var(--minima-highlight-gi-background-color);
    font-style: var(--minima-highlight-gi-font-style);
    font-weight: var(--minima-highlight-gi-font-weight); }
  .highlight .gi .x {
    color: var(--minima-highlight-gix-color);
    background-color: var(--minima-highlight-gix-background-color);
    font-style: var(--minima-highlight-gix-font-style);
    font-weight: var(--minima-highlight-gix-font-weight); }
  .highlight .go {
    color: var(--minima-highlight-go-color);
    background-color: var(--minima-highlight-go-background-color);
    font-style: var(--minima-highlight-go-font-style);
    font-weight: var(--minima-highlight-go-font-weight); }
  .highlight .gp {
    color: var(--minima-highlight-gp-color);
    background-color: var(--minima-highlight-gp-background-color);
    font-style: var(--minima-highlight-gp-font-style);
    font-weight: var(--minima-highlight-gp-font-weight); }
  .highlight .gs {
    color: var(--minima-highlight-gs-color);
    background-color: var(--minima-highlight-gs-background-color);
    font-style: var(--minima-highlight-gs-font-style);
    font-weight: var(--minima-highlight-gs-font-weight); }
  .highlight .gu {
    color: var(--minima-highlight-gu-color);
    background-color: var(--minima-highlight-gu-background-color);
    font-style: var(--minima-highlight-gu-font-style);
    font-weight: var(--minima-highlight-gu-font-weight); }
  .highlight .gt {
    color: var(--minima-highlight-gt-color);
    background-color: var(--minima-highlight-gt-background-color);
    font-style: var(--minima-highlight-gt-font-style);
    font-weight: var(--minima-highlight-gt-font-weight); }
  .highlight .kc {
    color: var(--minima-highlight-kc-color);
    background-color: var(--minima-highlight-kc-background-color);
    font-style: var(--minima-highlight-kc-font-style);
    font-weight: var(--minima-highlight-kc-font-weight); }
  .highlight .kd {
    color: var(--minima-highlight-kd-color);
    background-color: var(--minima-highlight-kd-background-color);
    font-style: var(--minima-highlight-kd-font-style);
    font-weight: var(--minima-highlight-kd-font-weight); }
  .highlight .kp {
    color: var(--minima-highlight-kp-color);
    background-color: var(--minima-highlight-kp-background-color);
    font-style: var(--minima-highlight-kp-font-style);
    font-weight: var(--minima-highlight-kp-font-weight); }
  .highlight .kr {
    color: var(--minima-highlight-kr-color);
    background-color: var(--minima-highlight-kr-background-color);
    font-style: var(--minima-highlight-kr-font-style);
    font-weight: var(--minima-highlight-kr-font-weight); }
  .highlight .kt {
    color: var(--minima-highlight-kt-color);
    background-color: var(--minima-highlight-kt-background-color);
    font-style: var(--minima-highlight-kt-font-style);
    font-weight: var(--minima-highlight-kt-font-weight); }
  .highlight .m {
    color: var(--minima-highlight-m-color);
    background-color: var(--minima-highlight-m-background-color);
    font-style: var(--minima-highlight-m-font-style);
    font-weight: var(--minima-highlight-m-font-weight); }
  .highlight .s {
    color: var(--minima-highlight-s-color);
    background-color: var(--minima-highlight-s-background-color);
    font-style: var(--minima-highlight-s-font-style);
    font-weight: var(--minima-highlight-s-font-weight); }
  .highlight .na {
    color: var(--minima-highlight-na-color);
    background-color: var(--minima-highlight-na-background-color);
    font-style: var(--minima-highlight-na-font-style);
    font-weight: var(--minima-highlight-na-font-weight); }
  .highlight .nb {
    color: var(--minima-highlight-nb-color);
    background-color: var(--minima-highlight-nb-background-color);
    font-style: var(--minima-highlight-nb-font-style);
    font-weight: var(--minima-highlight-nb-font-weight); }
  .highlight .nc {
    color: var(--minima-highlight-nc-color);
    background-color: var(--minima-highlight-nc-background-color);
    font-style: var(--minima-highlight-nc-font-style);
    font-weight: var(--minima-highlight-nc-font-weight); }
  .highlight .no {
    color: var(--minima-highlight-no-color);
    background-color: var(--minima-highlight-no-background-color);
    font-style: var(--minima-highlight-no-font-style);
    font-weight: var(--minima-highlight-no-font-weight); }
  .highlight .ni {
    color: var(--minima-highlight-ni-color);
    background-color: var(--minima-highlight-ni-background-color);
    font-style: var(--minima-highlight-ni-font-style);
    font-weight: var(--minima-highlight-ni-font-weight); }
  .highlight .ne {
    color: var(--minima-highlight-ne-color);
    background-color: var(--minima-highlight-ne-background-color);
    font-style: var(--minima-highlight-ne-font-style);
    font-weight: var(--minima-highlight-ne-font-weight); }
  .highlight .nf {
    color: var(--minima-highlight-nf-color);
    background-color: var(--minima-highlight-nf-background-color);
    font-style: var(--minima-highlight-nf-font-style);
    font-weight: var(--minima-highlight-nf-font-weight); }
  .highlight .nn {
    color: var(--minima-highlight-nn-color);
    background-color: var(--minima-highlight-nn-background-color);
    font-style: var(--minima-highlight-nn-font-style);
    font-weight: var(--minima-highlight-nn-font-weight); }
  .highlight .nt {
    color: var(--minima-highlight-nt-color);
    background-color: var(--minima-highlight-nt-background-color);
    font-style: var(--minima-highlight-nt-font-style);
    font-weight: var(--minima-highlight-nt-font-weight); }
  .highlight .nv {
    color: var(--minima-highlight-nv-color);
    background-color: var(--minima-highlight-nv-background-color);
    font-style: var(--minima-highlight-nv-font-style);
    font-weight: var(--minima-highlight-nv-font-weight); }
  .highlight .ow {
    color: var(--minima-highlight-ow-color);
    background-color: var(--minima-highlight-ow-background-color);
    font-style: var(--minima-highlight-ow-font-style);
    font-weight: var(--minima-highlight-ow-font-weight); }
  .highlight .w {
    color: var(--minima-highlight-w-color);
    background-color: var(--minima-highlight-w-background-color);
    font-style: var(--minima-highlight-w-font-style);
    font-weight: var(--minima-highlight-w-font-weight); }
  .highlight .mf {
    color: var(--minima-highlight-mf-color);
    background-color: var(--minima-highlight-mf-background-color);
    font-style: var(--minima-highlight-mf-font-style);
    font-weight: var(--minima-highlight-mf-font-weight); }
  .highlight .mh {
    color: var(--minima-highlight-nh-color);
    background-color: var(--minima-highlight-nh-background-color);
    font-style: var(--minima-highlight-nh-font-style);
    font-weight: var(--minima-highlight-nh-font-weight); }
  .highlight .mi {
    color: var(--minima-highlight-mi-color);
    background-color: var(--minima-highlight-mi-background-color);
    font-style: var(--minima-highlight-mi-font-style);
    font-weight: var(--minima-highlight-mi-font-weight); }
  .highlight .mo {
    color: var(--minima-highlight-mo-color);
    background-color: var(--minima-highlight-mo-background-color);
    font-style: var(--minima-highlight-mo-font-style);
    font-weight: var(--minima-highlight-mo-font-weight); }
  .highlight .sb {
    color: var(--minima-highlight-sb-color);
    background-color: var(--minima-highlight-sb-background-color);
    font-style: var(--minima-highlight-sb-font-style);
    font-weight: var(--minima-highlight-sb-font-weight); }
  .highlight .sc {
    color: var(--minima-highlight-sc-color);
    background-color: var(--minima-highlight-sc-background-color);
    font-style: var(--minima-highlight-sc-font-style);
    font-weight: var(--minima-highlight-sc-font-weight); }
  .highlight .sd {
    color: var(--minima-highlight-sd-color);
    background-color: var(--minima-highlight-sd-background-color);
    font-style: var(--minima-highlight-sd-font-style);
    font-weight: var(--minima-highlight-sd-font-weight); }
  .highlight .s2 {
    color: var(--minima-highlight-s2-color);
    background-color: var(--minima-highlight-s2-background-color);
    font-style: var(--minima-highlight-s2-font-style);
    font-weight: var(--minima-highlight-s2-font-weight); }
  .highlight .se {
    color: var(--minima-highlight-se-color);
    background-color: var(--minima-highlight-se-background-color);
    font-style: var(--minima-highlight-se-font-style);
    font-weight: var(--minima-highlight-se-font-weight); }
  .highlight .sh {
    color: var(--minima-highlight-sh-color);
    background-color: var(--minima-highlight-sh-background-color);
    font-style: var(--minima-highlight-sh-font-style);
    font-weight: var(--minima-highlight-sh-font-weight); }
  .highlight .si {
    color: var(--minima-highlight-si-color);
    background-color: var(--minima-highlight-si-background-color);
    font-style: var(--minima-highlight-si-font-style);
    font-weight: var(--minima-highlight-si-font-weight); }
  .highlight .sx {
    color: var(--minima-highlight-sx-color);
    background-color: var(--minima-highlight-sx-background-color);
    font-style: var(--minima-highlight-sx-font-style);
    font-weight: var(--minima-highlight-sx-font-weight); }
  .highlight .sr {
    color: var(--minima-highlight-sr-color);
    background-color: var(--minima-highlight-sr-background-color);
    font-style: var(--minima-highlight-sr-font-style);
    font-weight: var(--minima-highlight-sr-font-weight); }
  .highlight .s1 {
    color: var(--minima-highlight-s1-color);
    background-color: var(--minima-highlight-s1-background-color);
    font-style: var(--minima-highlight-s1-font-style);
    font-weight: var(--minima-highlight-s1-font-weight); }
  .highlight .ss {
    color: var(--minima-highlight-ss-color);
    background-color: var(--minima-highlight-ss-background-color);
    font-style: var(--minima-highlight-ss-font-style);
    font-weight: var(--minima-highlight-ss-font-weight); }
  .highlight .bp {
    color: var(--minima-highlight-bp-color);
    background-color: var(--minima-highlight-bp-background-color);
    font-style: var(--minima-highlight-bp-font-style);
    font-weight: var(--minima-highlight-bp-font-weight); }
  .highlight .vc {
    color: var(--minima-highlight-vc-color);
    background-color: var(--minima-highlight-vc-background-color);
    font-style: var(--minima-highlight-vc-font-style);
    font-weight: var(--minima-highlight-vc-font-weight); }
  .highlight .vg {
    color: var(--minima-highlight-vg-color);
    background-color: var(--minima-highlight-vg-background-color);
    font-style: var(--minima-highlight-vg-font-style);
    font-weight: var(--minima-highlight-vg-font-weight); }
  .highlight .vi {
    color: var(--minima-highlight-vi-color);
    background-color: var(--minima-highlight-vi-background-color);
    font-style: var(--minima-highlight-vi-font-style);
    font-weight: var(--minima-highlight-vi-font-weight); }
  .highlight .il {
    color: var(--minima-highlight-il-color);
    background-color: var(--minima-highlight-il-background-color);
    font-style: var(--minima-highlight-il-font-style);
    font-weight: var(--minima-highlight-il-font-weight); }

/* begin initialize.scss */
:root {
  --minima-base-font-family: -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", "Segoe UI Emoji", "Segoe UI Symbol", "Apple Color Emoji", Roboto, Helvetica, Arial, sans-serif ;
  --minima-code-font-family: "Menlo", "Inconsolata", "Consolas", "Roboto Mono", "Ubuntu Mono", "Liberation Mono", "Courier New", monospace;
  --minima-base-font-size: 16px ;
  --minima-base-font-weight: 400 ;
  --minima-small-font-size: calc(var(--minima-base-font-size) * 0.875) ;
  --minima-base-line-height: 1.5 ;
  --minima-spacing-unit: 30px ;
  --minima-table-text-align: left ; }

:root {
  --minima-content-width: 800px; }

/*
// Width of the content area
*/
@media screen and (min-width: 600px) {
  /* on-medium = on-palm */
  .site-nav {
    position: static;
    float: right;
    border: none;
    background-color: inherit; }
  .site-nav label[for="nav-trigger"] {
    display: none; }
  .site-nav .menu-icon {
    display: none; }
  .site-nav input ~ .trigger {
    display: block; }
  .site-nav .page-link {
    display: inline;
    padding: 0;
    margin-left: auto; }
    .site-nav .page-link:not(:last-child) {
      margin-right: 20px; }
  .footer-col-wrapper {
    display: flex; }
  .footer-col {
    width: calc(100% - (var(--minima-spacing-unit) / 2 ));
    padding: 0 calc(var(--minima-spacing-unit) * .5); }
    .footer-col:first-child {
      padding-right: calc(var(--minima-spacing-unit) * .5);
      padding-left: 0; }
    .footer-col:last-child {
      padding-right: 0;
      padding-left: calc(var(--minima-spacing-unit) * .5); } }

:root {
  --minima-wrapper-max-width: calc( var(--minima-content-width) - (var(--minima-spacing-unit)));
  --minima-wrapper-padding-left-right: calc(var(--minima-spacing-unit) * .5);
  --minima-post-content-h1-font-size: 2.625rem;
  --minima-post-content-h2-font-size: 1.75rem;
  --minima-post-content-h3-font-size: 1.375rem;
  --minima-footer-col1-width: calc(50% - (var(--minima-spacing-unit) / 2));
  --minima-footer-col2-width: calc(50% - (var(--minima-spacing-unit) / 2));
  --minima-footer-col3-width: calc(50% - (var(--minima-spacing-unit) / 2)); }

@media screen and (min-width: 800px) {
  :root {
    --minima-wrapper-max-width: calc( var(--minima-content-width) - (var(--minima-spacing-unit) * 2));
    --minima-wrapper-padding-left-right: var(--minima-spacing-unit);
    --minima-one-half-width: calc(50% - (var(--minima-spacing-unit) / 2 ));
    --minima-post-content-h1-font-size: 2.625rem;
    --minima-post-content-h2-font-size: 2rem;
    --minima-post-content-h3-font-size: 1.625rem;
    --minima-footer-col1-width: calc(35% - (var(--minima-spacing-unit) / 2));
    --minima-footer-col1-width: calc(20% - (var(--minima-spacing-unit) / 2 ));
    --minima-footer-col1-width: calc(45% - (var(--minima-spacing-unit) / 2 )); } }

@media screen and (max-width: 600px) {
  /* on-palm */
  :root {
    --minima-site-title-padding-right: 45px; } }

@media screen and (max-width: 800px) {
  /* on-laptop */
  :root {
    --minima-table-display: block;
    --minima-table-overflow-x: auto;
    --minima-table-webkit-overflow-scrolling: touch;
    --minima-table-ms-overflow-style: -ms-autohiding-scrollbar; } }

/*
// Syntax highlighting styles should be adjusted appropriately for every "skin"
// List of tokens: https://github.com/rouge-ruby/rouge/wiki/List-of-tokens
// Some colors come from Material Theme Darker:
// https://github.com/material-theme/vsc-material-theme/blob/master/scripts/generator/settings/specific/darker-hc.ts
// https://github.com/material-theme/vsc-material-theme/blob/master/scripts/generator/color-set.ts
// ----------------------------------------------------------------------------
// Use media queries like this:
// @include media-query($on-palm) {
//   .wrapper {
//     padding-right: $spacing-unit / 2;
//     padding-left: $spacing-unit / 2;
//   }
// }
// Notice the following mixin uses max-width, in a deprecated, desktop-first
// approach, whereas media queries used elsewhere now use min-width.

// Import pre-styling-overrides hook and style-partials.
*/
/* begin custom-styles.scss
// Placeholder to allow overriding predefined variables smoothly.
*/
/* begin _base.scss */
html {
  font-size: var(--minima-base-font-size); }

/**
 * Reset some basic elements
 */
body, h1, h2, h3, h4, h5, h6,
p, blockquote, pre, hr,
dl, dd, ol, ul, figure {
  margin: 0;
  padding: 0; }

/**
 * Basic styling
 */
body {
  font: var(--minima-base-font-weight) var(--minima-base-font-size)/var(--minima-base-line-height) var(--minima-base-font-family);
  color: var(--minima-text-color);
  background-color: var(--minima-background-color);
  -webkit-text-size-adjust: 100%;
  -webkit-font-feature-settings: "kern" 1;
  -moz-font-feature-settings: "kern" 1;
  -o-font-feature-settings: "kern" 1;
  font-feature-settings: "kern" 1;
  font-kerning: normal;
  display: flex;
  min-height: 100vh;
  flex-direction: column;
  overflow-wrap: break-word; }

/**
 * Set `margin-bottom` to maintain vertical rhythm
 */
h1, h2, h3, h4, h5, h6,
p, blockquote, pre,
ul, ol, dl, figure,
.highlight {
  margin-bottom: calc(var(--minima-spacing-unit) * .5); }

hr {
  margin-top: var(--minima-spacing-unit);
  margin-bottom: var(--minima-spacing-unit); }

/**
 * `main` element
 */
main {
  display: block;
  /* Default value of `display` of `main` element is 'inline' in IE 11. */ }

/**
 * Images
 */
img {
  max-width: 100%;
  vertical-align: middle; }

/**
 * Figures
 */
figure > img {
  display: block; }

figcaption {
  font-size: var(--minima-small-font-size); }

/**
 * Lists
 */
ul, ol {
  margin-left: var(--minima-spacing-unit); }

li > ul,
li > ol {
  margin-bottom: 0; }

/**
 * Headings
 */
h1, h2, h3, h4, h5, h6 {
  font-weight: var(--minima-base-font-weight); }

/**
 * Links
 */
a {
  color: var(--minima-link-base-color);
  text-decoration: none; }
  a:visited {
    color: var(--minima-link-visited-color); }
  a:hover {
    color: var(--minima-link-hover-color);
    text-decoration: underline; }
  .social-media-list a:hover, .pagination a:hover {
    text-decoration: none; }
    .social-media-list a:hover .username, .pagination a:hover .username {
      text-decoration: underline; }

/**
 * Blockquotes
 */
blockquote {
  color: var(--minima-brand-color);
  border-left: 4px solid var(--minima-border-color-01);
  padding-left: calc(var(--minima-spacing-unit) * .5);
  font-size: 1.125rem;
  font-style: italic; }
  blockquote > :last-child {
    margin-bottom: 0; }
  blockquote i, blockquote em {
    font-style: normal; }

/**
 * Code formatting
 */
pre,
code {
  font-family: var(--minima-code-font-family);
  font-size: 0.9375em;
  border: 1px solid var(--minima-border-color-01);
  border-radius: 3px;
  background-color: var(--minima-code-background-color); }

code {
  padding: 1px 5px; }

pre {
  padding: 8px 12px;
  overflow-x: auto; }
  pre > code {
    border: 0;
    padding-right: 0;
    padding-left: 0; }

.highlight {
  border-radius: 3px;
  background: var(--minima-code-background-color); }
  .highlighter-rouge .highlight {
    background: var(--minima-code-background-color); }

/**
 * Wrapper
 */
.wrapper {
  max-width: var(--minima-wrapper-max-width);
  margin-right: auto;
  margin-left: auto;
  padding-right: var(--minima-wrapper-padding-left-right);
  padding-left: var(--minima-wrapper-padding-left-right); }

/**
 * Clearfix
 */
.wrapper:after {
  content: "";
  display: table;
  clear: both; }

/**
 * Icons
 */
.orange {
  color: #f66a0a; }

.grey {
  color: #828282; }

.svg-icon {
  width: 1.25em;
  height: 1.25em;
  display: inline-block;
  fill: currentColor;
  vertical-align: text-bottom; }

/**
 * Tables
 */
table {
  margin-bottom: var(--minima-spacing-unit);
  width: 100%;
  text-align: var(--minima-table-text-align);
  color: var(--minima-table-text-color);
  border-collapse: collapse;
  border: 1px solid var(--minima-table-border-color);
  display: var(--minima-table-display);
  overflow-x: var(--minima-table-overflow-x);
  -webkit-overflow-scrolling: var(--minima-table-webkit-overflow-scrolling);
  -ms-overflow-style: var(--minima-table-ms-overflow-style); }
  table tr:nth-child(even) {
    background-color: var(--minima-table-zebra-color); }
  table th, table td {
    padding: calc(var(--minima-spacing-unit) * 33.3333333333 * .01) calc(var(--minima-spacing-unit) * .5); }
  table th {
    background-color: var(--minima-table-header-bg-color);
    border: 1px solid var(--minima-table-header-border); }
  table td {
    border: 1px solid var(--minima-table-border-color); }

/* begin _layout.scss */
/**
 * Site header
 */
.site-header {
  border-top: 5px solid var(--minima-border-color-03);
  border-bottom: 1px solid var(--minima-border-color-01);
  min-height: calc(var(--minima-spacing-unit) * 1.865);
  line-height: calc(var(--minima-base-line-height) * var(--minima-base-font-size) * 2.25);
  /*
  // Positioning context for the mobile navigation icon
  */
  position: relative; }

.site-title {
  font-size: 1.625rem;
  font-weight: 300;
  letter-spacing: -1px;
  margin-bottom: 0;
  float: left;
  padding-right: var(--minima-site-title-padding-right); }
  .site-title, .site-title:visited {
    color: var(--minima-site-title-color); }

.site-nav {
  position: absolute;
  top: 9px;
  right: calc(var(--minima-spacing-unit) * .5);
  background-color: var(--minima-background-color);
  border: 1px solid var(--minima-border-color-01);
  border-radius: 5px;
  text-align: right; }
  .site-nav .nav-trigger {
    display: none; }
  .site-nav .menu-icon {
    float: right;
    width: 36px;
    height: 26px;
    line-height: 0;
    padding-top: 10px;
    text-align: center; }
    .site-nav .menu-icon > svg path {
      fill: var(--minima-border-color-03); }
  .site-nav label[for="nav-trigger"] {
    display: block;
    float: right;
    width: 36px;
    height: 36px;
    z-index: 2;
    cursor: pointer; }
  .site-nav input ~ .trigger {
    clear: both;
    display: none; }
  .site-nav input:checked ~ .trigger {
    display: block;
    padding-bottom: 5px; }
  .site-nav .page-link {
    color: var(--minima-text-color);
    line-height: var(--minima-base-line-height);
    display: block;
    padding: 5px 10px;
    /*
    // Gaps between nav items, but not on the last one
    */
    margin-left: 20px; }
    .site-nav .page-link:not(:last-child) {
      margin-right: 0; }

/**
 * Site footer
 */
.site-footer {
  border-top: 1px solid var(--minima-border-color-01);
  padding: var(--minima-spacing-unit) 0; }

.footer-heading {
  font-size: 1.125rem;
  margin-bottom: calc(var(--minima-spacing-unit) * .5); }

.feed-subscribe .svg-icon {
  padding: 5px 5px 2px 0; }

.contact-list,
.social-media-list,
.pagination {
  list-style: none;
  margin-left: 0; }

.footer-col-wrapper,
.social-links {
  font-size: 0.9375rem;
  color: var(--minima-brand-color); }

.footer-col {
  margin-bottom: calc(var(--minima-spacing-unit) * .5); }

.footer-col-1 {
  width: var(--minima-footer-col1-width); }

.footer-col-2 {
  width: var(--minima-footer-col2-width); }

.footer-col-3 {
  width: var(--minima-footer-col3-width); }

/**
 * Page content
 */
.page-content {
  padding: var(--minima-spacing-unit) 0;
  flex: 1 0 auto; }

.page-heading {
  font-size: 2rem; }

.post-list-heading {
  font-size: 1.75rem; }

.post-list {
  margin-left: 0;
  list-style: none; }
  .post-list > li {
    margin-bottom: var(--minima-spacing-unit); }

.post-meta {
  font-size: var(--minima-small-font-size);
  color: var(--minima-brand-color); }

.post-link {
  display: block;
  font-size: 1.5rem; }

/**
 * Posts
 */
.post-header {
  margin-bottom: var(--minima-spacing-unit); }

.post-title,
.post-content h1 {
  font-size: var(--minima-post-content-h1-font-size);
  letter-spacing: -1px;
  line-height: 1.15; }

.post-content {
  margin-bottom: var(--minima-spacing-unit); }
  .post-content h1, .post-content h2, .post-content h3, .post-content h4, .post-content h5, .post-content h6 {
    margin-top: var(--minima-spacing-unit); }
  .post-content h2 {
    font-size: var(--minima-post-content-h2-font-size); }
  .post-content h3 {
    font-size: var(--minima-post-content-h3-font-size); }
  .post-content h4 {
    font-size: 1.25rem; }
  .post-content h5 {
    font-size: 1.125rem; }
  .post-content h6 {
    font-size: 1.0625rem; }

.social-media-list, .pagination {
  display: table;
  margin: 0 auto; }
  .social-media-list li, .pagination li {
    float: left;
    margin: 5px 10px 5px 0; }
    .social-media-list li:last-of-type, .pagination li:last-of-type {
      margin-right: 0; }
    .social-media-list li a, .pagination li a {
      display: block;
      padding: 10px 12px;
      border: 1px solid var(--minima-border-color-01); }
      .social-media-list li a:hover, .pagination li a:hover {
        border-color: var(--minima-border-color-02); }

/**
 * Pagination navbar
 */
.pagination {
  margin-bottom: var(--minima-spacing-unit); }
  .pagination li a, .pagination li div {
    min-width: 41px;
    text-align: center;
    box-sizing: border-box; }
  .pagination li div {
    display: block;
    padding: calc(var(--minima-spacing-unit) * .25);
    border: 1px solid transparent; }
    .pagination li div.pager-edge {
      color: var(--minima-border-color-01);
      border: 1px dashed; }

/**
 * Grid helpers
 */
.one-half {
  width: var(--minima-one-half-width); }

/* begin custom-variables.scss
// Placeholder to allow defining custom styles that override everything else.
// (Use `_sass/minima/custom-variables.scss` to override variable defaults)
*/
'''

style_css = '''
:root {
    --minima-navbar-height: 60px;
}

/* override minimacss defaults for burger menu hide for large screens */
@media screen and (min-width: 600px) {
  .site-nav label[for="nav-trigger"] {
    display: block !important; }
  .site-nav .menu-icon {
    display: block !important; }
}

.site-nav .trigger {
    overflow-y: scroll;
    position: fixed;
    bottom: 0;
    top: var(--minima-navbar-height);
    background-color: wheat;
    width: 50vw;
    left:  50vw;
}

.privacynotice {
    width:100%; 
    position: fixed; 
    left: 0; 
    bottom: 0; 
    background-color: skyblue; 
    color: white; 
    /*text-align: center;*/
    height: var(--minima-navbar-height);
    display: flex;
    justify-content: center;
    align-items: center;
}
.privacynotice[hidden] {
    display:none
}

''' + minimacss_classic_css + minimacss_auto_css


snippets_default = dict(
    style_css = style_css,

    home_html = home_html,
    post_html = post_html,
    page_html = page_html,
    base_html = base_html,

    googleanalytics_html = googleanalytics_html,
    comments_html = comments_html,
    seo_html = seo_html,
    page_author_html = page_author_html,
    customhead_html = customhead_html,
    head_html = head_html,
    site_header_pages_html = site_header_pages_html,
    post_list_html = post_list_html,
    header_html = header_html,
    footer_html = footer_html,
)

def render_page(content, layout, ctx, snippets = {}, num_snippets_renders = 5):
    #page__lang___or___site__lang___or___en page_twitter_card__or__site_twitter_card__or__summary_large_image site -> page
    
    ctx = ctx.copy() | snippets
    ctx['post_list_html'] = '\n'.join( resolve_template_variables(snippets['post_list_html'], dict(post__date = post.get('date', ''), post__url = post.get('url', ''), post__title = post.get('title', ''), post__excerpt  = post.get('excerpt', ''), **(dict(site__show_excerpts = True) if bool(ctx.get('site', {}).get('show_excerpts')) else {}))) for post in (ctx.get('paginator', {}).get('posts', []) if ctx.get('site', {}).get('paginate') else ctx.get('site', {}).get('posts', [])) )
    ctx['site_header_pages_html'] = '\n'.join(resolve_template_variables(snippets['site_header_pages_html'], dict(page__url = page.get('url', ''), page__title = page.get('title', ''))) for path in ctx.get('site', {}).get('header_pages', []) for page in ctx.get('site', {}).get('pages', []) if page.get('path') == path)
    if ctx.get('page', {}).get('date') is None:
        ctx['page__date'] = None
    if ctx.get('seo_tag', {}).get('image') is None:
        ctx['seo_tag__image'] = None
    if ctx.get('paginator', {}).get('previous_page') is None:
        ctx['paginator__previous_page'] = None
    if ctx.get('paginator', {}).get('next_page') is None:
        ctx['paginator__next_page'] = None
    if page_author := ctx.get('page', {}).get('author', ''):
        ctx['page_author_html'] = '\n'.join(resolve_template_variables(snippets['page_author_html'], dict(author = author)) for author in (page_author if isinstance(page_author, list) else [page_author]))
    
    res = resolve_template_variables(ctx['base_html'], dict(content_base = snippets[layout + '_html']))
    for k in range(num_snippets_renders):
        res = resolve_template_variables(res, ctx)
    res = resolve_template_variables(res, dict(content = content))
    res = resolve_template_variables(res, ctx)
    
    return res

def resolve_template_variables(res, ctx, sep = '__'):
    ctx_flat = {}
    stack = [('', ctx)]
    while stack:
        prefix, dic = stack.pop()
        for k, v in dic.items():
            if isinstance(v, dict):
                stack.append(((prefix + sep) * bool(prefix) + k, v))
                ctx_flat[(prefix + sep) * bool(prefix) + k + sep + jsonify.__name__] = jsonify(v, ctx)
            elif v is not None:
                ctx_flat[(prefix + sep) * bool(prefix) + k] = str(v)
                ctx_flat[(prefix + sep) * bool(prefix) + k + sep + escape.__name__] = escape(str(v), ctx)
                ctx_flat[(prefix + sep) * bool(prefix) + k + sep + absolute_url.__name__] = absolute_url(str(v), ctx)
                ctx_flat[(prefix + sep) * bool(prefix) + k + sep + relative_url.__name__] = relative_url(str(v), ctx)
                ctx_flat[(prefix + sep) * bool(prefix) + k + sep + removeATSIGN.__name__] = removeATSIGN(str(v), ctx)
                ctx_flat[(prefix + sep) * bool(prefix) + k + sep + date_to_xmlschema.__name__] = date_to_xmlschema(str(v), ctx)
                ctx_flat[(prefix + sep) * bool(prefix) + k + sep + date_format.__name__] = date_format(str(v), ctx)
            else:
                ctx_flat[(prefix + sep) * bool(prefix) + k + sep + 'is_none'] = None

    for k, v in ctx_flat.items():
        res = res.replace('<!--' + k + '\n', '').replace('\n' + k + '-->', '')
        if v is not None:
            res = res.replace('{{ ' + k + ' }}', v)
    
    return res

def render(input_path, output_path, context_path, sitemap_path, layout, snippets_dir, snippets_default = snippets_default):
    assert output_path
    
    content = ''
    if input_path and os.path.exists(input_path):
        with open(input_path) as fp:
            content = fp.read()
    
    ctx = {}
    if context_path and os.path.exists(context_path):
        with open(context_path) as fp:
            ctx = json.load(fp)
    
    sitemap = sitemap_read(sitemap_path)

    snippets = snippets_default | snippets_read(snippets_dir)

    rendered = render_page(content, layout = layout, ctx = ctx, snippets = snippets)
    url = output_path

    id = hash(output_path)
    abs_url = absolute_url(url, ctx)
    rel_url = relative_url(url, ctx)

    if sitemap_path:
        sitemap = sitemap_update(sitemap, id = id, loc = abs_url, locrel = rel_url)
        print(sitemap_write(sitemap_path, sitemap))

    os.makedirs(os.path.dirname(output_path) or '.', exist_ok = True)
    with open(output_path, 'w') as fp:
        fp.write(rendered)
    
    print(output_path)

def snippets_write(snippets_dir, snippets):
    os.makedirs(snippets_dir, exist_ok = True)
    for k, v in snippets.items():
        basename = k.replace('_css', '.css').replace('_html', '.html')
        path = os.path.join(snippets_dir, basename)
        with open(path, 'w') as f:
            f.write(v)
        print(path)

def snippets_read(snippets_dir):
    snippets = {}
    if snippets_dir and os.path.exists(snippets_dir):
        for basename in os.listdir(snippets_dir):
            k = basename.replace('.', '_')
            with open(os.path.join(snippets_dir, basename)) as fp:
                snippets[k] = fp.read()
    return snippets

def sitemap_read(path):
    xmlstr = ''
    if path and os.path.exists(path):
        with open(path, 'r') as fp:
            xmlstr = fp.read()
    if not xmlstr.strip():
        return []
    node_doc = xml.dom.minidom.parseString(xmlstr)
    assert node_doc.documentElement.nodeName == 'urlset'
    return [dict({n.nodeName : ''.join(nn.nodeValue for nn in n.childNodes if nn.nodeType == nn.TEXT_NODE) for n in node_url.childNodes if n.nodeType == n.ELEMENT_NODE}, id = node_url.getAttribute('id')) for node_url in node_doc.documentElement.getElementsByTagName('url')]
    
def sitemap_write(path, sitemap):
    # https://sitemaps.org/protocol.html
    node_doc = xml.dom.minidom.Document()
    node_root = node_doc.appendChild(node_doc.createElement('urlset'))
    node_root.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    node_root.setAttribute('xsi:schemaLocation', 'http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd')
    node_root.setAttribute('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    for entry in sitemap:
        entry = entry.copy()
        node_url = node_root.appendChild(node_doc.createElement('url'))
        if entry.get('id'):
            node_url.setAttribute('id', entry.pop('id'))
        for field, value in entry.items():
            node_url.appendChild(node_doc.createElement(field)).appendChild(node_doc.createTextNode(str(value)))
    with open(path, 'w') as fp:
        node_doc.writexml(fp, addindent = '  ', newl = '\n')
    return path

def sitemap_update(sitemap, id = '', loc = '', locrel = '', translate = {ord('-') : '', ord('_') : ''}):
    sitemap = sitemap[:]
    k = ([i for i, u in enumerate(sitemap) if (bool(u.get('id')) and u.get('id').translate(translate) == id.translate(translate)) or (bool(u.get('locrel')) and u.get('locrel') == locrel) or (bool(u.get('loc')) and u.get('loc') == loc)] or [-1])[0]
    if k == -1:
        sitemap.append({})
    sitemap[k] = sitemap[k] | dict(id = id, loc = loc, locrel = locrel)
    return sitemap

def absolute_url(v, ctx):
    site_url = ctx.get('site', {}).get('url', '')
    base_url = ctx.get('site', {}).get('baseurl', '')
    if site_url:
        return os.path.join(site_url, base_url.strip('/'), v)
    if base_url:
        return os.path.join('/' + base_url.strip('/'), v)
    return v

def relative_url(v, ctx):
    base_url = ctx.get('site', {}).get('baseurl', '')
    if base_url:
        return os.path.join('/' + base_url.strip('/'), v)
    return v

def removeATSIGN(v, ctx):
    return v.replace('@', '')

def date_to_xmlschema(v, ctx):
    return v

def date_format(v, ctx, fmt = "%b %-d, %Y"):
    fmt = ctx.get('site', {}).get('minima', {}.get('date_format', fmt)
    
    return v

def escape(v, ctx):
    return html.escape(v)

def jsonify(v, ctx):
    return json.dumps(v, ensure_ascii = False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-path', '-i')
    parser.add_argument('--output-path', '-o')
    parser.add_argument('--context-path', '-c')
    parser.add_argument('--sitemap-path', '-s')
    parser.add_argument('--layout', choices = ['home', 'page', 'post'], default = 'page')
    parser.add_argument('--snippets-dir')
    args = parser.parse_args()
    print(args)
    
    if args.input_path:
        render(**vars(args), snippets_default = snippets_default)
    else:
        snippets_write(args.snippets_dir, snippets_default)
