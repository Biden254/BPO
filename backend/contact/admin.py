# Register your models here.
# contact/admin.py
from django.contrib import admin
from .models import ContactSubmission

class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at')
    list_filter = ('submitted_at',)
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('submitted_at',)
    ordering = ('-submitted_at',) # Display latest submissions first

admin.site.register(ContactSubmission, ContactSubmissionAdmin)