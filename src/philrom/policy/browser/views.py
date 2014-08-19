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
