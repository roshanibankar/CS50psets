from django.test import TestCase
from .models import ContactMessage, Service

class HRServicesTestCase(TestCase):
    def test_string_representation(self):
        instance = Service(name="HR Services Test", description="Some description")
        self.assertEqual(str(instance), "HR Services Test")  # Make sure Service has __str__

class ContactMessageModelTests(TestCase):
    def test_message_submission(self):
        message = ContactMessage.objects.create(
            name="John Doe",
            email="john@example.com",
            message="I have a question about your services."
        )
        self.assertEqual(message.name, "John Doe")
        self.assertIsNotNone(message.submitted_at)


