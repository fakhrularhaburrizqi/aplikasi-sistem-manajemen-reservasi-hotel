class Kamar:
    def __init__(self, nomor_kamar: str, tipe: str, harga_per_malam: float):
        # Atribut private
        self._nomor_kamar = nomor_kamar
        self._tipe = tipe
        self._harga_per_malam = harga_per_malam # Menggunakan setter
        self._is_terisi = False

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
    
    def check_in(self):
        pass

    def check_out(self):
        pass