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
        ltool.manage_setLanguageSettings("de", ["de"])
        ltool.setLanguageBindings()

        self.issue = self.portal["sample-reviews"]["newspapera"]["summer"]["issue-2"]
        login(self.layer['app'], SITE_OWNER_NAME)
        self.maxDiff = None

    def test_review_monograph_decorated_title(self):
        item_id = "rm1"
        self.issue.invokeFactory(
            'Review Monograph',
            id=item_id,
            title='Tristano e Isotta',
            yearOfPublication="2013",
            reviewAuthors=({'firstname': 'Margherita', 'lastname': 'Lecco'},),
            authors=({'firstname': '', 'lastname': u'Béroul'},),
            editorial=({'firstname': 'Gioia', 'lastname': 'Paradisi'},),
        )
        item = self.issue[item_id]
        generated_title = self.issue[item_id].getDecoratedTitle()
        correct_title = (
            u"Gioia Paradisi (Hg.), Béroul, <span class='title'>Tristano e Isotta</span> "
            "(2013), rezensiert von Margherita Lecco"
        )
        self.assertEqual(correct_title, generated_title)

    def test_reviewjournal_decorated_title(self):
        item_id = "rj1"
        self.issue.invokeFactory(
            'Review Journal',
            id=item_id,
            title='Plone Mag',
            reviewAuthors=({'firstname': 'Cillian', 'lastname': 'de Róiste'},),
            yearOfPublication="2009",
            officialYearOfPublication="2010",
            volumeNumber="1",
            issueNumber="3",
        )
        generated_title = self.issue[item_id].getDecoratedTitle()
        correct_title = (
            u'<span class="title">Plone Mag, 1 (2010/2009), 3</span> (rezensiert von Cillian '
            u'de Róiste)'
        )
        self.assertEqual(correct_title, generated_title)

    def test_presentationmonograph_decorated_title(self):
        member_folder = self.portal.Members.fake_member
        item_id = "pm1"
        member_folder.invokeFactory(
            'Presentation Monograph',
            id=item_id,
            title=u'Gelebter Internationalismus',
            subtitle=u'Österreichs Linke und der algerische Widerstand (1958-1963)',
            authors=({'firstname': 'Fritz', 'lastname': ' Keller'},),
            reviewAuthors=({'firstname': 'Fritz', 'lastname': 'Keller'},),
            yearOfPublication="2009",
        )
        generated_title = member_folder[item_id].getDecoratedTitle()
        correct_title = (
            u"Fritz Keller, <span class='title'>Gelebter Internationalismus. Österreichs "
            u"Linke und der algerische Widerstand (1958-1963)</span> (präsentiert von "
            u"Fritz Keller)"
        )
        self.assertEqual(correct_title, generated_title)

    def test_presentationonlineresource_decorated_title(self):
        member_folder = self.portal.Members.fake_member
        item_id = "por1"
        member_folder.invokeFactory(
            'Presentation Online Resource',
            id=item_id,
            title=(
                u'Revues.org, plateforme de revues et de collections de livres en sciences '
                u'humaines et sociales'
            ),
            reviewAuthors=({'firstname': 'Delphine', 'lastname': 'Cavallo'},),
        )
        generated_title = member_folder[item_id].getDecoratedTitle()
        correct_title = (
            u"<span class='title'>Revues.org, plateforme de revues et de collections de livres en "
            u"sciences humaines et sociales</span> (präsentiert von Delphine Cavallo)"
        )
        self.assertEqual(correct_title, generated_title)

    def test_review_monograph_citation_string(self):
        item_id = "rm1"
        self.issue.invokeFactory(
            'Review Monograph',
            id=item_id,
            title='Tristano e Isotta',
            yearOfPublication="2013",
            reviewAuthors=({'firstname': 'Margherita', 'lastname': 'Lecco'},),
            authors=({'firstname': '', 'lastname': u'Béroul'},),
            editorial=({'firstname': 'Gioia', 'lastname': 'Paradisi'},),
        )
        item = self.issue[item_id]
        uid = item.UID()
        generated_citation_string = item.get_citation_string()
        correct_title = (
            u'Lecco, Margherita, Rezension über: Gioia Paradisi (Hg.), Béroul, '
            u'<span class="title">Tristano e Isotta</span>, '
            u'2013, in: Zeitschrift 1, Summer, Issue 2, <a href="http://nohost/plone/r/%s">'
            u'http://nohost/plone/r/%s</a>' % (uid, uid)
        )
        self.assertEqual(correct_title, generated_citation_string)

    def test_reviewjournal_citation_string(self):
        item_id = "rj1"
        self.issue.invokeFactory(
            'Review Journal',
            id=item_id,
            title='Plone Mag',
            reviewAuthors=({'firstname': 'Cillian', 'lastname': 'de Róiste'},),
            yearOfPublication="2009",
            officialYearOfPublication="2010",
            volumeNumber="1",
            issueNumber="3",
        )
        item = self.issue[item_id]
        uid = item.UID()
        generated_citation_string = item.get_citation_string()
        correct_title = (
            u'de Róiste, Cillian, Rezension über: <span class="title">Plone Mag, 1, 3 '
            u'(2010/2009)</span>, in: Zeitschrift 1, '
            u'Summer, Issue 2, <a href="http://nohost/plone/r/%s">http://nohost/plone/r/%s</a>' %
            (uid, uid)
        )
        self.assertEqual(correct_title, generated_citation_string)

    def test_presentationmonograph_citation_string(self):
        member_folder = self.portal.Members.fake_member
        item_id = "pm1"
        member_folder.invokeFactory(
            'Presentation Monograph',
            id=item_id,
            title=u'Gelebter Internationalismus',
            subtitle=u'Österreichs Linke und der algerische Widerstand (1958-1963)',
            authors=({'firstname': 'Fritz', 'lastname': ' Keller'},),
            reviewAuthors=({'firstname': 'Fritz', 'lastname': 'Keller'},),
            yearOfPublication="2009",
        )
        item = member_folder[item_id]
        uid = item.UID()
        generated_citation_string = item.get_citation_string()
        correct_title = (
            u'Keller, Fritz, Präsentation von: Fritz Keller, <span class="title">Gelebter '
            u'Internationalismus. Österreichs Linke und der algerische Widerstand (1958-1963)'
            u'</span>, 2009, <a href="http://nohost/plone/r/%s">http://nohost/plone/r/%s</a>'
            % (uid, uid)
        )
        self.assertEqual(correct_title, generated_citation_string)

    def test_presentationonlineresource_citation_string(self):
        member_folder = self.portal.Members.fake_member
        item_id = "por1"
        member_folder.invokeFactory(
            'Presentation Online Resource',
            id=item_id,
            title=(
                u'Revues.org, plateforme de revues et de collections de livres en sciences '
                u'humaines et sociales'
            ),
            reviewAuthors=({'firstname': 'Delphine', 'lastname': 'Cavallo'},),
        )
        item = member_folder[item_id]
        uid = item.UID()
        generated_citation_string = item.get_citation_string()
        correct_title = (
            u'Cavallo, Delphine, Präsentation von: <span class="title">Revues.org, plateforme de '
            u'revues et de collections de livres en sciences humaines et sociales</span>, '
            '<a href="http://nohost/plone/r/%s">http://nohost/plone/r/%s</a>' % (uid, uid)
        )
        self.assertEqual(correct_title, generated_citation_string)

    def test_article_citation_string(self):
        item_id = "art1"
        self.issue.invokeFactory(
            'Article',
            id=item_id,
            title='Tristano e Isotta',
            reviewAuthors=({'firstname': 'Margherita', 'lastname': 'Lecco'},),
            medievalAuthorsWorks=('Béroul',),
        )
        item = self.issue[item_id]
        uid = item.UID()
        generated_citation_string = item.get_citation_string()
        correct_title = (
            u'Margherita Lecco, <span class="title">Tristano e Isotta</span>, '
            u'in: Zeitschrift 1, Summer, Issue 2, <a href="http://nohost/plone/r/%s">'
            u'http://nohost/plone/r/%s</a>' % (uid, uid)
        )
        self.assertEqual(correct_title, generated_citation_string)
