import unittest
from richtext import render_news
class RichTextTests(unittest.TestCase):
 def test_existing_paragraphs_and_email_remain_readable(self):
  result=render_news('Första stycket.\n\nAndra stycket.\n\n📧 TRISSENSTYRELSEN@PROTON.ME')
  self.assertEqual(result.count('<p>'),3)
  self.assertIn('href="mailto:TRISSENSTYRELSEN@PROTON.ME"',result)
 def test_headings_bold_links_and_both_languages(self):
  for word in ['Välkommen','Welcome']:
   result=render_news(f'# {word}\n\n**Trissen**\n\n[Kontakt](https://example.org)')
   self.assertIn(f'<h3>{word}</h3>',result)
   self.assertIn('<strong>Trissen</strong>',result)
   self.assertIn('href="https://example.org"',result)
 def test_executable_html_and_unsafe_protocols_are_blocked(self):
  attacks=['<script>alert(1)</script>','<img src=x onerror=alert(1)>','<svg onload=alert(1)>','[x](javascript:alert(1))','[x](vbscript:bad)','[x](data:text/html,bad)','[x](jav&#x61;script:bad)','<iframe src="https://example.org"></iframe>']
  for attack in attacks:
   result=render_news(attack)
   for tag in ['<script','<img','<svg','<iframe']:self.assertNotIn(tag,result)
   self.assertNotRegex(result,r'href="(?:javascript|vbscript|data):')
 def test_markdown_inline_images_do_not_embed_external_resources(self):
  self.assertNotIn('<img',render_news('![Photo](https://example.org/tracker.png)'))
if __name__=='__main__':unittest.main()
