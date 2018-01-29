from django.contrib import admin
from .models import Tool, User, BusinessTag, DependencyTag, Update, Feedback

def merge_businesstags(modeladmin, request, tag_queryset):
    primary_tag = tag_queryset[0]
    if len(tag_queryset) > 1:
        for tag in tag_queryset[1:]:
            for tool in tag.tools.all():
                tool.business_tags.remove(tag)
                print(primary_tag)
                print(tool.business_tags.all())
                if not primary_tag in tool.business_tags.all():
                    tool.business_tags.add(primary_tag)
                tool.save()
            tag.delete()

merge_businesstags.short_description = "Merge tags"

class BusinessTagAdmin(admin.ModelAdmin):
    actions = [merge_businesstags]


def merge_dependencytags(modeladmin, request, tag_queryset):
    primary_tag = tag_queryset[0]
    if len(tag_queryset) > 1:
        for tag in tag_queryset[1:]:
            for tool in tag.tools.all():
                tool.dependency_tags.remove(tag)
                print(primary_tag)
                print(tool.dependency_tags.all())
                if not primary_tag in tool.dependency_tags.all():
                    tool.dependency_tags.add(primary_tag)
                tool.save()
            tag.delete()

merge_dependencytags.short_description = "Merge tags"

class DependencyTagAdmin(admin.ModelAdmin):
    actions = [merge_dependencytags]


class ShowDateAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)

admin.site.register(Tool)
admin.site.register(User)
admin.site.register(BusinessTag, BusinessTagAdmin)
admin.site.register(DependencyTag, DependencyTagAdmin)
admin.site.register(Update)
admin.site.register(Feedback, ShowDateAdmin)
