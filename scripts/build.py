"""Build only public, referenced content. No server or runtime dependencies."""
from pathlib import Path
from datetime import date, time
import json, shutil, hashlib, argparse
ROOT=Path(__file__).resolve().parents[1]
def build(root=ROOT, optimize=False, strict=False):
 root=Path(root); out=root/'dist'; shutil.rmtree(out,ignore_errors=True);out.mkdir()
 shutil.copy(root/'index.html',out/'index.html');shutil.copytree(root/'assets',out/'assets',ignore=shutil.ignore_patterns('content.js'))
 payload={'site':json.loads((root/'content/site.json').read_text()),'thumbnails':{}}
 if strict:
  assert payload['site'].get('hero'),'Falta la fotografía panorámica original en Inställningar.'
  assert payload['site'].get('responsible'),'Falta la persona responsable en Inställningar.'
  assert payload['site'].get('contact'),'Falta el correo para solicitar la retirada de fotografías.'
 email=payload['site'].get('contact','')
 if email: assert '@' in email and not any(c in email for c in '\r\n?&#'),'Correo no válido'
 cache={}
 def photo(path):
  if not path:return ''
  if path in cache:return cache[path]
  # CMS uses /media paths; resolve against source rather than domain root.
  relative=path.lstrip('/')
  assert relative.startswith('media/') and '..' not in Path(relative).parts,'La imagen debe estar en media/'
  source=(root/relative).resolve();assert source.is_relative_to((root/'media').resolve()) and source.is_file(),f'No existe {relative}'
  assert source.suffix.lower() in ('.jpg','.jpeg','.png','.webp'),f'Formato no permitido: {source}'
  destination=out/relative;destination.parent.mkdir(parents=True,exist_ok=True)
  url=relative
  if optimize:
   from PIL import Image, ImageOps
   digest=hashlib.sha256(source.read_bytes()).hexdigest()[:20]
   url=f'media/optimized/{digest}.webp';target=out/url;target.parent.mkdir(parents=True,exist_ok=True)
   with Image.open(source) as original:
    im=ImageOps.exif_transpose(original);im.thumbnail((2400,1600));im=im.convert('RGB');im.save(target,'WEBP',quality=85)
    im.thumbnail((640,480));thumb=f'media/optimized/{digest}-thumb.webp';im.save(out/thumb,'WEBP',quality=80);payload['thumbnails'][url]=thumb
  else:shutil.copy(source,destination)
  cache[path]=url
  return url
 payload['site']['hero']=photo(payload['site'].get('hero',''))
 for collection in ['news','events','albums']:
  items=json.loads((root/f'content/{collection}.json').read_text())['items'];payload[collection]=[]
  for item in items:
   if not item.get('published',False):continue
   for key in ['title','date']:
    assert isinstance(item.get(key),str) and item[key].strip(),f'{collection}: falta {key}'
   date.fromisoformat(item['date'])
   if item.get('time'):time.fromisoformat(item['time'])
   if item.get('image'):
    assert item.get('alt'),f'{collection}: falta texto alternativo'
    item['image']=photo(item['image'])
   if collection=='albums':
    assert item.get('photos'), 'El álbum publicado necesita fotografías'
    for image in item['photos']:
     assert image.get('alt'),'Falta texto alternativo de una fotografía'
     image['image']=photo(image['image'])
    item['cover']=photo(item.get('cover',''))
    assert not item['cover'] or item['cover'] in [p['image'] for p in item['photos']],'La portada debe pertenecer al álbum'
   payload[collection].append(item)
 (out/'assets/content.js').write_text('window.TRYSSEN='+json.dumps(payload,ensure_ascii=True)+';\n')
 (out/'.nojekyll').touch()
 return payload
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--optimize',action='store_true');parser.add_argument('--strict',action='store_true');a=parser.parse_args();build(optimize=a.optimize,strict=a.strict);print('Build correcto: dist/')
