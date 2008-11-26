# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2008 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================

from axiom import errors
from axiom.item import Item
from axiom.attributes import reference, text, timestamp

from epsilon.extime import Time

class Ping(Item):
    typeName = 'tubPing'
    schemaVersion = 1

    furl = text()
    timestamp = timestamp(defaultFactory=Time)

#    @classmethod
#    def get(cls, furl, store=None):
#        try:
#            return store.findUnique(Ping, Ping.furl==furl)
#        except errors.ItemNotFound:
#            return cls(furl=furl, store=store)


    def update(self):
        self.timestamp = Time()
        return self.timestamp


class TubCert(Item):
    typeName = 'tubCert'
    schemaVersion = 1

    certData = text()


class TubFurl(Item):
    typeName = 'tubFurl'
    schemaVersion = 1
    name = text()


class Tub(Item):
    typeName = 'tub'
    schemaVersion = 1

    name = text(doc="Service name")
    cert = reference()
    furl = reference()

    @classmethod
    def new(cls, name, certData, furl, store=None):
        try:
            return store.findUnique(Tub, Tub.name==unicode(name))
        except errors.ItemNotFound:
            cert = TubCert(certData=unicode(certData), store=store)
            furl = TubFurl(name=unicode(furl), store=store)
            return cls(name=unicode(name), cert=cert, furl=furl, store=store)
