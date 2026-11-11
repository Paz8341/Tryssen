"""Build-time Markdown rendering for Nyheter; no executable visitor-supplied HTML."""
from markdown_it import MarkdownIt
import bleach

TAGS={'p','br','strong','em','h3','h4','h5','h6','a','ul','ol','li','blockquote','code','pre','hr'}

def render_news(text):
 parser=MarkdownIt('commonmark',{'html':False,'linkify':True,'breaks':True}).enable('linkify').disable('image')
 tokens=parser.parse(text or '')
 # The article title is already h2; body headings start at h3.
 for token in tokens:
  if token.type in ('heading_open','heading_close'):
   token.tag='h'+str(min(6,int(token.tag[1:])+2))
 rendered=parser.renderer.render(tokens,parser.options,{})
 return bleach.clean(rendered,tags=TAGS,attributes={'a':['href','title']},protocols={'http','https','mailto'},strip=True)
