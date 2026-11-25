class TamuError(Exception):
    """Base exception untuk semua error pada Class Tamu."""
    pass

class InvalidNIKError(TamuError):
    """Muncul jika NIK kosong atau tidak 16 digit."""
    pass

class InvalidNamaError(TamuError):
    """Muncul jika nama tamu kosong."""
    pass

class InvalidNoTelpError(TamuError):
    """Muncul jika nomor telepon kosong atau bukan angka."""
    pass


class Tamu:
    def __init__(self, nik, nama, no_telp):
        if not nik or len(str(nik).strip()) != 16 or not str(nik).isdigit():
            raise InvalidNIKError("NIK harus terdiri dari 16 digit angka!")
        self.__nik = str(nik).strip()
        self.nama = nama
        self.no_telp = no_telp

    @property
    def nik(self):
        return self.__nik

    @property
    def nama(self):
        return self.__nama

    @property
    def no_telp(self):
        return self.__no_telp

    @nama.setter
    def nama(self, nama_baru):
        if not nama_baru or str(nama_baru).strip() == "":
            raise InvalidNamaError("Nama tamu tidak boleh kosong!")
        self.__nama = nama_baru.strip()

    @no_telp.setter
    def no_telp(self, no_telp_baru):
        if not no_telp_baru or not str(no_telp_baru).isdigit():
            raise InvalidNoTelpError("Nomor telepon harus berupa angka dan tidak boleh kosong!")
        self.__no_telp = str(no_telp_baru).strip()

    def get_info_tamu(self):
        return f"Tamu: {self.__nama} | NIK: {self.__nik} | Telp: {self.__no_telp}"