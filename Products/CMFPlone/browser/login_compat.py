from html import escape
from urllib import parse

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin
from Products.statusmessages.interfaces import IStatusMessage


LOGIN_TEMPLATE_IDS = set(
    "localhost logged_in login login_failed login_form login_password "
    "login_success logout logged_out registered mail_password mail_password_form "
    "register require_login member_search_results pwreset_finish".split()
)


class LegacyLoginFormView(BrowserView):
    """Small Zope 6 compatible replacement for the old login_form controller."""

    def __call__(self):
        self._set_no_cache_headers()
        if self.request.get("REQUEST_METHOD") == "POST":
            return self._handle_post()
        return self._render_form()

    def _set_no_cache_headers(self):
        response = self.request.response
        response.setHeader("Expires", "Sat, 1 Jan 2000 00:00:00 GMT")
        response.setHeader("Cache-Control", "max-age=0, must-revalidate, private")

    def _safe_came_from(self, came_from):
        if not came_from:
            return ""
        portal_url = getToolByName(self.context, "portal_url")
        if not portal_url.isURLInPortal(came_from):
            return ""
        path = parse.urlparse(came_from).path.split("/")
        if LOGIN_TEMPLATE_IDS.intersection(path):
            return ""
        return came_from

    def _get_came_from(self):
        return self._safe_came_from(
            self.request.get("came_from") or self.request.get("HTTP_REFERER")
        )

    def _authenticate(self, login, password):
        pas = getToolByName(self.context, "acl_users")
        credentials = {"login": login, "password": password}
        for _plugin_id, authenticator in pas.plugins.listPlugins(IAuthenticationPlugin):
            authenticated = authenticator.authenticateCredentials(credentials)
            if authenticated and authenticated[0]:
                return True
        return False

    def _posted_form(self):
        if self.request.form:
            return self.request.form
        environ = getattr(self.request, "environ", {})
        length = environ.get("CONTENT_LENGTH") or "0"
        try:
            length = int(length)
        except ValueError:
            length = 0
        if not length:
            return {}
        stream = environ.get("wsgi.input")
        if stream is None:
            return {}
        body = stream.read(length)
        values = parse.parse_qs(body.decode("utf-8", "replace"), keep_blank_values=True)
        return dict((key, value[-1] if value else "") for key, value in values.items())

    def _handle_post(self):
        form = self._posted_form()
        login = form.get("__ac_name", "") or form.get("login_name", "")
        password = form.get("__ac_password", "") or form.get("login_password", "")
        status = IStatusMessage(self.request)
        response = self.request.response

        if login and password and self._authenticate(login, password):
            pas = getToolByName(self.context, "acl_users")
            pas.updateCredentials(self.request, response, login, password)
            came_from = self._safe_came_from(form.get("came_from")) or self._get_came_from()
            return response.redirect(came_from or self.context.absolute_url())

        response.expireCookie("__ac", path="/")
        status.addStatusMessage(
            "Login failed. Both login name and password are case sensitive, "
            "check that caps lock is not enabled.",
            "error",
        )
        return self._render_form()

    def _render_form(self):
        came_from = escape(self._get_came_from(), quote=True)
        portal_url = escape(self.context.absolute_url(), quote=True)
        return """\
<!DOCTYPE html>
<html>
  <head>
    <title>Log in</title>
  </head>
  <body>
    <h1>Log in</h1>
    <form method="post" id="login_form" action="{portal_url}/login_form">
      <input type="hidden" name="came_from" value="{came_from}" />
      <input type="hidden" name="form.submitted" value="1" />
      <div>
        <label for="__ac_name">Login Name</label>
        <input type="text" name="__ac_name" id="__ac_name" />
      </div>
      <div>
        <label for="__ac_password">Password</label>
        <input type="password" name="__ac_password" id="__ac_password" />
      </div>
      <div>
        <input type="submit" name="submit" value="Log in" />
      </div>
    </form>
  </body>
</html>
""".format(portal_url=portal_url, came_from=came_from)
