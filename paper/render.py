"""Render paper/draft.md -> paper/draft.html (self-contained, print-ready; MathJax for ```latex blocks).
  python paper/render.py
"""
import datetime, re, markdown
src = open("paper/draft.md", encoding="utf-8").read()
src = re.sub(r"```latex\n(.*?)```", lambda m: "\n<div class=\"math\">\\[" + m.group(1).strip() + "\\]</div>\n", src, flags=re.S)
body = markdown.markdown(src, extensions=["tables", "fenced_code", "sane_lists", "smarty"])
body = body.replace("[TBD", "<span class=\"tbd\">[TBD").replace("TBD]", "TBD]</span>")
title = re.sub("<.*?>", "", re.search(r"<h1>(.*?)</h1>", body, re.S).group(1))
css = open("paper/style.css", encoding="utf-8").read()
html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<script>window.MathJax = {{ tex: {{ displayMath: [['\\\\[','\\\\]']] }} }};</script>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-chtml.js"></script>
<style>{css}</style></head>
<body>
{body}
<p style="margin-top:3em;color:var(--muted);font-size:0.85em">Rendered from <code>paper/draft.md</code> on {datetime.date.today().isoformat()}. Highlighted [TBD] entries are results still being computed.</p>
</body></html>"""
open("paper/draft.html", "w", encoding="utf-8").write(html)
print("wrote paper/draft.html")
