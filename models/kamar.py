# ----------------- 1. HIERARKI CUSTOM EXCEPTION -----------------
class KamarError(Exception):
    """Base exception untuk seluruh error pada class Kamar."""
    pass

class KamarSudahAdaError(KamarError):
    """Dilempar jika mendaftarkan kamar dengan nomor yang sudah ada."""
    pass

class KamarPenuhError(KamarError):
    """Dilempar jika mengubah status menjadi 'Terisi' pada kamar yang sudah terisi."""
    pass

class KamarKosongError(KamarError):
    """Dilempar jika mengubah status menjadi 'Tersedia' pada kamar yang memang sudah kosong."""
    pass

# ----------------------- 2. CLASS UTAMA -----------------------
class Kamar:
    # Koleksi daftar kamar hotel di level class (masukan dosen)
    daftar_kamar = []
    def __init__(self, nomor_kamar: str, tipe_kamar: str, harga: float, status: str = "Tersedia"):
        # Atribut private sesuai rancangan awal
        self._nomor_kamar = str(nomor_kamar).strip()
        self._tipe_kamar = str(tipe_kamar).strip()
        self.harga = harga  # Memanggil setter validasi harga
        self._status = status.strip().capitalize()

    # ---------------- ENKAPSULASI (@property) ----------------
    @property
    def nomor_kamar(self) -> str:
        return self._nomor_kamar
    
    @property
    def tipe_kamar(self) -> str:
        return self._tipe_kamar
    
    @property
    def harga(self) -> float:
        return self._harga
    
    @harga.setter
    def harga(self, nilai: float):
        if float(nilai) <= 0:
            raise ValueError("Harga kamar harus lebih besar dari Rp 0!")
        self._harga = float(nilai)

    @property
    def status(self) -> str:
        return self._status
    
    # ------------- METHOD -------------
    def get_info_kamar(self) -> str:
        """
        Method awal: Menampilkan informasi lengkap data kamar.
        """
        return f"Kamar {self._nomor_kamar} | Tipe: {self._tipe_kamar} | Harga: Rp{self._harga:,.0f} | Status: {self._status}"
    
    def ubah_status(self, status_baru: str) -> None:
        """
        Method awal: Mengubah status kamar ('Tersedia' atau 'Terisi')
        dilengkapi dengan validasi Custom Exception.
        """
        status_clean = str(status_baru).strip().capitalize()
        
        # Validasi pilihan status
        if status_clean not in ["Tersedia", "Terisi"]:
            raise ValueError("Status tidak valid! Hanya boleh 'Tersedia' atau 'Terisi'.")
        
        # Pengecekan Custom Exception jika statusnya sama
        if status_clean == self._status:
            if status_clean == "Terisi":
                raise KamarPenuhError(f"Kamar {self._nomor_kamar} sudah Terisi!")
            else:
                raise KamarKosongError(f"Kamar {self._nomor_kamar} memang sudah Tersedia!")
        self._status = status_clean

    # memanggil ubah_status
    def check_in(self) -> None:
        self.ubah_status("Terisi")

    def check_out(self) -> None:
        self.ubah_status("Tersedia")

    # ----------- CLASS METHOD -----------
    @classmethod
    def tambah_kamar(cls, nomor_kamar: str, tipe_kamar: str, harga: float):
        """Mendaftarkan kamar baru dengan validasi nomor duplikat."""
        nomor = str(nomor_kamar).strip()
        for k in cls.daftar_kamar:
            if k.nomor_kamar == nomor:
                raise KamarSudahAdaError(f"Kamar dengan nomor '{nomor}' sudah terdaftar di sistem!")
        kamar_baru = cls(nomor, tipe_kamar, harga)
        cls.daftar_kamar.append(kamar_baru)
        return kamar_baru
    
    @classmethod
    def cari_kamar_kosong(cls) -> list:
        """Mengambil seluruh objek kamar yang statusnya 'Tersedia'."""
        return [k for k in cls.daftar_kamar if k.status == "Tersedia"]
    
    @classmethod
    def reset_daftar_kamar(cls):
        """Helper untuk mengosongkan list saat unit testing."""
        cls.daftar_kamar.clear()

    def __str__(self) -> str:
        return self.get_info_kamar()