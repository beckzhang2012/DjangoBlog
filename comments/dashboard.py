from django.contrib import admin
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from .models import Comment, AuditStatus, CommentAuditHistory


def get_audit_stats():
    """Get audit statistics data"""
    total_comments = Comment.objects.count()
    
    # Status counts
    status_counts = Comment.objects.values('audit_status').annotate(count=Count('id')).order_by()
    
    pending_count = next((item['count'] for item in status_counts if item['audit_status'] == AuditStatus.PENDING), 0)
    approved_count = next((item['count'] for item in status_counts if item['audit_status'] == AuditStatus.APPROVED), 0)
    rejected_count = next((item['count'] for item in status_counts if item['audit_status'] == AuditStatus.REJECTED), 0)
    need_mod_count = next((item['count'] for item in status_counts if item['audit_status'] == AuditStatus.NEED_MODIFICATION), 0)
    
    # Calculate pass rate
    reviewed_count = approved_count + rejected_count + need_mod_count
    pass_rate = (approved_count / reviewed_count * 100) if reviewed_count > 0 else 0
    
    # Audit history stats
    total_audits = CommentAuditHistory.objects.count()
    
    return {
        'total_comments': total_comments,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
        'need_mod_count': need_mod_count,
        'reviewed_count': reviewed_count,
        'pass_rate': round(pass_rate, 2),
        'total_audits': total_audits
    }


class CommentAuditDashboard(admin.ModelAdmin):
    """Custom dashboard for comment audit statistics"""
    change_list_template = 'admin/comment_audit_dashboard.html'
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context.update(get_audit_stats())
        return super().changelist_view(request, extra_context)

    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False