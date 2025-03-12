from django.contrib import admin
from blog.models import MenuLink, SiteSetup, Tag




class MenuLinkInline(admin.TabularInline):
    model = MenuLink
    extra = 1

@admin.register(SiteSetup)
class SiteSetupAdmin(admin.ModelAdmin):
    list_display = ('title', 'description',)
    inlines = (MenuLinkInline,)
    
    def has_add_permission(self, request):
        return not SiteSetup.objects.exists()
    
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    list_display_links = ('name',)
    search_fields = ('name', 'slug',)
    list_per_page = 10
    ordering = ('name',)
    prepopulated_fields = {'slug': ('name',),}