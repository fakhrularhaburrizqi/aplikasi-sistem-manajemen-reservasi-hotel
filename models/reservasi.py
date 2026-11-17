class Reservasi:
    def __init__(self, id_reservasi, tamu):
        # Atribut (sesuai UML)
        self.__id_reservasi = id_reservasi   # primary key
        self.__tamu = tamu                   # foreign key -> Tamu (Association)
        self.__daftar_detail = []            # list DetailReservasi (Composition)

    def tambah_kamar(self, kamar, jumlah_malam):
        """Menambahkan detail kamar ke reservasi."""
        pass

    def hitung_total(self):
        """Menghitung total harga reservasi."""
        pass

    def cetak_struk(self):
        """Mencetak struk reservasi."""
        pass