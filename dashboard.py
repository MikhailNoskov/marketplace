"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'python_django_team5.dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'python_django_team5.dashboard.CustomAppIndexDashboard'
"""

try:
    # we use django.urls import as version detection as it will fail on django 1.11 and thus we are safe to use
    # gettext_lazy instead of ugettext_lazy instead
    from django.urls import reverse
    from django.utils.translation import gettext_lazy as _
except ImportError:
    from django.utils.translation import ugettext_lazy as _
from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard


class CustomPagesModule(modules.DashboardModule):
    title = _('Settings')
    template = 'admin/admin-setup-dashboard.html'

    def is_empty(self):
        return False

    def init_with_context(self, context):
        if self._initialized:
            return
        self._initialized = True


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard.
    """
    def init_with_context(self, context):
        # append an app list module for "Applications"
        self.children.append(modules.Group(
            display="tabs",
            children=[
                modules.AppList(
                    title=_('Administration'),
                    models=('django.contrib.*', 'allauth.*', 'profiles_app.*', 'taggit.*',),
                ),
                modules.AppList(
                    title=_('Applications'),
                    exclude=('django.contrib.*', 'allauth.*', 'profiles_app.*', 'taggit.*',),
                ),
                modules.AppList(
                    title=_('Settings'),
                    models=('dynamic_preferences.*',),
                    children=[CustomPagesModule()]),
            ]
        ))
        self.children.append(modules.RecentActions(_('Recent Actions'), 5))


class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard.
    """
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            ),

        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)
