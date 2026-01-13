from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils import timezone

# Register your models here.
from .models import Article, Category, Tag, Links, SideBar, BlogSettings


class ArticleForm(forms.ModelForm):
    # body = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = Article
        fields = '__all__'


def makr_article_publish(modeladmin, request, queryset):
    queryset.update(status='p')


def draft_article(modeladmin, request, queryset):
    queryset.update(status='d')


def close_article_commentstatus(modeladmin, request, queryset):
    queryset.update(comment_status='c')


def open_article_commentstatus(modeladmin, request, queryset):
    queryset.update(comment_status='o')


makr_article_publish.short_description = _('Publish selected articles')
draft_article.short_description = _('Draft selected articles')
close_article_commentstatus.short_description = _('Close article comments')
open_article_commentstatus.short_description = _('Open article comments')


class ArticlelAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ('body', 'title')
    form = ArticleForm
    list_display = (
        'id',
        'title',
        'author',
        'link_to_category',
        'creation_time',
        'views',
        'status',
        'type',
        'article_order')
    list_display_links = ('id', 'title')
    list_filter = ('status', 'type', 'category')
    date_hierarchy = 'creation_time'
    filter_horizontal = ('tags',)
    exclude = ('creation_time', 'last_mod_time')
    view_on_site = True
    actions = [
        makr_article_publish,
        draft_article,
        close_article_commentstatus,
        open_article_commentstatus]
    raw_id_fields = ('author', 'category',)

    def link_to_category(self, obj):
        info = (obj.category._meta.app_label, obj.category._meta.model_name)
        link = reverse('admin:%s_%s_change' % info, args=(obj.category.id,))
        return format_html(u'<a href="%s">%s</a>' % (link, obj.category.name))

    link_to_category.short_description = _('category')

    def get_form(self, request, obj=None, **kwargs):
        form = super(ArticlelAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['author'].queryset = get_user_model(
        ).objects.filter(is_superuser=True)
        return form

    def save_model(self, request, obj, form, change):
        # 将request传递给save方法，以便获取当前用户
        obj.save(request=request)
        # 不需要调用super，因为我们已经在obj.save中保存了

    def get_view_on_site_url(self, obj=None):
        if obj:
            url = obj.get_full_url()
            return url
        else:
            from djangoblog.utils import get_current_site
            site = get_current_site().domain
            return site


class ArticleVersionAdmin(admin.ModelAdmin):
    list_display = ('article', 'version_number', 'title', 'author', 'creation_time', 'is_current', 'change_type', 'restore_button', 'compare_select')
    list_filter = ('article', 'author', 'creation_time', 'change_type', 'is_current')
    search_fields = ('article__title', 'title', 'author__username', 'edit_summary')
    readonly_fields = ('article', 'version_number', 'title', 'body', 'author', 'creation_time', 'change_type', 'is_current', 'view_diff')
    ordering = ('-version_number',)
    actions = ['compare_selected_versions']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def restore_button(self, obj):
        return format_html('<a class="button" href="%s">恢复此版本</a>' 
                          % reverse('admin:restore_version', args=[obj.pk]))
    restore_button.short_description = '恢复操作'
    
    def compare_select(self, obj):
        return format_html('<input type="checkbox" name="version_ids" value="%s" />' % obj.pk)
    compare_select.short_description = '选择对比'
    
    def view_diff(self, obj):
        if obj.version_number > 1:
            prev_version = obj.article.versions.filter(version_number=obj.version_number - 1).first()
            if prev_version:
                return format_html('<a class="button" href="%s?version1=%s&version2=%s">与上一版本对比</a>' 
                                  % (reverse('admin:compare_versions'), prev_version.pk, obj.pk))
        return '无历史版本'
    view_diff.short_description = '版本对比'
    
    def compare_selected_versions(self, request, queryset):
        if len(queryset) != 2:
            self.message_user(request, '请选择恰好两个版本进行对比', level=messages.ERROR)
            return
        version1, version2 = queryset
        return redirect('%s?version1=%s&version2=%s' % (reverse('admin:compare_versions'), version1.pk, version2.pk))
    compare_selected_versions.short_description = '对比选中的两个版本'


class TagAdmin(admin.ModelAdmin):
    exclude = ('slug', 'last_mod_time', 'creation_time')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_category', 'index')
    exclude = ('slug', 'last_mod_time', 'creation_time')


class LinksAdmin(admin.ModelAdmin):
    exclude = ('last_mod_time', 'creation_time')


class SideBarAdmin(admin.ModelAdmin):
    list_display = ('name', 'content', 'is_enable', 'sequence')
    exclude = ('last_mod_time', 'creation_time')


class BlogSettingsAdmin(admin.ModelAdmin):
    pass


def restore_version(request, version_id):
    version = get_object_or_404(ArticleVersion, pk=version_id)
    article = version.article
    
    # 获取最新版本号
    latest_version = article.versions.order_by('-version_number').first()
    new_version_number = latest_version.version_number + 1 if latest_version else 1
    
    # 创建新版本
    restored_version = ArticleVersion.objects.create(
        article=article,
        version_number=new_version_number,
        title=version.title,
        body=version.body,
        author=request.user,
        creation_time=timezone.now(),
        change_type='rollback',
        edit_summary=f'恢复到版本 {version.version_number}',
        is_current=True
    )
    
    # 将其他版本标记为非当前版本
    ArticleVersion.objects.filter(article=article).exclude(version_number=new_version_number).update(is_current=False)
    
    # 更新文章内容
    article.title = version.title
    article.body = version.body
    article.save()
    
    messages.success(request, f'成功恢复到版本 {version.version_number}，并创建了新版本 {new_version_number}')
    return redirect(reverse('admin:blog_articleversion_changelist'))


def compare_versions(request):
    version1_id = request.GET.get('version1')
    version2_id = request.GET.get('version2')
    
    if not version1_id or not version2_id:
        messages.error(request, '请选择两个版本进行对比')
        return redirect(reverse('admin:blog_articleversion_changelist'))
    
    version1 = get_object_or_404(ArticleVersion, pk=version1_id)
    version2 = get_object_or_404(ArticleVersion, pk=version2_id)
    
    if version1.article != version2.article:
        messages.error(request, '只能对比同一篇文章的不同版本')
        return redirect(reverse('admin:blog_articleversion_changelist'))
    
    # 确保version1是较旧的版本，version2是较新的版本
    if version1.version_number > version2.version_number:
        version1, version2 = version2, version1
    
    # 比较标题差异
    title_diff = []
    if version1.title != version2.title:
        from difflib import Differ
        d = Differ()
        title_diff = list(d.compare(version1.title.splitlines(), version2.title.splitlines()))
    
    # 比较正文差异
    body_diff = []
    if version1.body != version2.body:
        from difflib import Differ
        d = Differ()
        body_diff = list(d.compare(version1.body.splitlines(), version2.body.splitlines()))
    
    return render(request, 'admin/compare_versions.html', {
        'version1': version1,
        'version2': version2,
        'title_diff': title_diff,
        'body_diff': body_diff,
        'title': f'版本对比: {version1.article.title}',
        'opts': ArticleVersion._meta,
        'site_header': admin.site.site_header,
        'site_title': admin.site.site_title,
    })


from .models import ArticleVersion
admin.site.register(Article, ArticlelAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Links, LinksAdmin)
admin.site.register(SideBar, SideBarAdmin)
admin.site.register(BlogSettings, BlogSettingsAdmin)
admin.site.register(ArticleVersion, ArticleVersionAdmin)

# 注册自定义admin URL
from django.urls import path

def get_admin_urls(urls):
    def get_urls():
        my_urls = [
            path('articleversion/restore/<int:version_id>/', restore_version, name='restore_version'),
            path('articleversion/compare/', compare_versions, name='compare_versions'),
        ]
        return my_urls + urls
    return get_urls

admin_urls = admin.site.get_urls()
admin.site.get_urls = get_admin_urls(admin_urls)
