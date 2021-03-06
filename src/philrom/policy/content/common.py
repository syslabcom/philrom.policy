from Products.ATVocabularyManager import NamedVocabulary
from Products.Archetypes import atapi
from Products.Archetypes.Widget import KeywordWidget
from recensio.policy import recensioMessageFactory as _


PhilromSchema = atapi.Schema(
    (
        atapi.LinesField(
            'textForm',
            multiValued=1,
            schemata="reviewed_text",
            storage=atapi.AnnotationStorage(),
            required=False,
            vocabulary=NamedVocabulary("text_form"),
            widget=atapi.MultiSelectionWidget(
                label=_(
                    u"label_text_form",
                    default=(u"Text form")
                )
            ),
            searchable=True,
        ),
        atapi.LinesField(
            'manuscriptsShelfmark',
            multiValued=1,
            accessor='getManuscriptsShelfmark',
            schemata="reviewed_text",
            storage=atapi.AnnotationStorage(),
            widget=KeywordWidget(
                label=_(u"Manuscripts (Shelfmark)"),
            ),
        ),
        atapi.LinesField(
            'medievalAuthorsWorks',
            multiValued=1,
            accessor='getMedievalAuthorsWorks',
            schemata="reviewed_text",
            storage=atapi.AnnotationStorage(),
            widget=KeywordWidget(
                label=_(u"Medieval authors/works"),
            ),
        ),
    )
)


PageStartEndOfArticleInPublicationSchema = atapi.Schema((
    atapi.StringField(
        'heading__page_number_of_article_in_publication',
        schemata="review",
        widget=atapi.LabelWidget(
            label=_(
                u"description_page_number_of_article_in_publication",
                default=(u"Page numbers of the article")
            )
        ),
    ),
    atapi.IntegerField(
        'pageStartOfArticleInPublication',
        schemata="review",
        storage=atapi.AnnotationStorage(),
        validators="isInt",
        widget=atapi.IntegerWidget(
            label=_(u"label_page_start_of_presented_review_in_journal"),
        ),
    ),
    atapi.IntegerField(
        'pageEndOfArticleInPublication',
        schemata="review",
        storage=atapi.AnnotationStorage(),
        validators="isInt",
        widget=atapi.IntegerWidget(
            label=_(u"label_page_end_of_presented_review_in_journal"),
        ),
    )
))


