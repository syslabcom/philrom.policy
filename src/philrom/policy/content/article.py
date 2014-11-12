#-*- coding: utf-8 -*-
from Products.Archetypes import atapi
from Products.PortalTransforms.transforms.safe_html import scrubHTML
from cgi import escape
from philrom.policy.content.common import PageStartEndOfArticleInPublicationSchema
from philrom.policy.content.common import PhilromSchema
from philrom.policy.content.metadataformat import BaseMetadataFormat
from recensio.contenttypes.citation import getFormatter
from recensio.contenttypes.content.review import BaseReview
from recensio.contenttypes.content.review import BaseReviewNoMagic
from recensio.contenttypes.content.review import get_formatted_names
from recensio.contenttypes.content.schemata import CommonReviewSchema
from recensio.contenttypes.content.schemata import PageStartEndInPDFSchema
from recensio.contenttypes.content.schemata import PagecountSchema
from recensio.contenttypes.content.schemata import ReviewSchema
from recensio.contenttypes.content.schemata import finalize_recensio_schema
from recensio.contenttypes.helperutilities import translate_message
from recensio.contenttypes.interfaces import IMetadataFormat
from recensio.policy import recensioMessageFactory as _
from zope.component import getMultiAdapter
from zope.i18nmessageid import Message
from zope.interface import Interface
from zope.interface import implements


ArticleSchema = (
    CommonReviewSchema.copy() +
#    AuthorsSchema.copy() +
    ReviewSchema.copy() +
    PageStartEndInPDFSchema.copy() +
    PageStartEndOfArticleInPublicationSchema.copy() +
    PagecountSchema.copy() +
    PhilromSchema.copy()
)
ArticleSchema['title'].storage = atapi.AnnotationStorage()
finalize_recensio_schema(ArticleSchema)

ArticleSchema["reviewAuthors"].widget.label = _(
    u"label_article_authors")

ArticleSchema['manuscriptsShelfmark'].schemata = "discussed_text"
ArticleSchema['medievalAuthorsWorks'].schemata = "discussed_text"
ArticleSchema['textForm'].schemata = "discussed_text"
ArticleSchema['title'].schemata = 'article'
ArticleSchema['pages'].schemata = 'article'
for field in ArticleSchema.fields():
    if field.schemata == 'review':
        field.schemata = 'article'
    elif field.schemata == 'reviewed_text':
        field.schemata = 'discussed_text'


class IArticle(Interface):
    """ """


class Article(BaseReview):
    implements(IArticle)

    meta_type = "Article"
    schema = ArticleSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # Base
    reviewAuthors = atapi.ATFieldProperty('reviewAuthors')
    languageReview = atapi.ATFieldProperty(
        'languageReview')
    languageReviewedText = atapi.ATFieldProperty('languageReviewedText')
    recensioID = atapi.ATFieldProperty('recensioID')
    subject = atapi.ATFieldProperty('subject')
    pdf = atapi.ATFieldProperty('pdf')
    doc = atapi.ATFieldProperty('doc')
    review = atapi.ATFieldProperty('review')
    customCitation = atapi.ATFieldProperty('customCitation')
    canonical_uri = atapi.ATFieldProperty('canonical_uri')
    uri = atapi.ATFieldProperty('uri')
    urn = atapi.ATFieldProperty('urn')

    # Common
    ddcPlace = atapi.ATFieldProperty('ddcPlace')
    ddcSubject = atapi.ATFieldProperty('ddcSubject')
    ddcTime = atapi.ATFieldProperty('ddcTime')

    # PageStartEnd
    pageStart = atapi.ATFieldProperty('pageStart')
    pageEnd = atapi.ATFieldProperty('pageEnd')

    # Pagecount
    pages = atapi.ATFieldProperty('pages')

    # Philrom
    medievalAuthorsWorks = atapi.ATFieldProperty('medievalAuthorsWorks')
    manuscriptsShelfmark = atapi.ATFieldProperty('manuscriptsShelfmark')
    textForm = atapi.ATFieldProperty('textForm')

    # Reorder the fields as required for the edit view
    ordered_fields = [
        "reviewAuthors",
        "title",
        "pages",
        "pdf",
        "pageStart",
        "pageEnd",
        "heading__page_number_of_article_in_publication",
        "pageStartOfArticleInPublication",
        "pageEndOfArticleInPublication",
        "doc",
        "languageReview",
        "review",
        "ddcPlace",
        "textForm",
        "medievalAuthorsWorks",
        "manuscriptsShelfmark",
        "ddcTime",
        "ddcSubject",
        "languageReviewedText",
        "subject",
        "customCitation",
        "canonical_uri",
        "urn",
        "bv",
    ]

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

    # An ordered list of fields used for the metadata area of the view

    metadata_fields = [
        "metadata_review_type_code", "get_journal_title",
        "metadata_start_end_pages", "metadata_review_author",
        "languageReview", "title",
        "pages", "urn", "ddcSubject", "ddcTime", "ddcPlace",
        "subject", "canonical_uri", "metadata_recensioID"]

    def get_publication_title(self):
        """ Equivalent of 'titleJournal'"""
        return self.get_title_from_parent_of_type("Publication")

    get_journal_title = get_publication_title #2542

    def get_publication_object(self):
        return self.get_parent_object_of_type("Publication")

    def get_volume_title(self):
        """ Equivalent of 'volume'"""
        return self.get_title_from_parent_of_type("Volume")

    def get_issue_title(self):
        """ Equivalent of 'issue'"""
        return self.get_title_from_parent_of_type("Issue")

    def getDecoratedTitle(self, lastname_first=False):
        metadata_format = getMultiAdapter((self, self.REQUEST), IMetadataFormat)
        return metadata_format.getDecoratedTitle(self, lastname_first)

    def get_citation_string(self):
        metadata_format = getMultiAdapter((self, self.REQUEST), IMetadataFormat)
        return metadata_format.get_citation_string(self)

    def getLicense(self):
        return ArticleNoMagic(self).getLicense()

    def getFirstPublicationData(self):
        return ArticleNoMagic(self).getFirstPublicationData()


class ArticleNoMagic(BaseReviewNoMagic):
    pass


atapi.registerType(Article, 'philrom.policy')


class MetadataFormat(BaseMetadataFormat):

    def getDecoratedTitle(self, obj, lastname_first=False):
        """
        >>> from mock import Mock
        >>> at_mock = Mock()
        >>> at_mock.customCitation = ''
        >>> at_mock.formatted_authors_editorial = "Patrick Gerken / Alexander Pilz"
        >>> at_mock.punctuated_title_and_subtitle = "Plone 4.0. Das Benutzerhandbuch"
        >>> at_mock.reviewAuthors = [{'firstname' : 'Cillian', 'lastname'  : 'de Roiste'}]
        >>> review = ArticleNoMagic(at_mock)
        >>> review.directTranslate = lambda a: a
        >>> review.getDecoratedTitle()
        u'Patrick Gerken / Alexander Pilz: Plone 4.0. Das Benutzerhandbuch (reviewed_by)'

        Original Spec:
        [Werkautor Vorname] [Werkautor Nachname]: [Werktitel]. [Werk-Untertitel] (reviewed by [Rezensent Vorname] [Rezensent Nachname])

        Analog, Werkautoren kann es mehrere geben (Siehe Citation)

        Hans Meier: Geschichte des Abendlandes. Ein Abriss (reviewed by Klaus Müller)

        """
        authors_string = get_formatted_names(
            u' / ', ', ', obj.reviewAuthors, lastname_first=True)

        rezensent_string = get_formatted_names(
            u' / ', ' ', obj.reviewAuthors, lastname_first=lastname_first)
        if rezensent_string:
            rezensent_string = "(%s)" % translate_message(
                Message(u"reviewed_by", "recensio", mapping={u"review_authors": rezensent_string}))

        title = "<span class='title'>%s</span>" % obj.title
        full_citation = getFormatter(', ')
        return full_citation(authors_string, title)

    def get_citation_string(self, obj):
        """
        Either return the custom citation or the generated one
        >>> from mock import Mock
        >>> at_mock = Mock()
        >>> at_mock.customCitation = ''
        >>> at_mock.get = lambda x: None
        >>> at_mock.formatted_authors_editorial = u"Gerken\u2665, Patrick\u2665 / Pilz, Alexander"
        >>> at_mock.title = "Plone 4.0♥?"
        >>> at_mock.subtitle = "Das Benutzerhandbuch♥"
        >>> at_mock.reviewAuthors = [{'firstname' : 'Cillian♥', 'lastname' : 'de Roiste♥'}]
        >>> at_mock.yearOfPublication = '2009♥'
        >>> at_mock.publisher = 'SYSLAB.COM GmbH♥'
        >>> at_mock.placeOfPublication = 'München♥'
        >>> at_mock.get_issue_title = lambda :'Open Source Mag 1♥'
        >>> at_mock.get_volume_title = lambda :'Open Source Mag Vol 1♥'
        >>> at_mock.get_publication_title = lambda :'Open Source♥'
        >>> at_mock.portal_url = lambda :'http://www.syslab.com'
        >>> at_mock.UID = lambda :'12345'
        >>> at_mock.canonical_uri = ''
        >>> at_mock.page_start_end_in_print = '11-21'
        >>> review = ArticleNoMagic(at_mock)
        >>> review.directTranslate = lambda m: m.default
        >>> review.get_citation_string()
        u'de Roiste\u2665, Cillian\u2665: review of: Gerken\u2665, Patrick\u2665 / Pilz, Alexander, Plone 4.0\u2665? Das Benutzerhandbuch\u2665, M\\xfcnchen\u2665: SYSLAB.COM GmbH\u2665, 2009\u2665, in: Open Source\u2665, Open Source Mag Vol 1\u2665, Open Source Mag 1\u2665, p. 11-21, <a href="http://syslab.com/r/12345">http://syslab.com/r/12345</a>'


        Original Spec:

        [Rezensent Nachname], [Rezensent Vorname]: review of: [Werkautor Nachname], [Werkautor Vorname], [Werktitel]. [Werk-Untertitel], [Erscheinungsort]: [Verlag], [Jahr], in: [Zs-Titel], [Nummer], [Heftnummer (Erscheinungsjahr)], p.[pageStart]-[pageEnd] URL recensio.

        Werkautoren kann es mehrere geben, die werden dann durch ' / ' getrennt alle aufgelistet.
        Note: gezähltes Jahr entfernt.
        Da es die Felder Zs-Titel, Nummer und Heftnummer werden die Titel der Objekte magazine, volume, issue genommen, in dem der Review liegt

        Müller, Klaus: review of: Meier, Hans, Geschichte des Abendlandes. Ein Abriss, München: Oldenbourg, 2010, in: Zeitschrift für Geschichte, 39, 3 (2008/2009), www.recensio.net/##

        """
        if obj.customCitation:
            return scrubHTML(obj.customCitation).decode('utf8')

        args = {
            'in': translate_message(Message(
                u"text_in", "recensio", default="in:")),
            'page': translate_message(Message(
                u"text_pages", "recensio", default="p.")),
            ':': translate_message(Message(
                u"text_colon", "recensio", default=":")),
        }
        rezensent_string = get_formatted_names(
            u' / ', ' ', obj.reviewAuthors, lastname_first = False)
        item_string = '<span class="title">%s</span>' % obj.title

        mag_number_formatter = getFormatter(u', ', u', ')
        mag_number_string = mag_number_formatter(
            obj.get_publication_title(), obj.get_volume_title(),
            obj.get_issue_title())

        location = obj.getUUIDUrl()
        if getattr(obj, "canonical_uri", False):  #3102
            location = translate_message(
                Message(u"label_downloaded_via_recensio", "recensio"))

        citation_formatter = getFormatter(
            u', ', ', %(in)s ' % args, ', %(page)s ' % args, u', ')

        citation_string = citation_formatter(
            escape(rezensent_string), item_string,
            escape(mag_number_string),
            obj.page_start_end_in_print, location)

        return citation_string
