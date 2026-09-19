# interface definitions

from zope.interface import Interface
from zope import schema

from .properties import IPropertiesTool
from .properties import ISimpleItemWithProperties
from .basetool import IPloneBaseTool
from .basetool import IPloneTool
from .basetool import IPloneCatalogTool
from .controlpanel import IControlPanel
from .events import ISiteManagerCreatedEvent
from .events import IReorderedEvent
from .interface import IInterfaceTool
from .installable import INonInstallable
from .migration import IMigrationTool
from .siteroot import IPloneSiteRoot
from .siteroot import IMigratingPloneSiteRoot
from .siteroot import ITestCasePloneSiteRoot
from .constrains import IConstrainTypes
from .constrains import ISelectableConstrainTypes
from .structure import INonStructuralFolder
from .factory import IFactoryTool
from .translationservice import ITranslationServiceTool
from .breadcrumbs import IHideFromBreadcrumbs
from .workflow import IWorkflowChain


XHTML_TAGS = (
    u"a abbr acronym address area b base bdo big blockquote body br "
    u"button caption cite code col colgroup dd del div dfn dl dt em "
    u"fieldset form h1 h2 h3 h4 h5 h6 head hr html i img input ins kbd "
    u"label legend li link map meta noscript object ol optgroup option "
    u"p param pre q samp script select small span strong style sub sup "
    u"table tbody td textarea tfoot th thead title tr tt ul var").split()


class ITagAttrPair(Interface):
    """Tag/attribute pair used by the HTML filtering registry schema."""

    tags = schema.TextLine(title=u"tags")
    attributes = schema.TextLine(title=u"attributes")


class IFilterTagsSchema(Interface):
    """HTML tag filtering configuration."""

    valid_tags = schema.List(
        title=u"Valid tags",
        default=XHTML_TAGS,
        value_type=schema.TextLine(),
        required=False)

    nasty_tags = schema.List(
        title=u"Nasty tags",
        default=[u"applet", u"embed", u"object", u"script"],
        value_type=schema.TextLine(),
        required=False)

    stripped_tags = schema.List(
        title=u"Stripped tags",
        default=[u"font"],
        value_type=schema.TextLine(),
        required=False)

    custom_tags = schema.List(
        title=u"Custom tags",
        default=[],
        value_type=schema.TextLine(),
        required=False)


class IFilterAttributesSchema(Interface):
    """HTML attribute filtering configuration."""

    stripped_attributes = schema.List(
        title=u"Stripped attributes",
        default=(u"dir lang valign halign border frame rules cellspacing "
                 u"cellpadding bgcolor").split(),
        value_type=schema.TextLine(),
        required=False)

    stripped_combinations = schema.List(
        title=u"Stripped combinations",
        default=[],
        value_type=schema.TextLine(),
        required=False)

    custom_attributes = schema.List(
        title=u"Custom attributes",
        default=[],
        value_type=schema.TextLine(),
        required=False)


class IFilterEditorSchema(Interface):
    """HTML editor filtering configuration."""

    style_whitelist = schema.List(
        title=u"Permitted properties",
        default=u"text-align list-style-type float text-decoration".split(),
        value_type=schema.TextLine(),
        required=False)

    class_blacklist = schema.List(
        title=u"Filtered classes",
        default=[],
        value_type=schema.TextLine(),
        required=False)


class IFilterSchema(IFilterTagsSchema, IFilterAttributesSchema,
                    IFilterEditorSchema):
    """BBB subset used by PortalTransforms safe_html under Python 3."""

    disable_filtering = schema.Bool(
        title=u"Disable filtering",
        default=False,
        required=False)


class IMarkupSchema(Interface):
    """Marker interface for markup configuration."""


class IEditingSchema(Interface):
    """BBB subset used by newer plone.locking during import/ZCML setup."""

    lock_on_ttw_edit = schema.Bool(
        title=u"Lock on through-the-web edit",
        default=True,
        required=False,
    )


class INavigationSchema(Interface):
    """BBB subset used by newer Plone support packages."""

    navigation_depth = schema.Int(
        title=u"Navigation depth",
        default=3,
        required=True,
    )
    generate_tabs = schema.Bool(
        title=u"Automatically generate tabs",
        default=True,
        required=False,
    )
    nonfolderish_tabs = schema.Bool(
        title=u"Generate tabs for items other than folders",
        default=True,
        required=False,
    )
    sort_tabs_on = schema.Choice(
        title=u"Sort tabs on",
        default=u"getObjPositionInParent",
        values=(u"getObjPositionInParent", u"sortable_title", u"getId"),
        required=True,
    )
    sort_tabs_reversed = schema.Bool(
        title=u"Reversed sort order for tabs",
        default=False,
        required=False,
    )
    displayed_types = schema.Tuple(
        title=u"Displayed content types",
        default=(
            u"Image", u"File", u"Link", u"News Item", u"Folder",
            u"Document", u"Event",
        ),
        missing_value=(),
        required=False,
        value_type=schema.TextLine(),
    )
    filter_on_workflow = schema.Bool(
        title=u"Filter on workflow state",
        default=False,
        required=False,
    )
    workflow_states_to_show = schema.Tuple(
        default=(),
        missing_value=(),
        required=False,
        value_type=schema.TextLine(),
    )
    show_excluded_items = schema.Bool(
        title=u"Show excluded items",
        default=True,
        required=False,
    )
    root = schema.TextLine(
        title=u"Root",
        default=u"/",
        required=True,
    )
    sitemap_depth = schema.Int(
        title=u"Sitemap depth",
        default=3,
        required=True,
    )
    parent_types_not_to_query = schema.List(
        title=u"Hide children of these types",
        default=[u"TempFolder"],
        missing_value=(),
        required=False,
        value_type=schema.TextLine(),
    )


class ILanguage(Interface):
    """BBB content language interface used by newer support packages."""

    def get_language():
        """Return the content language."""

    def set_language():
        """Set the content language."""


import zope.deferredimport

zope.deferredimport.deprecated(
    "It has been moved to Products.CMFDynamicViewFTI.interfaces. "
    "This alias will be removed in Plone 5.0",
    IBrowserDefault='Products.CMFDynamicViewFTI.interfaces:IBrowserDefault',
)

zope.deferredimport.deprecated(
    "It has been moved to Products.CMFDynamicViewFTI.interfaces. "
    "This alias will be removed in Plone 5.0",
    IDynamicViewTypeInformation='Products.CMFDynamicViewFTI.interfaces:IDynamicViewTypeInformation',
)

zope.deferredimport.deprecated(
    "It has been moved to Products.CMFDynamicViewFTI.interfaces. "
    "This alias will be removed in Plone 5.0",
    ISelectableBrowserDefault='Products.CMFDynamicViewFTI.interfaces:ISelectableBrowserDefault',
)
