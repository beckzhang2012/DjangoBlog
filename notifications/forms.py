from django import forms
from accounts.models import BlogUser
from .models import Notification


User = BlogUser

class SystemNotificationForm(forms.Form):
    recipient = forms.ModelChoiceField(
        queryset=BlogUser.objects.all(),
        required=False,
        help_text='Leave blank to send to all users'
    )
    title = forms.CharField(max_length=200)
    content = forms.CharField(widget=forms.Textarea)
    
    def save(self):
        recipient = self.cleaned_data['recipient']
        title = self.cleaned_data['title']
        content = self.cleaned_data['content']
        
        if recipient:
            # Send to specific user
            Notification.objects.create(
                recipient=recipient,
                notification_type='system',
                title=title,
                content=content
            )
        else:
            # Send to all users
            for user in BlogUser.objects.all():
                Notification.objects.create(
                    recipient=user,
                    notification_type='system',
                    title=title,
                    content=content
                )