##############################################################################
#
# Copyright (c) 2008 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from rwproperty import getproperty, setproperty

from zope import interface, component, event
from zope.lifecycleevent import ObjectModifiedEvent
from zope.proxy import removeAllProxies
from zope.app.intid.interfaces import IIntIdAddedEvent, IIntIdRemovedEvent
from zope.app.container.interfaces import IObjectAddedEvent, IObjectRemovedEvent

from interfaces import IContentItemPortletContent, IContentItemPortletable, \
                       IContentItemPortletAware


class ContentItemPortletContentExtension(object):

    @getproperty
    def enabled(self):
        context = removeAllProxies(self.context)
        return IContentItemPortletAware.providedBy(context)

    @setproperty
    def enabled(self, value):
        context = removeAllProxies(self.context)

        if value is None or not value:
            if IContentItemPortletAware.providedBy(context):
                interface.noLongerProvides(context, IContentItemPortletAware)
            self.data['enabled'] = False
        else:
            if not IContentItemPortletAware.providedBy(context):
                interface.alsoProvides(context, IContentItemPortletAware)

            self.data['enabled'] = value
        event.notify(ObjectModifiedEvent(context))
