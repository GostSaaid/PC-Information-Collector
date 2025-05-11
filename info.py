import platform
import socket
import psutil
import uuid
import datetime
import tkinter as tk
from tkinter import ttk, messagebox

class PCInfoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PC Information Collector")
        self.root.geometry("800x600")
        
        # Create main container
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_system_tab()
        self.create_cpu_tab()
        self.create_memory_tab()
        self.create_disk_tab()
        self.create_network_tab()
        
        # Add refresh button
        self.refresh_btn = ttk.Button(self.main_frame, text="Refresh", command=self.refresh_all)
        self.refresh_btn.pack(pady=5)
        
        # Add save button
        self.save_btn = ttk.Button(self.main_frame, text="Save to File", command=self.save_to_file)
        self.save_btn.pack(pady=5)
        
        # Initial data load
        self.refresh_all()
    
    def create_system_tab(self):
        self.system_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.system_tab, text="System")
        
        # System info treeview
        self.system_tree = ttk.Treeview(self.system_tab, columns=('value'), show='tree')
        self.system_tree.heading('#0', text='Property', anchor=tk.W)
        self.system_tree.heading('value', text='Value', anchor=tk.W)
        self.system_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.system_tab, orient="vertical", command=self.system_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.system_tree.configure(yscrollcommand=scrollbar.set)
    
    def create_cpu_tab(self):
        self.cpu_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.cpu_tab, text="CPU")
        
        self.cpu_tree = ttk.Treeview(self.cpu_tab, columns=('value'), show='tree')
        self.cpu_tree.heading('#0', text='Property', anchor=tk.W)
        self.cpu_tree.heading('value', text='Value', anchor=tk.W)
        self.cpu_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(self.cpu_tab, orient="vertical", command=self.cpu_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.cpu_tree.configure(yscrollcommand=scrollbar.set)
    
    def create_memory_tab(self):
        self.memory_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.memory_tab, text="Memory")
        
        self.memory_tree = ttk.Treeview(self.memory_tab, columns=('value'), show='tree')
        self.memory_tree.heading('#0', text='Property', anchor=tk.W)
        self.memory_tree.heading('value', text='Value', anchor=tk.W)
        self.memory_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(self.memory_tab, orient="vertical", command=self.memory_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.memory_tree.configure(yscrollcommand=scrollbar.set)
    
    def create_disk_tab(self):
        self.disk_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.disk_tab, text="Disks")
        
        # Disk info treeview
        self.disk_tree = ttk.Treeview(self.disk_tab, columns=('value'), show='tree')
        self.disk_tree.heading('#0', text='Disk', anchor=tk.W)
        self.disk_tree.heading('value', text='Details', anchor=tk.W)
        self.disk_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(self.disk_tab, orient="vertical", command=self.disk_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.disk_tree.configure(yscrollcommand=scrollbar.set)
    
    def create_network_tab(self):
        self.network_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.network_tab, text="Network")
        
        self.network_tree = ttk.Treeview(self.network_tab, columns=('value'), show='tree')
        self.network_tree.heading('#0', text='Property', anchor=tk.W)
        self.network_tree.heading('value', text='Value', anchor=tk.W)
        self.network_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(self.network_tab, orient="vertical", command=self.network_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.network_tree.configure(yscrollcommand=scrollbar.set)
    
    def get_system_info(self):
        try:
            info = {}
            
            # System Information
            info['System'] = platform.system()
            info['Node Name'] = platform.node()
            info['Release'] = platform.release()
            info['Version'] = platform.version()
            info['Machine'] = platform.machine()
            info['Processor'] = platform.processor()
            
            # Boot Time
            boot_time = psutil.boot_time()
            info['Boot Time'] = datetime.datetime.fromtimestamp(boot_time).strftime("%Y-%m-%d %H:%M:%S")
            
            # CPU Information
            info['Physical Cores'] = psutil.cpu_count(logical=False)
            info['Total Cores'] = psutil.cpu_count(logical=True)
            info['CPU Usage'] = f"{psutil.cpu_percent(interval=1)}%"
            
            # Memory Information
            mem = psutil.virtual_memory()
            info['Total Memory'] = f"{mem.total / (1024**3):.2f} GB"
            info['Available Memory'] = f"{mem.available / (1024**3):.2f} GB"
            info['Used Memory'] = f"{mem.used / (1024**3):.2f} GB"
            info['Memory Percentage'] = f"{mem.percent}%"
            
            # Disk Information
            partitions = psutil.disk_partitions()
            disk_info = []
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_info.append({
                        'Device': partition.device,
                        'Mountpoint': partition.mountpoint,
                        'File System': partition.fstype,
                        'Total Size': f"{usage.total / (1024**3):.2f} GB",
                        'Used': f"{usage.used / (1024**3):.2f} GB",
                        'Free': f"{usage.free / (1024**3):.2f} GB",
                        'Percentage': f"{usage.percent}%"
                    })
                except:
                    continue
            info['Disks'] = disk_info
            
            # Network Information
            info['Hostname'] = socket.gethostname()
            info['IP Address'] = socket.gethostbyname(socket.gethostname())
            info['MAC Address'] = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) 
                                         for ele in range(0,8*6,8)][::-1])
            
            # Additional Info
            info['Current User'] = psutil.Process().username()
            info['System Uptime'] = str(datetime.datetime.now() - datetime.datetime.fromtimestamp(boot_time))
            
            return info
        
        except Exception as e:
            return f"Error collecting system information: {str(e)}"
    
    def refresh_all(self):
        system_info = self.get_system_info()
        
        if isinstance(system_info, dict):
            # Clear all trees
            for tree in [self.system_tree, self.cpu_tree, self.memory_tree, self.disk_tree, self.network_tree]:
                for item in tree.get_children():
                    tree.delete(item)
            
            # Populate system tab
            for key, value in system_info.items():
                if key in ['System', 'Node Name', 'Release', 'Version', 'Machine', 'Processor', 
                          'Boot Time', 'Current User', 'System Uptime']:
                    self.system_tree.insert('', 'end', text=key, values=(value,))
                
                # CPU tab
                if key in ['Physical Cores', 'Total Cores', 'CPU Usage']:
                    self.cpu_tree.insert('', 'end', text=key, values=(value,))
                
                # Memory tab
                if key in ['Total Memory', 'Available Memory', 'Used Memory', 'Memory Percentage']:
                    self.memory_tree.insert('', 'end', text=key, values=(value,))
                
                # Network tab
                if key in ['Hostname', 'IP Address', 'MAC Address']:
                    self.network_tree.insert('', 'end', text=key, values=(value,))
            
            # Populate disk tab
            for disk in system_info.get('Disks', []):
                disk_node = self.disk_tree.insert('', 'end', text=disk['Device'], values=("",))
                for prop, value in disk.items():
                    if prop != 'Device':
                        self.disk_tree.insert(disk_node, 'end', text=prop, values=(value,))
        else:
            messagebox.showerror("Error", system_info)
    
    def save_to_file(self):
        try:
            system_info = self.get_system_info()
            if isinstance(system_info, str):  # If it's an error message
                raise Exception(system_info)
                
            filename = "system_info.txt"
            with open(filename, 'w') as f:
                for key, value in system_info.items():
                    if key == 'Disks':
                        f.write("\nDisk Information:\n")
                        for disk in value:
                            for k, v in disk.items():
                                f.write(f"  {k}: {v}\n")
                            f.write("\n")
                    else:
                        f.write(f"{key}: {value}\n")
            messagebox.showinfo("Success", f"Information saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PCInfoApp(root)
    root.mainloop()