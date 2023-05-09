from datetime import datetime

from django.contrib import admin, messages

import Person
from .models import Event, participation_event


class participationNumber(admin.SimpleListFilter):
    title = 'Nombre participants'
    parameter_name = 'nbe_participant'

    def lookups(self, request, model_admin):
        return (
            ('0 participant', '0 participant'),
            ('plusieurs participant', 'plusieurs participant')
        )

    def queryset(self, request, queryset):
        if self.value() == '0 participant':
            return queryset.filter(nbe_participant__exact=0)
        if self.value() == 'plusieurs participant':
            return queryset.filter(nbe_participant__gt=0)


def set_true(ModelAdmin, request, queryset):
    req = queryset.update(state=True)
    if req == 1:
        message = "1 event was"
    else:
        message = f"{req} events were"
    messages.success(request, message == "%s successfully accepted" % message)


set_true.short_description = "Accept"


class UpcomingEvent(admin.SimpleListFilter):
    title = "Event Date"
    parameter_name = 'evt_date'

    def lookups(self, request, model_admin):
        return (
            ('Past Events', 'past'),
            ('Upcoming Events', 'upcoming'),
            ('Today Events', 'today')
        )

    def queryset(self, request, queryset):
        if self.value() == 'Past Events':
            return queryset.filter(evt_date__lt=datetime.today())
        if self.value() == 'Upcoming Events':
            return queryset.filter(evt_date__gt=datetime.today())
        if self.value() == 'Today Events':
            return queryset.filter(evt_date__exact=datetime.today())


class ParticipationAdmin(admin.TabularInline):
    model = participation_event
    extra = 1




class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'description', 'nbe_participant', 'state', 'image', 'evt_date', 'creation_date', 'updated_at',
        'organizer', 'evt_participation')

    def evt_participation(self, obj):
        count = obj.participation.count()
        return count

    ordering = ('title', 'updated_at')
    list_per_page = 10
    list_filter = ('state', UpcomingEvent, participationNumber)

    def set_false(self, request, queryset):
        req = queryset.filter(state=False)
        if req.count() > 0:
            messages.error(request, f"{req.count()} events are already marked refused")
        else:
            req = queryset.update(state=False)
            if req == 1:
                message = "1 event was "
            else:
                message = f"{req} event were"
            messages.success(request, message="%s sucessfully refused" % message)

    set_false.short_description = "Refused"

    actions = [set_true, set_false]
    fieldsets = (
        ('A propos', {'fields': ('title', 'description', 'image')}),
        ('Date', {'fields': ('evt_date', 'creation_date', 'updated_at')}),
        ('Others', {'fields': ('category', 'nbe_participant')}),
        ('Personal', {'fields': ('organizer',)})

    )
    readonly_fields = ['creation_date', 'updated_at']
    inlines = (ParticipationAdmin,)
    autocomplete_fields = ('organizer',)

admin.site.register(Event, EventAdmin)
# Register your models here.
