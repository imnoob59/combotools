import os
from collections import defaultdict

def sort_combo_by_domain(input_file, output_folder, remove_duplicates=True):
    # Membersihkan path input dari tanda kutip jika ada
    input_file = input_file.strip('"')
    
    # Memeriksa apakah file input ada
    if not os.path.exists(input_file):
        print(f"Error: File not found - {input_file}")
        return
    
    try:
        # Membaca file input
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    # Membuat dictionary untuk menyimpan email berdasarkan domain
    domain_dict = defaultdict(set) if remove_duplicates else defaultdict(list)
    
    total_lines = 0
    valid_lines = 0
    duplicate_lines = 0
    seen_combos = set()

    for line in lines:
        total_lines += 1
        line = line.strip()
        if not line:
            continue
        
        # Split email:password
        if ':' in line:
            parts = line.split(':', 1)
            if len(parts) == 2:
                email, password = parts
                combo = f"{email}:{password}"
            else:
                continue
        else:
            continue
        
        # Validasi email dan ekstrak domain
        if '@' in email:
            domain = email.split('@')[-1].lower().strip()
            if domain:  # Pastikan domain tidak kosong
                if remove_duplicates:
                    if combo not in seen_combos:
                        seen_combos.add(combo)
                        domain_dict[domain].add(combo)
                        valid_lines += 1
                    else:
                        duplicate_lines += 1
                else:
                    domain_dict[domain].append(combo)
                    valid_lines += 1
    
    # Membuat folder output jika belum ada
    if not os.path.exists(output_folder):
        try:
            os.makedirs(output_folder)
        except Exception as e:
            print(f"Error creating output folder: {e}")
            return
    
    # Menyimpan ke file berdasarkan domain
    for domain, combos in domain_dict.items():
        # Membuat nama file yang aman untuk domain
        safe_domain = "".join(c for c in domain if c.isalnum() or c in ('.', '-', '_')).rstrip('.')
        output_file = os.path.join(output_folder, f"{safe_domain}.txt")
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                if remove_duplicates:
                    f.write('\n'.join(combos))
                else:
                    f.write('\n'.join(combos))
        except Exception as e:
            print(f"Error writing file for domain {domain}: {e}")
    
    # Hasil statistik
    print("\nProcessing completed:")
    print(f"Total lines processed: {total_lines}")
    print(f"Valid email:pass combos found: {valid_lines}")
    if remove_duplicates:
        print(f"Duplicate combos removed: {duplicate_lines}")
    print(f"Unique domains found: {len(domain_dict)}")
    print(f"Files saved to: {os.path.abspath(output_folder)}")

if __name__ == "__main__":
    print("ComboList Sorter by Domain with Duplicate Removal")
    print("------------------------------------------------")
    
    # Input file path
    input_filename = input("Enter input file name/path: ").strip().strip('"')
    
    # Output folder
    default_output = "sorted_domains"
    output_folder = input(f"Enter output folder name (default: {default_output}): ").strip() or default_output
    
    # Opsi hapus duplikat
    remove_dup = input("Remove duplicate combos? (Y/n): ").strip().lower()
    remove_duplicates = not (remove_dup == 'n' or remove_dup == 'no')
    
    sort_combo_by_domain(input_filename, output_folder, remove_duplicates)
    
    # Menjaga terminal tetap terbuka di Windows
    if os.name == 'nt':
        input("\nPress Enter to exit...")
