import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, Count
from django.utils.timezone import now

from comments.models import Comment
from blog.models import Article
from .models import ReviewHistory

logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class PendingReviewListView(ListView):
    """待审核内容列表视图"""
    template_name = 'servermanager/pending_review.html'
    context_object_name = 'items'
    paginate_by = 10
    
    def get_queryset(self):
        # 获取筛选条件
        review_type = self.request.GET.get('type', 'all')
        search_query = self.request.GET.get('q', '')
        
        # 构建基础查询
        comment_query = Comment.objects.filter(is_enable=False)
        article_query = Article.objects.filter(
            approval_status='pending',
            status='r'  # 只显示标记为待审核的文章
        )
        
        # 应用搜索过滤
        if search_query:
            comment_query = comment_query.filter(
                Q(body__icontains=search_query) | 
                Q(author__username__icontains=search_query) | 
                Q(article__title__icontains=search_query)
            )
            article_query = article_query.filter(
                Q(title__icontains=search_query) | 
                Q(author__username__icontains=search_query) | 
                Q(body__icontains=search_query)
            )
        
        # 根据类型筛选
        if review_type == 'comment':
            items = list(comment_query)
        elif review_type == 'article':
            items = list(article_query)
        else:  # all
            items = list(comment_query) + list(article_query)
        
        # 按创建时间排序
        items.sort(key=lambda x: x.creation_time, reverse=True)
        
        return items
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 添加筛选条件到上下文
        context['review_type'] = self.request.GET.get('type', 'all')
        context['search_query'] = self.request.GET.get('q', '')
        
        # 添加统计数据
        context['pending_comments_count'] = Comment.objects.filter(is_enable=False).count()
        context['pending_articles_count'] = Article.objects.filter(
            approval_status='pending',
            status='r'
        ).count()
        
        return context


@method_decorator(login_required, name='dispatch')
class ReviewHistoryListView(ListView):
    """审核历史记录视图"""
    model = ReviewHistory
    template_name = 'servermanager/review_history.html'
    context_object_name = 'history_records'
    paginate_by = 20
    
    def get_queryset(self):
        # 获取筛选条件
        review_type = self.request.GET.get('type', 'all')
        reviewer = self.request.GET.get('reviewer', '')
        start_date = self.request.GET.get('start_date', '')
        end_date = self.request.GET.get('end_date', '')
        
        # 构建基础查询
        queryset = ReviewHistory.objects.all()
        
        # 应用筛选条件
        if review_type != 'all':
            queryset = queryset.filter(review_type=review_type)
        
        if reviewer:
            queryset = queryset.filter(reviewer__username__icontains=reviewer)
        
        if start_date:
            queryset = queryset.filter(review_time__gte=start_date)
        
        if end_date:
            queryset = queryset.filter(review_time__lte=end_date)
        
        return queryset.order_by('-review_time')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 添加筛选条件到上下文
        context['review_type'] = self.request.GET.get('type', 'all')
        context['reviewer'] = self.request.GET.get('reviewer', '')
        context['start_date'] = self.request.GET.get('start_date', '')
        context['end_date'] = self.request.GET.get('end_date', '')
        
        return context


@login_required
def review_detail(request, content_type, object_id):
    """审核详情视图"""
    # 获取要审核的内容
    try:
        content_type_obj = ContentType.objects.get(model=content_type)
        content = content_type_obj.get_object_for_this_type(id=object_id)
    except:
        messages.error(request, '要审核的内容不存在')
        return redirect('servermanager:pending_review')
    
    if request.method == 'POST':
        # 处理审核操作
        result = request.POST.get('result')
        comment = request.POST.get('comment', '')
        
        # 验证结果
        if result not in ['approved', 'rejected', 'need_modification']:
            messages.error(request, '无效的审核结果')
            return redirect('servermanager:review_detail', content_type=content_type, object_id=object_id)
        
        # 更新内容状态
        if content_type == 'comment':
            if result == 'approved':
                content.is_enable = True
            content.save()
        elif content_type == 'article':
            content.approval_status = result
            content.approved_by = request.user
            content.approved_time = now()
            content.approval_comment = comment
            # 如果审核通过，发布文章
            if result == 'approved':
                content.status = 'p'
            content.save()
        
        # 记录审核历史
        ReviewHistory.objects.create(
            review_type=content_type,
            reviewer=request.user,
            result=result,
            comment=comment,
            content_type=content_type_obj,
            object_id=object_id
        )
        
        messages.success(request, '审核操作已完成')
        return redirect('servermanager:pending_review')
    
    # 获取审核历史记录（如果有）
    review_history = ReviewHistory.objects.filter(
        content_type=content_type_obj,
        object_id=object_id
    ).order_by('-review_time')
    
    context = {
        'content': content,
        'content_type': content_type,
        'review_history': review_history
    }
    
    return render(request, 'servermanager/review_detail.html', context)


@login_required  
def batch_review(request):
    """批量审核视图"""
    if request.method == 'POST':
        # 获取选中的项目
        item_ids = request.POST.getlist('item_ids')
        content_types = request.POST.getlist('content_types')
        result = request.POST.get('result')
        comment = request.POST.get('comment', '')
        
        if not item_ids or not content_types or result not in ['approved', 'rejected', 'need_modification']:
            messages.error(request, '批量审核参数无效')
            return redirect('servermanager:pending_review')
        
        # 处理批量审核
        success_count = 0
        for i in range(len(item_ids)):
            try:
                object_id = item_ids[i]
                content_type = content_types[i]
                
                content_type_obj = ContentType.objects.get(model=content_type)
                content = content_type_obj.get_object_for_this_type(id=object_id)
                
                # 更新内容状态
                if content_type == 'comment':
                    if result == 'approved':
                        content.is_enable = True
                    content.save()
                elif content_type == 'article':
                    content.approval_status = result
                    content.approved_by = request.user
                    content.approved_time = now()
                    content.approval_comment = comment
                    # 如果审核通过，发布文章
                    if result == 'approved':
                        content.status = 'p'
                    content.save()
                
                # 记录审核历史
                ReviewHistory.objects.create(
                    review_type=content_type,
                    reviewer=request.user,
                    result=result,
                    comment=comment,
                    content_type=content_type_obj,
                    object_id=object_id
                )
                
                success_count += 1
            except Exception as e:
                logger.error(f'批量审核出错: {e}')
                continue
        
        messages.success(request, f'批量审核完成，成功处理 {success_count} 条内容')
        return redirect('servermanager:pending_review')
    
    messages.error(request, '无效的请求方式')
    return redirect('servermanager:pending_review')


@login_required
def review_statistics(request):
    """审核统计视图"""
    # 计算待审核数量
    pending_comments = Comment.objects.filter(is_enable=False).count()
    pending_articles = Article.objects.filter(
        approval_status='pending',
        status='r'
    ).count()
    
    # 计算审核通过率
    total_approved_comments = ReviewHistory.objects.filter(
        review_type='comment',
        result='approved'
    ).count()
    total_reviewed_comments = ReviewHistory.objects.filter(
        review_type='comment'
    ).count()
    comment_approval_rate = 0
    if total_reviewed_comments > 0:
        comment_approval_rate = (total_approved_comments / total_reviewed_comments) * 100
    
    total_approved_articles = ReviewHistory.objects.filter(
        review_type='article',
        result='approved'
    ).count()
    total_reviewed_articles = ReviewHistory.objects.filter(
        review_type='article'
    ).count()
    article_approval_rate = 0
    if total_reviewed_articles > 0:
        article_approval_rate = (total_approved_articles / total_reviewed_articles) * 100
    
    # 计算今日审核数据
    today = now().date()
    today_approved_comments = ReviewHistory.objects.filter(
        review_type='comment',
        result='approved',
        review_time__date=today
    ).count()
    today_rejected_comments = ReviewHistory.objects.filter(
        review_type='comment',
        result='rejected',
        review_time__date=today
    ).count()
    today_need_modification_comments = ReviewHistory.objects.filter(
        review_type='comment',
        result='need_modification',
        review_time__date=today
    ).count()
    
    today_approved_articles = ReviewHistory.objects.filter(
        review_type='article',
        result='approved',
        review_time__date=today
    ).count()
    today_rejected_articles = ReviewHistory.objects.filter(
        review_type='article',
        result='rejected',
        review_time__date=today
    ).count()
    today_need_modification_articles = ReviewHistory.objects.filter(
        review_type='article',
        result='need_modification',
        review_time__date=today
    ).count()
    
    context = {
        # 待审核数量
        'pending_comments': pending_comments,
        'pending_articles': pending_articles,
        
        # 通过率
        'comment_approval_rate': round(comment_approval_rate, 2),
        'article_approval_rate': round(article_approval_rate, 2),
        
        # 今日数据
        'today_approved_comments': today_approved_comments,
        'today_rejected_comments': today_rejected_comments,
        'today_need_modification_comments': today_need_modification_comments,
        
        'today_approved_articles': today_approved_articles,
        'today_rejected_articles': today_rejected_articles,
        'today_need_modification_articles': today_need_modification_articles,
    }
    
    return render(request, 'servermanager/review_statistics.html', context)
