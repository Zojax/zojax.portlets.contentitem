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
from zope import interface, component
from zope.security import checkPermission
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.app.intid.interfaces import IIntIds
from zope.traversing.api import getParents
from zope.traversing.interfaces import IContainmentRoot

from zojax.catalog.interfaces import ICatalog
from zojax.content.type.interfaces import IItem, IContent, IContentContainer

from interfaces import _


class Vocabulary(SimpleVocabulary):

    def getTerm(self, value):
        try:
            return self.by_value[value]
        except KeyError:
            return self.by_value[self.by_value.keys()[0]]


def descriptionVocabulary(context):
    return SimpleVocabulary((
        SimpleTerm(1, '1', _(u'Short')),
        SimpleTerm(2, '2', _(u'Full')),
        SimpleTerm(3, '3', _(u"Minimal")),
        ))


class ContentItems(object):
    interface.implements(IVocabularyFactory)

    def __call__(self, context):
        catalog = component.queryUtility(ICatalog)
        ids = component.getUtility(IIntIds)

        if catalog is None:
            return Vocabulary(())

        terms = []
        for content in catalog.searchResults(isContentItemPortletContent = {'any_of': (True,)}):
            id = ids.getId(content)
            title = self.getTitle(content)
            terms.append((title, SimpleTerm(id, id, title)))

        terms.sort()
        return SimpleVocabulary([term for t, term in terms])

    def getTitle(self, content):

        def itemtitle(i):
            item = IItem(i, None)
            if item is None:
                return i.__name__
            else:
                return u'%s (%s)'%(item.title, i.__name__)
        items = filter(lambda x: x.__name__ is not None, \
                       reversed([content] + getParents(content)))
        return "/".join(map(itemtitle, items))
