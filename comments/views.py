# Create your views here.
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.utils.translation import gettext_lazy as _

from accounts.models import BlogUser, Notification
from blog.models import Article
from .forms import CommentForm
from .models import Comment


class CommentPostView(FormView):
    form_class = CommentForm
    template_name = 'blog/article_detail.html'

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(CommentPostView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        article_id = self.kwargs['article_id']
        article = get_object_or_404(Article, pk=article_id)
        url = article.get_absolute_url()
        return HttpResponseRedirect(url + "#comments")

    def form_invalid(self, form):
        article_id = self.kwargs['article_id']
        article = get_object_or_404(Article, pk=article_id)

        return self.render_to_response({
            'form': form,
            'article': article
        })

    def form_valid(self, form):
        """提交的数据验证合法后的逻辑"""
        user = self.request.user
        author = BlogUser.objects.get(pk=user.pk)
        article_id = self.kwargs['article_id']
        article = get_object_or_404(Article, pk=article_id)

        if article.comment_status == 'c' or article.status == 'c':
            raise ValidationError("该文章评论已关闭.")
        comment = form.save(False)
        comment.article = article
        from djangoblog.utils import get_blog_setting
        settings = get_blog_setting()
        if not settings.comment_need_review:
            comment.is_enable = True
        comment.author = author

        if form.cleaned_data['parent_comment_id']:
            parent_comment = Comment.objects.get(
                pk=form.cleaned_data['parent_comment_id'])
            comment.parent_comment = parent_comment

        comment.save(True)
        
        # 发送评论回复通知
        if comment.parent_comment:
            parent_comment = comment.parent_comment
            if parent_comment.author != comment.author:  # 避免给自己发通知
                # 创建通知
                notification = Notification()
                notification.title = _('Comment Reply')
                notification.content = _('You have a comment reply from %(username)s: %(content)s' % {
                    'username': comment.author.username,
                    'content': comment.body[:50] + '...' if len(comment.body) > 50 else comment.body
                })
                notification.type = 'comment_reply'
                notification.user = parent_comment.author
                notification.related_object_id = article.pk
                notification.related_object_type = 'article'
                notification.save()
        
        return HttpResponseRedirect(
            "%s#div-comment-%d" %
            (article.get_absolute_url(), comment.pk))
