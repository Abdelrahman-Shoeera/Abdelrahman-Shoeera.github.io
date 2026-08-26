"""
Patches every *.html file in the repo:
  - inserts meta description, canonical, favicon links, OG tags, Twitter card,
    and the GoatCounter analytics snippet inside <head>
  - idempotent: safe to run again
"""
import re, sys, pathlib

BASE_URL = "https://abdelrahman-shoeera.github.io"
OG_IMAGE = f"{BASE_URL}/og-image.png"
GOATCOUNTER_CODE = "abdelrahman-shoeera"

PAGES = {
    "index.html": {
        "path": "/",
        "desc": "Portfolio of Abdelrahman Shoeera — computer engineering student building backend and AI software. Looking for a summer 2026 internship.",
        "og_title": "Abdelrahman Shoeera — Backend & AI engineer",
    },
    "projects.html": {
        "path": "/projects.html",
        "desc": "Selected projects by Abdelrahman Shoeera — backend systems, AI experiments, and Java desktop games.",
        "og_title": "Projects — Abdelrahman Shoeera",
    },
    "about.html": {
        "path": "/about.html",
        "desc": "About Abdelrahman Shoeera — computer engineering student at GUC (New Cairo). Python, Java, PostgreSQL, FastAPI.",
        "og_title": "About — Abdelrahman Shoeera",
    },
    "contact.html": {
        "path": "/contact.html",
        "desc": "Get in touch with Abdelrahman Shoeera — email, GitHub, LinkedIn.",
        "og_title": "Contact — Abdelrahman Shoeera",
    },
    "doordash.html": {
        "path": "/doordash.html",
        "desc": "DoorDasH — a competitive Java desktop board game set in the Monsters, Inc. universe. Case study by Abdelrahman Shoeera.",
        "og_title": "DoorDasH — Case study — Abdelrahman Shoeera",
    },
}

MARK_START = "<!-- BEGIN meta:auto -->"
MARK_END   = "<!-- END meta:auto -->"

def build_block(meta):
    url = BASE_URL + meta["path"]
    lines = [
        MARK_START,
        f'<meta name="description" content="{meta["desc"]}">',
        f'<link rel="canonical" href="{url}">',
        '',
        '<link rel="icon" type="image/svg+xml" href="/favicon.svg">',
        '<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">',
        '<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">',
        '<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">',
        '<link rel="shortcut icon" href="/favicon.ico">',
        '<meta name="theme-color" content="#12141A">',
        '',
        '<meta property="og:type" content="website">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:title" content="{meta["og_title"]}">',
        f'<meta property="og:description" content="{meta["desc"]}">',
        f'<meta property="og:image" content="{OG_IMAGE}">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta property="og:site_name" content="Abdelrahman Shoeera">',
        '',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{meta["og_title"]}">',
        f'<meta name="twitter:description" content="{meta["desc"]}">',
        f'<meta name="twitter:image" content="{OG_IMAGE}">',
        '',
        '<!-- analytics: GoatCounter -->',
        f'<script data-goatcounter="https://{GOATCOUNTER_CODE}.goatcounter.com/count"',
        '        async src="//gc.zgo.at/count.js"></script>',
        MARK_END,
    ]
    return "\n".join(lines)

def patch(repo_dir):
    repo = pathlib.Path(repo_dir)
    for fname, meta in PAGES.items():
        f = repo / fname
        if not f.exists():
            print(f"skip: {fname}"); continue
        html = f.read_text(encoding="utf-8")
        block = build_block(meta)
        pat = re.compile(re.escape(MARK_START) + r".*?" + re.escape(MARK_END), flags=re.DOTALL)
        if pat.search(html):
            new_html = pat.sub(block, html)
        else:
            m = re.search(r"([ \t]*)</head>", html, flags=re.IGNORECASE)
            if not m:
                print(f"skip: {fname} (no </head>)"); continue
            indent = m.group(1)
            indented = "\n".join(indent + line for line in block.split("\n"))
            new_html = html[:m.start()] + indented + "\n" + m.group(0) + html[m.end():]
        if new_html != html:
            f.write_text(new_html, encoding="utf-8")
            print(f"patched: {fname}")
        else:
            print(f"unchanged: {fname}")

if __name__ == "__main__":
    patch(sys.argv[1] if len(sys.argv) > 1 else ".")
