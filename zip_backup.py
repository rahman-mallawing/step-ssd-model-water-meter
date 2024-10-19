# Cara menjalankan program:
# 1. Menjalankan program dengan versi saja (tanpa opsi minimal):
#    last_step = get_last_step()

# Definisikan direktori penyimpanan zip
#    dir_path = '/content/gdrive/MyDrive/WaterMeterVersion'

#     Menjalankan zip_backup.py dengan argumen versi dan direktori
#    !python zip_backup.py --v=backup_{last_step} --dir={dir_path}
#
# 2. Menjalankan program dengan versi dan opsi minimal (menggunakan files_to_zip_minimal):
#    !python zip_backup.py --v=backup_{last_step} --dir={dir_path} --minimal

import os
import datetime
import zipfile
import argparse
import pytz

# Folder lokasi file dan folder yang akan di-zip
folder_path = '/content/'
files_to_zip = [
    folder_path + 'images/',
    folder_path + 'models/',
    folder_path + 'training/',
    folder_path + "create_csv.py",
    folder_path + "create_tfrecord.py",
    folder_path + "labelmap.pbtxt",
    folder_path + "labelmap.txt",
    folder_path + "train_val_test_split.py",
    folder_path + "train.tfrecord",
    folder_path + "val.tfrecord",
    folder_path + "backup_info.txt",
    folder_path + "read_last_step_train.py",
    folder_path + "zip_backup.py"
]

# Daftar file minimal yang di-zip jika argumen 'minimal' diberikan
files_to_zip_minimal = [
    folder_path + 'models/',
    folder_path + 'training/',
    folder_path + "backup_info.txt",
    folder_path + "read_last_step_train.py",
    folder_path + "zip_backup.py"
]

# Fungsi untuk membuat file info.txt
def create_info_file(version):
    """Membuat atau memperbarui file info.txt dengan informasi versi yang diinput, tanggal, dan waktu"""
    file_name = "backup_info.txt"

    # Dapatkan waktu dengan zona waktu GMT+8 (Asia/Singapore atau Asia/Makassar)
    tz = pytz.timezone('Asia/Singapore')
    waktu_sekarang = datetime.datetime.now(tz)

    # Cek apakah file sudah ada
    if os.path.exists(file_name):
        # Jika file ada, tambahkan informasi baru di akhir file
        with open(file_name, "a") as f:  # 'a' untuk append mode
            f.write(f"\n-- Additional Backup Information --\n")
            f.write(f"Version: {version}\n")
            f.write(f"Tanggal dan waktu: {waktu_sekarang}\n")
    else:
        # Jika file tidak ada, buat file baru dan tuliskan informasi
        with open(file_name, "w") as f:  # 'w' untuk write mode (file baru)
            f.write("Program Water-Meter\n")
            f.write(f"Version: {version}\n")
            f.write(f"Tanggal dan waktu: {waktu_sekarang}\n")
    
    return file_name

# Fungsi untuk membuat ZIP file
def create_zip(files_to_zip, version, zip_save_path, zip_file_name="archive.zip"):
    """Membuat file ZIP yang berisi file-file dan folder-folder yang ditentukan"""
    zip_file_path = os.path.join(zip_save_path, zip_file_name)
    
    with zipfile.ZipFile(zip_file_path, 'w') as zipObj:
        # Tambahkan info.txt satu kali di root ZIP
        info_file_path = os.path.join(os.getcwd(), "backup_info.txt")
        zipObj.write(info_file_path, "info.txt")
        
        for file in files_to_zip:
            # Jika path adalah folder, zip semua file di dalam folder
            if os.path.isdir(file):
                for foldername, subfolders, filenames in os.walk(file):
                    for filename in filenames:
                        file_path = os.path.join(foldername, filename)
                        # Tambahkan file ke dalam ZIP, pertahankan struktur folder
                        zipObj.write(file_path, os.path.relpath(file_path, folder_path))
            else:
                # Jika file, tambahkan langsung
                zipObj.write(file, os.path.relpath(file, folder_path))
    
    return zip_file_path

def main():
    # Parsing argumen menggunakan argparse
    parser = argparse.ArgumentParser(description="Backup ZIP Script")
    parser.add_argument('--v', type=str, required=True, help='Version name for the backup')
    parser.add_argument('--dir', type=str, default='/content/gdrive/MyDrive/WaterMeterVersion', help='Directory where the ZIP file will be saved')
    parser.add_argument('--minimal', action='store_true', help='Use minimal set of files to zip')

    args = parser.parse_args()
    
    version = args.v
    zip_save_path = args.dir
    archive = "WaterMeter"
    
    # Pilih file minimal atau tidak
    if args.minimal:
        files_to_use = files_to_zip_minimal
        zip_file_name = f"{archive}-{version}-minimal.zip"
    else:
        files_to_use = files_to_zip        
        zip_file_name = f"{archive}-{version}.zip"

    # Buat file info
    info_file = create_info_file(version)
    
    # Tambahkan file info dan file lainnya ke dalam ZIP
    zip_file_path = create_zip([info_file] + files_to_use, version, zip_save_path, zip_file_name)
    
    print(f"File ZIP '{zip_file_path}' telah dibuat!")

if __name__ == "__main__":
    main()
