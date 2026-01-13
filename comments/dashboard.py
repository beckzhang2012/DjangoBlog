from django.contrib import admin
from django.db.models import Count, F
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from .models import AuditLog, AuditStatus, Comment
from blog.models import Article


class AuditDashboard:
    def __init__(self, request):
        self.request = request
        self.stats = self.get_audit_stats()
    
    def get_audit_stats(self):
        # 待审核总数
        pending_comments = Comment.objects.filter(audit_status=AuditStatus.PENDING).count()
        pending_articles = Article.objects.filter(audit_status=AuditStatus.PENDING).count()
        
        # 总审核数
        total_audited = AuditLog.objects.exclude(audit_status=AuditStatus.PENDING).count()
        approved = AuditLog.objects.filter(audit_status=AuditStatus.APPROVED).count()
        rejected = AuditLog.objects.filter(audit_status=AuditStatus.REJECTED).count()
        need_modification = AuditLog.objects.filter(audit_status=AuditStatus.NEED_MODIFICATION).count()
        
        # 通过率
        pass_rate = (approved / total_audited * 100) if total_audited > 0 else 0
        
        return {
            'pending_total': pending_comments + pending_articles,
            'pending_comments': pending_comments,
            'pending_articles': pending_articles,
            'total_audited': total_audited,
            'approved': approved,
            'rejected': rejected,
            'need_modification': need_modification,
            'pass_rate': round(pass_rate, 2)
        }
    
    def render(self):
        stats = self.stats
        
        return format_html('''
        <div class="dashboard-module">
            <h2>{audit_stats}</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 15px;">
                <div style="background: #f8f9fa; padding: 15px; border-radius: 4px; border-left: 4px solid #dc3545;">
                    <h3 style="margin-top: 0; margin-bottom: 10px;">{pending_review}</h3>
                    <p style="font-size: 24px; font-weight: bold; color: #dc3545;">{pending_total}</p>
                    <small>{comments}: {pending_comments} | {articles}: {pending_articles}</small>
                </div>
                <div style="background: #f8f9fa; padding: 15px; border-radius: 4px; border-left: 4px solid #28a745;">
                    <h3 style="margin-top: 0; margin-bottom: 10px;">{approved}</h3>
                    <p style="font-size: 24px; font-weight: bold; color: #28a745;">{approved_count}</p>
                </div>
                <div style="background: #f8f9fa; padding: 15px; border-radius: 4px; border-left: 4px solid #ffc107;">
                    <h3 style="margin-top: 0; margin-bottom: 10px;">{rejected}</h3>
                    <p style="font-size: 24px; font-weight: bold; color: #ffc107;">{rejected_count}</p>
                </div>
                <div style="background: #f8f9fa; padding: 15px; border-radius: 4px; border-left: 4px solid #17a2b8;">
                    <h3 style="margin-top: 0; margin-bottom: 10px;">{pass_rate}</h3>
                    <p style="font-size: 24px; font-weight: bold; color: #17a2b8;">{pass_rate_value}%</p>
                </div>
            </div>
            <div style="margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 4px;">
                <h3 style="margin-top: 0;">{quick_actions}</h3>
                <p>
                    <a href="/admin/comments/comment/?audit_status__exact=pending" class="button">{review_comments}</a>
                    <a href="/admin/blog/article/?audit_status__exact=pending" class="button">{review_articles}</a>
                    <a href="/admin/comments/auditlog/" class="button">{view_history}</a>
                </p>
            </div>
        </div>
        ''',
        audit_stats=_('Audit Statistics'),
        pending_review=_('Pending Review'),
        pending_total=stats['pending_total'],
        comments=_('Comments'),
        pending_comments=stats['pending_comments'],
        articles=_('Articles'),
        pending_articles=stats['pending_articles'],
        approved=_('Approved'),
        approved_count=stats['approved'],
        rejected=_('Rejected'),
        rejected_count=stats['rejected'],
        pass_rate=_('Pass Rate'),
        pass_rate_value=stats['pass_rate'],
        quick_actions=_('Quick Actions'),
        review_comments=_('Review Comments'),
        review_articles=_('Review Articles'),
        view_history=_('View Audit History')
        )


# 注册到admin dashboard
def audit_dashboard(request, **kwargs):
    return AuditDashboard(request).render()


try:
    admin.site.add_to_index('audit_dashboard', audit_dashboard)
except:
    pass