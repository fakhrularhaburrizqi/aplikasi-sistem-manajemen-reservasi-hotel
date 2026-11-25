class DetailReservasiError(Exception):
    """Exception dasar untuk semua kesalahan pada DetailReservasi."""


class DataDetailTidakLengkapError(DetailReservasiError):
    """Dilempar jika reservasi, kamar, jumlah_malam, atau harga_kamar belum diisi."""

    def __init__(self, field):
        self.field = field
        super().__init__(f"Data detail tidak lengkap: '{field}' belum diisi")


class JumlahMalamTidakValidError(DetailReservasiError):
    """Dilempar jika jumlah_malam bukan bilangan bulat lebih dari 0."""

    def __init__(self, jumlah_malam):
        self.jumlah_malam = jumlah_malam
        super().__init__(
            f"Jumlah malam tidak valid: {jumlah_malam!r} "
            "(harus bilangan bulat lebih dari 0)"
        )


class HargaKamarTidakValidError(DetailReservasiError):
    """Dilempar jika harga_kamar bukan angka atau kurang dari 0."""

    def __init__(self, harga_kamar):
        self.harga_kamar = harga_kamar
        super().__init__(
            f"Harga kamar tidak valid: {harga_kamar!r} (harus angka >= 0)"
        )


class DetailSudahAdaError(DetailReservasiError):
    """Dilempar jika tambah_detail() dipanggil pada detail yang sudah ditambahkan."""

    def __init__(self):
        super().__init__("Detail reservasi sudah ditambahkan sebelumnya")


class DetailTidakDitemukanError(DetailReservasiError):
    """Dilempar jika ubah_detail()/hapus_detail() dipanggil sebelum detail ditambahkan."""

    def __init__(self):
        super().__init__("Detail reservasi belum ditambahkan / tidak ditemukan")


class DetailReservasi:
    def __init__(self, id_detail=None, reservasi=None, kamar=None,
                 jumlah_malam=None, harga_kamar=None):
        self.id_detail = id_detail
        self.reservasi = reservasi
        self.kamar = kamar
        self.jumlah_malam = jumlah_malam
        self.harga_kamar = harga_kamar
        self.subtotal = None

  
    def _validasi(self):
        if self.reservasi is None:
            raise DataDetailTidakLengkapError("reservasi")
        if self.kamar is None:
            raise DataDetailTidakLengkapError("kamar")
        if self.jumlah_malam is None:
            raise DataDetailTidakLengkapError("jumlah_malam")
        if self.harga_kamar is None:
            raise DataDetailTidakLengkapError("harga_kamar")

        if (isinstance(self.jumlah_malam, bool)
                or not isinstance(self.jumlah_malam, int)
                or self.jumlah_malam <= 0):
            raise JumlahMalamTidakValidError(self.jumlah_malam)

        if (isinstance(self.harga_kamar, bool)
                or not isinstance(self.harga_kamar, (int, float))
                or self.harga_kamar < 0):
            raise HargaKamarTidakValidError(self.harga_kamar)

    def tambah_detail(self):
        """Menambahkan detail reservasi (validasi data lalu hitung subtotal)."""
        if self.subtotal is not None:
            raise DetailSudahAdaError()
        self.hitung_subtotal()

    def ubah_detail(self, kamar=None, jumlah_malam=None, harga_kamar=None):
        """Mengubah detail yang sudah ada; subtotal dihitung ulang.
        Jika data baru tidak valid, data lama dikembalikan."""
        if self.subtotal is None:
            raise DetailTidakDitemukanError()

        lama = (self.kamar, self.jumlah_malam, self.harga_kamar, self.subtotal)
        if kamar is not None:
            self.kamar = kamar
        if jumlah_malam is not None:
            self.jumlah_malam = jumlah_malam
        if harga_kamar is not None:
            self.harga_kamar = harga_kamar

        try:
            self.hitung_subtotal()
        except DetailReservasiError:
            self.kamar, self.jumlah_malam, self.harga_kamar, self.subtotal = lama
            raise

    def hapus_detail(self):
        """Menghapus detail: mengosongkan kamar, jumlah malam, harga, dan subtotal."""
        if self.subtotal is None:
            raise DetailTidakDitemukanError()
        self.kamar = None
        self.jumlah_malam = None
        self.harga_kamar = None
        self.subtotal = None

    def hitung_subtotal(self):
        """Menghitung subtotal = harga_kamar x jumlah_malam."""
        self._validasi()
        self.subtotal = self.harga_kamar * self.jumlah_malam
        return self.subtotal
