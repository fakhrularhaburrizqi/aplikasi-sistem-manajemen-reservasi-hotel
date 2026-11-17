class Tamu:
    def __init__(self, nik, nama, no_telp):
        self.__nik = nik
        self.__nama = nama
        self.__no_telp = no_telp

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
        if nama_baru:
            self.__nama = nama_baru

    @no_telp.setter
    def no_telp(self, no_telp_baru):
        if no_telp_baru:
            self.__no_telp = no_telp_baru

    def get_info_tamu(self):
        return f"Tamu: {self.__nama} | NIK: {self.__nik} | Telp: {self.__no_telp}"