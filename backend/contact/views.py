from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import ContactSubmission
from .serializers import ContactSubmissionSerializer
from django.core.mail import send_mail

# contact/views.py
class ContactSubmissionCreateView(generics.CreateAPIView):
    queryset = ContactSubmission.objects.all()
    serializer_class = ContactSubmissionSerializer
    permission_classes = [AllowAny] # Allow unauthenticated users to submit

    def perform_create(self, serializer):
        # Save the submission
        submission = serializer.save()

        # Send email notification
        send_mail(
            subject=f"New Contact Submission: {submission.subject}",
            message=f"Name: {submission.name}\nEmail: {submission.email}\nMessage: {submission.message}",
            from_email='nftbpo@gmail.com',  # Replace with your email
            recipient_list=['your_email@example.com'],  # Replace with the recipient's email
            fail_silently=False,
        )