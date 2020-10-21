# -*- coding: utf-8 -*-
"""Jinja formatters for Oneboxes and Embeds."""

import re
import pystache

def format_webembed(url):
    if url.lower().startswith('<iframe '):
        return url
    if url.startswith('https://query.wikidata.org/'):
        url = url.replace('https://query.wikidata.org/', 'https://query.wikidata.org/embed.html')
    # TODO: add more embeddables
    return '<iframe src="%s"></iframe>' % url

boxhtml = r"""
<div class="onebox">
<a href="{{link}}">
<img src="{{image_url}}" />
<h5 class="name">{{name}}</h5>
<div class="phase">{{phase}}</div>
<p>{{summary}}</p>
</a>
</div>
"""

def repl_onebox(mat=None, li=[]):
    if mat == None:
        li[:] = []
        return
    if mat.group(1) and mat.group(2):
        url = mat.group(1).strip()
        if url != mat.group(2).strip(): return mat.group()
        # Try to parse a server link
        if '/project/' in url:
            project_link = mat.group(1)
            project_id = int(url.split('/')[-1])
            from .user.models import Project
            project = Project.query.filter_by(id=project_id).first()
            if not project: return mat.group()
            pd = project.data
            pd['link'] = project_link
            return pystache.render(boxhtml, pd)
    return mat.group()

def make_onebox(raw_html):
    regexp = re.compile('<p><a href="(.+?)">(.+?)</a></p>')
    return re.sub(regexp, repl_onebox, raw_html)