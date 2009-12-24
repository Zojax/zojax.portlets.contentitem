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
from zope import interface
from zope.proxy import removeAllProxies
from zojax.layoutform import button, Fields, PageletEditSubForm, PageletEditForm

from interfaces import IContentItemPortletContent


class ContentItemPortletContentEdit(PageletEditForm):

    prefix = 'portlet.contentitem'

    extension = None

    @property
    def fields(self):
        return Fields(self.extension.__schema__)

    def getContent(self):
        return self.extension

    def update(self):
        self.extension = IContentItemPortletContent(removeAllProxies(self.context), None)
        super(ContentItemPortletContentEdit, self).update()

    def isAvailable(self):
        return self.extension is not None
