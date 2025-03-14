from django.db import models
from utils.model_validators import validate_png
from utils.images import resize_image
from utils.slug_rand import slugify_new
from django.contrib.auth.models import User
from django_summernote.models import AbstractAttachment
from django.urls import reverse




# Criação do Manager para filtrar e ordenar os posts
class PostManager(models.Manager):
    def get_published(self):
        return self.filter(is_published=True).order_by('-pk')


# Model para redimenssionar as imagens do Post
class PostAttachment(AbstractAttachment):
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name

        current_file_name = str(self.file.name)
        super_save = super().save(*args, **kwargs)
        file_changed = False

        if self.file:
            file_changed = current_file_name != self.file.name

        if file_changed:
            resize_image(self.file, 900, True, 70)

        return super_save


# Model para configurações do site
class MenuLink(models.Model):
    class Meta:
        verbose_name = 'Menu Link'
        verbose_name_plural = 'Menu Links'

    text = models.CharField(max_length=50, verbose_name='Texto')
    url_or_path = models.CharField(max_length=2048, verbose_name='Link')
    new_tab = models.BooleanField(default=False)
    site_setup = models.ForeignKey('SiteSetup', on_delete=models.CASCADE, blank=True, null=True, default=None)

    def __str__(self):
        return self.text
    

# Model para configuração do site
class SiteSetup(models.Model):
    class Meta:
        verbose_name = 'Setup'
        verbose_name_plural = 'Setup'

    title = models.CharField(max_length=64, verbose_name='Título')
    description = models.CharField(blank=True, max_length=255, verbose_name='Descrição')
    show_header = models.BooleanField(default=True, verbose_name='Mostrar header')
    show_search = models.BooleanField(default=True, verbose_name='Mostrar busca')
    show_menu = models.BooleanField(default=True, verbose_name='Mostrar menu')
    show_description = models.BooleanField(default=True, verbose_name='Mostrar descrição')
    show_pagination = models.BooleanField(default=True, verbose_name='Mostrar paginação')
    show_footer = models.BooleanField(default=True, verbose_name='Mostrar footer')
    favicon = models.ImageField(upload_to='favicon/', blank=True, default='', validators=[validate_png], verbose_name='Favicon')

    def save(self, *args, **kwargs):
        current_favicon_name = str(self.favicon.name)
        super().save(*args, **kwargs)
        favicon_changed = False

        if self.favicon:
            favicon_changed = current_favicon_name != self.favicon.name

        if favicon_changed:
            resize_image(self.favicon, 32, True, 100)


    def __str__(self):
        return self.title
    

# Model para criação das Tags
class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    name = models.CharField(max_length=255, verbose_name='Nome')
    slug = models.SlugField(unique=True, default=None, null=True, blank=True, max_length=255)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name, 5)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    

# Model para criação das categorias
class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=255, verbose_name='Nome')
    slug = models.SlugField(unique=True, default=None, null=True, blank=True, max_length=255)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name, 5)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    

# Model para criação de Page
class Page(models.Model):
    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    title = models.CharField(max_length=255, verbose_name='Título')
    slug = models.SlugField(unique=True, default='', null=False, blank=True, max_length=255)
    is_published = models.BooleanField(default=False, verbose_name='Publicar', help_text='Precisa estar marcado para a página ser exibida.')
    content = models.TextField(verbose_name='Conteúdo')

    def get_absolute_url(self):
        if self.is_published:
            return reverse('blog:page', args=(self.slug,))
        return reverse('blog:index')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title, 5)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    

# Model para Post
class Post(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    objects = PostManager()

    title = models.CharField(max_length=255, verbose_name='Título')
    slug = models.SlugField(unique=True, default='', null=False, blank=True, max_length=255)
    excerpt = models.CharField(max_length=255, verbose_name='Resumo')
    is_published = models.BooleanField(default=False, verbose_name='Publicar', help_text='Precisa estar marcado para a página ser exibida.')
    content = models.TextField(verbose_name='Conteúdo')
    cover = models.ImageField(upload_to='posts', blank=True, default='', verbose_name='Imagem da capa')
    cover_in_post = models.BooleanField(default=True, help_text='Exibe a imagem da capa no conteúdo do post.', verbose_name='Imagem no post')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    created_by = models.ForeignKey(User, blank=True, null=True, related_name='post_created_by', on_delete=models.SET_NULL, verbose_name='Criado por')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    updated_by = models.ForeignKey(User, blank=True, null=True, related_name='post_updated_by', on_delete=models.SET_NULL, verbose_name='Atualizado por')
    category = models.ForeignKey(Category, blank=True, default=None, null=True, on_delete=models.SET_NULL, verbose_name='Categoria')
    tags = models.ManyToManyField(Tag, blank=True, default='')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        if self.is_published:
            return reverse('blog:post', args=(self.slug,))
        return reverse('blog:index')
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title, 5)

        current_cover_name = str(self.cover.name)
        super_save = super().save(*args, **kwargs)
        cover_changed = False

        if self.cover:
            cover_changed = current_cover_name != self.cover.name

        if cover_changed:
            resize_image(self.cover, 900, True, 75)
            
        return super_save