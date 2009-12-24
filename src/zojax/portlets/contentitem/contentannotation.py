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
import re
import sys

from zope import interface, component

from zojax.richtext.interfaces import IRichTextData

from interfaces import IContentAnnotation


class ContentAnnotation(object):

    component.adapts(interface.Interface, interface.Interface)
    interface.implements(IContentAnnotation)

    def __init__(self, context, request):
        self.context, self.request = context, request

    def getContentText(self):
        res = self.context.description or \
              getattr(self.context, 'text', self.context.description)
        if IRichTextData.providedBy(res):
            if not res.cooked:
                return self.context.description
            return res.cooked
        if res:
            return res
        return u''

    def getText(self, min_length=1, max_length=sys.maxint, text=None):
        if text is None:
            text = self.getContentText()
        temp = re.sub("(?u)<[^>]+>", " ",
            re.sub("(?u)\s+", " ", text))
        s = re.sub("(?u)\s+([\.,!?:;])", "\g<1>", temp)
        s = re.sub("(?u)&nbsp;", " ", s)
        s = re.sub("(?u)&quot;", '"', s)
        s = re.sub("(?u)&lt;", "<", s)
        s = re.sub("(?u)&gt;", ">", s)
        s = re.sub("(?u)&amp;", "&", s)

        return self.toNearPoint(s, min_length, max_length)

    def toNearPoint(self, data, min_length, max_length):
        ln = len(data)
        if ln < min_length:
            return data
        n = self.getNearPoint(data, u'.', min_length, max_length)
        if n > -1 and n <= max_length and n>=min_length:
            return data[:n] + u'..'
        else:
            n = self.getNearPoint(data, u' ', min_length, max_length)
            if n == -1 or n > max_length:
                n = max_length - 1
            return data[:n-1] + u'...'

    def getNearPoint(self, data, c, min_length, max_length):
        l = data.rfind(c, 0, min_length -1)
        r = data.find(c, min_length)
        if l > -1 and r > -1:
            lst = sorted([l, r], key=lambda x: abs(x-min_length))
            return lst[0] + 1
        elif l > -1 or r > -1:
            return max(l, r) + 1
        else:
            return -1
