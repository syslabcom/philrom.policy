from Products.CMFPlone.utils import safe_unicode
from recensio.contenttypes.citation import getFormatter
from recensio.contenttypes.content.review import get_formatted_names
from recensio.contenttypes.helperutilities import translate_message
from recensio.contenttypes.interfaces import IMetadataFormat
from recensio.theme.browser.views import recensioTranslate
from zope import interface
from zope.i18nmessageid import Message


class BaseMetadataFormat(object):
    interface.implements(IMetadataFormat)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getDecoratedTitle(self, obj, lastname_first=False):
        authors_string = obj.formatted_authors_editorial()

        rezensent_string = get_formatted_names(
            u' / ', ' ', obj.reviewAuthors, lastname_first=lastname_first)
        if rezensent_string:
            rezensent_string = "%s" % translate_message(
                Message(
                    u"reviewed_by", "recensio",
                    mapping={u"review_authors": rezensent_string},
                )
            )

        titles = "<span class='title'>%s</span>" % obj.punctuated_title_and_subtitle
        pub_year = "(%s)" % obj.yearOfPublication
        full_citation = getFormatter(', ', ' ', ', ')
        return full_citation(authors_string, titles, pub_year, rezensent_string)

    def formatted_authors_editorial(self, obj):
        """ #3111
        PMs and RMs have an additional field for editors"""
        authors_list = []
        if hasattr(obj, 'getAuthors'):
            for author in obj.getAuthors():
                if author['lastname'] or author['firstname']:
                    author_name = u'%s %s' % (
                        safe_unicode(author['firstname']),
                        safe_unicode(author['lastname']))
                    authors_list.append(author_name.strip())
        authors_str = u" / ".join(authors_list)

        editor_str = ""
        result = ""
        if hasattr(obj, "editorial"):
            editorial = obj.getEditorial()
            label_editor = ""
            if len(editorial) > 0 and editorial != (
                    {'lastname': '', 'firstname': ''}):
                if len(editorial) == 1:
                    label_editor = recensioTranslate(u"label_abbrev_editor")
                    editor = editorial[0]
                    editor_name = u'%s %s' % (
                        safe_unicode(editor['firstname']), safe_unicode(editor['lastname']))
                    editor_str = editor_name.strip()
                else:
                    label_editor = recensioTranslate(u"label_abbrev_editors")
                    editors = []
                    for editor in editorial:
                        editor_name = u'%s %s' % (
                            safe_unicode(editor['firstname']), safe_unicode(editor['lastname']))
                        editors.append(editor_name.strip())
                    editor_str = u" / ".join(editors)

                if editor_str != "":
                    result = editor_str + " " + label_editor
                    if authors_str != "":
                        result = result + ", " + authors_str

        if result == "" and authors_str != "":
            result = authors_str

        return result
