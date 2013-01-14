# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import getMultiAdapter, getUtility
from zope.interface import alsoProvides

from plone.app.testing import TEST_USER_ID
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.registry.interfaces import IRegistry

from collective.soap_search.interfaces import ISettings, ICollectiveSoapSearchLayer
from collective.soap_search.testing import COLLECTIVE_SOAP_SEARCH_INTEGRATION_TESTING
from collective.soap_search.config import PROJECTNAME


class ControlPanelTestCase(unittest.TestCase):

    layer = COLLECTIVE_SOAP_SEARCH_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.controlpanel = self.portal['portal_controlpanel']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        alsoProvides(self.portal.REQUEST, ICollectiveSoapSearchLayer)

    def test_controlpanel_has_view(self):
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name='collective.soap_search.settings')
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_is_protected(self):
        from AccessControl import Unauthorized
        logout()
        self.assertRaises(Unauthorized,
                          self.portal.restrictedTraverse,
                          '@@collective.soap_search.settings')

    def test_controlpanel_installed(self):
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertIn('collective.soap_search.settings', actions,
                      'control panel was not installed')

    def test_controlpanel_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[PROJECTNAME])
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertNotIn('collective.soap_search.settings', actions,
                         'control panel was not removed')


class RegistryTestCase(unittest.TestCase):

    layer = COLLECTIVE_SOAP_SEARCH_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(ISettings)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_max_batch_size_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'max_batch_size'))
        self.assertEqual(self.settings.max_batch_size, None)

    def test_records_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[PROJECTNAME])
        prefix = 'collective.soap_search.interfaces.ISettings.%s'
        registry = getUtility(IRegistry)
        self.assertNotIn(prefix % 'max_batch_size', registry)
