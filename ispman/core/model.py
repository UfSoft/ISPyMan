# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2008 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================

from axiom.attributes import boolean, reference, text, timestamp
from axiom.errors import ItemNotFound
from axiom.item import Item
from epsilon.extime import Time
import cPickle as pickle


class HostService(Item):
    typeName = 'hostService'
    schemaVersion = 1
    # Columns
    name = text(doc="Service name; mail, web, etc")
    host = reference()


class Host(Item):
    typeName = 'host'
    schemaVersion = 1
    # Columns
    furl = text(
        indexed=True, caseSensitive=False, allowNone=False,
        doc='The furl URL of the host'
    )
    alias = text(
        caseSensitive=False, allowNone=True,
        doc='A string naming an alias of an ISPMan host. '
            'This maybe the display name of the machine'
    )
    info = text(
        caseSensitive=False, allowNone=True, doc='Simple description of host'
    )
    registered = timestamp(defaulFactory=Time)
    alive = timestamp(defaulFactory=Time, doc="Last time host was alive")

    @classmethod
    def new(self, furl, store=None):
        try:
            return store.findUnique(Host, Host.furl==furl)
        except ItemNotFound:
            return Host(furl=furl, store=store)

    def registerService(self, service_name):
        try:
            return self.store.findUnique(HostService,
                                         HostService.host==self,
                                         HostService.name==service_name)
        except ItemNotFound:
            return HostService(name=service_name, host=self, store=self.store)

    def services(self):
        return self.store.query(HostService, HostService.host==self)



class Ping(Item):
    typeName = 'ping'
    schemaVersion = 1

    host = reference()
    ts = timestamp(allowNone=False, defaultFactory=Time)


class Process(Item):
    typeName = 'process'
    schemaVersion = 1
    host = reference()
    command = text()
    _args = text(
        allowNone=False, doc="Pickled command arguments"
    )
    _kwargs = text(
        allowNone=False, doc="Pickled command keyword arguments"
    )
    created = timestamp(allowNone=False, defaultFactory=Time)
    finished = timestamp()
    completed = boolean()

    def set_args(self, *args):
        self._args = unicode(pickle.dumps(args))
    def get_args(self):
        return pickle.loads(self._args)
    args = property(set_args, get_args)
    del get_args, set_args

    def set_kwargs(self, **kwargs):
        self._kwargs = unicode(pickle.dumps(kwargs))
    def get_kwargs(self):
        return pickle.loads(self._kwargs)
    kwargs = property(set_kwargs, get_kwargs)
    del get_kwargs, set_kwargs

    @classmethod
    def new(cls, host, command, store=None, *args, **kwargs):
        return Process(host=host, command=command, args=args, kwargs=kwargs,
                       store=store)


class Queue(Item):
    typeName = 'queue'
    schemaVersion = 1
    process = reference()
    _status = text()

    def queue(cls, process, store=None):
        return Queue(_status='queued', process=process, store=store)

    def __set_status(self, value):
        if value not in ('queued', 'in-progress', 'completed'):
            raise AttributeError
    def __get_status(self):
        return self._status
    status = property(__get_status, __set_status)
