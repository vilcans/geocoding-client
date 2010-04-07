#!/usr/bin/env python
import sys
import json
import urllib

from genshi.template import TemplateLoader
template_loader = TemplateLoader([ '.' ], auto_reload=True)
template = template_loader.load('template.kml')

query = u' '.join(a.decode() for a in sys.argv[1:])

s = urllib.urlopen('http://maps.google.com/maps/api/geocode/json?address=' + urllib.quote(query.encode('utf-8')) + '&sensor=false')

raw_data = s.read()
sys.stdout.write(raw_data)
j = json.loads(raw_data)
stream = template.generate(json=j, query=query)

with open((query + '.kml').encode(), 'w') as f:
    # Google Earth doesn't support namespaces, so remove kml: prefix
    f.write(stream.render('xml').replace('kml:', ''))
