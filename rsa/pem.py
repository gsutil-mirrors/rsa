# -*- coding: utf-8 -*-
#
#  Copyright 2011 Sybren A. Stüvel <sybren@stuvel.eu>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

'''Functions that load and write PEM-encoded files.'''

import base64

def _markers(pem_marker):
    '''Returns the start and end PEM markers

    >>> _markers('RSA PRIVATE KEY')
    ('-----BEGIN RSA PRIVATE KEY-----', '-----END RSA PRIVATE KEY-----')

    '''

    return ('-----BEGIN %s-----' % pem_marker,
            '-----END %s-----' % pem_marker)

def load_pem(contents, pem_marker):
    '''Loads a PEM file.

    @param contents: the contents of the file to interpret
    @param pem_marker: the marker of the PEM content, such as 'RSA PRIVATE KEY'
        when your file has '-----BEGIN RSA PRIVATE KEY-----' and
        '-----END RSA PRIVATE KEY-----' markers.

    @return the base64-decoded content between the start and end markers.

    @raise ValueError: when the content is invalid, for example when the start
        marker cannot be found.

    '''

    (pem_start, pem_end) = _markers(pem_marker)

    pem_lines = []
    in_pem_part = False

    for line in contents.split('\n'):
        line = line.strip()

        # Handle start marker
        if line == pem_start:
            if in_pem_part:
                raise ValueError('Seen start marker "%s" twice' % pem_start)

            in_pem_part = True
            continue

        # Skip stuff before first marker
        if not in_pem_part:
            continue

        # Handle end marker
        if in_pem_part and line == pem_end:
            in_pem_part = False
            break

        pem_lines.append(line)

    # Do some sanity checks
    if not pem_lines:
        raise ValueError('No PEM start marker "%s" found' % pem_start)

    if in_pem_part:
        raise ValueError('No PEM end marker "%s" found' % pem_end)

    # Base64-decode the contents
    pem = ''.join(pem_lines)
    return base64.decodestring(pem)

def save_pem(contents, pem_marker):
    '''Saves a PEM file.

    @param contents: the contents to encode in PEM format
    @param pem_marker: the marker of the PEM content, such as 'RSA PRIVATE KEY'
        when your file has '-----BEGIN RSA PRIVATE KEY-----' and
        '-----END RSA PRIVATE KEY-----' markers.

    @return the base64-encoded content between the start and end markers.

    '''

    (pem_start, pem_end) = _markers(pem_marker)

    b64 = base64.encodestring(contents).replace('\n', '')
    pem_lines = [pem_start]
    
    for block_start in range(0, len(b64), 64):
        block = b64[block_start:block_start + 64]
        pem_lines.append(block)

    pem_lines.append(pem_end)
    pem_lines.append('')

    return '\n'.join(pem_lines)
    
