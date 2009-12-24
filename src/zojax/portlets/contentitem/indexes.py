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
from zope import interface
from zope.component import getAdapters, queryUtility
from zope.app.component.interfaces import ISite
from zope.security.proxy import removeSecurityProxy
from zc.catalog.catalogindex import ValueIndex, SetIndex
from zojax.catalog.utils import Indexable, getAccessList
from zojax.catalog.interfaces import ICatalogIndexFactory
from zojax.content.type.interfaces import IContent, IContentType

from interfaces import IContentItemPortletAware, IContentItemPortletable


def isContentItemPortletContent():
    return ValueIndex(
    'value', \
    Indexable('zojax.portlets.contentitem.indexes.IsContentItemPortletContentChecker'))


class IsContentItemPortletContentChecker(object):
    """
    >>> from zojax.content.type.item import Item
    >>> from zope import interface
    >>> class Content(Item):
    ...     interface.implements(IContent)

    >>> content = Content()
    >>> IsContentItemPortletContentChecker(content).value
    False

    >>> from zojax.portlets.contentitem.interfaces import IContentFeaturedAware
    >>> interface.alsoProvides(content, IContentFeaturedAware)

    >>> IsContentItemPortletContentChecker(content).value
    True
    """

    def __init__(self, content, default=None):
        self.value = default
        if IContentItemPortletable.providedBy(content):
            self.value = IContentItemPortletAware.providedBy(content)
