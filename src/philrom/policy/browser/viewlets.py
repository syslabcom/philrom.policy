from recensio.theme.browser.viewlets import _render_cachekey
from recensio.theme.browser.viewlets import publicationlisting
from plone.memoize import ram
from zope.interface import implements
from zope.viewlet.interfaces import IViewlet


class PhilromPublicationListing(publicationlisting):
    """ Lists Volumes/Issues/Reviews in the current Journal or Edited Volume"""
    implements(IViewlet)

    def visible(self):
        if hasattr(self.context, 'portal_type') and \
           self.context.portal_type == 'Document' and \
           hasattr(self.parent, 'portal_type') and \
           self.parent.portal_type in ('Journal', 'EditedVolume'):
            return True
        return False

    @ram.cache(_render_cachekey)
    def reviews(self, volume, issue=None):
        if not volume in self.parent.objectIds():
            return []
        if issue is None:
            review_objs = self.parent[volume].getFolderContents(
                {'portal_type': [
                    'Review Monograph', 'Review Journal', 'Article']},
                full_objects=True)
        else:
            if not issue in self.parent[volume].objectIds():
                return []
            review_objs = self.parent[volume][issue].getFolderContents(
                {'portal_type': [
                    'Review Monograph', 'Review Journal', 'Article']},
                full_objects=True)
        review_objs = sorted(review_objs,
                             key=lambda v: v.listAuthorsAndEditors())
        reviews = [self._make_dict(rev) for rev in review_objs]
        return reviews

    def _get_css_classes(self, obj):
        css_classes = []
        if len(obj.objectIds(
                ['ReviewMonograph', 'ReviewJournal', 'Article'])) > 0:
            css_classes.append('review_container')
            if self.is_expanded(obj.UID()):
                css_classes.append('expanded')
        return ' '.join(css_classes) or None
