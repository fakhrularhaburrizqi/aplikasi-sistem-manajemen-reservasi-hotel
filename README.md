# Aplikasi Manajemen Reservasi Hotel — MVC + Streamlit + SQLite

Aplikasi berbasis **Object-Oriented Programming (OOP)**, arsitektur **MVC (Model-View-Controller)**, dan **Streamlit** untuk mengelola data kamar, tamu, dan reservasi hotel dengan **SQLite** sebagai database.

---

## Class Diagram

```mermaid
classDiagram
    class Tamu {
        -nik: str
        -nama: str
        -no_telp: str
        +get_info_tamu() str
    }

    class Reservasi {
        -id_reservasi
        -tamu: Tamu
        -tgl_check_in: date
        -tgl_check_out: date
        -daftar_detail: list
        +tambah_kamar(kamar)
        +hitung_total() float
        +cetak_struk() str
        +jumlah_malam() int
    }

    class DetailReservasi {
        +id_detail
        +reservasi
        +kamar
        +jumlah_malam: int
        +harga_kamar: float
        +subtotal: float
        +tambah_detail()
        +ubah_detail()
        +hapus_detail()
        +hitung_subtotal() float
    }

    class Kamar {
        +daftar_kamar: list$
        -nomor_kamar: str
        -tipe_kamar: str
        -harga: float
        -status: str
        +get_info_kamar() str
        +ubah_status(status_baru)
        +check_in()
        +check_out()
        +tambah_kamar()$ Kamar
        +cari_kamar_kosong()$ list
        +reset_daftar_kamar()$
    }

    Tamu "1" -- "0..*" Reservasi : melakukan
    Reservasi "1" *-- "1..*" DetailReservasi : memiliki
    Kamar "1" -- "0..*" DetailReservasi : dipesan
```

Keterangan notasi: `-` private, `+` public, `$` atribut/method tingkat class (`@classmethod`).

---

## Rincian Entitas

### 1. Tamu
- **Atribut**: `nik` (primary key), `nama`, `no_telp`
- **Method**: `get_info_tamu()` — mengembalikan informasi lengkap tamu
- **Relasi**: **Association** ke `Reservasi` (1 tamu dapat memiliki 0..* reservasi)

### 2. Reservasi
- **Atribut**: `id_reservasi` (primary key), `tamu` (foreign key ke Tamu), `tgl_check_in`, `tgl_check_out`, `daftar_detail`
- **Method**:
  - `tambah_kamar(kamar)` — menambahkan detail kamar ke reservasi
  - `hitung_total()` — menjumlahkan subtotal seluruh detail
  - `cetak_struk()` — membuat struk reservasi dalam bentuk teks
  - `jumlah_malam` — selisih hari check-out dan check-in
- **Relasi**: **Composition** ke `DetailReservasi` (1 reservasi memiliki 1..* detail; jika reservasi dihapus, detailnya ikut terhapus)

### 3. DetailReservasi
- **Atribut**: `id_detail`, `reservasi`, `kamar`, `jumlah_malam`, `harga_kamar`, `subtotal`
- **Method**:
  - `tambah_detail()` — validasi data lalu menghitung subtotal
  - `ubah_detail()` — mengubah detail (data lama dikembalikan jika data baru tidak valid)
  - `hapus_detail()` — mengosongkan detail
  - `hitung_subtotal()` — `harga_kamar × jumlah_malam`
- **Relasi**: **Association** ke `Kamar` (setiap detail merujuk tepat 1 kamar)

### 4. Kamar
- **Atribut**: `nomor_kamar` (primary key), `tipe_kamar`, `harga`, `status` (`Tersedia` / `Terisi`), `daftar_kamar` (koleksi level class)
- **Method**:
  - `get_info_kamar()` — info lengkap kamar beserta status
  - `ubah_status(status_baru)` — mengubah status dengan validasi
  - `check_in()` / `check_out()` — memanggil `ubah_status()`
  - `tambah_kamar()`, `cari_kamar_kosong()`, `reset_daftar_kamar()` — class method
- **Relasi**: Dirujuk oleh `DetailReservasi` (1 kamar dapat muncul di 0..* detail)

---

## Custom Exception

| Kelas | Exception | Kondisi |
|---|---|---|
| Kamar | `KamarSudahAdaError` | Nomor kamar sudah terdaftar |
| Kamar | `KamarPenuhError` | Check-in pada kamar yang sudah terisi |
| Kamar | `KamarKosongError` | Check-out pada kamar yang sudah tersedia |
| DetailReservasi | `DataDetailTidakLengkapError` | Field detail belum diisi |
| DetailReservasi | `JumlahMalamTidakValidError` | Jumlah malam bukan bilangan bulat > 0 |
| DetailReservasi | `HargaKamarTidakValidError` | Harga bukan angka atau < 0 |
| DetailReservasi | `DetailSudahAdaError` / `DetailTidakDitemukanError` | Tambah ganda / ubah-hapus sebelum ada |
| Reservasi | `TamuTidakValidError` | Tamu bukan objek `Tamu` |
| Reservasi | `TanggalTidakValidError` | Tanggal tidak valid atau check-out ≤ check-in |
| Reservasi | `KamarTidakTersediaError` | Kamar yang dipilih tidak tersedia |
| Reservasi | `ReservasiKosongError` | Cetak struk tanpa kamar |

---

## Struktur Proyek MVC

```text
reservasi_hotel_mvc_database/
├── app.py
├── pages/
│   ├── 1_Kamar.py
│   ├── 2_Tamu.py
│   └── 3_Reservasi.py
├── models/
│   ├── __init__.py
│   ├── kamar.py
│   ├── tamu.py
│   ├── reservasi.py
│   ├── detail_reservasi.py
│   └── user.py
├── views/
│   ├── auth_view.py
│   ├── kamar_view.py
│   ├── tamu_view.py
│   └── reservasi_view.py
├── controllers/
│   ├── auth_controller.py
│   ├── kamar_controller.py
│   ├── tamu_controller.py
│   └── reservasi_controller.py
├── database/
│   ├── db.py
│   └── reservasi_hotel.db
├── tests/
│   ├── __init__.py
│   ├── test_kamar.py
│   ├── test_tamu.py
│   └── test_reservasi.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## Cara Menjalankan

```bash
# 1. Buat dan aktifkan virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependensi
pip install -r requirements.txt

# 3. Salin konfigurasi environment
cp .env.example .env            # Windows: copy .env.example .env

# 4. Jalankan aplikasi
streamlit run app.py
```

## Menjalankan Unit Test

```bash
python -m unittest discover tests
```

---
