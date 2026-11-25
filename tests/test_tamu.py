import unittest
from models.tamu import Tamu, InvalidNIKError, InvalidNamaError, InvalidNoTelpError

class TestTamu(unittest.TestCase):
    def setUp(self):
        self.tamu = Tamu("1234567890123456", "Budi Santoso", "081234567890")

    def test_inisialisasi_tamu(self):
        self.assertEqual(self.tamu.nik, "1234567890123456")
        self.assertEqual(self.tamu.nama, "Budi Santoso")
        self.assertEqual(self.tamu.no_telp, "081234567890")

    def test_nik_tidak_valid(self):
        with self.assertRaises(InvalidNIKError):
            Tamu("12345", "Budi Santoso", "081234567890")

    def test_setter_nama_valid(self):
        self.tamu.nama = "Andi Wijaya"
        self.assertEqual(self.tamu.nama, "Andi Wijaya")

    def test_setter_nama_memicu_exception(self):
        with self.assertRaises(InvalidNamaError):
            self.tamu.nama = ""

    def test_setter_no_telp_memicu_exception(self):
        with self.assertRaises(InvalidNoTelpError):
            self.tamu.no_telp = "abc123"

    def test_get_info_tamu(self):
        hasil_diharapkan = "Tamu: Budi Santoso | NIK: 1234567890123456 | Telp: 081234567890"
        self.assertEqual(self.tamu.get_info_tamu(), hasil_diharapkan)

if __name__ == '__main__':
    unittest.main()