# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.interface import alsoProvides

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from collective.soap_search.interfaces import ICollectiveSoapSearchLayer
from collective.soap_search.testing import COLLECTIVE_SOAP_SEARCH_INTEGRATION_TESTING


class SoapSearchTestCase(unittest.TestCase):

    layer = COLLECTIVE_SOAP_SEARCH_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.controlpanel = self.portal['portal_controlpanel']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        alsoProvides(self.portal.REQUEST, ICollectiveSoapSearchLayer)

    def test_results(self):
        pass
