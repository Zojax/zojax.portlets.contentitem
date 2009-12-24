##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
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
from zope.security import checkPermission
from zope import component
from zope.app.intid.interfaces import IIntIds

from zojax.content.type.interfaces import IItem, IContent, IContentContainer


class ContentItemPortlet(object):

    content = None
    contentTitle = None
    contentDescription = None

    def update(self):
        super(ContentItemPortlet, self).update()

        context = self.context
        try:
            content = component.getUtility(IIntIds).queryObject(int(self.item))
        except TypeError:
            return

        if content is not None and checkPermission('zope.View', content):
            self.content = content

            item = IItem(content, None)
            self.contentTitle = getattr(item, 'title', u'')
            self.contentDescription = getattr(item, 'description', u'')

    def isAvailable(self):
        return self.content is not None
