from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from recensio.theme.browser.publications import PublicationsView as PublicationsViewBase
from recensio.theme.browser.topical import BrowseTopicsView as BrowseTopicsViewBase
from recensio.theme.browser.authorsearch import AuthorSearchView as AuthorSearchViewBase
from recensio.theme.browser.authorsearch import PRESENTATION_TYPES
from recensio.theme.browser.authorsearch import REVIEW_TYPES
from recensio.theme.browser.homepage import HomepageView as HomepageViewBase
from recensio.theme.browser.publications import PublicationsView as PublicationsViewBase
from recensio.theme.browser.topical import BrowseTopicsView as BrowseTopicsViewBase


class PublicationsView(PublicationsViewBase):
    def publications(self):
        pc = self.context.portal_catalog
        publist = []
        currlang = self.context.portal_languages.getPreferredLanguage()
        pubs = pc(object_provides="recensio.contenttypes.interfaces.publication.IPublication",
                  path='/'.join(self.context.getPhysicalPath()),
                  sort_on="sortable_title",
                  review_state='published')
        for pub in pubs:
            publist.append(self.brain_to_pub(pub, currlang))
        return publist


class BrowseTopicsView(BrowseTopicsViewBase):
    """Also include Articles."""

    def __init__(self, context, request):
        super(BrowseTopicsView, self).__init__(context, request)
        self.default_query['portal_type'].append('Article')
        self.default_query['sort_on'] = 'yearOfPublication'
        self.default_query['sort_order'] = 'reverse'


class AuthorSearchView(AuthorSearchViewBase):
    """Also include Articles."""

    template = ViewPageTemplateFile('templates/authorsearch.pt')

    def all_authors(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        membership_tool = getToolByName(self.context, 'portal_membership')

        reviews = catalog({
            'fq': '+portal_type:(' + ' OR '.join(
                map(lambda x: '"%s"' % x, REVIEW_TYPES)) + ')',
            'facet': 'true',
            'facet.field': 'authors',
            'facet.limit': '-1',
            'facet.mincount': '1',
        }).facet_counts['facet_fields']['authors']
        presentations = catalog({
            'fq': '+portal_type:(' + ' OR '.join(
                map(lambda x: '"%s"' % x, PRESENTATION_TYPES)) + ')',
            'facet': 'true',
            'facet.field': 'authors',
            'facet.limit': '-1',
            'facet.mincount': '1',
        }).facet_counts['facet_fields']['authors']
        articles = catalog({
            'fq': '+portal_type:(' + ' OR '.join(
                map(lambda x: '"%s"' % x, ['Article'])) + ')',
            'facet': 'true',
            'facet.field': 'authors',
            'facet.limit': '-1',
            'facet.mincount': '1',
        }).facet_counts['facet_fields']['authors']
        commentator_user_ids = catalog.uniqueValuesFor('commentators')
        comments = {}
        for commentator_id in commentator_user_ids:
            member = membership_tool.getMemberById(commentator_id)
            if not member:
                continue
            comments[safe_unicode(('%s, %s' % (
                member.getProperty('lastname'),
                member.getProperty('firstname'))
            ))] = commentator_id

        authors = [dict(name=x.strip(', '),
                   reviews=reviews.get(safe_unicode(x), 0),
                   presentations=presentations.get(safe_unicode(x), 0),
                   articles=articles.get(safe_unicode(x), 0),
                   comments=comments.get(safe_unicode(x), 0))
                   for x in catalog.uniqueValuesFor('authors')]
        authors = filter(lambda x: x['presentations'] + x['reviews']
                         + x['articles']
                         + (1 if x['comments'] else 0) != 0, authors)

        return authors


class HomepageView(HomepageViewBase):
    """Custom homepage for philrom"""

    template = ViewPageTemplateFile('templates/homepage.pt')

    def getObjectsOfTypes(self, types):
        pc = getToolByName(self.context, 'portal_catalog')
        query = dict(portal_type=types,
                     review_state="published",
                     sort_on='effective',
                     sort_order='reverse', b_size=3)
        res = pc(query)
        resultset = [dict(
            authors=self.format_authors(x),
            url=x.getURL(),
            title=x.getObject().Title(),
            date=self.format_effective_date(x['EffectiveDate'])
        ) for x in res[:3]
        ]
        return resultset

    def getEditedVolumes(self):
        return self.getObjectsOfTypes(["EditedVolume"])

    def getJournals(self):
        return self.getObjectsOfTypes(["Journal"])

    def getArticles(self):
        return self.getObjectsOfTypes(["Article"])

    def getReviews(self):
        return self.getObjectsOfTypes(["Review Monograph", "Review Journal"])
