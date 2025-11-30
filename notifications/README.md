# Notifications App

This app provides notification functionality for the DjangoBlog project.

## Features
- Comment reply notifications
- Unread notification count in navigation bar
- Notification list page with mark as read functionality
- Admin interface for managing notifications

## Installation
1. Add 'notifications' to INSTALLED_APPS in settings.py
2. Run migrations: python manage.py makemigrations notifications
3. Run migrate: python manage.py migrate notifications

## Usage
- Users will receive notifications when someone replies to their comments
- Unread notifications are displayed in the navigation bar
- Users can view all notifications at /notifications/
- Users can mark notifications as read individually or all at once
- Admins can manage notifications in the admin interface

## Models
- Notification: Stores notification details including recipient, sender, type, message, read status, and related object