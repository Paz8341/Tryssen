import unittest,tempfile,json,shutil
from pathlib import Path
from build import build,ROOT
class BuildTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)/'site';shutil.copytree(ROOT,self.root,ignore=shutil.ignore_patterns('dist','__pycache__'))
  (self.root/'content/site.json').write_text(json.dumps({'hero':'','contact':'','responsible':''}))
  for name in ['news','events','albums']:self.save(name,[])
 def tearDown(self):self.tmp.cleanup()
 def save(self,name,items): (self.root/f'content/{name}.json').write_text(json.dumps({'items':items}))
 def test_publication_and_drafts(self):
  self.save('news',[{'published':False,'title':'DO NOT PUBLISH','body':'SECRET'},{'published':True,'title':'Nyhet','date':'2026-11-10','body':'Hej'}]);build(self.root)
  result=(self.root/'dist/assets/content.js').read_text();self.assertNotIn('SECRET',result);self.assertIn('Nyhet',result);self.assertFalse((self.root/'dist/content').exists())
 def test_subpath_assets_and_multiple_photos(self):
  from PIL import Image
  for name,color in [('a.png','red'),('b.png','blue')]:Image.new('RGB',(4,6),color).save(self.root/'media'/name)
  self.save('albums',[{'published':True,'title':'Album','date':'2026-11-10','cover':'/media/b.png','photos':[{'image':'/media/a.png','alt':'A'},{'image':'/media/b.png','alt':'B'}]}]);result=build(self.root)
  self.assertEqual(len(result['albums'][0]['photos']),2);self.assertEqual(result['albums'][0]['cover'],'media/b.png')
  for photo in result['albums'][0]['photos']:self.assertTrue((self.root/'dist'/photo['image']).exists());self.assertFalse(photo['image'].startswith('/'))
 def test_optimized_gallery_outputs(self):
  from PIL import Image
  Image.new('RGB',(3000,2000),(80,120,30)).save(self.root/'media/photo.jpg')
  self.save('albums',[{'published':True,'title':'Album','date':'2026-11-10','photos':[{'image':'/media/photo.jpg','alt':'Garden'}]}])
  result=build(self.root,optimize=True);url=result['albums'][0]['photos'][0]['image'];thumb=result['thumbnails'][url]
  self.assertTrue(url.endswith('.webp'));self.assertFalse((self.root/'dist/media/photo.jpg').exists())
  with Image.open(self.root/'dist'/url) as im:self.assertLessEqual(im.width,2400);self.assertLessEqual(im.height,1600)
  with Image.open(self.root/'dist'/thumb) as im:self.assertLessEqual(im.width,640);self.assertLessEqual(im.height,480)
 def test_events_and_cancellation(self):
  self.save('events',[{'published':True,'title':'Träff','date':'2026-11-20','time':'14:30','cancelled':True}]);self.assertTrue(build(self.root)['events'][0]['cancelled'])
 def test_cms_multiple_upload_optional_captions_and_originals_preserved(self):
  from PIL import Image
  for name,color in [('a.png','red'),('b.png','blue')]:Image.new('RGB',(4,6),color).save(self.root/'media'/name)
  shutil.copy(self.root/'media/a.png',self.root/'media/copy.png')
  self.save('albums',[{'published':True,'title':'Album','date':'2026-11-10','cover':'/media/copy.png','photos':[{'image':['/media/a.png','/media/b.png','/media/copy.png']}]}])
  source=(self.root/'content/albums.json').read_bytes()
  result=build(self.root)['albums'][0]
  self.assertEqual(len(result['photos']),2)
  self.assertEqual(result['cover'],'media/a.png')
  self.assertTrue(all(p['alt'] and p['alt_en'] for p in result['photos']))
  self.assertEqual((self.root/'content/albums.json').read_bytes(),source)
  self.assertTrue((self.root/'media/copy.png').is_file())
 def test_captioned_groups_and_first_image_cover(self):
  from PIL import Image
  Image.new('RGB',(4,6),'red').save(self.root/'media/a.png')
  self.save('albums',[{'published':True,'title':'Album','date':'2026-11-10','photos':[{'image':['/media/a.png'],'alt':'Beskrivning','alt_en':'Description'}]}])
  result=build(self.root)['albums'][0]
  self.assertEqual(result['cover'],'media/a.png')
  self.assertEqual(result['photos'][0]['alt'],'Beskrivning')
  self.assertEqual(result['photos'][0]['alt_en'],'Description')
 def test_saved_content_matches_cms_multiple_image_fields(self):
  config=json.loads((self.root/'.pages.yml').read_text())
  def check(obj,fields,location):
   for field in fields:
    value=obj.get(field['name'])
    path=f"{location}.{field['name']}"
    if field['type']=='object':
     for i,item in enumerate(value or []):check(item,field.get('fields',[]),f'{path}.{i}')
    elif field['type']=='image' and field.get('options',{}).get('multiple'):
     self.assertIsInstance(value,list,f'{path}: Pages CMS requires an array, not a string')
     self.assertTrue(all(isinstance(image,str) and image for image in value),path)
  for content in config['content']:
   if content['type']=='file':
    check(json.loads((ROOT/content['path']).read_text()),content['fields'],content['path'])
 def test_news_rich_text_and_informative_image_description(self):
  from PIL import Image
  Image.new('RGB',(4,6),'red').save(self.root/'media/a.png')
  item={'published':True,'title':'Hej Trissen','title_en':'Hello Trissen','date':'2026-11-11','body':'**Hej!**\n\n## Kontakt\n\nTrissenstyrelsen@proton.me','body_en':'**Hello!**\n\n[Write to us](mailto:Trissenstyrelsen@proton.me)','image':'/media/a.png','alt':'Ett rött färgfält'}
  self.save('news',[item]);source=(self.root/'content/news.json').read_bytes()
  result=build(self.root)['news'][0]
  self.assertIn('<strong>Hej!</strong>',result['body_html'])
  self.assertIn('<h4>Kontakt</h4>',result['body_html'])
  self.assertIn('href="mailto:',result['body_html'])
  self.assertIn('<strong>Hello!</strong>',result['body_html_en'])
  self.assertEqual(result['alt'],'Ett rött färgfält')
  self.assertEqual((self.root/'content/news.json').read_bytes(),source)
 def test_news_without_photograph_needs_no_alt(self):
  self.save('news',[{'published':True,'title':'Nyhet','date':'2026-11-11','body':'Text utan bild'}])
  result=build(self.root)['news'][0]
  self.assertNotIn('image',result)
  self.assertIn('Text utan bild',result['body_html'])
 def test_informative_news_image_without_alt_is_rejected(self):
  from PIL import Image
  Image.new('RGB',(4,6),'red').save(self.root/'media/a.png')
  self.save('news',[{'published':True,'title':'Nyhet','date':'2026-11-11','image':'/media/a.png'}])
  with self.assertRaisesRegex(AssertionError,'informativa'):build(self.root)
 def test_explicitly_decorative_news_image_has_empty_alt(self):
  from PIL import Image
  Image.new('RGB',(4,6),'red').save(self.root/'media/a.png')
  self.save('news',[{'published':True,'title':'Nyhet','date':'2026-11-11','image':'/media/a.png','image_decorative':True}])
  self.assertEqual(build(self.root)['news'][0]['alt'],'')
 def test_lucia_photo_description_does_not_rewrite_cms_data(self):
  self.save('news',[{'published':True,'title':'Lucia','date':'2026-11-11','image':'/media/mwbpb14x-lpqk98si.jpg'}])
  original=(self.root/'content/news.json').read_bytes()
  result=build(self.root)['news'][0]
  self.assertIn('luciatåg',result['alt'])
  self.assertIn('Lucia procession',result['alt_en'])
  self.assertEqual((self.root/'content/news.json').read_bytes(),original)
 def test_community_name_is_display_only_and_keeps_urls(self):
  text='Tryssen [Tryssen](https://paz8341.github.io/Tryssen/) tryssen@example.org'
  self.save('news',[{'published':True,'title':'Tryssen','date':'2026-11-11','body':text}])
  original=(self.root/'content/news.json').read_bytes()
  result=build(self.root)['news'][0]
  self.assertEqual(result['title'],'Trissen')
  self.assertIn('href="https://paz8341.github.io/Tryssen/"',result['body_html'])
  self.assertIn('href="mailto:tryssen@example.org"',result['body_html'])
  self.assertEqual((self.root/'content/news.json').read_bytes(),original)
 def test_blocks_missing_event_photo_alt(self):
  self.save('events',[{'published':True,'title':'Hej','date':'2026-11-10','image':'/media/missing.png'}])
  with self.assertRaises(AssertionError):build(self.root)
 def test_blocks_external_and_traversal_images(self):
  for path in ['https://example.com/a.jpg','/media/../../etc/passwd']:
   (self.root/'content/site.json').write_text(json.dumps({'hero':path}))
   with self.assertRaises(AssertionError):build(self.root)
 def test_public_release_requires_original_photo_and_contact(self):
  with self.assertRaisesRegex(AssertionError,'panorámica'):build(self.root,strict=True)
 def test_invalid_date_fails(self):
  self.save('news',[{'published':True,'title':'Hej','date':'2026-02-31'}])
  with self.assertRaises(ValueError):build(self.root)
if __name__=='__main__':unittest.main()
