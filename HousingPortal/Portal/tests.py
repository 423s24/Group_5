from django.test import TestCase
from django.utils import timezone
from .models import *

# Create your tests here.

class MaintenaceNotesTestCase(TestCase):
    def setUp(self):
        self.user = UserAccount.objects.create(username='testuser', password='Not4password')

        self.maintenance_request = MaintenanceRequest.objects.create(
            user_id=self.user,
            first_name="Test",
            last_name="User",
            phone="1234567890",
            unit='Test Unit',
            address="Test Address",
            date_submitted=timezone.now(),
            status='New',
            title='Test Request',
            request='Test request Description',
            entry_permission=False
        )

    def test_maintenance_note_creation(self):
        maintenance_notes = MaintenanceNotes.objects.create(
            maintenanceRequestId=self.maintenance_request,
            user_id=self.user,
            date_submitted=timezone.now(),
            tenant_viewable=True,
            notes='Test Note'
        )

        self.assertEqual(maintenance_notes.maintenanceRequestId, self.maintenance_request)
        self.assertEqual(maintenance_notes.user_id, self.user)
        self.assertTrue(maintenance_notes.tenant_viewable)
        self.assertEqual(maintenance_notes.notes, 'Test Note')

    def test_maintenance_note_default(self):
        maintenance_notes = MaintenanceNotes.objects.create(
            maintenanceRequestId=self.maintenance_request,
            user_id=self.user,
            date_submitted=timezone.now()
        )

        self.assertFalse(maintenance_notes.tenant_viewable)
        self.assertEqual(maintenance_notes.notes, '')