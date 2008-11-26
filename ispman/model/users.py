# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8 et
# ==============================================================================
# Copyright © 2008 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# License: BSD - Please view the LICENSE file for additional information.
# ==============================================================================

import sha
import random
import string

from axiom import item, attributes
from axiom.attributes import reference, text, integer

class UserLevel(item.Item):
    typeName = 'userLevel'
    schemaVersion = 1

    num = integer(
        indexed=True, allowNone=False, doc="User level; 0, 1, 2"
    )
    name = text(
        caseSensitive=False, allowNone=False,
        doc="Display name of the user level; ADMIN, MANAGER, USER"
    )

class User(item.Item):
    typeName = 'user'
    schemaVersion = 1

    username = text(
        indexed=True, caseSensitive=True, allowNone=False,
        doc="User's username"
    )
    username.unique = True
    salt = text(
        defaultFactory=lambda: ''.join(random.sample(string.printable, 15)),
        caseSensitive=True, allowNone=False,
    )
    _password = text(
        caseSensitive=True, allowNone=False,
        doc="SHA hexdigest of the password"
    )
    level = reference()


    def set_password(self, password):
        self._password = sha.new("%s$%s" % (self.salt, password)).hexdigest()
    def get_password(self):
        return self._password
    password = property(get_password, set_password)
    del get_password, set_password
