from metadataformat import BaseMetadataFormat
from recensio.contenttypes.citation import getFormatter
from recensio.contenttypes.helperutilities import translate_message
from zope.i18nmessageid import Message


class PresentationMonographMetadataFormat(BaseMetadataFormat):

    def getDecoratedTitle(self, obj):
        rezensent_string = getFormatter(' ')(
            obj.reviewAuthors[0]["firstname"], obj.reviewAuthors[0]["lastname"])
        if rezensent_string:
            rezensent_string = "(%s)" % translate_message(
                Message(u"presented_by", "recensio", mapping={u"review_authors": rezensent_string}))
        titles = "<span class='title'>%s</span>" % obj.punctuated_title_and_subtitle
        full_citation = getFormatter(', ', ' ')
        return full_citation(obj.formatted_authors_editorial(), titles, rezensent_string)


class PresentationOnlineResourceMetadataFormat(BaseMetadataFormat):

    def getDecoratedTitle(self, obj):
        rezensent_string = getFormatter(' ')(
            obj.reviewAuthors[0]["firstname"], obj.reviewAuthors[0]["lastname"])
        if rezensent_string:
            rezensent_string = "(%s)" % translate_message(
                Message(u"presented_by", "recensio",
                        mapping={u"review_authors": rezensent_string}))
        full_citation = getFormatter(' ')
        title = "<span class='title'>%s</span>" % obj.title.decode('utf-8')
        return full_citation(title, rezensent_string)
