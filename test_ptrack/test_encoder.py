from ptrack.encoder import PtrackEncoder


class TestPtrackEncoder:
    def test_encrypt_decrypt_roundtrip(self):
        encoded_data = PtrackEncoder.encrypt(my_data="hello")
        assert isinstance(encoded_data, str)
        assert PtrackEncoder.decrypt(encoded_data) == [[], {"my_data": "hello"}]
