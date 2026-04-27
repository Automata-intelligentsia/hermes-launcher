#!/usr/bin/env python3
"""
Quick Launch for Hermes Agent - Single-file launcher for Hermes Agent ecosystem
A sleek, dark-themed GUI for managing Hermes services with auto-discovery
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import subprocess
import threading
import time
import json
import os
import urllib.request
from datetime import datetime
from pathlib import Path

# === Configuration ===
CONFIG_FILE = os.path.expanduser("~/.hermes/launcher-config.json")
LOG_FILE = os.path.expanduser("~/.hermes/logs/launcher-health.log")
THEME = {
    "bg": "#0a0a0f",
    "fg": "#e0e0e0",
    "accent": "#00d4ff",
    "accent2": "#7c3aed",
    "success": "#22c55e",
    "error": "#ef4444",
    "warning": "#f59e0b",
    "card_bg": "#12121a",
    "border": "#1e1e2e",
    "font_main": ("Inter", 10),
    "font_header": ("Inter", 11, "bold"),
    "font_title": ("Inter", 18, "bold"),
}

# Default services that ship with the launcher
DEFAULT_SERVICES = {
    "gateway": {
        "name": "Hermes Gateway",
        "port": 8653,
        "health_url": "http://127.0.0.1:8653/health",
        "script": "~/.local/bin/hermes-gateway",
        "enabled": True,
        "category": "core"
    },
    "dashboard": {
        "name": "Hermes Dashboard",
        "port": 9119,
        "health_url": "http://127.0.0.1:9119",
        "script": "~/.local/bin/hermes-dashboard",
        "enabled": True,
        "category": "core"
    },
    "workspace": {
        "name": "Hermes Workspace",
        "port": 3000,
        "health_url": "http://127.0.0.1:3000/api/auth-check",
        "script": "~/.local/bin/hermes-workspace",
        "enabled": True,
        "category": "core"
    },
    "honcho": {
        "name": "Honcho Memory",
        "port": 8000,
        "health_url": "http://127.0.0.1:8000/health",
        "script": "cd ~/honcho && nohup uv run fastapi dev src/main.py --port 8000 > /tmp/honcho.log 2>&1 &",
        "enabled": True,
        "category": "memory"
    },
    "swarmclaw": {
        "name": "SwarmClaw",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/swarmclaw",
        "enabled": False,
        "category": "agents"
    },
    "zeroclaw": {
        "name": "ZeroClaw",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/zeroclaw",
        "enabled": False,
        "category": "agents"
    },
    "ceo": {
        "name": "CEO Agent",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/ceo",
        "enabled": False,
        "category": "agents"
    },
    "cto": {
        "name": "CTO Agent",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/cto",
        "enabled": False,
        "category": "agents"
    },
    "cfo": {
        "name": "CFO Agent",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/cfo",
        "enabled": False,
        "category": "agents"
    },
    "coo": {
        "name": "COO Agent",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/coo",
        "enabled": False,
        "category": "agents"
    },
    "cio": {
        "name": "CIO Agent",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/cio",
        "enabled": False,
        "category": "agents"
    },
    "cmo": {
        "name": "CMO Agent",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/cmo",
        "enabled": False,
        "category": "agents"
    },
    "cold-outreach": {
        "name": "Cold Outreach Agent",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/cold-outreach",
        "enabled": False,
        "category": "agents"
    },
    "content-strategist": {
        "name": "Content Strategist",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/content-strategist",
        "enabled": False,
        "category": "agents"
    },
    "customer-service": {
        "name": "Customer Service Agent",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/customer-service",
        "enabled": False,
        "category": "agents"
    },
    "data-engineer": {
        "name": "Data Engineer",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/data-engineer",
        "enabled": False,
        "category": "agents"
    },
    "frontend-developer": {
        "name": "Frontend Developer",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/frontend-developer",
        "enabled": False,
        "category": "agents"
    },
    "graphic-designer": {
        "name": "Graphic Designer",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/graphic-designer",
        "enabled": False,
        "category": "agents"
    },
    "head-of-ai-innovation": {
        "name": "Head of AI Innovation",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/head-of-ai-innovation",
        "enabled": False,
        "category": "agents"
    },
    "head-of-bizdev": {
        "name": "Head of BizDev",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/head-of-bizdev",
        "enabled": False,
        "category": "agents"
    },
    "lead-developer": {
        "name": "Lead Developer",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/lead-developer",
        "enabled": False,
        "category": "agents"
    },
    "personal-assistant": {
        "name": "Personal Assistant",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/personal-assistant",
        "enabled": False,
        "category": "agents"
    },
    "presentation-designer": {
        "name": "Presentation Designer",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/presentation-designer",
        "enabled": False,
        "category": "agents"
    },
    "project-manager": {
        "name": "Project Manager",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/project-manager",
        "enabled": False,
        "category": "agents"
    },
    "qa-engineer": {
        "name": "QA Engineer",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/qa-engineer",
        "enabled": False,
        "category": "agents"
    },
    "social-media-manager": {
        "name": "Social Media Manager",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/social-media-manager",
        "enabled": False,
        "category": "agents"
    },
    "ux-designer": {
        "name": "UX Designer",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/ux-designer",
        "enabled": False,
        "category": "agents"
    },
}


class ModernButton(tk.Canvas):
    """Custom styled button with hover effects"""
    def __init__(self, parent, text, command, width=120, height=32, bg_color=None, **kwargs):
        self.bg_color = bg_color or THEME["accent"]
        self.hover_color = self._lighten(self.bg_color, 20)
        self.command = command
        
        super().__init__(parent, width=width, height=height, bg=THEME["card_bg"], 
                        highlightthickness=0, bd=0, **kwargs)
        
        self.round_rect(2, 2, width-2, height-2, 8, fill=self.bg_color, outline="")
        self.text_id = self.create_text(width//2, height//2, text=text, fill="white",
                                       font=("Inter", 9, "bold"))
        
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        self.bind("<ButtonRelease-1>", self._on_release)
        
    def round_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [x1+radius, y1, x2-radius, y1, x2, y1, x2, y1+radius,
                  x2, y2-radius, x2, y2, x2-radius, y2, x1+radius, y2,
                  x1, y2, x1, y2-radius, x1, y1+radius, x1, y1]
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def _lighten(self, color, percent):
        # Simple hex lighten
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        r = min(255, r + percent)
        g = min(255, g + percent)
        b = min(255, b + percent)
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def _on_enter(self, e):
        self.itemconfig(1, fill=self.hover_color)
        self.config(cursor="hand2")
    
    def _on_leave(self, e):
        self.itemconfig(1, fill=self.bg_color)
        self.config(cursor="")
    
    def _on_click(self, e):
        self.itemconfig(1, fill=self._lighten(self.bg_color, -20))
    
    def _on_release(self, e):
        self.itemconfig(1, fill=self.hover_color)
        if self.command:
            self.command()


class QuickLaunchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quick Launch for Hermes Agent")
        self.root.geometry("1000x700")
        self.root.minsize(900, 500)
        self.root.configure(bg=THEME["bg"])
        
        # Configure ttk styles
        self._setup_styles()
        
        self.services = self.load_config()
        self.health_check_running = False
        self.health_thread = None
        
        self.build_ui()
        self.start_health_monitor()
    
    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure("Dark.TFrame", background=THEME["bg"])
        style.configure("Card.TFrame", background=THEME["card_bg"])
        style.configure("Dark.TLabel", background=THEME["bg"], foreground=THEME["fg"], font=THEME["font_main"])
        style.configure("Header.TLabel", background=THEME["bg"], foreground=THEME["fg"], font=THEME["font_header"])
        style.configure("Title.TLabel", background=THEME["bg"], foreground=THEME["accent"], font=THEME["font_title"])
        style.configure("Accent.TLabel", background=THEME["bg"], foreground=THEME["accent"], font=THEME["font_main"])
        
        # Checkbutton
        style.configure("Dark.TCheckbutton", background=THEME["card_bg"], foreground=THEME["fg"])
        style.map("Dark.TCheckbutton", background=[("active", THEME["card_bg"])])
        
        # Notebook
        style.configure("Dark.TNotebook", background=THEME["bg"], tabmargins=[2, 5, 2, 0])
        style.configure("Dark.TNotebook.Tab", background=THEME["card_bg"], foreground=THEME["fg"], 
                       padding=[15, 8], font=("Inter", 9))
        style.map("Dark.TNotebook.Tab", background=[("selected", THEME["accent"])], 
                  foreground=[("selected", "white")])
        
    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    saved = json.load(f)
                    # Merge with defaults to get any new services
                    merged = DEFAULT_SERVICES.copy()
                    merged.update(saved)
                    return merged
            except Exception as e:
                print(f"Error loading config: {e}")
        return DEFAULT_SERVICES.copy()
    
    def save_config(self):
        try:
            os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.services, f, indent=2)
        except Exception as e:
            self.log(f"Error saving config: {e}")
    
    def build_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=THEME["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Header
        header = tk.Frame(main_frame, bg=THEME["bg"])
        header.pack(fill=tk.X, pady=(0, 15))
        
        # Logo/title area
        title_frame = tk.Frame(header, bg=THEME["bg"])
        title_frame.pack(side=tk.LEFT)
        
        tk.Label(title_frame, text="⚡", font=("Inter", 24), bg=THEME["bg"], fg=THEME["accent"]).pack(side=tk.LEFT)
        tk.Label(title_frame, text="Quick Launch", font=THEME["font_title"], 
                bg=THEME["bg"], fg=THEME["fg"]).pack(side=tk.LEFT, padx=(10, 0))
        tk.Label(title_frame, text="for Hermes Agent", font=("Inter", 10), 
                bg=THEME["bg"], fg=THEME["accent"]).pack(side=tk.LEFT, padx=(5, 0))
        
        # Status indicator
        self.status_label = tk.Label(header, text="● Monitoring", font=("Inter", 9),
                                     bg=THEME["bg"], fg=THEME["success"])
        self.status_label.pack(side=tk.RIGHT)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame, style="Dark.TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Services tab
        services_tab = tk.Frame(self.notebook, bg=THEME["bg"])
        self.notebook.add(services_tab, text=" Services ")
        self.build_services_tab(services_tab)
        
        # Logs tab
        logs_tab = tk.Frame(self.notebook, bg=THEME["bg"])
        self.notebook.add(logs_tab, text=" Logs ")
        self.build_logs_tab(logs_tab)
        
        # Settings tab
        settings_tab = tk.Frame(self.notebook, bg=THEME["bg"])
        self.notebook.add(settings_tab, text=" Settings ")
        self.build_settings_tab(settings_tab)
        
    def build_services_tab(self, parent):
        # Top actions bar
        actions = tk.Frame(parent, bg=THEME["bg"])
        actions.pack(fill=tk.X, pady=(0, 10))
        
        ModernButton(actions, "▶ Launch All", self.launch_all, bg_color=THEME["accent"]).pack(side=tk.LEFT, padx=(0, 8))
        ModernButton(actions, "↻ Health Check", self.manual_health_check, bg_color=THEME["accent2"]).pack(side=tk.LEFT, padx=(0, 8))
        ModernButton(actions, "＋ Auto-Discover", self.auto_discover_services, bg_color="#059669").pack(side=tk.LEFT)
        
        # Create scrollable frame for services
        canvas = tk.Canvas(parent, bg=THEME["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=THEME["bg"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Category headers
        self.service_vars = {}
        self.status_labels = {}
        self.service_cards = {}
        
        categories = {
            "core": "🔥 Core Services", 
            "memory": "🧠 Memory & Storage", 
            "agents": "🤖 AI Agents",
            "custom": "⚙️ Custom Services"
        }
        
        for cat_key, cat_name in categories.items():
            # Check if any services in this category
            cat_services = {k: v for k, v in self.services.items() if v.get("category", "custom") == cat_key}
            if not cat_services:
                continue
                
            cat_frame = tk.LabelFrame(scrollable_frame, text=cat_name, bg=THEME["card_bg"], 
                                     fg=THEME["fg"], font=THEME["font_header"], bd=1,
                                     highlightbackground=THEME["border"], highlightthickness=1)
            cat_frame.pack(fill=tk.X, pady=5, padx=2)
            
            for key, svc in self.services.items():
                if svc.get("category", "custom") == cat_key:
                    self._create_service_row(cat_frame, key, svc)
    
    def _create_service_row(self, parent, key, svc):
        row = tk.Frame(parent, bg=THEME["card_bg"])
        row.pack(fill=tk.X, pady=2, padx=5)
        
        # Status dot
        status_label = tk.Label(row, text="○", font=("Inter", 14), bg=THEME["card_bg"], fg="gray")
        status_label.pack(side=tk.LEFT, padx=(5, 10))
        self.status_labels[key] = status_label
        
        # Service info
        info_frame = tk.Frame(row, bg=THEME["card_bg"])
        info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(info_frame, text=svc["name"], font=THEME["font_header"], 
                bg=THEME["card_bg"], fg=THEME["fg"]).pack(anchor=tk.W)
        
        port_info = f"Port {svc['port']}" if svc.get('port', 0) > 0 else "No port"
        tk.Label(info_frame, text=f"{port_info} • {svc.get('category', 'custom')}", 
                font=("Inter", 8), bg=THEME["card_bg"], fg="#888").pack(anchor=tk.W)
        
        # Controls
        ctrl_frame = tk.Frame(row, bg=THEME["card_bg"])
        ctrl_frame.pack(side=tk.RIGHT)
        
        var = tk.BooleanVar(value=svc.get("enabled", True))
        self.service_vars[key] = var
        ttk.Checkbutton(ctrl_frame, variable=var, style="Dark.TCheckbutton",
                       command=lambda k=key: self.toggle_service(k)).pack(side=tk.LEFT, padx=2)
        
        ModernButton(ctrl_frame, "Restart", lambda k=key: self.restart_service(k), 
                    width=70, height=24, bg_color=THEME["accent2"]).pack(side=tk.LEFT, padx=2)
        ModernButton(ctrl_frame, "Logs", lambda k=key: self.show_logs(k), 
                    width=50, height=24, bg_color="#4b5563").pack(side=tk.LEFT, padx=2)
        ModernButton(ctrl_frame, "Stop", lambda k=key: self.stop_service(k), 
                    width=50, height=24, bg_color=THEME["error"]).pack(side=tk.LEFT, padx=2)
    
    def build_logs_tab(self, parent):
        # Log toolbar
        toolbar = tk.Frame(parent, bg=THEME["bg"])
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        ModernButton(toolbar, "📋 Copy Errors", self.copy_error_logs, bg_color=THEME["error"]).pack(side=tk.LEFT, padx=(0, 8))
        ModernButton(toolbar, "💾 Save Logs", self.save_logs_dialog, bg_color=THEME["accent2"]).pack(side=tk.LEFT, padx=(0, 8))
        ModernButton(toolbar, "🗑 Clear", self.clear_logs, bg_color="#4b5563").pack(side=tk.LEFT)
        
        # Log display
        self.log_text = scrolledtext.ScrolledText(
            parent, wrap=tk.WORD, font=("JetBrains Mono", 9),
            bg=THEME["card_bg"], fg=THEME["fg"], insertbackground=THEME["fg"],
            highlightbackground=THEME["border"], highlightthickness=1
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log("Quick Launch for Hermes Agent initialized. Health monitor active.")
    
    def build_settings_tab(self, parent):
        # Settings content
        settings_frame = tk.Frame(parent, bg=THEME["bg"])
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(settings_frame, text="Configuration", font=THEME["font_title"],
                bg=THEME["bg"], fg=THEME["fg"]).pack(anchor=tk.W, pady=(0, 15))
        
        # Config file path
        path_frame = tk.Frame(settings_frame, bg=THEME["bg"])
        path_frame.pack(fill=tk.X, pady=5)
        tk.Label(path_frame, text="Config file:", font=THEME["font_main"], 
                bg=THEME["bg"], fg=THEME["fg"]).pack(side=tk.LEFT)
        tk.Label(path_frame, text=CONFIG_FILE, font=("JetBrains Mono", 9), 
                bg=THEME["bg"], fg=THEME["accent"]).pack(side=tk.LEFT, padx=(10, 0))
        
        # Auto-start option
        self.autostart_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(settings_frame, text="Auto-start services on launch", 
                       variable=self.autostart_var, style="Dark.TCheckbutton").pack(anchor=tk.W, pady=10)
        
        # Health check interval
        interval_frame = tk.Frame(settings_frame, bg=THEME["bg"])
        interval_frame.pack(fill=tk.X, pady=5)
        tk.Label(interval_frame, text="Health check interval (seconds):", 
                font=THEME["font_main"], bg=THEME["bg"], fg=THEME["fg"]).pack(side=tk.LEFT)
        self.interval_var = tk.StringVar(value="30")
        tk.Entry(interval_frame, textvariable=self.interval_var, width=6,
                bg=THEME["card_bg"], fg=THEME["fg"], insertbackground=THEME["fg"],
                highlightbackground=THEME["border"]).pack(side=tk.LEFT, padx=(10, 0))
        
        # Save button
        ModernButton(settings_frame, "💾 Save Settings", self.save_config, 
                    bg_color=THEME["accent"], width=150).pack(anchor=tk.W, pady=20)
    
    def toggle_service(self, key):
        self.services[key]["enabled"] = self.service_vars[key].get()
        state = "Enabled" if self.services[key]["enabled"] else "Disabled"
        self.log(f"{state} {self.services[key]['name']}")
    
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        
        try:
            os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
            with open(LOG_FILE, 'a') as f:
                f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")
        except:
            pass
    
    def check_service_health(self, key, svc):
        if not svc.get("health_url"):
            # For agents without health URLs, check if process is running
            try:
                script_name = os.path.basename(svc["script"])
                result = subprocess.run(["pgrep", "-f", script_name], 
                                      capture_output=True, timeout=2)
                return result.returncode == 0
            except:
                return False
        
        try:
            req = urllib.request.Request(svc["health_url"], method='GET')
            req.add_header('User-Agent', 'QuickLaunch/1.0')
            with urllib.request.urlopen(req, timeout=3) as resp:
                return resp.status == 200
        except:
            return False
    
    def update_health_display(self):
        for key, svc in self.services.items():
            healthy = self.check_service_health(key, svc)
            label = self.status_labels.get(key)
            if label:
                if healthy:
                    label.config(text="●", fg=THEME["success"])
                else:
                    label.config(text="○", fg=THEME["error"])
    
    def health_monitor_loop(self):
        while self.health_check_running:
            self.update_health_display()
            
            for key, svc in self.services.items():
                if not svc.get("enabled", True):
                    continue
                
                healthy = self.check_service_health(key, svc)
                if not healthy and svc.get("health_url"):  # Only auto-restart services with health URLs
                    self.log(f"⚠ {svc['name']} is down. Auto-restarting...")
                    self.restart_service(key, silent=True)
            
            time.sleep(30)
    
    def start_health_monitor(self):
        self.health_check_running = True
        self.health_thread = threading.Thread(target=self.health_monitor_loop, daemon=True)
        self.health_thread.start()
    
    def manual_health_check(self):
        self.log("Manual health check...")
        self.update_health_display()
        
        for key, svc in self.services.items():
            healthy = self.check_service_health(key, svc)
            status = "✓ OK" if healthy else "✗ FAIL"
            self.log(f"  {svc['name']}: {status}")
    
    def auto_discover_services(self):
        """Auto-discover Hermes services from daemon scripts"""
        self.log("Auto-discovering services...")
        
        # Check for hermes daemon scripts
        daemon_dir = os.path.expanduser("~/.local/bin")
        if os.path.exists(daemon_dir):
            for file in os.listdir(daemon_dir):
                if file.startswith("hermes-") and file not in ["hermes-gateway", "hermes-dashboard", "hermes-workspace", "hermes-autostart.sh", "hermes-gateway-daemon.sh"]:
                    service_name = file.replace("hermes-", "")
                    if service_name not in self.services:
                        # Auto-add discovered service
                        self.services[service_name] = {
                            "name": f"Hermes {service_name.title()}",
                            "port": 0,  # Unknown, user can set
                            "health_url": "",
                            "script": f"~/.local/bin/{file}",
                            "enabled": False,
                            "category": "custom",
                            "discovered": True
                        }
                        self.log(f"Discovered: {file}")
        
        self.log("Auto-discovery complete. Enable discovered services in Settings.")
        messagebox.showinfo("Discovery Complete", "New services discovered! Check the Services tab to enable them.")
    
    def stop_service(self, key):
        svc = self.services[key]
        self.log(f"Stopping {svc['name']}...")
        
        try:
            if key == "honcho":
                subprocess.run(["wsl", "-d", "Ubuntu", "pkill", "-f", "fastapi dev.*honcho"],
                              capture_output=True, timeout=5)
            else:
                script_path = os.path.expanduser(svc["script"])
                if os.path.exists(script_path):
                    subprocess.run([script_path, "stop"], capture_output=True, timeout=5)
                else:
                    subprocess.run(["wsl", "-d", "Ubuntu", script_path, "stop"],
                                  capture_output=True, timeout=5)
            self.log(f"  Stop command sent to {svc['name']}")
        except Exception as e:
            self.log(f"  Error stopping {svc['name']}: {e}")
    
    def restart_service(self, key, silent=False):
        svc = self.services[key]
        if not silent:
            self.log(f"Restarting {svc['name']}...")
        
        try:
            # Stop existing
            self.stop_service(key)
            time.sleep(1)
            
            # Start new
            if key == "honcho":
                subprocess.Popen(["wsl", "-d", "Ubuntu", "bash", "-c",
                                 "cd ~/honcho && nohup uv run fastapi dev src/main.py "
                                 "--port 8000 > /tmp/honcho.log 2>&1 &"])
            else:
                script_path = os.path.expanduser(svc["script"])
                if os.path.exists(script_path):
                    subprocess.run([script_path, "start"], capture_output=True, timeout=5)
                else:
                    subprocess.run(["wsl", "-d", "Ubuntu", script_path, "start"],
                                  capture_output=True, timeout=5)
            
            if not silent:
                self.log(f"  Restart command sent to {svc['name']}")
        except Exception as e:
            self.log(f"  ERROR restarting {svc['name']}: {e}")
    
    def launch_all(self):
        enabled = [k for k, v in self.services.items() if v.get("enabled", True)]
        
        if not enabled:
            messagebox.showwarning("No Services", "No services enabled. Please check at least one service.")
            return
        
        self.log(f"Launching all enabled services: {', '.join(enabled)}")
        
        # Build bash commands
        cmds = []
        for key in enabled:
            svc = self.services[key]
            if key == "honcho":
                cmds.append("cd ~/honcho && nohup uv run fastapi dev src/main.py --port 8000 > /tmp/honcho.log 2>&1 &")
            else:
                cmds.append(f"~/.local/bin/hermes-{key} start")
        
        bash_cmd = "; ".join(cmds)
        
        try:
            subprocess.Popen(["wt.exe", "-p", "Ubuntu", "wsl.exe", "-d", "Ubuntu", "-e", "bash", "-lic", bash_cmd])
            self.log("Terminal launched successfully")
        except Exception as e:
            messagebox.showerror("Launch Failed", f"Failed to launch terminal:\n{e}")
            self.log(f"ERROR: Failed to launch: {e}")
    
    def show_logs(self, key):
        log_paths = {
            "gateway": "~/.hermes/logs/gateway-daemon.log",
            "dashboard": "~/.hermes/logs/dashboard-daemon.log",
            "workspace": "~/.hermes/logs/workspace-daemon.log",
            "honcho": "/tmp/honcho.log"
        }
        path = os.path.expanduser(log_paths.get(key, "~/.hermes/logs/launcher-health.log"))
        
        try:
            with open(path, 'r') as f:
                content = f.read()[-8000:]
        except Exception as e:
            content = f"Could not read log file:\n{path}\n\nError: {e}"
        
        log_window = tk.Toplevel(self.root)
        log_window.title(f"Logs: {self.services[key]['name']}")
        log_window.geometry("850x600")
        log_window.configure(bg=THEME["bg"])
        
        text = scrolledtext.ScrolledText(log_window, wrap=tk.WORD, font=("JetBrains Mono", 9),
                                        bg=THEME["card_bg"], fg=THEME["fg"])
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text.insert(tk.END, content)
        text.config(state=tk.DISABLED)
        
        ModernButton(log_window, "Refresh", lambda: self.refresh_log(text, path), 
                    bg_color=THEME["accent"]).pack(pady=5)
    
    def refresh_log(self, text_widget, path):
        try:
            with open(path, 'r') as f:
                content = f.read()[-8000:]
            text_widget.config(state=tk.NORMAL)
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, content)
            text_widget.config(state=tk.DISABLED)
        except Exception as e:
            text_widget.config(state=tk.NORMAL)
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, f"Error reading log: {e}")
            text_widget.config(state=tk.DISABLED)
    
    def copy_error_logs(self):
        log_content = self.log_text.get(1.0, tk.END)
        error_lines = [line for line in log_content.split('\n')
                      if any(x in line for x in ['ERROR', 'FAIL', '✗', '⚠', 'Error'])]
        
        if not error_lines:
            messagebox.showinfo("No Errors", "No error lines found in the log.")
            return
        
        error_text = '\n'.join(error_lines)
        self.root.clipboard_clear()
        self.root.clipboard_append(error_text)
        self.root.update()
        self.log(f"Copied {len(error_lines)} error lines to clipboard")
        messagebox.showinfo("Copied", f"{len(error_lines)} error lines copied to clipboard.")
    
    def save_logs_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Save Logs")
        dialog.geometry("350x200")
        dialog.configure(bg=THEME["bg"])
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Choose what to save:", font=THEME["font_header"],
                bg=THEME["bg"], fg=THEME["fg"]).pack(pady=(15, 10))
        
        choice = tk.StringVar(value="all")
        tk.Radiobutton(dialog, text="All logs", variable=choice, value="all",
                      bg=THEME["bg"], fg=THEME["fg"], selectcolor=THEME["card_bg"]).pack(anchor=tk.W, padx=30)
        tk.Radiobutton(dialog, text="Error logs only", variable=choice, value="errors",
                      bg=THEME["bg"], fg=THEME["fg"], selectcolor=THEME["card_bg"]).pack(anchor=tk.W, padx=30)
        
        def do_save():
            log_content = self.log_text.get(1.0, tk.END)
            
            if choice.get() == "errors":
                lines = [line for line in log_content.split('\n')
                        if any(x in line for x in ['ERROR', 'FAIL', '✗', '⚠', 'Error'])]
                content = '\n'.join(lines)
                default_name = f"quick-launch-errors-{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            else:
                content = log_content
                default_name = f"quick-launch-logs-{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            if not content.strip():
                messagebox.showwarning("Empty", "No content to save.")
                return
            
            path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                initialfile=default_name,
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Save Logs"
            )
            
            if path:
                try:
                    with open(path, 'w') as f:
                        f.write(content)
                    self.log(f"Logs saved to: {path}")
                    messagebox.showinfo("Saved", f"Logs saved to:\n{path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save:\n{e}")
            
            dialog.destroy()
        
        ModernButton(dialog, "Save", do_save, bg_color=THEME["accent"]).pack(pady=15)
    
    def clear_logs(self):
        self.log_text.delete(1.0, tk.END)
        self.log("Logs cleared.")
    
    def on_closing(self):
        self.health_check_running = False
        self.save_config()
        self.root.destroy()


def main():
    root = tk.Tk()
    
    # Set DPI awareness
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    
    app = QuickLaunchApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
