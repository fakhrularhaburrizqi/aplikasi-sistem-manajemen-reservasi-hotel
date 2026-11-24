class Kamar:
    # 1. Collection penampung seluruh kamar hotel (Class Variable)
    daftar_kamar = []

    def __init__(self, nomor_kamar: str, tipe: str, harga_per_malam: float):
        # 2. Deklarasi atribut private (Enkapsulasi)
        self._nomor_kamar = str(nomor_kamar)
        self._tipe = str(tipe)
        self._harga_per_malam = harga_per_malam # Memanggil setter untuk validasi
        self._is_terisi = False

    # ---------------- ENKAPSULASI (@property) ----------------
    @property
    def nomor_kamar(self) -> str:
        return self._nomor_kamar
    
    @property
    def tipe(self) -> str:
        return self._tipe
    
    @property
    def harga_per_malam(self) -> float:
        return self._harga_per_malam
    
    @harga_per_malam.setter
    def harga_per_malam(self, nilai: float):
        if nilai <= 0:
            raise ValueError("Harga per malam harus lebih dari 0!")
        self._harga_per_malam = float(nilai)

    @property
    def is_terisi(self) -> bool:
        return self._is_terisi

    # ----------- SKELETON METHOD (Masih 'pass') -----------
    @classmethod
    def tambah_kamar(cls, nomor_kamar: str, tipe: str, harga_per_malam: float):
        """
        Skeleton method untuk menambahkan kamar baru ke daftar_kamar hotel.
        (Logika validasi duplikat & insert akan diisi di Pertemuan 13).
        """
        pass

    def check_in(self):
        """Skeleton: Mengubah status kamar menjadi terisi."""
        pass

    def check_out(self):
        """Skeleton: Mengubah status kamar menjadi kosong."""
        pass