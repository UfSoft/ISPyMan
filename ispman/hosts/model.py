# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2008 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================


from axiom.attributes import reference, text
from axiom.item import Item

class HostType(Item):
    typeName = 'hostType'
    schemaVersion = 1
    # Columns
    type = text(
        indexed=True, caseSensitive=False, allowNone=False,
        doc='Host Types. For example, mail, smtp, webserver, shells, etc...'
    )
    info = text(
        caseSensitive=False, allowNone=False,
        doc='Simple description of host type'
    )


class HostGroupAssociation(Item):
    typeName = 'hostGroupAssociation'
    schemaVersion = 1
    # Columns
    host = reference()
    group = reference()


class Host(Item):
    typeName = 'host'
    schemaVersion = 1
    # Columns
    name = text(
        indexed=True, caseSesitive=False, allowNone=False,
        doc='A string naming an ISPMan host. This should be a '
            'hostname -f output on a unix host'
    )
    ip = text(
        indexed=True, caseSesitive=False, allowNone=False,
        doc='IP address as a dotted decimal, eg. 192.168.1.1'
    )
    alias = text(
        caseSesitive=False, allowNone=False,
        doc='A string naming an alias of an ISPMan host. '
            'This maybe the display name of the machine'
    )
    info = text(
        caseSesitive=False, allowNone=False, doc='Simple description of host'
    )
    type = reference(doc='Host type reference')

    def groups(self):
        """The groups this host belongs to"""
        for association in self.store.query(HostGroupAssociation,
                                            HostGroupAssociation.host==self):
            yield association.host


class HostGroup(Item):
    typeName = 'hostGroup'
    schemaVersion = 1
    # Columns
    name = text(
        indexed=True, caseSensitive=False, allowNone=False,
        doc='A string naming an ISPMan host group.'
    )
    info = text(
        caseSesitive=False, allowNone=False,
        doc="Simple description of the host group"
    )

    def members(self):
        """Hosts that take part in this host group"""
        for association in self.store.query(HostGroupAssociation,
                                            HostGroupAssociation.group==self):
            yield association.group

