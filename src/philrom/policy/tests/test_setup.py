# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from philrom.policy.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of philrom.policy into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if philrom.policy is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('philrom.policy'))

    def test_uninstall(self):
        """Test if philrom.policy is cleanly uninstalled."""
        self.installer.uninstallProducts(['philrom.policy'])
        self.assertFalse(self.installer.isProductInstalled('philrom.policy'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IPhilromLayer is registered."""
        from philrom.policy.interfaces import IPhilromLayer
        from plone.browserlayer import utils
        self.failUnless(IPhilromLayer in utils.registered_layers())
