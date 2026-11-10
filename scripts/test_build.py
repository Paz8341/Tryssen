import unittest,tempfile,json,shutil
from pathlib import Path
from build import build,ROOT
class BuildTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)/'site';shutil.copytree(ROOT,self.root,ignore=shutil.ignore_patterns('dist','__pycache__'))
 def tearDown(self):self.tmp.cleanup()
 def save(self,name,items): (self.root/f'content/{name}.json').write_text(json.dumps({'items':items}))
 def test_publication_and_drafts(self):
  self.save('news',[{'published':False,'title':'DO NOT PUBLISH','body':'SECRET'},{'published':True,'title':'Nyhet','date':'2026-11-10','body':'Hej'}]);build(self.root)
  result=(self.root/'dist/assets/content.js').read_text();self.assertNotIn('SECRET',result);self.assertIn('Nyhet',result);self.assertFalse((self.root/'dist/content').exists())
 def test_subpath_assets_and_multiple_photos(self):
  # Tiny valid PNG, sufficient for build copy path checks.
  import base64
  for name in ['a.png','b.png']:(self.root/'media'/name).write_bytes(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/l1sAAAAASUVORK5CYII='))
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
 def test_blocks_missing_photo_alt(self):
  self.save('news',[{'published':True,'title':'Hej','date':'2026-11-10','image':'/media/missing.png'}])
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
