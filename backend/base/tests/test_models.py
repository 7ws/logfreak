from django.core.exceptions import ValidationError
import pytest

from backend.base.models import ContactPhone


class TestContactPhone:

    """Tests for the ContactPhone model
    """

    def test_contact_phone_msisdn_raises_when_invalid_number(self):
        """ContactPhone MSISDN raises ValidationError if number is invalid
        """
        phone = ContactPhone(msisdn='123NaN456')
        with pytest.raises(ValidationError) as exc:
            phone.clean_fields()
        assert 'msisdn' in exc.value.message_dict
