```cfgrlanguage
        html = response.content.decode()
        self.assertInHTML(self.source_name1, html)
        self.assertInHTML(self.source_name2, html)
```