from django.contrib import admin
from .models import Job, Application, BlogPost, Service, Testimonial, ContactMessage, NewsletterSignup

class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'posted_on', 'is_active')
    list_filter = ('is_active', 'posted_on', 'location')
    search_fields = ('title', 'description')
admin.site.register(Job, JobAdmin)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'job', 'submitted_on']
    list_filter = ['job']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'submitted_at']

# Register the rest normally
admin.site.register(BlogPost)
admin.site.register(Service)
admin.site.register(Testimonial)
admin.site.register(NewsletterSignup)
