import unittest

from models.detail_reservasi import (
    DataDetailTidakLengkapError,
    DetailReservasi,
    DetailReservasiError,
    DetailSudahAdaError,
    DetailTidakDitemukanError,
    HargaKamarTidakValidError,
    JumlahMalamTidakValidError,
)


class TestDetailReservasi(unittest.TestCase):
    def setUp(self):
        self.reservasi = object()
        self.kamar = object()
        self.detail = DetailReservasi(
            id_detail=1,
            reservasi=self.reservasi,
            kamar=self.kamar,
            jumlah_malam=3,
            harga_kamar=500_000,
        )

    def test_atribut_awal_kosong(self):
        d = DetailReservasi()
        self.assertIsNone(d.id_detail)
        self.assertIsNone(d.reservasi)
        self.assertIsNone(d.kamar)
        self.assertIsNone(d.jumlah_malam)
        self.assertIsNone(d.harga_kamar)
        self.assertIsNone(d.subtotal)

    def test_atribut_terisi(self):
        self.assertEqual(self.detail.id_detail, 1)
        self.assertIs(self.detail.reservasi, self.reservasi)
        self.assertIs(self.detail.kamar, self.kamar)
        self.assertEqual(self.detail.jumlah_malam, 3)
        self.assertEqual(self.detail.harga_kamar, 500_000)

    def test_hitung_subtotal(self):
        self.assertEqual(self.detail.hitung_subtotal(), 1_500_000)
        self.assertEqual(self.detail.subtotal, 1_500_000)

    def test_hitung_subtotal_harga_desimal(self):
        self.detail.harga_kamar = 250_000.5
        self.assertAlmostEqual(self.detail.hitung_subtotal(), 750_001.5)

    def test_hitung_subtotal_harga_nol(self):
        self.detail.harga_kamar = 0
        self.assertEqual(self.detail.hitung_subtotal(), 0)

    def test_tambah_detail_berhasil(self):
        self.detail.tambah_detail()
        self.assertEqual(self.detail.subtotal, 1_500_000)

    def test_tambah_detail_dua_kali_error(self):
        self.detail.tambah_detail()
        with self.assertRaises(DetailSudahAdaError):
            self.detail.tambah_detail()

    def test_tambah_detail_data_tidak_lengkap(self):
        for field in ("reservasi", "kamar", "jumlah_malam", "harga_kamar"):
            with self.subTest(field=field):
                d = DetailReservasi(1, self.reservasi, self.kamar, 2, 100_000)
                setattr(d, field, None)
                with self.assertRaises(DataDetailTidakLengkapError) as ctx:
                    d.tambah_detail()
                self.assertEqual(ctx.exception.field, field)
                self.assertIsNone(d.subtotal)

    def test_jumlah_malam_tidak_valid(self):
        for nilai in (0, -1, 2.5, "3", True):
            with self.subTest(nilai=nilai):
                self.detail.jumlah_malam = nilai
                with self.assertRaises(JumlahMalamTidakValidError):
                    self.detail.tambah_detail()

    def test_harga_kamar_tidak_valid(self):
        for nilai in (-1, "500000", True):
            with self.subTest(nilai=nilai):
                self.detail.harga_kamar = nilai
                with self.assertRaises(HargaKamarTidakValidError):
                    self.detail.tambah_detail()

    def test_ubah_detail_berhasil(self):
        self.detail.tambah_detail()
        kamar_baru = object()
        self.detail.ubah_detail(kamar=kamar_baru, jumlah_malam=2, harga_kamar=600_000)
        self.assertIs(self.detail.kamar, kamar_baru)
        self.assertEqual(self.detail.jumlah_malam, 2)
        self.assertEqual(self.detail.harga_kamar, 600_000)
        self.assertEqual(self.detail.subtotal, 1_200_000)

    def test_ubah_detail_sebagian(self):
        self.detail.tambah_detail()
        self.detail.ubah_detail(jumlah_malam=5)
        self.assertEqual(self.detail.subtotal, 2_500_000)

    def test_ubah_detail_sebelum_tambah_error(self):
        with self.assertRaises(DetailTidakDitemukanError):
            self.detail.ubah_detail(jumlah_malam=2)

    def test_ubah_detail_tidak_valid_data_lama_kembali(self):
        self.detail.tambah_detail()
        with self.assertRaises(JumlahMalamTidakValidError):
            self.detail.ubah_detail(jumlah_malam=0)
        self.assertEqual(self.detail.jumlah_malam, 3)
        self.assertEqual(self.detail.subtotal, 1_500_000)

    def test_hapus_detail_berhasil(self):
        self.detail.tambah_detail()
        self.detail.hapus_detail()
        self.assertIsNone(self.detail.kamar)
        self.assertIsNone(self.detail.jumlah_malam)
        self.assertIsNone(self.detail.harga_kamar)
        self.assertIsNone(self.detail.subtotal)

    def test_hapus_detail_sebelum_tambah_error(self):
        with self.assertRaises(DetailTidakDitemukanError):
            self.detail.hapus_detail()

    def test_hapus_dua_kali_error(self):
        self.detail.tambah_detail()
        self.detail.hapus_detail()
        with self.assertRaises(DetailTidakDitemukanError):
            self.detail.hapus_detail()

    def test_semua_exception_turunan_base(self):
        for exc in (DataDetailTidakLengkapError("x"), JumlahMalamTidakValidError(0),
                    HargaKamarTidakValidError(-1), DetailSudahAdaError(),
                    DetailTidakDitemukanError()):
            with self.subTest(exc=type(exc).__name__):
                self.assertIsInstance(exc, DetailReservasiError)

    def test_pesan_exception(self):
        self.detail.jumlah_malam = -5
        with self.assertRaises(JumlahMalamTidakValidError) as ctx:
            self.detail.hitung_subtotal()
        self.assertIn("-5", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
