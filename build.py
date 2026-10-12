import glob, os, re, html, markdown, datetime
BASE="https://benegar1995-star.github.io/study-and-bake-guides/"; OUT="docs"; os.makedirs(OUT,exist_ok=True)
CSS="""body{font:17px/1.65 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:#222;margin:0;background:#fcfcfa}
header,footer{background:#1F3A5F;color:#fff;padding:14px 20px}header a,footer a{color:#fff;text-decoration:none}footer{font-size:14px;margin-top:40px}
main{max-width:740px;margin:0 auto;padding:20px}h1{line-height:1.25;color:#1F3A5F}h2{margin-top:1.8em;color:#1F3A5F}a{color:#8A4B5C}
.cta{background:#FBEFF1;border-left:4px solid #8A4B5C;padding:14px 18px;margin:28px 0}.card{display:block;padding:14px 18px;margin:12px 0;background:#fff;border:1px solid #e3e3e3;border-radius:8px;text-decoration:none;color:#222}
.card b{color:#1F3A5F}blockquote{background:#f2f2f2;margin:0;padding:10px 16px;border-radius:6px}code{background:#eee;padding:1px 4px}"""
def page(title,desc,body,path):
    canon=BASE+path
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}"><link rel="canonical" href="{canon}">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:type" content="article">
<link rel="stylesheet" href="{'../' if path else ''}style.css"></head><body><header><a href="{BASE}"><b>Study &amp; Bake Guides</b></a></header><main>{body}</main>
<footer>Practical guides for students and home bakers. Some links go to templates we sell on Gumroad. Guides are general information, not legal, tax, or financial advice. Written with AI assistance and reviewed before publishing.</footer></body></html>"""
open(f"{OUT}/style.css","w").write(CSS); open(f"{OUT}/.nojekyll","w").write("")
guides=[]
for f in sorted(glob.glob("src/*.md")):
    raw=open(f).read(); fm,body=raw.split("---",2)[1:]
    meta=dict(l.split(": ",1) for l in fm.strip().splitlines())
    h=markdown.markdown(body)
    url,name=meta["product"].split("|")
    cta=f'<div class="cta"><b>Want a head start?</b> Get the <a href="{url}">{name}</a>, which is ready to use in minutes.</div>'
    h=h.replace("<h2>",cta+"<h2>",1) if h.count("<h2>")>2 else h+cta
    os.makedirs(f"{OUT}/{meta['slug']}",exist_ok=True)
    open(f"{OUT}/{meta['slug']}/index.html","w").write(page(meta["title"],meta["desc"],f"<article><h1>{html.escape(meta['title'])}</h1>{h}</article><p><a href='../'>← All guides</a></p>",meta["slug"]+"/"))
    guides.append(meta)
cards=lambda gs:"".join(f'<a class="card" href="{g["slug"]}/"><b>{html.escape(g["title"])}</b><br><small>{html.escape(g["desc"])}</small></a>' for g in gs)
idx=f"<h1>Study &amp; Bake Guides</h1><p>Plain-English, practical guides for two groups we build tools for: students applying for college and scholarships, and people running a bakery from their home kitchen.</p><h2>Scholarships &amp; college applications</h2>{cards(guides[:4])}<h2>Home bakery business</h2>{cards(guides[4:])}"
open(f"{OUT}/index.html","w").write(page("Study & Bake Guides: Scholarships, College Applications & Home Bakery Business","Free practical guides on tracking scholarships, college applications, comparing financial aid, pricing baked goods, cake order forms, cottage food labels, and home bakery bookkeeping.",idx,""))
today=datetime.date.today().isoformat()
open(f"{OUT}/sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f"<url><loc>{BASE}{p}</loc><lastmod>{today}</lastmod></url>\n" for p in [""]+[g["slug"]+"/" for g in guides])+"</urlset>\n")
open(f"{OUT}/robots.txt","w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n")
print(len(guides))
