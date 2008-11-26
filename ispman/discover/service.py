# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2008 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================

from foolscap import Referenceable
from ispman.discover.model import Ping

class DiscoverService(Referenceable):

    def __init__(self, store):
        self.store = store

    def remote_ping(self, furl):
        ping = Ping(furl=unicode(furl), store=self.store)
        return True

    def remote_register(self, furl):
        print "Registering FURL:", furl

    def remote_add(self, a, b):
        return a+b
    def remote_subtract(self, a, b):
        return a-b
