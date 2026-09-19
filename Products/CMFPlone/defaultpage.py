# -*- coding: utf-8 -*-
from Acquisition import aq_base
from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2Base
from Products.CMFCore.interfaces import IFolderish
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFDynamicViewFTI.interfaces import IBrowserDefault
from Products.CMFDynamicViewFTI.interfaces import IDynamicViewTypeInformation
from plone.registry.interfaces import IRegistry
from zope.component import queryAdapter
from zope.component import queryMultiAdapter
from zope.component import queryUtility


def get_default_page(context):
    """Return the configured default page id for a folderish object."""
    if not IFolderish.providedBy(context):
        return None

    ids = set()
    if isinstance(aq_base(context), BTreeFolder2Base):
        ids = context
    elif hasattr(aq_base(context), 'objectIds'):
        ids = set(context.objectIds())

    if 'index_html' in ids:
        return 'index_html'

    browser_default = context
    if not IBrowserDefault.providedBy(context):
        browser_default = queryAdapter(context, IBrowserDefault)

    if browser_default is not None:
        fti = context.getTypeInfo()
        if fti is not None:
            dynamic_fti = fti
            if not IDynamicViewTypeInformation.providedBy(fti):
                dynamic_fti = queryAdapter(fti, IDynamicViewTypeInformation)
            if dynamic_fti is not None:
                page = dynamic_fti.getDefaultPage(context, check_exists=True)
                if page is not None:
                    return page

    pages = getattr(aq_base(context), 'default_page', [])
    if isinstance(pages, str):
        pages = [pages]
    for page in pages:
        if page and page in ids:
            return page

    portal = queryUtility(ISiteRoot)
    if portal is not None:
        for page in pages:
            if portal.unrestrictedTraverse(page, None):
                return page

    registry = queryUtility(IRegistry)
    if registry is not None:
        for page in registry.get('plone.default_page', []):
            if page in ids:
                return page

    return None


def is_default_page(container, obj):
    """Return True when obj is the explicit default page of container."""
    parent_default_page = get_default_page(container)
    precondition = (
        parent_default_page is not None
        and '/' not in parent_default_page
        and hasattr(aq_base(obj), 'getId')
    )
    return precondition and parent_default_page == obj.getId()


def _getDefaultPageView(obj, request):
    view = queryMultiAdapter((obj, request), name='default_page')
    if view is None:
        from plone.app.layout.navigation.defaultpage import DefaultPage
        view = DefaultPage(obj, request)
    return view


def check_default_page_via_view(obj, request):
    container = aq_parent(aq_inner(obj))
    if container is None:
        return False
    view = _getDefaultPageView(container, request)
    return view.isDefaultPage(obj)


def get_default_page_via_view(obj, request):
    if not obj.isPrincipiaFolderish:
        return None
    view = _getDefaultPageView(obj, request)
    return view.getDefaultPage()
