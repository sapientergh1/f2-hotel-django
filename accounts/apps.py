from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        # Wire up the signal handlers defined in models.py
        import accounts.models  # noqa: F401

        # Customise admin branding
        from django.contrib import admin
        admin.site.site_header  = '🏨 F2 Hotel Administration'
        admin.site.site_title   = 'F2 Hotel Admin'
        admin.site.index_title  = 'Hotel Management Dashboard'
