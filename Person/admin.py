from django.contrib import admin
from .models import Person


class DisplayActiveUser(admin.SimpleListFilter):
    title = "Peronne actifs"
    parameter_name = "is_active"

    def lookups(self, request, model_admin):
        return (
            ('active', 'active'),
            ('non active', 'non active')
        )

    def queryset(self, request, queryset):
        if self.value() == 'active':
            return queryset.filter(is_active__exact=True)
        if self.value() == 'non active':
            return queryset.filter(is_active__exact=False)


class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username', 'email', 'cin', 'is_active', 'is_staff', 'date_joined')
    ordering = ('date_joined',)
    list_filter = (DisplayActiveUser,)
    search_fields = ('first_name', 'last_name', 'username', 'email', 'cin')
    list_per_page = 10


admin.site.register(Person, PersonAdmin)

# Register your models here.
