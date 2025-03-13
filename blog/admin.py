from django.contrib import admin
from blog.models import *
from django_summernote.admin import SummernoteModelAdmin




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

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    list_display_links = ('name',)
    search_fields = ('name', 'slug',)
    list_per_page = 10
    ordering = ('name',)
    prepopulated_fields = {'slug': ('name',),}

@admin.register(Page)
class PageAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ('id', 'title', 'slug', 'is_published',)
    list_display_links = ('title',)
    list_per_page = 10
    list_editable = ('is_published',)
    search_fields = ('title', 'slug',)
    ordering = ('title',)
    prepopulated_fields = {'slug': ('title',),}

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ('id', 'title', 'category', 'created_by', 'is_published',)
    list_display_links = ('title',)
    list_editable = ('is_published',)
    list_filter = ('category', 'is_published')
    list_per_page = 10
    search_fields = ('category', 'content', 'title', 'slug',)
    ordering = ('title',)
    prepopulated_fields = {'slug': ('title',),}
    readonly_fields = ('created_at', 'created_by', 'updated_at', 'updated_by',)
    autocomplete_fields = ('tags', 'category',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        obj.save()