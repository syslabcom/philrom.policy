from Products.ATVocabularyManager import NamedVocabulary
from Products.Archetypes import atapi

from philrom.policy import _


PhilromSchema = atapi.Schema(
    (
        atapi.LinesField(
            'manuscriptsShelfmark',
            schemata="reviewed_text",
            storage=atapi.AnnotationStorage(),
            vocabulary=NamedVocabulary("manuscripts_shelfmark"),
            widget=atapi.MultiSelectionWidget(
                label=_(u"Manuscripts (Shelfmark)"),
                size=10,
            ),
        ),
        atapi.LinesField(
            'medievalAuthorsWorks',
            schemata="reviewed_text",
            storage=atapi.AnnotationStorage(),
            vocabulary=NamedVocabulary("medieval_authors_works"),
            widget=atapi.MultiSelectionWidget(
                label=_(u"Medieval authors/works"),
                size=10,
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
            label = _(u"label_page_start_of_presented_review_in_journal"),
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


