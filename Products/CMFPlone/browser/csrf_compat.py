from Products.Five.browser import BrowserView
from plone.protect.utils import safeWrite


class MarkArchetypesDocumentReadSafe(BrowserView):
    """Mark legacy Archetypes render-time writes as safe for GET views."""

    def __call__(self):
        if self.request.get("REQUEST_METHOD") != "GET":
            return ""
        if getattr(self.context, "portal_type", None) != "Document":
            return ""

        safeWrite(self.context, self.request)
        for name in ("__annotations__", "_md"):
            value = getattr(self.context, name, None)
            if value is not None:
                safeWrite(value, self.request)
        return ""
