# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2008 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# ==============================================================================

from axiom import item, attributes
from axiom.attributes import reference, text

class HostType(item.Item):
    typeName = 'hosttype'
    schemaVersion = 1
    # Columns
    type = text(indexed=True, caseSensitive=False, allowNone=False,
                doc='Host Types. Ie, mail, smtp, webserver, shells, etc...')
    info = text(caseSensitive=False, allowNone=False,
                doc='Simple description of host type')


class Host(item.Item):
    typeName = 'host'
    schemaVersion = 1
    # Columns
    name = text(indexed=True, caseSesitive=False, allowNone=False,
                doc='A string naming an ISPMan host. This should be a '
                    'hostname -f output on a unix host')
    ip = text(indexed=True, caseSesitive=False, allowNone=False,
              doc='IP address as a dotted decimal, eg. 192.168.1.1')
    alias = text(caseSesitive=False, allowNone=False,
                 doc='A string naming an alias of an ISPMan host. '
                     'This maybe the display name of the machine')
    info = text(caseSesitive=False, allowNone=False,
                doc='Simple description of host')
    type = reference(doc='Host type')
