#!/usr/bin/env python3

# Copyright 2014 Google Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
    Call Google Closure compiler
    Taken from https://developers.google.com/closure/compiler/docs/compilation_levels?csw=1
    Usage:
      ./compilejs.py FILE_TO_COMPILE [OUTPUT_FILE]
    if there's no optional argument OUPUT_FILE, the script
    will add automaticly .min.js at the end of the file.
    e.g.: myapp.js -> myapp.min.js
"""

__author__ = 'Google - Modified by Régis FLORET'

import http.client
import urllib.request
import urllib.parse
import urllib.error
import sys
import os

params = urllib.parse.urlencode([
    ('js_code', open(sys.argv[1]).read()),
    ('compilation_level', 'SIMPLE_OPTIMIZATIONS'),
    ('output_format', 'text'),
    ('output_info', 'compiled_code'),
  ])

headers = { "Content-type": "application/x-www-form-urlencoded" }
conn = http.client.HTTPConnection('closure-compiler.appspot.com')
conn.request('POST', '/compile', params, headers)
response = conn.getresponse()
data = response.read()
if len(sys.argv) == 2:
    name, ext = os.path.splitext(sys.argv[1])
    output = "{}.min{}".format(name, ext)
else:
    output = sys.argv[2]

open(output, 'w').write(data.decode('utf-8'))
conn.close()
