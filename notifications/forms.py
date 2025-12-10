from django import forms
from django.utils.translation import gettext_lazy as _
from accounts.models import BlogUser


class SystemNotificationForm(forms.Form):
    recipient_choice = forms.ChoiceField(
        label=_('接收者'),
        choices=[
            ('all', _('所有用户')),
            ('specific', _('特定用户'))
        ],
        widget=forms.RadioSelect
    )
    recipients = forms.ModelMultipleChoiceField(
        label=_('选择用户'),
        queryset=BlogUser.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'size': 10})
    )
    title = forms.CharField(label=_('通知标题'), max_length=200)
    content = forms.CharField(label=_('通知内容'), widget=forms.Textarea(attrs={'rows': 5}))
    url = forms.URLField(label=_('跳转链接'), required=False, help_text=_('可选，点击通知后跳转的链接'))

    def clean(self):
        cleaned_data = super().clean()
        recipient_choice = cleaned_data.get('recipient_choice')
        recipients = cleaned_data.get('recipients')
        
        if recipient_choice == 'specific' and not recipients:
            raise forms.ValidationError(_('请选择接收用户'))
        
        return cleaned_data