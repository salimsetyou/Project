import csv
import os
import datetime

# ---------- KONSTANTA: Nama File dan Headers ----------

USERS_FILE = 'users.csv'
LIVESTOCK_FILE = 'livestock.csv'
HEALTH_FILE = 'health_records.csv'
FEEDING_FILE = 'feeding_log.csv'

# Headers (Kepala Kolom) untuk setiap file CSV
HEADERS_USERS = ['username', 'password', 'role']
HEADERS_LIVESTOCK = ['ternak_id', 'jenis_ternak', 'tgl_lahir', 'berat_sekarang', 'status_kesehatan', 'kandang_id']
HEADERS_HEALTH = ['record_id', 'ternak_id', 'tanggal', 'gejala', 'tindakan', 'dicatat_oleh']
HEADERS_FEEDING = ['log_id', 'kandang_id', 'tanggal', 'jenis_pakan', 'jumlah_kg', 'dicatat_oleh']

# ---------- FUNGSI SETUP ----------

def setup_files():
    # Memeriksa apakah file CSV ada. Jika tidak, buat file dengan headernya.
    file_headers_map = {
        USERS_FILE: HEADERS_USERS,
        LIVESTOCK_FILE: HEADERS_LIVESTOCK,
        HEALTH_FILE: HEADERS_HEALTH,
        FEEDING_FILE: HEADERS_FEEDING
    }
    
    for filename, headers in file_headers_map.items():
        if not os.path.exists(filename):
            try:
                with open(filename, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(headers)
                print(f"File '{filename}' berhasil dibuat.")
            except IOError as e:
                print(f"ERROR: Tidak dapat membuat file {filename}. {e}")
    
    # Tambahkan admin default jika file users baru dibuat dan kosong
    if not read_csv(USERS_FILE):
         # Data admin default
        admin_data = {'username': 'admin', 'password': 'admin', 'role': 'admin'}
        append_csv_row(USERS_FILE, admin_data, HEADERS_USERS)
        print("Akun 'admin' (pass: 'admin') default telah ditambahkan.")


# ---------- FUNGSI HELPER CSV (OPERASI FILE) ----------

def read_csv(filename):
    # Membaca seluruh data dari file CSV dan mengembalikannya sebagai list of dicts.
    data = []
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            # DictReader otomatis menggunakan baris pertama sebagai keys
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print(f"ERROR: File {filename} tidak ditemukan.")
    except Exception as e:
        print(f"ERROR: Terjadi kesalahan saat membaca {filename}. {e}")
    return data

def write_csv_overwrite(filename, data, headers):
    # Menulis ulang (overwrite) seluruh file CSV dengan data baru.
    # bagian dari algoritma READ-MODIFY-WRITE.
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()  # Menulis header
            writer.writerows(data) # Menulis semua baris data
    except IOError as e:
        print(f"ERROR: Tidak dapat menulis ke file {filename}. {e}")

def append_csv_row(filename, data_dict, headers):
    #Menambahkan satu baris data (dict) baru ke akhir file CSV.
    try:
        # 'a' (append) untuk menambahkan, bukan 'w' (write)
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            # fieldnames penting agar urutan penulisan benar
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writerow(data_dict)
    except IOError as e:
        print(f"ERROR: Tidak dapat menambahkan data ke file {filename}. {e}")

# ---------- FUNGSI HELPER UTILITAS ----------

def clear_screen():
    # Membersihkan layar terminal.
    # 'nt' adalah windows
    os.system('cls' if os.name == 'nt' else 'clear')

def get_current_date():
    # Mengembalikan tanggal hari ini dalam format YYYY-MM-DD.
    return datetime.date.today().strftime('%Y-%m-%d')

def generate_id(prefix, filename, id_column):
    # Membuat ID unik baru berdasarkan data yang ada (contoh: S001 -> S002).
    data = read_csv(filename)
    if not data:
        return f"{prefix}001"
    
    # Ambil ID terakhir, ambil angkanya, tambah 1
    try:
        last_id = data[-1][id_column]
        last_num = int(last_id.replace(prefix, ''))
        new_num = last_num + 1
        # zfill(3) untuk padding nol (001, 002, ... 010, ... 100)
        return f"{prefix}{str(new_num).zfill(3)}"
    except (KeyError, IndexError, ValueError):
        # Fallback jika ada data korup atau format ID tidak terduga
        return f"{prefix}{len(data) + 1:03d}"


def print_table(data_list, headers):
    # Mencetak list of dictionaries sebagai tabel yang rapi.
    if not data_list:
        print("\n[ Tidak ada data untuk ditampilkan ]")
        return
    
    # Tentukan lebar kolom (bisa di-improve, tapi ini cara sederhana)
    col_widths = {header: len(header) for header in headers}
    for row in data_list:
        for header in headers:
            col_widths[header] = max(col_widths[header], len(str(row.get(header, ''))))
            
    # Cetak Header
    header_str = " | ".join(header.ljust(col_widths[header]) for header in headers)
    print("\n" + header_str)
    print("-" * len(header_str))
    
    # Cetak Data
    for row in data_list:
        row_str = " | ".join(str(row.get(header, '')).ljust(col_widths[header]) for header in headers)
        print(row_str)

def get_float_input(prompt):
    # Memvalidasi input agar pasti float.
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Input tidak valid. Masukkan angka (contoh: 150.5)")

# ---------- FUNGSI ALGORITMA (SORTING) ----------

def bubble_sort(data_list, key, reverse=False):
    # Implementasi Algoritma Bubble Sort untuk daftar ternak.
    # Dapat mengurutkan berdasarkan 'berat_sekarang' (float) atau 'tgl_lahir' (string).
    n = len(data_list)
    sorted_list = list(data_list) 
    
    for i in range(n - 1):
        swapped = False
        for j in range(0, n - i - 1):
            try:
                # Ambil nilai
                val_a = sorted_list[j][key]
                val_b = sorted_list[j+1][key]
                
                # Konversi jika perlu
                if key == 'berat_sekarang':
                    val_a = float(val_a)
                    val_b = float(val_b)
                
                # Tentukan kondisi pembanding
                condition = (val_a > val_b) if not reverse else (val_a < val_b)
                
                if condition:
                    # Tukar (Swap)
                    sorted_list[j], sorted_list[j+1] = sorted_list[j+1], sorted_list[j]
                    swapped = True
            except (KeyError, ValueError):
                print(f"Warning: Gagal membandingkan data pada key '{key}'.")
                continue # Lanjut ke iterasi berikutnya
                
        if not swapped:
            break # Jika tidak ada yang ditukar, list sudah terurut
            
    return sorted_list

# ---------- FUNGSI LOGIKA: LOGIN ----------

def fungsi_login():
    # Menangani login pengguna.
    # Menggunakan ALGORITMA LINEAR SEARCH untuk mencari user.
    print("--- LOGIN SimTernak ---")
    username = input("Username: ")
    password = input("Password: ")
    
    users = read_csv(USERS_FILE)
    
    # ALGORITMA: Linear Search
    for user in users:
        if user['username'] == username and user['password'] == password:
            print(f"Login berhasil! Selamat datang, {user['username']} ({user['role']})")
            return user['username'], user['role']
            
    print("Username atau password salah.")
    return None, None

# ---------- FUNGSI FITUR: PEKERJA ----------

def pekerja_catat_kesehatan(username):
    # Pekerja mencatat cek kesehatan harian.
    clear_screen()
    print(f"--- Catat Cek Kesehatan Harian (Dicatat oleh: {username}) ---")
    
    # Tampilkan ternak untuk memudahkan
    print_table(read_csv(LIVESTOCK_FILE), HEADERS_LIVESTOCK)
    
    ternak_id = input("\nID Ternak yang dicek: ").upper()
    gejala = input("Gejala (kosongi jika sehat): ")
    tindakan = input("Tindakan yang diberikan: ")
    tanggal = get_current_date()
    record_id = generate_id('H', HEALTH_FILE, 'record_id')
    
    record_data = {
        'record_id': record_id,
        'ternak_id': ternak_id,
        'tanggal': tanggal,
        'gejala': gejala if gejala else "Cek Rutin",
        'tindakan': tindakan,
        'dicatat_oleh': username
    }
    
    # 1. Simpan ke health_records.csv (APPEND)
    append_csv_row(HEALTH_FILE, record_data, HEADERS_HEALTH)
    print(f"Catatan kesehatan {record_id} untuk {ternak_id} berhasil disimpan.")
    
    # 2. (Fitur Tambahan) Update status di livestock.csv jika sakit
    if gejala:
        pekerja_update_status_ternak(ternak_id, "Sakit")

def pekerja_update_status_ternak(ternak_id, status_baru):
    # Fungsi helper untuk update status ternak.
    # Menggunakan ALGORITMA READ-MODIFY-OVERWRITE.
    # 1. READ (Baca)
    livestock_data = read_csv(LIVESTOCK_FILE)
    
    found = False
    # 2. MODIFY (Modifikasi di memori)
    for ternak in livestock_data:
        if ternak['ternak_id'] == ternak_id:
            ternak['status_kesehatan'] = status_baru
            found = True
            break
    
    # 3. OVERWRITE (Tulis Ulang)
    if found:
        write_csv_overwrite(LIVESTOCK_FILE, livestock_data, HEADERS_LIVESTOCK)
        print(f"Status ternak {ternak_id} telah di-update menjadi '{status_baru}'.")
    else:
        print(f"Warning: Gagal update status, ternak {ternak_id} tidak ditemukan.")

def pekerja_catat_pakan(username):
    # Pekerja mencatat pemberian pakan.
    clear_screen()
    print(f"--- Catat Pemberian Pakan (Dicatat oleh: {username}) ---")
    
    kandang_id = input("ID Kandang yang diberi pakan: ").upper()
    jenis_pakan = input("Jenis Pakan (Misal: Konsentrat / Rumput): ")
    jumlah_kg = get_float_input("Jumlah (kg): ")
    tanggal = get_current_date()
    log_id = generate_id('F', FEEDING_FILE, 'log_id')

    log_data = {
        'log_id': log_id,
        'kandang_id': kandang_id,
        'tanggal': tanggal,
        'jenis_pakan': jenis_pakan,
        'jumlah_kg': jumlah_kg,
        'dicatat_oleh': username
    }
    
    # Simpan ke feeding_log.csv (APPEND)
    append_csv_row(FEEDING_FILE, log_data, HEADERS_FEEDING)
    print(f"Catatan pakan {log_id} untuk kandang {kandang_id} berhasil disimpan.")

def pekerja_update_bobot():
    """
    Pekerja meng-update bobot ternak setelah ditimbang.
    Ini adalah implementasi utama ALGORITMA READ-MODIFY-OVERWRITE.
    """
    clear_screen()
    print("--- Update Bobot Timbang Ternak ---")
    
    # Tampilkan data ternak agar mudah dilihat
    print_table(read_csv(LIVESTOCK_FILE), HEADERS_LIVESTOCK)
    
    ternak_id = input("\nID Ternak yang ditimbang: ").upper()
    
    # 1. READ (Baca)
    livestock_data = read_csv(LIVESTOCK_FILE)
    
    found = False
    
    # 2. MODIFY (Modifikasi di memori)
    # Algoritma Linear Search untuk menemukan ID yang tepat
    for ternak in livestock_data:
        if ternak['ternak_id'] == ternak_id:
            print(f"Bobot saat ini untuk {ternak_id}: {ternak['berat_sekarang']} kg")
            berat_baru = get_float_input("Masukkan bobot baru (kg): ")
            ternak['berat_sekarang'] = berat_baru
            found = True
            break # Hentikan loop jika sudah ditemukan
            
    # 3. OVERWRITE (Tulis Ulang)
    if found:
        write_csv_overwrite(LIVESTOCK_FILE, livestock_data, HEADERS_LIVESTOCK)
        print(f"Bobot ternak {ternak_id} berhasil di-update.")
    else:
        print(f"ERROR: Ternak dengan ID {ternak_id} tidak ditemukan.")

def pekerja_lihat_ternak():
    """Pekerja melihat daftar ternak (Read-only)."""
    clear_screen()
    print("--- Daftar Semua Ternak (Read-Only) ---")
    data_ternak = read_csv(LIVESTOCK_FILE)
    print_table(data_ternak, HEADERS_LIVESTOCK)


# ---------- 8. FUNGSI FITUR: ADMIN ----------

def admin_manajemen_ternak():
    """Sub-menu untuk Admin mengelola data master ternak (CRUD)."""
    while True:
        clear_screen()
        print("--- Manajemen Ternak ---")
        print("1. Tambah Ternak Baru")
        print("2. Update Data Ternak")
        print("3. Hapus Data Ternak (Terjual/Mati)")
        print("4. Kembali ke Menu Admin")
        pilihan = input("Pilihan [1-4]: ")
        
        if pilihan == '1':
            # --- CREATE (APPEND) ---
            print("\n--- 1. Tambah Ternak Baru ---")
            ternak_id = generate_id('S', LIVESTOCK_FILE, 'ternak_id')
            print(f"ID Ternak Baru (Otomatis): {ternak_id}")
            jenis = input("Jenis Ternak (Misal: Limosin): ")
            tgl_lahir = input("Tgl Lahir (YYYY-MM-DD): ") # Validasi bisa ditambahkan
            berat_awal = get_float_input("Berat Awal (kg): ")
            kandang = input("ID Kandang: ").upper()
            
            ternak_baru = {
                'ternak_id': ternak_id,
                'jenis_ternak': jenis,
                'tgl_lahir': tgl_lahir,
                'berat_sekarang': berat_awal,
                'status_kesehatan': 'Sehat', # Default
                'kandang_id': kandang
            }
            append_csv_row(LIVESTOCK_FILE, ternak_baru, HEADERS_LIVESTOCK)
            print(f"Ternak {ternak_id} berhasil ditambahkan.")
            
        elif pilihan == '2':
            # --- UPDATE (READ-MODIFY-OVERWRITE) ---
            print("\n--- 2. Update Data Ternak ---")
            print_table(read_csv(LIVESTOCK_FILE), HEADERS_LIVESTOCK)
            ternak_id = input("\nID Ternak yang akan di-update: ").upper()
            
            data = read_csv(LIVESTOCK_FILE)
            found = False
            for ternak in data:
                if ternak['ternak_id'] == ternak_id:
                    print(f"Mengubah data untuk {ternak_id}...")
                    print(f"Kandang saat ini: {ternak['kandang_id']}")
                    ternak['kandang_id'] = input("ID Kandang Baru (kosongi jika tidak berubah): ") or ternak['kandang_id']
                    
                    print(f"Status saat ini: {ternak['status_kesehatan']}")
                    ternak['status_kesehatan'] = input("Status Kesehatan Baru (kosongi jika tidak berubah): ") or ternak['status_kesehatan']
                    found = True
                    break
            
            if found:
                write_csv_overwrite(LIVESTOCK_FILE, data, HEADERS_LIVESTOCK)
                print(f"Data ternak {ternak_id} berhasil di-update.")
            else:
                print(f"Ternak {ternak_id} tidak ditemukan.")

        elif pilihan == '3':
            # --- DELETE (READ-FILTER-OVERWRITE) ---
            print("\n--- 3. Hapus Data Ternak ---")
            print_table(read_csv(LIVESTOCK_FILE), HEADERS_LIVESTOCK)
            ternak_id = input("\nID Ternak yang akan Dihapus: ").upper()
            
            data = read_csv(LIVESTOCK_FILE)
            data_baru_setelah_hapus = []
            
            # Algoritma: Baca semua, tulis ulang KECUALI yang ID-nya cocok
            for ternak in data:
                if ternak['ternak_id'] != ternak_id:
                    data_baru_setelah_hapus.append(ternak)
            
            if len(data) != len(data_baru_setelah_hapus):
                write_csv_overwrite(LIVESTOCK_FILE, data_baru_setelah_hapus, HEADERS_LIVESTOCK)
                print(f"Ternak {ternak_id} berhasil dihapus.")
            else:
                print(f"Ternak {ternak_id} tidak ditemukan.")
                
        elif pilihan == '4':
            break
        else:
            print("Pilihan tidak valid.")
        
        input("\nTekan Enter untuk kembali ke Manajemen Ternak...")


def admin_laporan_ternak():
    """
    Admin melihat laporan ternak dengan ALGORITMA SORTING.
    """
    clear_screen()
    print("--- Laporan Ternak (Sortir) ---")
    print("Urutkan berdasarkan:")
    print("1. Berat Ternak (Ringan -> Berat)")
    print("2. Berat Ternak (Berat -> Ringan)")
    print("3. Umur Ternak (Muda -> Tua)")
    print("4. Umur Ternak (Tua -> Muda)")
    pilihan = input("Pilihan [1-4]: ")
    
    data_ternak = read_csv(LIVESTOCK_FILE)
    hasil_sortir = []
    
    # Panggil Algoritma Bubble Sort
    if pilihan == '1':
        hasil_sortir = bubble_sort(data_ternak, key='berat_sekarang', reverse=False)
    elif pilihan == '2':
        hasil_sortir = bubble_sort(data_ternak, key='berat_sekarang', reverse=True)
    elif pilihan == '3':
        # Tgl lahir terbaru (muda) ke terlama (tua)
        hasil_sortir = bubble_sort(data_ternak, key='tgl_lahir', reverse=True) 
    elif pilihan == '4':
        # Tgl lahir terlama (tua) ke terbaru (muda)
        hasil_sortir = bubble_sort(data_ternak, key='tgl_lahir', reverse=False)
    else:
        print("Pilihan tidak valid. Menampilkan data standar.")
        hasil_sortir = data_ternak

    print("\n--- Hasil Laporan Terurut ---")
    print_table(hasil_sortir, HEADERS_LIVESTOCK)

def admin_cari_riwayat_kesehatan():
    """
    Admin mencari riwayat kesehatan spesifik.
    Menggunakan ALGORITMA LINEAR SEARCH.
    """
    clear_screen()
    print("--- Cari Riwayat Kesehatan Ternak ---")
    
    # Tampilkan ternak untuk memudahkan
    print_table(read_csv(LIVESTOCK_FILE), HEADERS_LIVESTOCK)
    
    ternak_id = input("\nMasukkan ID Ternak untuk melihat riwayat: ").upper()
    
    print(f"\nMenampilkan riwayat kesehatan untuk: {ternak_id}")
    
    # 1. Baca data riwayat
    data_kesehatan = read_csv(HEALTH_FILE)
    hasil_pencarian = []
    
    # 2. Algoritma Linear Search
    for record in data_kesehatan:
        if record['ternak_id'] == ternak_id:
            hasil_pencarian.append(record)
            
    # 3. Tampilkan hasil
    if hasil_pencarian:
        print_table(hasil_pencarian, HEADERS_HEALTH)
    else:
        print(f"\n[ Tidak ditemukan riwayat kesehatan untuk {ternak_id} ]")

def admin_tambah_pekerja():
    """Admin mendaftarkan akun pekerja baru."""
    clear_screen()
    print("--- Tambah Pengguna (Pekerja) Baru ---")
    username = input("Username baru: ")
    password = input("Password baru: ")
    
    # Validasi (Linear Search) untuk pastikan username unik
    users = read_csv(USERS_FILE)
    for user in users:
        if user['username'] == username:
            print(f"ERROR: Username '{username}' sudah ada. Registrasi dibatalkan.")
            return
            
    user_baru = {
        'username': username,
        'password': password,
        'role': 'pekerja'
    }
    
    append_csv_row(USERS_FILE, user_baru, HEADERS_USERS)
    print(f"Akun pekerja '{username}' berhasil didaftarkan.")

# ---------- 9. FUNGSI MENU UTAMA (Navigasi) ----------

def menu_admin(username):
    """Menampilkan menu utama untuk Admin."""
    while True:
        clear_screen()
        print(f"--- Menu Admin (Login sebagai: {username}) ---")
        print("1. Manajemen Ternak (Tambah/Update/Hapus)")
        print("2. Lihat Laporan Ternak (Sortir)")
        print("3. Lihat Riwayat Kesehatan Ternak (Search)")
        print("4. Lihat Log Pemberian Pakan")
        print("5. Manajemen Pengguna (Tambah Pekerja)")
        print("6. Logout")
        
        pilihan = input("Pilihan [1-6]: ")
        
        if pilihan == '1':
            admin_manajemen_ternak()
        elif pilihan == '2':
            admin_laporan_ternak()
        elif pilihan == '3':
            admin_cari_riwayat_kesehatan()
        elif pilihan == '4':
            clear_screen()
            print("--- Log Pemberian Pakan ---")
            print_table(read_csv(FEEDING_FILE), HEADERS_FEEDING)
        elif pilihan == '5':
            admin_tambah_pekerja()
        elif pilihan == '6':
            print("Logout berhasil.")
            break
        else:
            print("Pilihan tidak valid.")
            
        input("\nTekan Enter untuk kembali ke menu...")

def menu_pekerja(username):
    """Menampilkan menu utama untuk Pekerja."""
    while True:
        clear_screen()
        print(f"--- Menu Pekerja (Login sebagai: {username}) ---")
        print("1. Catat Cek Kesehatan Harian")
        print("2. Catat Pemberian Pakan")
        print("3. Update Bobot Ternak (Timbang)")
        print("4. Lihat Daftar Semua Ternak (Read-only)")
        print("5. Logout")
        
        pilihan = input("Pilihan [1-5]: ")
        
        if pilihan == '1':
            pekerja_catat_kesehatan(username)
        elif pilihan == '2':
            pekerja_catat_pakan(username)
        elif pilihan == '3':
            pekerja_update_bobot()
        elif pilihan == '4':
            pekerja_lihat_ternak()
        elif pilihan == '5':
            print("Logout berhasil.")
            break
        else:
            print("Pilihan tidak valid.")
        
        input("\nTekan Enter untuk kembali ke menu...")

# ---------- 10. FUNGSI MAIN (Titik Awal Program) ----------

def main():
    """Fungsi utama untuk menjalankan program."""
    
    # 1. Siapkan file CSV (buat jika belum ada)
    setup_files()
    
    # 2. Loop Program Utama
    while True:
        clear_screen()
        print("========================================")
        print("  Selamat Datang di SimTernak v1.0")
        print("========================================")
        print("1. Login")
        print("2. Exit")
        
        pilihan_utama = input("Pilihan [1-2]: ")
        
        if pilihan_utama == '1':
            # 3. Proses Login
            username, role = fungsi_login()
            
            # 4. Arahkan ke menu yang sesuai
            if role == 'admin':
                menu_admin(username)
            elif role == 'pekerja':
                menu_pekerja(username)
            else:
                input("\nTekan Enter untuk mencoba login kembali...")
                
        elif pilihan_utama == '2':
            print("Terima kasih telah menggunakan SimTernak.")
            break
        else:
            print("Pilihan tidak valid.")
            input("\nTekan Enter untuk melanjutkan...")

# --- Menjalankan Program ---
if __name__ == "__main__":
    main()