import unittest
import os
import sys

# Menambahkan root project ke sys.path agar folder 'models' terbaca dari mana saja
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.kamar import (
    Kamar,
    KamarError,
    KamarSudahAdaError,
    KamarPenuhError,
    KamarKosongError
)

class TestKamar(unittest.TestCase):
    def setUp(self):
        """Menyiapkan data uji sebelum setiap test method berjalan."""
        Kamar.reset_daftar_kamar()
        self.kamar = Kamar("101", "Deluxe", 500000)

    # 1. Test Inisialisasi Atribut Sesuai Rancangan Awal
    def test_01_inisialisasi_atribut(self):
        self.assertEqual(self.kamar.nomor_kamar, "101")
        self.assertEqual(self.kamar.tipe_kamar, "Deluxe")
        self.assertEqual(self.kamar.harga, 500000.0)
        self.assertEqual(self.kamar.status, "Tersedia")

    # 2. Test Method get_info_kamar()
    def test_02_get_info_kamar(self):
        info = self.kamar.get_info_kamar()
        self.assertIn("101", info)
        self.assertIn("Deluxe", info)
        self.assertIn("Rp500,000", info)
        self.assertIn("Tersedia", info)

    # 3. Test Enkapsulasi Setter Harga
    def test_03_setter_harga_valid(self):
        self.kamar.harga = 600000
        self.assertEqual(self.kamar.harga, 600000.0)
    def test_04_setter_harga_tidak_valid(self):
        with self.assertRaises(ValueError):
            self.kamar.harga = 0
        with self.assertRaises(ValueError):
            self.kamar.harga = -10000

    # 4. Test Method ubah_status() Berhasil
    def test_05_ubah_status_berhasil(self):
        self.kamar.ubah_status("Terisi")
        self.assertEqual(self.kamar.status, "Terisi")
        
        self.kamar.ubah_status("Tersedia")
        self.assertEqual(self.kamar.status, "Tersedia")

    # 5. Test Custom Exception pada ubah_status()
    def test_06_ubah_status_penuh_error(self):
        self.kamar.ubah_status("Terisi")

        # Mengubah jadi Terisi lagi harus melempar KamarPenuhError
        with self.assertRaises(KamarPenuhError):
            self.kamar.ubah_status("Terisi")

    def test_07_ubah_status_kosong_error(self):
        # Mengubah jadi Tersedia saat sudah Tersedia harus melempar KamarKosongError
        with self.assertRaises(KamarKosongError):
            self.kamar.ubah_status("Tersedia")

    def test_08_ubah_status_input_tidak_valid(self):
        # Input status selain Tersedia/Terisi
        with self.assertRaises(ValueError):
            self.kamar.ubah_status("Rusak")

    # 6. Test Operasi check_in dan check_out
    def test_09_check_in_dan_check_out(self):
        self.kamar.check_in()
        self.assertEqual(self.kamar.status, "Terisi")
        self.kamar.check_out()
        self.assertEqual(self.kamar.status, "Tersedia")

    # 7. Test Tambah Kamar & Validasi Duplikat (Custom Exception)
    def test_10_tambah_kamar_dan_duplikat_error(self):
        Kamar.tambah_kamar("102", "Standard", 350000)
        self.assertEqual(len(Kamar.daftar_kamar), 1)

        # Nomor 102 didaftarkan lagi -> harus KamarSudahAdaError
        with self.assertRaises(KamarSudahAdaError):
            Kamar.tambah_kamar("102", "Suite", 700000)

    # 8. Test Cari Kamar Kosong
    def test_11_cari_kamar_kosong(self):
        k1 = Kamar.tambah_kamar("201", "Suite", 750000)
        k2 = Kamar.tambah_kamar("202", "Suite", 750000)
        k1.ubah_status("Terisi")
        kamar_kosong = Kamar.cari_kamar_kosong()
        self.assertEqual(len(kamar_kosong), 1)
        self.assertEqual(kamar_kosong[0].nomor_kamar, "202")
        
if __name__ == "__main__":
    unittest.main()