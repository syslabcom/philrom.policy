import unittest2 as unittest
from plone.app.testing import login
from plone.app.testing import SITE_OWNER_NAME
from recensio.contenttypes.interfaces.review import IParentGetter

from philrom.policy.testing import INTEGRATION_TESTING


class TestParentGetter(unittest.TestCase):
    """ """
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.publication = self.portal["sample-reviews"]["newspapera"]
        login(self.layer['app'], SITE_OWNER_NAME)
        article_id = self.publication['summer']['issue-2'].invokeFactory(
            'Article', 'article')
        self.article = self.publication['summer']['issue-2'][article_id]

        journal_id = self.portal["sample-reviews"].invokeFactory(
            'Journal', id='journal1', title='Journal 1')
        self.journal = self.portal["sample-reviews"][journal_id]
        vol_id = self.journal.invokeFactory('Volume', id='volume1')
        rm_id = self.journal[vol_id].invokeFactory(
            'Review Monograph', id='rm1')
        self.review = self.journal[vol_id][rm_id]
        article2_id = self.journal[vol_id].invokeFactory(
            'Article', 'article')
        self.article2 = self.journal[vol_id][article2_id]

    def test_get_parent_publication_of_article_in_publication(self):
        result = IParentGetter(self.article).get_parent_object_of_type(
            'Publication')
        self.assertEqual(result, self.publication)

    def test_get_parent_publication_of_article_in_journal(self):
        result = IParentGetter(self.article2).get_parent_object_of_type(
            'Publication')
        self.assertEqual(result, self.journal)

    def test_get_parent_journal_of_article_in_journal(self):
        result = IParentGetter(self.article2).get_parent_object_of_type(
            'Journal')
        self.assertEqual(result, self.journal)

    def test_get_parent_publication_of_review_monograph_in_journal(self):
        result = IParentGetter(self.review).get_parent_object_of_type(
            'Publication')
        self.assertEqual(result, self.journal)

    def test_get_parent_journal_of_review_monograph_in_journal(self):
        result = IParentGetter(self.review).get_parent_object_of_type(
            'Journal')
        self.assertEqual(result, self.journal)
