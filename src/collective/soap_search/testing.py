from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting

from zope.configuration import xmlconfig


class Collectivesoap_SearchLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.soap_search
        xmlconfig.file('configure.zcml', collective.soap_search, context=configurationContext)

        # Install products that use an old-style initialize() function
        #z2.installProduct(app, 'Products.PloneFormGen')

#    def tearDownZope(self, app):
#        # Uninstall products installed above
#        z2.uninstallProduct(app, 'Products.PloneFormGen')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.soap_search:default')

COLLECTIVE_SOAP_SEARCH_FIXTURE = Collectivesoap_SearchLayer()
COLLECTIVE_SOAP_SEARCH_INTEGRATION_TESTING = IntegrationTesting(bases=(COLLECTIVE_SOAP_SEARCH_FIXTURE,), name="Collectivesoap_SearchLayer:Integration")
