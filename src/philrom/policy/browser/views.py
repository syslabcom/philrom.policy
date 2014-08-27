from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ZTUtils import make_query
from recensio.theme.browser.publications import PublicationsView as PublicationsViewBase
from recensio.theme.browser.topical import BrowseTopicsView as BrowseTopicsViewBase
from recensio.theme.browser.homepage import HomepageView as HomepageViewBase


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


class HomepageView(HomepageViewBase):
    """Custom homepage for philrom"""

    template = ViewPageTemplateFile('templates/homepage.pt')

    def getJournals(self):
        pc = getToolByName(self.context, 'portal_catalog')
        query = dict(portal_type=["Journal"],
                     review_state="published",
                     sort_on='effective',
                     sort_order='reverse', b_size=5)
        res = pc(query)
        resultset = [dict(
            authors=self.format_authors(x),
            url=x.getURL(),
            title=x.getObject().Title(),
            date=self.format_effective_date(x['EffectiveDate'])
        ) for x in res[:5]
        ]
        # print "getReviewMonographs", lang, len(res)
        return resultset

    def getArticles(self):
        pc = getToolByName(self.context, 'portal_catalog')
        query = dict(portal_type=["Article"],
                     review_state="published",
                     sort_on='effective',
                     sort_order='reverse', b_size=5)
        resultset = list()
        res = pc(query)
        resultset = [dict(
            authors=self.format_authors(x),
            url=x.getURL(),
            title=x.getObject().Title(),
            date=self.format_effective_date(x['EffectiveDate'])
        ) for x in res[:5]
        ]
        # print "getReviewMonographs", lang, len(res)
        return resultset

