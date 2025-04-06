import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
import os
import re
from collections import defaultdict

class ComboManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ComboList Manager Pro")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # Variables
        self.input_file = tk.StringVar()
        self.output_dir = tk.StringVar(value=str(Path.home() / "ComboResults"))
        self.status_text = tk.StringVar(value="Ready")
        
        self.create_main_menu()
        self.create_widgets()
    
    def configure_styles(self):
        self.style.configure('TFrame', background='#f5f5f5')
        self.style.configure('TLabel', background='#f5f5f5', font=('Segoe UI', 10))
        self.style.configure('TButton', font=('Segoe UI', 10), padding=5)
        self.style.configure('Accent.TButton', foreground='white', background='#4CAF50')
        self.style.configure('Primary.TButton', foreground='white', background='#2196F3')
        self.style.configure('TNotebook', background='#f5f5f5')
        self.style.configure('TNotebook.Tab', font=('Segoe UI', 10, 'bold'))
        self.style.map('TNotebook.Tab', background=[('selected', '#f5f5f5')])
    
    def create_main_menu(self):
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open Combo File", command=self.browse_file)
        file_menu.add_command(label="Set Output Directory", command=self.browse_dir)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="Combo Splitter", command=lambda: self.show_tab(0))
        tools_menu.add_command(label="Combo Sorter", command=lambda: self.show_tab(1))
        tools_menu.add_command(label="Duplicate Remover", command=lambda: self.show_tab(2))
        tools_menu.add_command(label="Combo Merger", command=lambda: self.show_tab(3))
        menubar.add_cascade(label="Tools", menu=tools_menu)
        
        self.root.config(menu=menubar)
    
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Notebook (Tabbed interface)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Combo Splitter
        self.create_splitter_tab()
        
        # Tab 2: Combo Sorter
        self.create_sorter_tab()
        
        # Tab 3: Duplicate Remover
        self.create_duplicate_remover_tab()
        
        # Tab 4: Combo Merger
        self.create_merger_tab()
        
        # Status bar
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        ttk.Label(status_frame, textvariable=self.status_text, relief=tk.SUNKEN, anchor=tk.W).pack(fill=tk.X)
    
    def create_splitter_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Combo Splitter")
        
        # Variables
        self.split_prefix = tk.StringVar(value="combo")
        self.lines_per_file = tk.IntVar(value=1000)
        
        # Content
        ttk.Label(tab, text="Split ComboList into multiple files", font=('Segoe UI', 12)).pack(pady=10)
        
        input_frame = ttk.Frame(tab)
        input_frame.pack(fill=tk.X, pady=5)
        ttk.Label(input_frame, text="Input File:").pack(side=tk.LEFT)
        ttk.Entry(input_frame, textvariable=self.input_file, width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(input_frame, text="Browse", command=self.browse_file).pack(side=tk.LEFT)
        
        output_frame = ttk.Frame(tab)
        output_frame.pack(fill=tk.X, pady=5)
        ttk.Label(output_frame, text="Output Folder:").pack(side=tk.LEFT)
        ttk.Entry(output_frame, textvariable=self.output_dir, width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(output_frame, text="Browse", command=self.browse_dir).pack(side=tk.LEFT)
        
        settings_frame = ttk.Frame(tab)
        settings_frame.pack(fill=tk.X, pady=5)
        ttk.Label(settings_frame, text="File Prefix:").pack(side=tk.LEFT)
        ttk.Entry(settings_frame, textvariable=self.split_prefix, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Label(settings_frame, text="Lines per File:").pack(side=tk.LEFT, padx=(20,5))
        ttk.Spinbox(settings_frame, from_=1, to=100000, textvariable=self.lines_per_file, width=10).pack(side=tk.LEFT)
        
        ttk.Button(tab, text="Split Files", command=self.process_split, style='Accent.TButton').pack(pady=20)
    
    def create_sorter_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Combo Sorter")
        
        # Variables
        self.sort_prefix = tk.StringVar(value="sorted")
        
        # Content
        ttk.Label(tab, text="Sort ComboList by Domain", font=('Segoe UI', 12)).pack(pady=10)
        
        input_frame = ttk.Frame(tab)
        input_frame.pack(fill=tk.X, pady=5)
        ttk.Label(input_frame, text="Input File:").pack(side=tk.LEFT)
        ttk.Entry(input_frame, textvariable=self.input_file, width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(input_frame, text="Browse", command=self.browse_file).pack(side=tk.LEFT)
        
        output_frame = ttk.Frame(tab)
        output_frame.pack(fill=tk.X, pady=5)
        ttk.Label(output_frame, text="Output Folder:").pack(side=tk.LEFT)
        ttk.Entry(output_frame, textvariable=self.output_dir, width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(output_frame, text="Browse", command=self.browse_dir).pack(side=tk.LEFT)
        
        settings_frame = ttk.Frame(tab)
        settings_frame.pack(fill=tk.X, pady=5)
        ttk.Label(settings_frame, text="File Prefix:").pack(side=tk.LEFT)
        ttk.Entry(settings_frame, textvariable=self.sort_prefix, width=15).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(tab, text="Sort by Domain", command=self.process_sort, style='Primary.TButton').pack(pady=20)
        
        # Log area
        self.sort_log = scrolledtext.ScrolledText(tab, height=10, wrap=tk.WORD)
        self.sort_log.pack(fill=tk.BOTH, expand=True, pady=10)
        self.sort_log.insert(tk.END, "Logs will appear here...")
        self.sort_log.config(state=tk.DISABLED)
    
    def create_duplicate_remover_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Duplicate Remover")
        
        # Content
        ttk.Label(tab, text="Remove Duplicate Combos", font=('Segoe UI', 12)).pack(pady=10)
        
        input_frame = ttk.Frame(tab)
        input_frame.pack(fill=tk.X, pady=5)
        ttk.Label(input_frame, text="Input File:").pack(side=tk.LEFT)
        ttk.Entry(input_frame, textvariable=self.input_file, width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(input_frame, text="Browse", command=self.browse_file).pack(side=tk.LEFT)
        
        output_frame = ttk.Frame(tab)
        output_frame.pack(fill=tk.X, pady=5)
        ttk.Label(output_frame, text="Output File:").pack(side=tk.LEFT)
        self.dedup_output = ttk.Entry(output_frame, width=50)
        self.dedup_output.pack(side=tk.LEFT, padx=5)
        self.dedup_output.insert(0, "deduplicated_combos.txt")
        
        ttk.Button(tab, text="Remove Duplicates", command=self.process_dedupe, style='Primary.TButton').pack(pady=20)
        
        # Stats frame
        self.dedup_stats = ttk.Label(tab, text="", font=('Segoe UI', 10))
        self.dedup_stats.pack(pady=5)
    
    def create_merger_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Combo Merger")
        
        # Variables
        self.merge_files = []
        
        # Content
        ttk.Label(tab, text="Merge Multiple Combo Files", font=('Segoe UI', 12)).pack(pady=10)
        
        # File listbox
        self.merge_listbox = tk.Listbox(tab, selectmode=tk.EXTENDED, height=8)
        self.merge_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Button frame
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="Add Files", command=self.add_merge_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Remove Selected", command=self.remove_merge_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear All", command=self.clear_merge_files).pack(side=tk.LEFT, padx=5)
        
        # Output frame
        output_frame = ttk.Frame(tab)
        output_frame.pack(fill=tk.X, pady=5)
        ttk.Label(output_frame, text="Output File:").pack(side=tk.LEFT)
        self.merge_output = ttk.Entry(output_frame, width=50)
        self.merge_output.pack(side=tk.LEFT, padx=5)
        self.merge_output.insert(0, "merged_combos.txt")
        
        ttk.Button(tab, text="Merge Files", command=self.process_merge, style='Accent.TButton').pack(pady=20)
        
        # Stats frame
        self.merge_stats = ttk.Label(tab, text="", font=('Segoe UI', 10))
        self.merge_stats.pack(pady=5)
    
    def show_tab(self, tab_index):
        self.notebook.select(tab_index)
    
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select ComboList File",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if file_path:
            self.input_file.set(file_path)
    
    def browse_dir(self):
        dir_path = filedialog.askdirectory(
            title="Select Output Directory",
            initialdir=self.output_dir.get()
        )
        if dir_path:
            self.output_dir.set(dir_path)
    
    def add_merge_files(self):
        files = filedialog.askopenfilenames(
            title="Select Combo Files to Merge",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if files:
            for file in files:
                if file not in self.merge_files:
                    self.merge_files.append(file)
                    self.merge_listbox.insert(tk.END, file)
    
    def remove_merge_files(self):
        selected = self.merge_listbox.curselection()
        for index in selected[::-1]:
            self.merge_files.pop(index)
            self.merge_listbox.delete(index)
    
    def clear_merge_files(self):
        self.merge_files = []
        self.merge_listbox.delete(0, tk.END)
    
    def process_split(self):
        input_path = self.input_file.get()
        output_dir = self.output_dir.get()
        prefix = self.split_prefix.get()
        lines_per_file = self.lines_per_file.get()
        
        if not input_path:
            messagebox.showerror("Error", "Please select an input file")
            return
        
        try:
            # Create output directory if it doesn't exist
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            # Read input file
            with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = [line.strip() for line in f if line.strip()]
            
            total_files = (len(lines) // lines_per_file) + (1 if len(lines) % lines_per_file else 0)
            
            # Process with progress bar
            progress = tk.Toplevel(self.root)
            progress.title("Processing...")
            progress.geometry("400x100")
            progress.resizable(False, False)
            
            tk.Label(progress, text=f"Splitting {len(lines)} lines into {total_files} files...").pack(pady=10)
            pb = ttk.Progressbar(progress, orient=tk.HORIZONTAL, length=300, mode='determinate')
            pb.pack(pady=5)
            pb['maximum'] = total_files
            self.root.update()
            
            # Split and write files
            for i in range(total_files):
                start = i * lines_per_file
                end = start + lines_per_file
                chunk = lines[start:end]
                
                output_file = Path(output_dir) / f"{prefix}_{i+1}.txt"
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(chunk))
                
                pb['value'] = i + 1
                progress.update()
            
            progress.destroy()
            messagebox.showinfo("Success", f"Successfully created {total_files} files in:\n{output_dir}")
            self.status_text.set(f"Completed: Split into {total_files} files")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
            self.status_text.set("Error occurred")
    
    def process_sort(self):
        input_path = self.input_file.get()
        output_dir = self.output_dir.get()
        prefix = self.sort_prefix.get()
        
        if not input_path:
            messagebox.showerror("Error", "Please select an input file")
            return
        
        try:
            # Create output directory if it doesn't exist
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            # Read input file and extract domains
            domain_combos = defaultdict(list)
            total_combos = 0
            unique_domains = set()
            
            with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Extract email (assuming format email:pass)
                    if ':' in line:
                        email = line.split(':', 1)[0]
                        # Extract domain from email
                        if '@' in email:
                            domain = email.split('@')[-1].lower()
                            domain_combos[domain].append(line)
                            unique_domains.add(domain)
                            total_combos += 1
            
            # Write sorted files
            self.sort_log.config(state=tk.NORMAL)
            self.sort_log.delete(1.0, tk.END)
            self.sort_log.insert(tk.END, f"Processing {total_combos} combos from {len(unique_domains)} domains...\n\n")
            
            for domain in sorted(domain_combos.keys()):
                output_file = Path(output_dir) / f"{prefix}_{domain}.txt"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(domain_combos[domain]))
                
                self.sort_log.insert(tk.END, f"Created: {output_file} ({len(domain_combos[domain])} combos)\n")
                self.sort_log.see(tk.END)
                self.root.update()
            
            self.sort_log.insert(tk.END, f"\nSorting completed! {len(unique_domains)} files created.")
            self.sort_log.config(state=tk.DISABLED)
            
            messagebox.showinfo("Success", f"Successfully sorted combos by {len(unique_domains)} domains")
            self.status_text.set(f"Completed: Sorted by {len(unique_domains)} domains")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
            self.status_text.set("Error occurred")
    
    def process_dedupe(self):
        input_path = self.input_file.get()
        output_file = self.dedup_output.get()
        
        if not input_path:
            messagebox.showerror("Error", "Please select an input file")
            return
        
        try:
            # Read and deduplicate
            unique_combos = set()
            total_count = 0
            
            with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        unique_combos.add(line)
                        total_count += 1
            
            # Write output
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(unique_combos))
            
            # Show stats
            removed = total_count - len(unique_combos)
            self.dedup_stats.config(
                text=f"Removed {removed} duplicates ({len(unique_combos)} unique combos saved)"
            )
            
            messagebox.showinfo("Success", f"Removed {removed} duplicates\nSaved {len(unique_combos)} unique combos")
            self.status_text.set(f"Completed: Removed {removed} duplicates")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
            self.status_text.set("Error occurred")
    
    def process_merge(self):
        if not self.merge_files:
            messagebox.showerror("Error", "Please add files to merge")
            return
        
        output_file = self.merge_output.get()
        
        try:
            # Read all files and merge
            all_combos = set()
            total_files = 0
            total_combos = 0
            
            for file in self.merge_files:
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            all_combos.add(line)
                            total_combos += 1
                total_files += 1
            
            # Write output
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(all_combos))
            
            # Show stats
            unique_combos = len(all_combos)
            self.merge_stats.config(
                text=f"Merged {total_files} files with {total_combos} total combos\n"
                     f"Saved {unique_combos} unique combos (removed {total_combos - unique_combos} duplicates)"
            )
            
            messagebox.showinfo("Success", 
                f"Merged {total_files} files\n"
                f"Total combos: {total_combos}\n"
                f"Unique combos: {unique_combos}"
            )
            self.status_text.set(f"Completed: Merged {total_files} files")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
            self.status_text.set("Error occurred")

if __name__ == "__main__":
    root = tk.Tk()
    app = ComboManagerApp(root)
    root.mainloop()
