from django.test import TestCase
from reservations.forms import ReservationForm

class TestReservationForm(TestCase):
    # This is a test class for the ReservationForm

    def test_form_is_valid(self):
        # Test case to check if the form is valid with correct data
        form_data = {
            # Valid inputs for test
            'reservation_name': 'Test User',
            'date': '2024-12-01',
            'time': '18:00',
            'number_of_guests': 2
        }

        # Fill the ReservationForm with the form_data
        reservation_form = ReservationForm(form_data)
        # Check if the form is valid with the provided data
        self.assertTrue(reservation_form.is_valid(), msg="Form is invalid")
