import uuid

from ptrack.encoder import PtrackEncoder


class TestPtrackEncoder:
    def test_encrypt_decrypt_roundtrip(self):
        encoded_data = PtrackEncoder.encrypt(my_data="hello")
        assert isinstance(encoded_data, str)
        assert PtrackEncoder.decrypt(encoded_data) == [[], {"my_data": "hello"}]
    
    def test_uuid(self):
        encoded_data = PtrackEncoder.encrypt(my_data=uuid.UUID(int=0))
        assert isinstance(encoded_data, str)
        assert PtrackEncoder.decrypt(encoded_data) == [[], {"my_data": "00000000-0000-0000-0000-000000000000"}]
