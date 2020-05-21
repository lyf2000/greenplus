import datetime
import os

from django import forms
from django.contrib import admin

# Register your models here.


# from django.contrib.gis.db import models
# from mapwidgets.widgets import GooglePointFieldWidget


# class CityAdmin(admin.ModelAdmin):
#     formfield_overrides = {
#         models.PointField: {"widget": GooglePointFieldWidget}
#     }
from django.db.models import Count

from taggit.forms import TagField
from taggit_labels.widgets import LabelWidget

from blog.models import Post, Meet
from django.utils.safestring import mark_safe
from django.db import models


class PostForm(forms.ModelForm):
    tags = TagField(required=False, widget=LabelWidget)

    class Meta:
        model = Post
        exclude = []


class LastWeekMonthFilter(admin.SimpleListFilter):
    title = 'is_very_benevolent'

    parameter_name = 'is_very_benevolent'

    def lookups(self, request, model_admin):
        return (
            ('week', 'Week'),
            ('month', 'Month'),
        )

    def queryset(self, request, queryset):
        value = self.value()

        if value == 'week':
            return queryset.filter(created__gte=datetime.datetime.now() - datetime.timedelta(days=7))
        elif value == 'month':
            return queryset.filter(created__gte=datetime.datetime.now() - datetime.timedelta(days=30))
        return queryset


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'author', 'added_count', 'tags_display',)
    readonly_fields = ['main_img_image', 'created']

    list_filter = [LastWeekMonthFilter]
    form = PostForm

    fieldsets = (
        ('Standard info', {
            'fields': ('title', 'created', 'author', 'text', 'added',
                       ),
        }),
        ('Image info', {
            'fields': ('main_img', 'main_img_image',
                       ),
        }),
        ('Tags', {
            'fields': ('tags',
                       ),
        })
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        queryset = queryset.annotate(
            _added_count=Count("added", distinct=True),

        )
        return queryset

    def main_img_image(self, obj):
        return mark_safe(
            '<img src="{url}" width="{width}" height={height} />'
                .format(
                url=os.path.join('media/', obj.main_img.url),
                # width=obj.main_img.width,
                # height=obj.main_img.height,
                height=550,
                width=800,
            ))

    def added_count(self, obj):
        return obj._added_count

    added_count.admin_order_field = '_added_count'

    def tags_display(self, obj):
        return ", ".join([child.name for child in obj.tags.all()])

    tags_display.short_description = "Tags"


class MeetForm(forms.ModelForm):
    tags = TagField(required=False, widget=LabelWidget)

    class Meta:
        model = Meet
        exclude = []


@admin.register(Meet)
class MeetAdmin(admin.ModelAdmin):
    change_form_template = 'admin/meet_change_form.html'
    form = MeetForm
    filter_vertical = ['participants']

    readonly_fields = ('mapp',)

    fieldsets = (
        ('Participants info', {
            'fields': ('participants',
                       ),
            'classes': ['collapse']

        }),
        ('Meet Process', {
            'fields': ('meet_date',
                       ),
        }),
        ('Map info', {
            'fields': ('title', 'lat', 'lng', ('mapp'),
                       ),
        }),
        ('Tags', {
            'fields': ('tags',
                       ),
        }),

    )

    def mapp(self, obj):
        return mark_safe('<div id="map"></div>')

    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #     extra = extra_context or {}
    #     # extra['filter_form'] = FilterForm()
    #     return super(ProcessAdmin, self).change_view(request, object_id,
    #                                              form_url, extra_context=extra)
