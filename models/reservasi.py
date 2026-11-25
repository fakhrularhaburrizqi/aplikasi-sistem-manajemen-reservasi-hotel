from datetime import date, datetime

from models.tamu import Tamu
from models.detail_reservasi import DetailReservasi

STATUS_TERSEDIA = "tersedia"


class ReservasiError(Exception):
    """Exception dasar untuk semua kesalahan pada Reservasi."""


class TamuTidakValidError(ReservasiError):
    """Dilempar jika Reservasi dibuat tanpa objek Tamu yang valid."""

    def __init__(self, pesan="Tamu tidak valid, harus berupa objek Tamu"):
        super().__init__(pesan)


class TanggalTidakValidError(ReservasiError):
    """Dilempar jika tanggal bukan objek date atau check-out tidak setelah check-in."""

    def __init__(self, pesan, tgl_check_in=None, tgl_check_out=None):
        self.tgl_check_in = tgl_check_in
        self.tgl_check_out = tgl_check_out
        super().__init__(pesan)


class KamarTidakTersediaError(ReservasiError):
    """Dilempar jika kamar yang dipilih sedang tidak tersedia."""

    def __init__(self, nomor_kamar):
        self.nomor_kamar = nomor_kamar
        super().__init__(f"Kamar {nomor_kamar} tidak tersedia")


class ReservasiKosongError(ReservasiError):
    """Dilempar jika struk dicetak padahal belum ada kamar yang dipesan."""

    def __init__(self, id_reservasi):
        self.id_reservasi = id_reservasi
        super().__init__(f"Reservasi {id_reservasi} belum memiliki kamar")


class Reservasi:
    def __init__(self, id_reservasi, tamu, tgl_check_in, tgl_check_out):
        if not isinstance(tamu, Tamu):
            raise TamuTidakValidError()
        self.__validasi_tanggal(tgl_check_in, tgl_check_out)

        self.__id_reservasi = id_reservasi
        self.__tamu = tamu
        self.__tgl_check_in = tgl_check_in
        self.__tgl_check_out = tgl_check_out
        self.__daftar_detail = []

    @staticmethod
    def __validasi_tanggal(tgl_check_in, tgl_check_out):
        for nama, tgl in (("check-in", tgl_check_in), ("check-out", tgl_check_out)):
            if not isinstance(tgl, date) or isinstance(tgl, datetime):
                raise TanggalTidakValidError(
                    f"Tanggal {nama} harus berupa objek date, bukan {type(tgl).__name__}",
                    tgl_check_in, tgl_check_out,
                )
        if tgl_check_out <= tgl_check_in:
            raise TanggalTidakValidError(
                "Tanggal check-out harus setelah tanggal check-in",
                tgl_check_in, tgl_check_out,
            )

    @property
    def id_reservasi(self):
        return self.__id_reservasi

    @property
    def tamu(self):
        return self.__tamu

    @property
    def tgl_check_in(self):
        return self.__tgl_check_in

    @property
    def tgl_check_out(self):
        return self.__tgl_check_out

    @property
    def jumlah_malam(self):
        """Lama menginap = selisih hari check-out dan check-in."""
        return (self.__tgl_check_out - self.__tgl_check_in).days

    @property
    def daftar_detail(self):
        return list(self.__daftar_detail)

    def tambah_kamar(self, kamar):
        """Menambahkan detail kamar ke reservasi."""
        if kamar.status != STATUS_TERSEDIA:
            raise KamarTidakTersediaError(kamar.nomor_kamar)

        detail = DetailReservasi(
            reservasi=self,
            kamar=kamar,
            jumlah_malam=self.jumlah_malam,
            harga_kamar=kamar.harga,
        )
        detail.tambah_detail()
        self.__daftar_detail.append(detail)
        kamar.ubah_status()
        return detail

    def hitung_total(self):
        """Menghitung total harga reservasi."""
        return sum(d.subtotal for d in self.__daftar_detail)

    def cetak_struk(self):
        """Mengembalikan struk reservasi dalam bentuk string."""
        if not self.__daftar_detail:
            raise ReservasiKosongError(self.__id_reservasi)

        garis = "=" * 44
        baris = [
            garis,
            "STRUK RESERVASI HOTEL".center(44),
            garis,
            f"{'ID Reservasi':<13}: {self.__id_reservasi}",
            self.__tamu.get_info_tamu(),
            f"{'Check-in':<13}: {self.__tgl_check_in.strftime('%d-%m-%Y')}",
            f"{'Check-out':<13}: {self.__tgl_check_out.strftime('%d-%m-%Y')}",
            f"{'Lama menginap':<13}: {self.jumlah_malam} malam",
            "-" * 44,
        ]
        for d in self.__daftar_detail:
            k = d.kamar
            baris.append(
                f"Kamar {k.nomor_kamar} ({k.tipe_kamar}) "
                f"{d.jumlah_malam} malam x Rp{d.harga_kamar:,.0f}"
            )
            baris.append(f"{'Subtotal':>30}: Rp{d.subtotal:,.0f}")
        baris += ["-" * 44, f"{'TOTAL':>30}: Rp{self.hitung_total():,.0f}", garis]
        return "\n".join(baris)
