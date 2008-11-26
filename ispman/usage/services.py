# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2008 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================

import os
import sys
from axiom.errors import ItemNotFound
from axiom.store import Store
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker
from twisted.python import usage, log
from zope.interface import implements

from ispman.discover import model

class _BaseOptions(usage.Options):

    def opt_version(self):
        """Show version"""
        print os.path.basename(sys.argv[0]), '- 0.1'
    opt_v = opt_version

    def opt_help(self):
        """Show this help message"""
        super(_BaseOptions, self).opt_help()
    opt_h = opt_help

    def postOptions(self):
        super(_BaseOptions, self).postOptions()
        self.parent.postOptions()
#        self.runService()

    def runService(self):
        raise NotImplemented

class TestTubService(_BaseOptions):

    def getService(self):
        from ispman.discover.service import DiscoverService
        service = DiscoverService(self.parent.store)

        from foolscap import Referenceable, UnauthenticatedTub, Tub, SturdyRef

        tub = UnauthenticatedTub()
        tub.listenOn("tcp:%(port)i" % self.parent)
        tub.setLocation("localhost:%(port)i" % self.parent)
        url = tub.registerReference(service, 'ping')
        print "Serving on", url
        return tub


        class MathServer(Referenceable):
            def remote_add(self, a, b):
                return a+b
            def remote_subtract(self, a, b):
                return a-b

        myserver = MathServer()

        try:
            dbtub = self.parent.store.findUnique(
                model.Tub, model.Tub.name==unicode(self.parent.subCommand)
            )
            tub = Tub(certData=dbtub.cert.certData)
            tub.listenOn("tcp:%(port)i" % self.parent)
            tub.setLocation("localhost:%(port)i" % self.parent)
            url = tub.registerReference(myserver, str(dbtub.furl.name))
        except ItemNotFound:
            tub = Tub()
            tub.listenOn("tcp:%(port)i" % self.parent)
            tub.setLocation("localhost:%(port)i" % self.parent)
            certData = tub.getCertData()
            url = tub.registerReference(myserver)
            # Store Tub details on DB
            a = model.Tub.new(name=self.parent.subCommand,
                          certData=certData,
                          furl=SturdyRef(url).name,
                          store=self.parent.store)
#        reactor.callLater(0, lambda: log.msg("Tub is available on %s" % url))
        print "the object is available at:", url
#        tub.startService()
        self.tub = tub
        return tub


class MasterServiceOptions(_BaseOptions):
    store = None
    longdesc = "ISPMan Master Service"

    optParameters = [
        ["port", "p", 12345, "service port number", int],
        ["storage", "s", "./storage", "Database storage folder"],
    ]

    subCommands = [
        ["test", None, TestTubService, "Test Tub Service"],
    ]

    defaultSubCommand = 'test'

    def postOptions(self):
        self.store = Store(self.opts.get('storage'))




class ServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = 'ispman'
    description = "ISPMan Services"
    options = MasterServiceOptions

    def makeService(self, options):
        self.__service = options.subOptions.getService()
        return self.__service
#        return options.subOptions.getService()
