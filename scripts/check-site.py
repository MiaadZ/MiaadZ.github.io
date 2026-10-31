#!/usr/bin/env python3
"""Check rendered HTML, internal links, fragments and local assets. No dependencies."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
import sys


class Document(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.assets, self.tags, self.canonicals = [], [], [], [], []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append(tag)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a' and attrs.get('href'):
            self.links.append(attrs['href'])
        if tag in ('img', 'script', 'source') and attrs.get('src'):
            self.assets.append(attrs['src'])
        if tag in ('img', 'source') and attrs.get('srcset'):
            self.assets.extend(item.strip().split()[0] for item in attrs['srcset'].split(','))
        if tag == 'link' and attrs.get('href'):
            if attrs.get('rel') == 'canonical':
                self.canonicals.append(attrs['href'])
            elif attrs.get('rel') == 'stylesheet':
                self.assets.append(attrs['href'])

    handle_startendtag = handle_starttag


def check(root):
    root = root.resolve()
    documents = {p: Document(p) for p in root.rglob('*.html')}
    assert documents, 'No rendered HTML found'
    for path, doc in documents.items():
        label = path.relative_to(root)
        assert doc.tags.count('main') == doc.tags.count('h1') == 1, f'Expected one main/H1: {label}'
        assert len(doc.ids) == len(set(doc.ids)), f'Duplicate HTML IDs: {label}'
        assert len(doc.canonicals) == 1, f'Missing/duplicate canonical: {label}'
        assert 'script' not in doc.tags, f'Unexpected frontend JavaScript: {label}'
        for asset in doc.assets:
            parts = urlsplit(asset)
            assert not parts.scheme and not parts.netloc, f'External runtime asset: {asset}'
        for link in doc.links + doc.assets:
            parts = urlsplit(link)
            if parts.scheme or parts.netloc:
                continue
            resolved = urlsplit(urljoin('/' + label.as_posix(), link))
            target = root / unquote(resolved.path).lstrip('/')
            if target.is_dir():
                target /= 'index.html'
            assert target.exists(), f'Missing target: {label} → {link}'
            if resolved.fragment and target in documents:
                assert unquote(resolved.fragment) in documents[target].ids, f'Missing anchor: {label} → {link}'
    for name in ('AGENTS.md', 'README.md', 'Gemfile', 'Gemfile.lock', 'vendor', 'scripts', '_templates', '_plugins'):
        assert not (root / name).exists(), f'Development file published: {name}'
    assert not list(root.rglob('*.map')), 'Published source map'
    print(f'PASS: {len(documents)} pages; internal links, anchors, images, landmarks and publishing exclusions')


if __name__ == '__main__':
    check(Path(sys.argv[1] if len(sys.argv) > 1 else '_site'))
