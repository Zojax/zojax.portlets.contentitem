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
from zope import interface, schema
from zope.i18n import MessageFactory

from zojax.content.type.interfaces import ISearchableContent

_ = MessageFactory('zojax.portlets')


class IContentItemPortletContent(interface.Interface):

    enabled = schema.Bool(
        title = _('Show in content item portlet'),
        description = _('Content item portlet content marker'),
        default=False)


class IContentItemPortletable(ISearchableContent):
    """Marker interface for content item portlet content."""


class IContentItemPortletAware(interface.Interface):
    """ Marker interface for content item portlet aware content """


class IContentItemPortlet(interface.Interface):
    """ Portlet to show content of selected content item """

    label = schema.TextLine(
        title = _(u'Label'),
        required = False)

    item = schema.Choice(
        title = _(u'Content item'),
        description = _(u'Select content item.'),
        vocabulary = 'portlet.contentitem.items',
        required = True)


class IContentItemPortlet2(IContentItemPortlet):
    """ Portlet to show content of selected content item """

    decoration = schema.Bool(
        title = _(u'Portlet decoration'),
        description = _(u'Show portlet decoration, or just html.'),
        default = True,
        required = False)
