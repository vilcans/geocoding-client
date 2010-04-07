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
sys.stderr.write(raw_data)
j = json.loads(raw_data)
stream = template.generate(json=j, query=query)
print stream.render('xml').replace('kml:', '')
