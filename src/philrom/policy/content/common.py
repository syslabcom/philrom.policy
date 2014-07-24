from Products.Archetypes import atapi
from Products.Archetypes.Widget import KeywordWidget
from recensio.policy import recensioMessageFactory as _


PhilromSchema = atapi.Schema(
    (
        atapi.LinesField(
            'manuscriptsShelfmark',
            multiValued=1,
            schemata="reviewed_text",
            storage=atapi.AnnotationStorage(),
            widget=KeywordWidget(
                label=_(u"Manuscripts (Shelfmark)"),
            ),
        ),
        atapi.LinesField(
            'medievalAuthorsWorks',
            multiValued=1,
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


