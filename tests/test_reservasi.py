import unittest
from datetime import date, datetime
from unittest.mock import Mock

from models.tamu import Tamu
from models.kamar import Kamar
from models.detail_reservasi import DetailReservasi, HargaKamarTidakValidError
from models.reservasi import (
    Reservasi,
    ReservasiError,
    TamuTidakValidError,
    TanggalTidakValidError,
    KamarTidakTersediaError,
    ReservasiKosongError,
)


class TestReservasi(unittest.TestCase):
    def setUp(self):
        self.tamu = Tamu("3326010101010001", "Buang Santoso", "081234567890")
        self.check_in = date(2026, 11, 20)
        self.check_out = date(2026, 11, 22)
        self.k1 = Kamar("101", "Deluxe", 500000)
        self.k2 = Kamar("202", "Suite", 1200000)
        self.reservasi = Reservasi("RSV-001", self.tamu, self.check_in, self.check_out)

    def test_atribut_awal(self):
        self.assertEqual(self.reservasi.id_reservasi, "RSV-001")
        self.assertIs(self.reservasi.tamu, self.tamu)
        self.assertEqual(self.reservasi.tgl_check_in, self.check_in)
        self.assertEqual(self.reservasi.tgl_check_out, self.check_out)
        self.assertEqual(self.reservasi.daftar_detail, [])

    def test_tamu_tidak_valid(self):
        for tamu in ("bukan objek tamu", None):
            with self.assertRaises(TamuTidakValidError):
                Reservasi("RSV-002", tamu, self.check_in, self.check_out)

    def test_daftar_detail_adalah_salinan(self):
        self.reservasi.tambah_kamar(self.k1)
        self.reservasi.daftar_detail.clear()
        self.assertEqual(len(self.reservasi.daftar_detail), 1)

    def test_jumlah_malam_dari_tanggal(self):
        self.assertEqual(self.reservasi.jumlah_malam, 2)
        r = Reservasi("RSV-003", self.tamu, date(2026, 12, 30), date(2027, 1, 2))
        self.assertEqual(r.jumlah_malam, 3)

    def test_check_out_sama_dengan_check_in(self):
        with self.assertRaises(TanggalTidakValidError):
            Reservasi("RSV-002", self.tamu, self.check_in, self.check_in)

    def test_check_out_sebelum_check_in(self):
        with self.assertRaises(TanggalTidakValidError) as ctx:
            Reservasi("RSV-002", self.tamu, self.check_out, self.check_in)
        self.assertEqual(ctx.exception.tgl_check_in, self.check_out)
        self.assertEqual(ctx.exception.tgl_check_out, self.check_in)

    def test_tanggal_bukan_objek_date(self):
        for nilai in ("2026-11-20", None, 20261120, datetime(2026, 11, 20, 14, 0)):
            with self.assertRaises(TanggalTidakValidError):
                Reservasi("RSV-002", self.tamu, nilai, self.check_out)
            with self.assertRaises(TanggalTidakValidError):
                Reservasi("RSV-002", self.tamu, self.check_in, nilai)

    def test_tambah_kamar_menambah_detail(self):
        detail = self.reservasi.tambah_kamar(self.k1)
        self.assertIsInstance(detail, DetailReservasi)
        self.assertEqual(len(self.reservasi.daftar_detail), 1)

    def test_tambah_kamar_jumlah_malam_sesuai_tanggal(self):
        detail = self.reservasi.tambah_kamar(self.k1)
        self.assertEqual(detail.jumlah_malam, 2)

    def test_tambah_kamar_mengisi_data_detail(self):
        detail = self.reservasi.tambah_kamar(self.k1)
        self.assertIs(detail.reservasi, self.reservasi)
        self.assertIs(detail.kamar, self.k1)
        self.assertEqual(detail.harga_kamar, 500000)
        self.assertEqual(detail.subtotal, 1000000)

    def test_tambah_kamar_harga_tidak_valid_tidak_mengubah_apa_pun(self):
        kamar = Mock()
        kamar.nomor_kamar, kamar.tipe_kamar, kamar.harga = "999", "Rusak", -1
        kamar.status = "Tersedia"
        with self.assertRaises(HargaKamarTidakValidError):
            self.reservasi.tambah_kamar(kamar)
        kamar.ubah_status.assert_not_called()
        self.assertEqual(self.reservasi.daftar_detail, [])

    def test_tambah_kamar_mengubah_status(self):
        self.reservasi.tambah_kamar(self.k1)
        self.assertEqual(self.k1.status, "Terisi")

    def test_tambah_kamar_tidak_tersedia(self):
        self.reservasi.tambah_kamar(self.k1)
        with self.assertRaises(KamarTidakTersediaError) as ctx:
            self.reservasi.tambah_kamar(self.k1)
        self.assertEqual(ctx.exception.nomor_kamar, "101")
        self.assertEqual(len(self.reservasi.daftar_detail), 1)

    def test_tambah_kamar_yang_sudah_terisi(self):
        kamar = Kamar("303", "Standard", 300000, "Terisi")
        with self.assertRaises(KamarTidakTersediaError):
            self.reservasi.tambah_kamar(kamar)
        self.assertEqual(self.reservasi.daftar_detail, [])

    def test_semua_exception_turunan_reservasi_error(self):
        with self.assertRaises(ReservasiError):
            Reservasi("RSV-002", self.tamu, self.check_out, self.check_in)

    def test_hitung_total_kosong(self):
        self.assertEqual(self.reservasi.hitung_total(), 0)

    def test_hitung_total_satu_kamar(self):
        self.reservasi.tambah_kamar(self.k1)
        self.assertEqual(self.reservasi.hitung_total(), 1000000)

    def test_hitung_total_banyak_kamar(self):
        self.reservasi.tambah_kamar(self.k1)
        self.reservasi.tambah_kamar(self.k2)
        self.assertEqual(self.reservasi.hitung_total(), 3400000)

    def test_cetak_struk_berisi_data(self):
        self.reservasi.tambah_kamar(self.k1)
        struk = self.reservasi.cetak_struk()
        for teks in ("RSV-001", "Budi Santoso", "Kamar 101",
                     "20-11-2026", "22-11-2026", "2 malam", "TOTAL", "1,000,000"):
            self.assertIn(teks, struk)

    def test_cetak_struk_reservasi_kosong(self):
        with self.assertRaises(ReservasiKosongError) as ctx:
            self.reservasi.cetak_struk()
        self.assertEqual(ctx.exception.id_reservasi, "RSV-001")


if __name__ == "__main__":
    unittest.main(verbosity=2)
