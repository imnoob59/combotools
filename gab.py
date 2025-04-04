import os
import sys
import re
from collections import defaultdict

def combine_combolists(input_files, output_file, remove_duplicates=True):
    combined_combos = set() if remove_duplicates else []
    total_combos = 0
    duplicate_count = 0
    processed_files = 0
    
    for file_path in input_files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                print(f"Memproses file: {os.path.basename(file_path)}...")
                lines = f.readlines()
                
                for line in lines:
                    line = line.strip()
                    if not line or ':' not in line:
                        continue
                        
                    total_combos += 1
                    
                    if remove_duplicates:
                        if line not in combined_combos:
                            combined_combos.add(line)
                        else:
                            duplicate_count += 1
                    else:
                        combined_combos.append(line)
                
                processed_files += 1
                
        except Exception as e:
            print(f"  Gagal memproses {os.path.basename(file_path)}: {str(e)}")
            continue
    
    # Menulis ke file output
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(sorted(combined_combos)))
            
        print("\n" + "="*50)
        print("LAPORAN PENGGABUNGAN".center(50))
        print("="*50)
        print(f"▪ Total file diproses: {len(input_files)}")
        print(f"▪ File berhasil dibaca: {processed_files}")
        print(f"▪ Total kombinasi ditemukan: {total_combos:,}")
        if remove_duplicates:
            print(f"▪ Duplikat dihapus: {duplicate_count:,}")
            print(f"▪ Kombinasi unik tersimpan: {len(combined_combos):,}")
        print(f"\nFile output disimpan di:\n{os.path.abspath(output_file)}")
        print("="*50)
        
    except Exception as e:
        print(f"Error saat menyimpan file output: {str(e)}")

def parse_drag_and_drop():
    """
    Parse argumen command line untuk drag and drop di Windows
    """
    if len(sys.argv) > 1:
        files = []
        for arg in sys.argv[1:]:
            # Bersihkan path dari tanda kutip
            clean_path = arg.strip('"')
            if os.path.isfile(clean_path):
                files.append(clean_path)
            elif os.path.isdir(clean_path):
                # Jika yang di-drop adalah folder, tambahkan semua file .txt di dalamnya
                for root, _, filenames in os.walk(clean_path):
                    for filename in filenames:
                        if filename.lower().endswith('.txt'):
                            files.append(os.path.join(root, filename))
        return files
    return None

def main():
    print("=== COMBOLIST MERGER PLUS ===")
    print("Gabungkan banyak file email:pass sekaligus\n")
    
    # Cek drag and drop
    input_files = parse_drag_and_drop()
    
    if input_files:
        print(f"Deteksi {len(input_files)} file dari drag & drop:")
        for i, f in enumerate(input_files, 1):
            print(f"{i}. {f}")
        confirm = input("\nGunakan file-file ini? (Y/n): ").strip().lower()
        if confirm == 'n':
            input_files = None
    
    if not input_files:
        # Mode input manual
        print("\nMasukkan path file (pisahkan dengan koma atau spasi):")
        print("Contoh: C:\\file1.txt C:\\file2.txt")
        print("Atau drag & drop file(s) langsung ke jendela terminal\n")
        
        input_str = input("File(s): ").strip()
        if not input_str:
            print("Tidak ada file yang dimasukkan!")
            return
            
        # Pisahkan path yang mengandung spasi
        input_files = re.split(r'[,\s]+', input_str)
        input_files = [f.strip('"') for f in input_files if f.strip()]
    
    # Validasi file
    valid_files = []
    for f in input_files:
        if os.path.isfile(f):
            valid_files.append(f)
        else:
            print(f"File tidak ditemukan: {f}")
    
    if not valid_files:
        print("Tidak ada file valid yang diproses!")
        return
    
    # Nama file output
    default_output = "combined_combos.txt"
    print(f"\nFile output akan disimpan sebagai: {default_output}")
    output_file = input("Nama file output (Enter untuk default): ").strip() or default_output
    
    # Opsi hapus duplikat
    remove_dup = input("Hapus duplikat? (Y/n): ").strip().lower()
    remove_duplicates = not (remove_dup == 'n' or remove_dup == 'no')
    
    # Proses penggabungan
    combine_combolists(valid_files, output_file, remove_duplicates)
    
    # Menjaga terminal tetap terbuka di Windows
    if os.name == 'nt':
        input("\nTekan Enter untuk keluar...")

if __name__ == "__main__":
    main()
