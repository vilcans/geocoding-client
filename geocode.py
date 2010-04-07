#!/usr/bin/env python
import sys
import json
import urllib
try:
    from genshi.template import TemplateLoader
except ImportError:
    sys.stderr.write("Genshi is required. Run 'easy_install genshi'.")
    sys.exit(2)

if len(sys.argv) < 2:
    sys.stderr.write('Usage: \n    geocode.py <string to geocode>\n')
    sys.exit(1)

template = TemplateLoader(['.']).load('template.kml')

query = u' '.join(a.decode() for a in sys.argv[1:])

s = urllib.urlopen('http://maps.google.com/maps/api/geocode/json?address=' + urllib.quote(query.encode('utf-8')) + '&sensor=false')

raw_data = s.read()
sys.stdout.write(raw_data)
j = json.loads(raw_data)
stream = template.generate(json=j, query=query)

filename = query + '.kml'
sys.stdout.write('Writing %s\n' % filename)
with open(filename.encode(), 'w') as f:
    # Google Earth doesn't support namespaces, so remove kml: prefix
    f.write(stream.render('xml').replace('kml:', ''))
