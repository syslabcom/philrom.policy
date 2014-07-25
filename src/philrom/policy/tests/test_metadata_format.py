#-*- coding: utf-8 -*-
from philrom.policy.interfaces import IPhilromLayer
from philrom.policy.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import login
from zope.interface import directlyProvides

import unittest2 as unittest


class TestMetadataFormat(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        # register the browser layer
        self.request = self.layer["request"]
        directlyProvides(self.request, IPhilromLayer)

        # FIXME Change the examples to Italian after we have translations
        ltool = api.portal.get_tool("portal_languages")
        ltool.manage_setLanguageSettings("en", ["en"])
        ltool.setLanguageBindings()

        issue = self.portal["sample-reviews"]["newspapera"]["summer"]["issue-2"]
        login(self.layer['app'], SITE_OWNER_NAME)
        rm_id = issue.invokeFactory(
            'Review Monograph',
            id='rm1',
            title='Tristano e Isotta',
            yearOfPublication="2013",
            reviewAuthors=({'firstname': 'Margherita', 'lastname': 'Lecco'},),
            authors=({'firstname': '', 'lastname': u'Béroul'},),
            editorial=({'firstname': 'Gioia', 'lastname': 'Paradisi'},),
        )
        self.review = issue[rm_id]

    def test_review_monograph_decorated_title(self):
        generated_title = self.review.getDecoratedTitle()
        correct_title = (
            u"Gioia Paradisi (ed.), Béroul, <span class='titles'>Tristano e Isotta</span> "
            "(2013), reviewed by Margherita Lecco"
        )
        self.assertEqual(correct_title, generated_title)
