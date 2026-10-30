"""Build the four-page portfolio with Python's standard library. No package install needed."""
from pathlib import Path
from html import escape as e
from urllib.parse import quote
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_site'
OUT.mkdir(exist_ok=True)
PROJECTS = json.loads((ROOT / 'scripts/projects.json').read_text())
GROUPS = {
    'psychology': ('01', 'Psychology-driven design', 'Understanding people. Shaping experiences.', 'Exploring how behavior, emotion, and social connection inform the things we design.'),
    'usability': ('02', 'Usability & evaluation', 'A little less friction. A little more possibility.', 'Looking closely at where experiences get difficult—and how thoughtful design can help.'),
    'human-ai': ('03', 'Human–AI interaction', 'Human feeling. Machine reasoning.', 'Investigating what happens when technology meets the complexity of human emotional experience.'),
}

def asset(path):
    return quote(path, safe='/')

for p in PROJECTS:
    source = ROOT / p['folder']
    files = list(source.glob('*.jpg')) if source.is_dir() else [source]
    files.sort(key=lambda f: int(re.search(r'_(\d+)\.jpg$', f.name)[1]) if re.search(r'_(\d+)\.jpg$', f.name) else 0)
    if not files or any(not f.is_file() for f in files):
        raise RuntimeError('Missing project assets: ' + p['folder'])
    dest = OUT / 'media' / p['id']
    dest.mkdir(parents=True, exist_ok=True)
    p['images'] = []
    for i, src in enumerate(files, 1):
        name = f'{i:02}.jpg'
        shutil.copy2(src, dest / name)
        p['images'].append(f'media/{p["id"]}/{name}')

shutil.copytree(ROOT / 'assets', OUT / 'assets', dirs_exist_ok=True)
BY_ID = {p['id']: p for p in PROJECTS}

def nav(current):
    links = [('index', 'Home')] + [(k, v[1]) for k, v in GROUPS.items()]
    items = []
    for key, label in links:
        active = ' aria-current="page"' if key == current else ''
        items.append(f'<a href="{key}.html"{active}>{e(label)}</a>')
    return '<header class="site-header"><a class="wordmark" href="index.html" aria-label="Nannan Fu home">nf<span aria-hidden="true">✳︎</span></a><nav aria-label="Main navigation">' + ''.join(items) + '</nav><a class="hello-link" href="mailto:nancy0606fu@gmail.com">Say hello <span aria-hidden="true">↗</span></a></header>'

def footer():
    return '''<footer id="contact"><div class="footer-top"><div><p class="eyebrow">A good experience starts with a conversation.</p><h2>Let’s make something <span class="hand">thoughtful.</span></h2></div><a class="circle-link" href="mailto:nancy0606fu@gmail.com" aria-label="Email Nannan Fu"><span aria-hidden="true">↗</span></a></div><div class="footer-bottom"><a href="mailto:nancy0606fu@gmail.com">nancy0606fu@gmail.com</a><div class="socials"><a href="https://www.linkedin.com/in/nannan-fu-085b7b338/">LinkedIn ↗</a><a href="https://www.instagram.com/of.unsaidwords/">Photography ↗</a><a href="assets/Nannan-Fu-Resume.pdf">Résumé (PDF) ↗</a></div><span class="colophon">Nannan Fu · Made with curiosity.</span></div></footer>'''

def vector_symbols(markup):
    paths = {
        '↗': 'M5 19 19 5M5 5h14v14',
        '↓': 'M12 4v16M5 13l7 7 7-7',
        '←': 'M20 12H4M11 5l-7 7 7 7',
        '→': 'M4 12h16M13 5l7 7-7 7',
        '✳': 'M12 2v20M2 12h20M5 5l14 14M5 19 19 5',
    }
    def replace(run):
        text = run.group(0).replace('\ufe0e', '')
        for char, path in paths.items():
            icon = f'<svg class="glyph-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="{path}"/></svg>'
            text = text.replace(char, icon)
        return text
    return re.sub(r'(?<=>)[^<]+(?=<)', replace, markup)


def document(title, content, current):
    description = 'Nannan Fu’s portfolio: psychology-driven UX design, usability evaluation, human–AI research, and visual explorations.'
    page_slug = current.replace('.html', '') if current else 'index'
    markup = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(title)} | Nannan Fu</title><meta name="description" content="{e(description)}"><meta name="theme-color" content="#f6f3eb"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="preload" href="assets/fonts/mazzy-regular.ttf" as="font" type="font/ttf" crossorigin><link rel="stylesheet" href="assets/style.css"><link rel="stylesheet" href="assets/refinement.css"><link rel="stylesheet" href="assets/textile.css"><link rel="stylesheet" href="assets/materials.css"><link rel="stylesheet" href="assets/pastels.css"><link rel="stylesheet" href="assets/handdrawn.css"><script src="assets/site.js" defer></script></head><body class="page-{page_slug}"><a class="skip-link" href="#main">Skip to content</a>{nav(current)}<main id="main">{content}</main>{footer()}<dialog class="viewer" aria-labelledby="viewer-title"><div class="viewer-toolbar"><h2 id="viewer-title">Project image</h2><a id="viewer-original" href="#">Open original ↗</a><button type="button" id="viewer-close" aria-label="Close image viewer">Close ×</button></div><div class="viewer-body"><img id="viewer-image" alt=""></div><div class="viewer-controls"><button type="button" id="viewer-prev">← Previous</button><span id="viewer-count" role="status" aria-live="polite"></span><button type="button" id="viewer-next">Next →</button></div></dialog></body></html>'''
    return vector_symbols(markup)

def card(p, n):
    return f'''<a class="project-card" href="{p['group']}.html#{p['id']}"><div class="card-image"><img src="{p['images'][0]}" alt="" loading="lazy" width="1024" height="576"><span class="card-arrow" aria-hidden="true">↗</span></div><div class="card-info"><p class="eyebrow">{e(p['label'])}</p><h3>{e(p['title'])}</h3><p>{e(p['short'])}</p><span class="project-number" aria-hidden="true">0{n}</span></div></a>'''

def gallery(p):
    items = ''.join(f'''<figure><button type="button" class="image-button" data-gallery="{p['id']}" data-index="{i}" data-title="{e(p['artifact'])} — page {i+1}" aria-label="Enlarge {e(p['artifact'])}, page {i+1}"><img src="{url}" alt="{e(p['artifact'])}, original page {i+1}. See the project overview for a text summary." loading="lazy"></button><figcaption>Page {i+1:02} <a href="{url}">Open original ↗<span class="sr-only">, {e(p['artifact'])} page {i+1}</span></a></figcaption></figure>''' for i, url in enumerate(p['images']))
    return f'''<details class="project-gallery"><summary>Explore the original {e(p['artifact'].lower())} <span class="gallery-count">{len(p['images'])} {"page" if len(p['images']) == 1 else "pages"}</span><span class="plus" aria-hidden="true">+</span></summary><p class="gallery-note">Original project pages, in reading order. Select an image to enlarge it. Text within these original images is not a full accessible transcript; the overview above provides a text summary.</p><div class="gallery-grid">{items}</div></details>'''

def study(p, n):
    question = f'<p class="study-question">{e(p["question"])}</p>' if 'question' in p else ''
    facts = '<ul class="facts">' + ''.join(f'<li>{e(f)}</li>' for f in p['facts']) + '</ul>' if p['facts'] else ''
    return f'''<article class="study" id="{p['id']}"><div class="study-heading"><span class="study-index">{n:02}</span><div><p class="eyebrow">{e(p['label'])}</p><h2>{e(p['title'])}</h2></div></div><div class="study-content"><div class="study-cover"><img src="{p['images'][0]}" alt="Cover of {e(p['artifact'])}" loading="lazy"></div><div class="study-overview">{question}<p>{e(p['description'])}</p>{facts}</div></div>{gallery(p)}</article>'''

expertise = ''.join(f'''<a class="expertise-card" href="{key}.html"><span class="eyebrow">{v[0]} / A way of thinking</span><h3>{e(v[1])}</h3><p>{e(v[3])}</p><span class="expertise-action">Explore the work <span aria-hidden="true">↗</span></span></a>''' for key, v in GROUPS.items())
selected = ''.join(card(BY_ID[k], i+1) for i,k in enumerate(['glowrift-pitch','solar-terms','llm-emotions']))
graphic = ''.join(study(p,i+1) for i,p in enumerate(PROJECTS) if p['group']=='graphic')

home = (ROOT / 'scripts/hero.html').read_text() + f'''
<section class="section expertise-section" id="expertise"><div class="section-heading"><div><p class="eyebrow">01 / Skills & expertise</p><h2>Different lenses.<br><span class="hand">One human perspective.</span></h2></div><p>From understanding behavior to evaluating an interface, I start with the person experiencing it.</p></div><div class="expertise-grid">{expertise}</div></section>
<section class="section" id="selected"><div class="section-heading"><div><p class="eyebrow">02 / Selected work</p><h2>Ideas, tested.<br><span class="hand">Experiences, considered.</span></h2></div><span class="margin-note hand">a few things I’ve<br>been thinking about ↙</span></div><div class="project-grid">{selected}</div></section>
<section class="about-section section" id="about"><div><p class="eyebrow">03 / The person behind the projects</p><h2>A mind for psychology.<br><span class="hand">An eye for possibility.</span></h2><a class="pill-link" href="assets/Nannan-Fu-Resume.pdf">Read my résumé (PDF) ↗</a></div><div class="about-copy"><p>I’m Nannan Fu, a Psychology student at the University of Michigan, with minors in UX Design and Linguistics.</p><p>My work connects user research, interaction design, and the study of emotion. I’m interested in what makes an experience intuitive, meaningful, and accessible—from the way we navigate a game to the way we relate to AI.</p><div class="skill-tags"><span>User research</span><span>Usability testing</span><span>Heuristic evaluation</span><span>Wireframing & prototyping</span><span>Figma</span><span>R / RStudio</span></div></div></section>
<section class="section visual-section" id="beyond"><div class="section-heading"><div><p class="eyebrow">04 / Beyond the interface</p><h2>Looking a little closer.<br><span class="hand">Making a little differently.</span></h2></div><a class="text-link" href="https://www.instagram.com/of.unsaidwords/">My photography ↗</a></div><p class="section-intro">A small collection of graphic design and photographic explorations.</p>{graphic}</section>
'''
(OUT / 'index.html').write_text(document('Designing for the mind', home, 'index'))
for key, (number, title, subtitle, description) in GROUPS.items():
    ps = [p for p in PROJECTS if p['group']==key]
    jump = ''.join(f'<a href="#{p["id"]}">{e(p["title"])} <span aria-hidden="true">↓</span></a>' for p in ps)
    content = f'''<section class="collection-hero"><a class="back-link" href="index.html#expertise">← Back to the overview</a><p class="eyebrow">{number} / {e(title)}</p><h1>{e(subtitle.split('. ')[0])}<br><span class="hand">{e('. '.join(subtitle.split('. ')[1:]))}</span></h1><p class="collection-description">{e(description)}</p><nav class="project-jump" aria-label="Projects on this page">{jump}</nav></section><section class="section collection-studies" aria-label="Case studies">{''.join(study(p,i+1) for i,p in enumerate(ps))}</section><aside class="next-collection"><p class="eyebrow">Keep exploring</p>{''.join(f'<a href="{k}.html">{e(v[1])} ↗</a>' for k,v in GROUPS.items() if k!=key)}</aside>'''
    (OUT / f'{key}.html').write_text(document(title, content, key))
print(f'Built 4 pages, {len(PROJECTS)} projects, {sum(len(p["images"]) for p in PROJECTS)} original images → {OUT}')
