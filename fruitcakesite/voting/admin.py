from voting.models import Poll, Choice
from django.contrib import admin

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

#admin.site.register(Poll)
class PollAdmin(admin.ModelAdmin):
#    fields = ['pub_date', 'question']
    fieldsets = [
            (None,                  {'fields': ['question']}),
            ('Date information',    {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question', 'pub_date', 'was_published_recently',)
    list_filter = ['pub_date']
    search_fields = ['question']
    date_hierarchy = 'pub_date'

admin.site.register(Poll, PollAdmin)

#admin.site.register(Choice)


