#-*- coding: utf-8 -*-
from Products.Archetypes import atapi
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.PortalTransforms.transforms.safe_html import scrubHTML
from cgi import escape
from recensio.contenttypes.citation import getFormatter
from recensio.contenttypes.content.review import BaseReview
from recensio.contenttypes.content.review import BaseReviewNoMagic
from recensio.contenttypes.content.review import get_formatted_names
from recensio.contenttypes.content.reviewmonograph import ReviewMonograph
from recensio.contenttypes.content.reviewmonograph import ReviewMonographSchema
from recensio.contenttypes.content.schemata import AuthorsSchema
from recensio.contenttypes.content.schemata import CommonReviewSchema
from recensio.contenttypes.content.schemata import PagecountSchema
from recensio.contenttypes.content.schemata import PageStartEndInPDFSchema
from recensio.contenttypes.content.schemata import ReviewSchema
from recensio.contenttypes.content.schemata import finalize_recensio_schema
from recensio.contenttypes.interfaces.reviewmonograph import IReviewMonograph
from zope.i18nmessageid import Message
from zope.interface import Interface
from zope.interface import implements

from recensio.policy import recensioMessageFactory as _
from philrom.policy.content.common import PageStartEndOfArticleInPublicationSchema
from philrom.policy.content.common import PhilromSchema


ArticleJournalSchema = (
    CommonReviewSchema.copy() +
#    AuthorsSchema.copy() +
    ReviewSchema.copy() +
    PageStartEndInPDFSchema.copy() +
    PageStartEndOfArticleInPublicationSchema.copy() +
    PagecountSchema.copy() +
    PhilromSchema.copy()
)
ArticleJournalSchema['title'].storage = atapi.AnnotationStorage()
finalize_recensio_schema(ArticleJournalSchema)

ArticleJournalSchema["reviewAuthors"].widget.label = _(
    u"label_article_authors")

ArticleJournalSchema['manuscriptsShelfmark'].schemata = "discussed_text"
ArticleJournalSchema['medievalAuthorsWorks'].schemata = "discussed_text"
ArticleJournalSchema['title'].schemata = 'article'
ArticleJournalSchema['pages'].schemata = 'article'
for field in ArticleJournalSchema.fields():
    if field.schemata == 'review':
        field.schemata = 'article'
    elif field.schemata == 'reviewed_text':
        field.schemata = 'discussed_text'


class IArticleJournal(Interface):
    """ """


class ArticleJournal(BaseReview):
    implements(IArticleJournal)

    meta_type = "ArticleJournal"
    schema = ArticleJournalSchema

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
        return ArticleJournalNoMagic(self).getDecoratedTitle(lastname_first)

    def get_citation_string(self):
        return ArticleJournalNoMagic(self).get_citation_string()

    def getLicense(self):
        return ArticleJournalNoMagic(self).getLicense()

    def getFirstPublicationData(self):
        return ArticleJournalNoMagic(self).getFirstPublicationData()


class ArticleJournalNoMagic(BaseReviewNoMagic):

    def getDecoratedTitle(real_self, lastname_first=False):
        """
        >>> from mock import Mock
        >>> at_mock = Mock()
        >>> at_mock.customCitation = ''
        >>> at_mock.formatted_authors_editorial = "Patrick Gerken / Alexander Pilz"
        >>> at_mock.punctuated_title_and_subtitle = "Plone 4.0. Das Benutzerhandbuch"
        >>> at_mock.reviewAuthors = [{'firstname' : 'Cillian', 'lastname'  : 'de Roiste'}]
        >>> review = ArticleJournalNoMagic(at_mock)
        >>> review.directTranslate = lambda a: a
        >>> review.getDecoratedTitle()
        u'Patrick Gerken / Alexander Pilz: Plone 4.0. Das Benutzerhandbuch (reviewed_by)'

        Original Spec:
        [Werkautor Vorname] [Werkautor Nachname]: [Werktitel]. [Werk-Untertitel] (reviewed by [Rezensent Vorname] [Rezensent Nachname])

        Analog, Werkautoren kann es mehrere geben (Siehe Citation)

        Hans Meier: Geschichte des Abendlandes. Ein Abriss (reviewed by Klaus Müller)

        """
        self = real_self.magic

        authors_string = get_formatted_names(
            u' / ', ', ', self.reviewAuthors, lastname_first = True)

        rezensent_string = get_formatted_names(u' / ', ' ', self.reviewAuthors,
                                               lastname_first = lastname_first)
        if rezensent_string:
            rezensent_string = "(%s)" % real_self.directTranslate(
                Message(u"reviewed_by", "recensio",
                        mapping={u"review_authors": rezensent_string}))

        full_citation = getFormatter(': ')
        return full_citation(
            authors_string, self.title)

    def get_citation_string(real_self):
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
        >>> review = ArticleJournalNoMagic(at_mock)
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
        self = real_self.magic
        if self.customCitation:
            return scrubHTML(self.customCitation).decode('utf8')

        args = {
            'in'        : real_self.directTranslate(Message(
                    u"text_in", "recensio", default="in:")),
            'page'      : real_self.directTranslate(Message(
                    u"text_pages", "recensio", default="p.")),
            ':'         : real_self.directTranslate(Message(
                    u"text_colon", "recensio", default=":")),
            }
        rev_details_formatter = getFormatter(
            u', ')
        rezensent_string = get_formatted_names(
            u' / ', ' ', self.reviewAuthors, lastname_first = False)
        authors_string = u' / '.join(self.medievalAuthorsWorks)
        item_string = rev_details_formatter(authors_string, self.title)

        mag_number_formatter = getFormatter(u', ', u', ')
        mag_number_string = mag_number_formatter(
            self.get_publication_title(), self.get_volume_title(),
            self.get_issue_title())

        location = real_self.getUUIDUrl()
        if getattr(self, "canonical_uri", False):  #3102
            location = real_self.directTranslate(
                Message(u"label_downloaded_via_recensio", "recensio"))

        citation_formatter = getFormatter(
            u', ', ', %(in)s ' % args, ', %(page)s ' % args, u', ')

        citation_string = citation_formatter(
            escape(rezensent_string), escape(item_string),
            escape(mag_number_string),
            self.page_start_end_in_print, location)

        return citation_string


atapi.registerType(ArticleJournal, 'philrom.policy')
