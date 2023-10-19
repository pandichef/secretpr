from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Service, Provider, Review

# from django.contrib.auth.models import Group
from django.contrib.admin import AdminSite


class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_display = ("name",)


class ProviderAdmin(admin.ModelAdmin):
    list_display = ("name", "service", "created_at", "updated_at")
    list_filter = ("service", "created_at", "updated_at")
    search_fields = ("name", "service")


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "provider",
        "service",
        "rating",
        # "created_at",
        "updated_at",
        "comments",
    )
    list_filter = ("rating", "created_at", "updated_at")
    search_fields = ("comments",)

    def service(self, obj):
        return obj.provider.service.name


# def has_view_permission(self, request) -> bool:
#     return request.user.is_authenticated

# def has_view_permission(self, request, obj=None):
#     return request.user.is_authenticated

# def has_module_permission(self, request) -> bool:
#     return request.user.is_authenticated


class CustomAdminSite(AdminSite):
    """https://books.agiliq.com/projects/django-admin-cookbook/en/latest/two_admin.html"""

    site_header = "Secret PR"
    site_title = ""
    index_title = "Membership Fee: $x per year (1101.01)"

    def get_app_list(self, request, app_label=None):
        """https://books.agiliq.com/projects/django-admin-cookbook/en/latest/set_ordering.html?highlight=order#how-to-set-ordering-of-apps-and-models-in-django-admin-dashboard"""
        ordering = {"Users": 1, "Services": 2, "Providers": 3, "Reviews": 4}
        app_dict = self._build_app_dict(request)
        app_list = sorted(app_dict.values(), key=lambda x: x["name"].lower())
        for app in app_list:
            app["models"].sort(key=lambda x: ordering[x["name"]])
        return app_list


custom_admin_site = CustomAdminSite()


# custom_admin_site.unregister(Group)
custom_admin_site.register(User, UserAdmin)
custom_admin_site.register(Provider, ProviderAdmin)
custom_admin_site.register(Service, ServiceAdmin)
custom_admin_site.register(Review, ReviewAdmin)
