from pathlib import Path
import re

OUTPUT_FILE = Path("all-pages-elementor.html")

html_files = sorted(
    [p for p in Path('.').glob('*.html') if p.name != OUTPUT_FILE.name],
    key=lambda p: (p.name != 'index.html', p.name)
)

head_links = []
head_styles = []
head_scripts = []
body_sections = []

for path in html_files:
    content = path.read_text(encoding='utf-8')

    links = re.findall(r'<link\b[^>]*>', content, flags=re.IGNORECASE)
    styles = re.findall(r'<style\b[^>]*>.*?</style>', content, flags=re.IGNORECASE | re.DOTALL)
    scripts = re.findall(r'<script\b[^>]*>.*?</script>', content, flags=re.IGNORECASE | re.DOTALL)

    body_match = re.search(r'<body\b[^>]*>(.*?)</body>', content, flags=re.IGNORECASE | re.DOTALL)
    body_inner = body_match.group(1).strip() if body_match else content.strip()

    for link in links:
        if link not in head_links:
            head_links.append(link)
    for style in styles:
        if style not in head_styles:
            head_styles.append(style)
    for script in scripts:
        if script not in head_scripts:
            head_scripts.append(script)

    body_sections.append(
        f'  <section class="source-page" id="page-{path.stem}">\n'
        f'    <!-- Start: {path.name} -->\n'
        f'{body_inner}\n'
        f'    <!-- End: {path.name} -->\n'
        f'  </section>'
    )

output = [
    '<!doctype html>',
    '<html lang="en">',
    '<head>',
    '  <meta charset="utf-8" />',
    '  <meta name="viewport" content="width=device-width, initial-scale=1" />',
    '  <title>MCAST Library - Combined Pages (Elementor)</title>',
    '  <meta name="description" content="Single-file combined export of all MCAST Library HTML pages." />',
]

output.extend([f'  {link}' for link in head_links])
output.extend([f'  {style}' for style in head_styles])
output.extend([f'  {script}' for script in head_scripts])

output.extend([
    '</head>',
    '<body>',
    '  <!-- Combined from all .html files in repository root -->',
    *body_sections,
    '</body>',
    '</html>',
    ''
])

OUTPUT_FILE.write_text('\n'.join(output), encoding='utf-8')

print(f'Created {OUTPUT_FILE} from {len(html_files)} files:')
for p in html_files:
    print(f'- {p.name}')
