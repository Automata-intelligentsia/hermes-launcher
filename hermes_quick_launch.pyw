#!/usr/bin/env python3
"""
Quick Launch for Hermes Agent - Single-file launcher for Hermes Agent ecosystem
Nous Research aesthetic: dark forest green + gold + white
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

# Nous Research color scheme: dark forest green + gold + white
THEME = {
    "bg": "#0d1f0d",           # Dark forest green background
    "fg": "#f5f5f0",           # Warm white text
    "accent": "#c9a227",       # Gold accent
    "accent2": "#8b7355",      # Bronze secondary
    "success": "#4ade80",      # Green success
    "error": "#ef4444",        # Red error
    "warning": "#fbbf24",      # Amber warning
    "card_bg": "#1a2e1a",      # Slightly lighter forest green
    "border": "#2d4a2d",       # Forest green border
    "gold_light": "#e8d5a3",   # Light gold
    "forest_light": "#2d5a2d", # Light forest
    "font_main": ("Inter", 10),
    "font_header": ("Inter", 11, "bold"),
    "font_title": ("Inter", 18, "bold"),
}

# Default services organized by category
DEFAULT_SERVICES = {
    # === CORE ===
    "gateway": {
        "name": "Hermes Gateway",
        "port": 8653,
        "health_url": "http://127.0.0.1:8653/health",
        "script": "~/.local/bin/hermes-gateway",
        "enabled": True,
        "category": "core",
        "autostart": True
    },
    "dashboard": {
        "name": "Hermes Dashboard",
        "port": 9119,
        "health_url": "http://127.0.0.1:9119",
        "script": "~/.local/bin/hermes-dashboard",
        "enabled": True,
        "category": "core",
        "autostart": True
    },
    "honcho": {
        "name": "Honcho Memory",
        "port": 8000,
        "health_url": "http://127.0.0.1:8000/health",
        "script": "cd ~/honcho && nohup uv run fastapi dev src/main.py --port 8000 > /tmp/honcho.log 2>&1 &",
        "enabled": True,
        "category": "core",
        "autostart": True
    },
    # === ORCHESTRATION ===
    "workspace": {
        "name": "Hermes Workspace",
        "port": 3000,
        "health_url": "http://127.0.0.1:3000/api/auth-check",
        "script": "~/.local/bin/hermes-workspace",
        "enabled": True,
        "category": "orchestration",
        "autostart": True
    },
    "swarmclaw": {
        "name": "SwarmClaw",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/swarmclaw",
        "enabled": False,
        "category": "orchestration",
        "autostart": False
    },
    "paperclip": {
        "name": "Paperclip AI",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/paperclip",
        "enabled": False,
        "category": "orchestration",
        "autostart": False
    },
    "refusion": {
        "name": "Refusion",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/refusion",
        "enabled": False,
        "category": "orchestration",
        "autostart": False
    },
    # === AGENTS (Main) ===
    "hermes-agent": {
        "name": "Hermes Agent",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/hermes-agent",
        "enabled": False,
        "category": "agents",
        "autostart": False
    },
    # === SUB-AGENTS ===
    "ceo": {
        "name": "CEO Agent",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/ceo",
        "enabled": False,
        "category": "sub-agents",
        "autostart": False
    },
    "cto": {
        "name": "CTO Agent",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/cto",
        "enabled": False,
        "category": "sub-agents",
        "autostart": False
    },
    "cfo": {
        "name": "CFO Agent",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/cfo",
        "enabled": False,
        "category": "sub-agents",
        "autostart": False
    },
    "coo": {
        "name": "COO Agent",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/coo",
        "enabled": False,
        "category": "sub-agents",
        "autostart": False
    },
    "cio": {
        "name": "CIO Agent",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/cio",
        "enabled": False,
        "category": "sub-agents",
        "autostart": False
    },
    "cmo": {
        "name": "CMO Agent",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/cmo",
        "enabled": False,
        "category": "sub-agents",
        "autostart": False
    },
    "cold-outreach": {
        "name": "Cold Outreach Agent",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/cold-outreach",
        "enabled": False,
        "category": "sub-agents",
        "autostart": False
    },
    "content-strategist": {
        "name": "Content Strategist",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/content-strategist",
        "enabled": False,
        "category": "sub-agents",
        "autostart": False
    },
    "customer-service": {
        "name": "Customer Service Agent",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/customer-service",
        "enabled": False,
        "category": "sub-agents",
        "autostart": False
    },
    "data-engineer": {
        "name": "Data Engineer",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/data-engineer",
        "enabled": False,
        "category": "sub-agents",
        "autostart": False
    },
    "frontend-developer": {
        "name": "Frontend Developer",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/frontend-developer",
        "enabled": False,
        "category": "sub-agents",
        "autostart": False
    },
    "graphic-designer": {
        "name": "Graphic Designer",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/graphic-designer",
        "enabled": False,
        "category": "sub-agents",
        "autostart": False
    },
    "head-of-ai-innovation": {
        "name": "Head of AI Innovation",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/head-of-ai-innovation",
        "enabled": False,
        "category": "sub-agents",
        "autostart": False
    },
    "head-of-bizdev": {
        "name": "Head of BizDev",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/head-of-bizdev",
        "enabled": False,
        "category": "sub-agents",
        "autostart": False
    },
    "lead-developer": {
        "name": "Lead Developer",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/lead-developer",
        "enabled": False,
        "category": "sub-agents",
        "autostart": False
    },
    "personal-assistant": {
        "name": "Personal Assistant",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/personal-assistant",
        "enabled": False,
        "category": "sub-agents",
        "autostart": False
    },
    "presentation-designer": {
        "name": "Presentation Designer",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/presentation-designer",
        "enabled": False,
        "category": "sub-agents",
        "autostart": False
    },
    "project-manager": {
        "name": "Project Manager",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/project-manager",
        "enabled": False,
        "category": "sub-agents",
        "autostart": False
    },
    "qa-engineer": {
        "name": "QA Engineer",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/qa-engineer",
        "enabled": False,
        "category": "sub-agents",
        "autostart": False
    },
    "social-media-manager": {
        "name": "Social Media Manager",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/social-media-manager",
        "enabled": False,
        "category": "sub-agents",
        "autostart": False
    },
    "ux-designer": {
        "name": "UX Designer",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/ux-designer",
        "enabled": False,
        "category": "sub-agents",
        "autostart": False
    },
    # === OTHER ===
    "zeroclaw": {
        "name": "ZeroClaw",
        "port": 0,
        "health_url": "",
        "script": "~/.local/bin/zeroclaw",
        "enabled": False,
        "category": "other",
        "autostart": False
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


class SpinnerLabel(tk.Label):
    """Animated spinner for processing state"""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, text="", font=("Inter", 14), 
                        bg=THEME["card_bg"], fg=THEME["accent"], **kwargs)
        self.spinner_chars = ["◐", "◓", "◑", "◒"]
        self.spinner_idx = 0
        self.animating = False
        self._animate_id = None
    
    def start(self):
        self.animating = True
        self._animate()
    
    def stop(self):
        self.animating = False
        if self._animate_id:
            self.after_cancel(self._animate_id)
        self.config(text="")
    
    def _animate(self):
        if not self.animating:
            return
        self.spinner_idx = (self.spinner_idx + 1) % len(self.spinner_chars)
        self.config(text=self.spinner_chars[self.spinner_idx])
        self._animate_id = self.after(150, self._animate)


class QuickLaunchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quick Launch for Hermes Agent")
        self.root.geometry("1400x800")
        self.root.minsize(1200, 600)
        self.root.configure(bg=THEME["bg"])
        
        self._setup_styles()
        
        self.services = self.load_config()
        self.health_check_running = False
        self.health_thread = None
        self.spinners = {}
        self.service_log_buffers = {}
        self.current_log_view = "all"
        
        self.build_ui()
        self.start_health_monitor()
        self.start_log_monitor()
    
    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("Dark.TFrame", background=THEME["bg"])
        style.configure("Card.TFrame", background=THEME["card_bg"])
        style.configure("Dark.TLabel", background=THEME["bg"], foreground=THEME["fg"], font=THEME["font_main"])
        style.configure("Header.TLabel", background=THEME["bg"], foreground=THEME["fg"], font=THEME["font_header"])
        style.configure("Title.TLabel", background=THEME["bg"], foreground=THEME["accent"], font=THEME["font_title"])
        style.configure("Accent.TLabel", background=THEME["bg"], foreground=THEME["accent"], font=THEME["font_main"])
        
        style.configure("Dark.TCheckbutton", background=THEME["card_bg"], foreground=THEME["fg"])
        style.map("Dark.TCheckbutton", background=[("active", THEME["card_bg"])])
        
        # Fixed-size tabs - uniform padding, only color changes
        style.configure("Dark.TNotebook", background=THEME["bg"], tabmargins=[0, 0, 0, 0])
        style.configure("Dark.TNotebook.Tab", 
                       background=THEME["card_bg"], 
                       foreground=THEME["fg"], 
                       padding=[20, 10],
                       font=("Inter", 10))
        style.map("Dark.TNotebook.Tab", 
                 background=[("selected", THEME["accent"]), ("active", THEME["forest_light"])], 
                 foreground=[("selected", "#000000")],
                 expand=[("selected", [0, 0, 0, 0])])
        
        # Combobox style
        style.configure("Dark.TCombobox", 
                       fieldbackground=THEME["card_bg"],
                       background=THEME["card_bg"],
                       foreground=THEME["fg"],
                       arrowcolor=THEME["accent"])
    
    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    saved = json.load(f)
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
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Header
        header = tk.Frame(main_frame, bg=THEME["bg"])
        header.pack(fill=tk.X, pady=(0, 10))
        
        title_frame = tk.Frame(header, bg=THEME["bg"])
        title_frame.pack(side=tk.LEFT)
        
        tk.Label(title_frame, text="⚡", font=("Inter", 24), bg=THEME["bg"], fg=THEME["accent"]).pack(side=tk.LEFT)
        tk.Label(title_frame, text="Quick Launch", font=THEME["font_title"], 
                bg=THEME["bg"], fg=THEME["fg"]).pack(side=tk.LEFT, padx=(10, 0))
        tk.Label(title_frame, text="for Hermes Agent", font=("Inter", 10), 
                bg=THEME["bg"], fg=THEME["accent"]).pack(side=tk.LEFT, padx=(5, 0))
        
        self.status_label = tk.Label(header, text="● Monitoring", font=("Inter", 9),
                                     bg=THEME["bg"], fg=THEME["success"])
        self.status_label.pack(side=tk.RIGHT)
        
        # Content area - split into left (services) and right (live log)
        content_frame = tk.Frame(main_frame, bg=THEME["bg"])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Services with notebook tabs
        left_panel = tk.Frame(content_frame, bg=THEME["bg"])
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.notebook = ttk.Notebook(left_panel, style="Dark.TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Services tab
        services_tab = tk.Frame(self.notebook, bg=THEME["bg"])
        self.notebook.add(services_tab, text=" Services ")
        self.build_services_tab(services_tab)
        
        # Logs tab (full log history)
        logs_tab = tk.Frame(self.notebook, bg=THEME["bg"])
        self.notebook.add(logs_tab, text=" Logs ")
        self.build_logs_tab(logs_tab)
        
        # Settings tab
        settings_tab = tk.Frame(self.notebook, bg=THEME["bg"])
        self.notebook.add(settings_tab, text=" Settings ")
        self.build_settings_tab(settings_tab)
        
        # Right panel - Live log viewer
        right_panel = tk.Frame(content_frame, bg=THEME["bg"], width=450)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        right_panel.pack_propagate(False)
        
        self.build_live_log_panel(right_panel)
    
    def build_services_tab(self, parent):
        # Top actions bar
        actions = tk.Frame(parent, bg=THEME["bg"])
        actions.pack(fill=tk.X, pady=(0, 10))
        
        ModernButton(actions, "▶ Launch All", self.launch_all, bg_color=THEME["accent"]).pack(side=tk.LEFT, padx=(0, 8))
        ModernButton(actions, "↻ Health Check", self.manual_health_check, bg_color=THEME["accent2"]).pack(side=tk.LEFT, padx=(0, 8))
        ModernButton(actions, "＋ Auto-Discover", self.auto_discover_services, bg_color="#2d5a2d").pack(side=tk.LEFT)
        
        # Create scrollable frame for services with mouse wheel support
        canvas = tk.Canvas(parent, bg=THEME["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=THEME["bg"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Mouse wheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Category headers
        self.service_vars = {}
        self.autostart_vars = {}
        self.status_labels = {}
        self.spinners = {}
        self.service_cards = {}
        
        categories = {
            "core": "🔥 Core Services",
            "orchestration": "🎛️ Orchestration",
            "agents": "🤖 AI Agents",
            "sub-agents": "👥 Sub-Agents",
            "other": "⚙️ Other",
            "custom": "⚙️ Custom Services"
        }
        
        for cat_key, cat_name in categories.items():
            cat_services = {k: v for k, v in self.services.items() if v.get("category", "custom") == cat_key}
            if not cat_services:
                continue
                
            cat_frame = tk.LabelFrame(scrollable_frame, text=cat_name, bg=THEME["card_bg"], 
                                     fg=THEME["accent"], font=THEME["font_header"], bd=1,
                                     highlightbackground=THEME["border"], highlightthickness=1)
            cat_frame.pack(fill=tk.X, pady=5, padx=2)
            
            for key, svc in self.services.items():
                if svc.get("category", "custom") == cat_key:
                    self._create_service_row(cat_frame, key, svc)
    
    def _create_service_row(self, parent, key, svc):
        row = tk.Frame(parent, bg=THEME["card_bg"])
        row.pack(fill=tk.X, pady=2, padx=5)
        
        # Left side: spinner + status dot
        left_frame = tk.Frame(row, bg=THEME["card_bg"])
        left_frame.pack(side=tk.LEFT, padx=(5, 5))
        
        # Spinner (hidden by default)
        spinner = SpinnerLabel(left_frame)
        spinner.pack(side=tk.LEFT)
        self.spinners[key] = spinner
        
        # Status dot
        status_label = tk.Label(left_frame, text="○", font=("Inter", 14), bg=THEME["card_bg"], fg="gray")
        status_label.pack(side=tk.LEFT, padx=(5, 0))
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
        
        # Auto-start checkbox
        auto_var = tk.BooleanVar(value=svc.get("autostart", False))
        self.autostart_vars[key] = auto_var
        ttk.Checkbutton(ctrl_frame, variable=auto_var, style="Dark.TCheckbutton",
                       command=lambda k=key: self.toggle_autostart(k)).pack(side=tk.LEFT, padx=1)
        
        # Enable/disable checkbox
        var = tk.BooleanVar(value=svc.get("enabled", True))
        self.service_vars[key] = var
        ttk.Checkbutton(ctrl_frame, variable=var, style="Dark.TCheckbutton",
                       command=lambda k=key: self.toggle_service(k)).pack(side=tk.LEFT, padx=1)
        
        ModernButton(ctrl_frame, "Settings", lambda k=key: self.show_settings(k), 
                    width=60, height=24, bg_color=THEME["accent2"]).pack(side=tk.LEFT, padx=1)
        ModernButton(ctrl_frame, "Restart", lambda k=key: self.restart_service(k), 
                    width=60, height=24, bg_color=THEME["accent"]).pack(side=tk.LEFT, padx=1)
        ModernButton(ctrl_frame, "Logs", lambda k=key: self.show_logs(k), 
                    width=40, height=24, bg_color="#4b5563").pack(side=tk.LEFT, padx=1)
        ModernButton(ctrl_frame, "Stop", lambda k=key: self.stop_service(k), 
                    width=40, height=24, bg_color=THEME["error"]).pack(side=tk.LEFT, padx=1)
    
    def build_live_log_panel(self, parent):
        """Build the live log panel on the right side"""
        # Header
        header = tk.Frame(parent, bg=THEME["bg"])
        header.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(header, text="📋 Live Log", font=THEME["font_header"],
                bg=THEME["bg"], fg=THEME["accent"]).pack(side=tk.LEFT)
        
        # Service selector dropdown
        self.log_service_var = tk.StringVar(value="all")
        services_list = ["all"] + sorted([k for k in self.services.keys()])
        
        dropdown = ttk.Combobox(header, textvariable=self.log_service_var, 
                                 values=services_list, state="readonly",
                                 width=15, style="Dark.TCombobox")
        dropdown.pack(side=tk.RIGHT)
        dropdown.bind("<<ComboboxSelected>>", self.on_log_service_changed)
        
        # Live log text area
        self.live_log = scrolledtext.ScrolledText(
            parent, wrap=tk.WORD, font=("JetBrains Mono", 9),
            bg=THEME["card_bg"], fg=THEME["fg"], insertbackground=THEME["fg"],
            highlightbackground=THEME["border"], highlightthickness=1,
            height=20
        )
        self.live_log.pack(fill=tk.BOTH, expand=True)
        self.live_log.insert(tk.END, "Live log initialized. Select a service or 'all' to view logs.\n")
        
        # Log toolbar
        toolbar = tk.Frame(parent, bg=THEME["bg"])
        toolbar.pack(fill=tk.X, pady=(5, 0))
        
        ModernButton(toolbar, "📋 Copy", self.copy_live_logs, bg_color=THEME["accent2"], width=60).pack(side=tk.LEFT, padx=2)
        ModernButton(toolbar, "💾 Save", self.save_live_logs, bg_color=THEME["accent"], width=60).pack(side=tk.LEFT, padx=2)
        ModernButton(toolbar, "🗑 Clear", self.clear_live_logs, bg_color="#4b5563", width=60).pack(side=tk.LEFT, padx=2)
    
    def build_logs_tab(self, parent):
        toolbar = tk.Frame(parent, bg=THEME["bg"])
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        ModernButton(toolbar, "📋 Copy Errors", self.copy_error_logs, bg_color=THEME["error"]).pack(side=tk.LEFT, padx=(0, 8))
        ModernButton(toolbar, "💾 Save Logs", self.save_logs_dialog, bg_color=THEME["accent2"]).pack(side=tk.LEFT, padx=(0, 8))
        ModernButton(toolbar, "🗑 Clear", self.clear_logs, bg_color="#4b5563").pack(side=tk.LEFT)
        
        self.log_text = scrolledtext.ScrolledText(
            parent, wrap=tk.WORD, font=("JetBrains Mono", 9),
            bg=THEME["card_bg"], fg=THEME["fg"], insertbackground=THEME["fg"],
            highlightbackground=THEME["border"], highlightthickness=1
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log("Quick Launch for Hermes Agent initialized. Health monitor active.")
    
    def build_settings_tab(self, parent):
        settings_frame = tk.Frame(parent, bg=THEME["bg"])
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(settings_frame, text="Configuration", font=THEME["font_title"],
                bg=THEME["bg"], fg=THEME["fg"]).pack(anchor=tk.W, pady=(0, 15))
        
        path_frame = tk.Frame(settings_frame, bg=THEME["bg"])
        path_frame.pack(fill=tk.X, pady=5)
        tk.Label(path_frame, text="Config file:", font=THEME["font_main"], 
                bg=THEME["bg"], fg=THEME["fg"]).pack(side=tk.LEFT)
        tk.Label(path_frame, text=CONFIG_FILE, font=("JetBrains Mono", 9), 
                bg=THEME["bg"], fg=THEME["accent"]).pack(side=tk.LEFT, padx=(10, 0))
        
        self.autostart_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(settings_frame, text="Auto-start services on launch", 
                       variable=self.autostart_var, style="Dark.TCheckbutton").pack(anchor=tk.W, pady=10)
        
        interval_frame = tk.Frame(settings_frame, bg=THEME["bg"])
        interval_frame.pack(fill=tk.X, pady=5)
        tk.Label(interval_frame, text="Health check interval (seconds):", 
                font=THEME["font_main"], bg=THEME["bg"], fg=THEME["fg"]).pack(side=tk.LEFT)
        self.interval_var = tk.StringVar(value="30")
        tk.Entry(interval_frame, textvariable=self.interval_var, width=6,
                bg=THEME["card_bg"], fg=THEME["fg"], insertbackground=THEME["fg"],
                highlightbackground=THEME["border"]).pack(side=tk.LEFT, padx=(10, 0))
        
        ModernButton(settings_frame, "💾 Save Settings", self.save_config, 
                    bg_color=THEME["accent"], width=150).pack(anchor=tk.W, pady=20)
    
    def toggle_service(self, key):
        self.services[key]["enabled"] = self.service_vars[key].get()
        state = "Enabled" if self.services[key]["enabled"] else "Disabled"
        self.log(f"{state} {self.services[key]['name']}")
    
    def toggle_autostart(self, key):
        self.services[key]["autostart"] = self.autostart_vars[key].get()
        state = "Auto-start" if self.services[key]["autostart"] else "Manual start"
        self.log(f"{state} {self.services[key]['name']}")
    
    def log(self, message, service_key=None):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_line = f"[{timestamp}] {message}\n"
        
        # Add to main log
        self.log_text.insert(tk.END, log_line)
        self.log_text.see(tk.END)
        
        # Add to service-specific buffer
        if service_key:
            if service_key not in self.service_log_buffers:
                self.service_log_buffers[service_key] = []
            self.service_log_buffers[service_key].append(log_line)
            # Keep last 500 lines per service
            self.service_log_buffers[service_key] = self.service_log_buffers[service_key][-500:]
        
        # Add to "all" buffer
        if "all" not in self.service_log_buffers:
            self.service_log_buffers["all"] = []
        self.service_log_buffers["all"].append(log_line)
        self.service_log_buffers["all"] = self.service_log_buffers["all"][-500:]
        
        # Update live log if viewing this service or "all"
        if self.current_log_view in ["all", service_key]:
            self.live_log.insert(tk.END, log_line)
            self.live_log.see(tk.END)
        
        # Write to file
        try:
            os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
            with open(LOG_FILE, 'a') as f:
                f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")
        except:
            pass
    
    def on_log_service_changed(self, event=None):
        """Handle live log service dropdown change"""
        self.current_log_view = self.log_service_var.get()
        self.live_log.delete(1.0, tk.END)
        
        if self.current_log_view in self.service_log_buffers:
            for line in self.service_log_buffers[self.current_log_view][-100:]:
                self.live_log.insert(tk.END, line)
        else:
            self.live_log.insert(tk.END, f"No logs for {self.current_log_view} yet.\n")
        
        self.live_log.see(tk.END)
    
    def copy_live_logs(self):
        content = self.live_log.get(1.0, tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        self.root.update()
    
    def save_live_logs(self):
        content = self.live_log.get(1.0, tk.END)
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=f"live-logs-{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            filetypes=[("Text files", "*.txt")]
        )
        if path:
            with open(path, 'w') as f:
                f.write(content)
    
    def clear_live_logs(self):
        self.live_log.delete(1.0, tk.END)
    
    def check_service_health(self, key, svc):
        if not svc.get("health_url"):
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
                if not healthy and svc.get("health_url"):
                    self.log(f"⚠ {svc['name']} is down. Auto-restarting...", service_key=key)
                    self.restart_service(key, silent=True)
            
            time.sleep(30)
    
    def start_health_monitor(self):
        self.health_check_running = True
        self.health_thread = threading.Thread(target=self.health_monitor_loop, daemon=True)
        self.health_thread.start()
    
    def start_log_monitor(self):
        """Start background thread to tail log files"""
        def monitor_logs():
            log_paths = {
                "gateway": os.path.expanduser("~/.hermes/logs/gateway-daemon.log"),
                "dashboard": os.path.expanduser("~/.hermes/logs/dashboard-daemon.log"),
                "workspace": os.path.expanduser("~/.hermes/logs/workspace-daemon.log"),
                "honcho": "/tmp/honcho.log"
            }
            
            file_positions = {}
            
            while True:
                for key, path in log_paths.items():
                    if os.path.exists(path):
                        try:
                            with open(path, 'r') as f:
                                pos = file_positions.get(key, 0)
                                f.seek(pos)
                                new_lines = f.readlines()
                                if new_lines:
                                    file_positions[key] = f.tell()
                                    for line in new_lines:
                                        line = line.strip()
                                        if line:
                                            self.log(f"[{key}] {line}", service_key=key)
                        except:
                            pass
                
                time.sleep(2)
        
        log_thread = threading.Thread(target=monitor_logs, daemon=True)
        log_thread.start()
    
    def manual_health_check(self):
        self.log("Manual health check...")
        self.update_health_display()
        
        for key, svc in self.services.items():
            healthy = self.check_service_health(key, svc)
            status = "✓ OK" if healthy else "✗ FAIL"
            self.log(f"  {svc['name']}: {status}", service_key=key)
    
    def auto_discover_services(self):
        self.log("Auto-discovering services...")
        
        daemon_dir = os.path.expanduser("~/.local/bin")
        if os.path.exists(daemon_dir):
            for file in os.listdir(daemon_dir):
                if file.startswith("hermes-") and file not in ["hermes-gateway", "hermes-dashboard", "hermes-workspace", "hermes-autostart.sh", "hermes-gateway-daemon.sh"]:
                    service_name = file.replace("hermes-", "")
                    if service_name not in self.services:
                        self.services[service_name] = {
                            "name": f"Hermes {service_name.title()}",
                            "port": 0,
                            "health_url": "",
                            "script": f"~/.local/bin/{file}",
                            "enabled": False,
                            "category": "custom",
                            "autostart": False,
                            "discovered": True
                        }
                        self.log(f"Discovered: {file}")
        
        self.log("Auto-discovery complete. Enable discovered services in Settings.")
        messagebox.showinfo("Discovery Complete", "New services discovered! Check the Services tab to enable them.")
    
    def show_settings(self, key):
        """Show settings dialog for a service"""
        svc = self.services[key]
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Settings: {svc['name']}")
        dialog.geometry("400x350")
        dialog.configure(bg=THEME["bg"])
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text=svc["name"], font=THEME["font_title"],
                bg=THEME["bg"], fg=THEME["accent"]).pack(pady=(15, 10))
        
        # Port
        port_frame = tk.Frame(dialog, bg=THEME["bg"])
        port_frame.pack(fill=tk.X, pady=5, padx=20)
        tk.Label(port_frame, text="Port:", font=THEME["font_main"], 
                bg=THEME["bg"], fg=THEME["fg"]).pack(side=tk.LEFT)
        port_var = tk.StringVar(value=str(svc.get("port", 0)))
        tk.Entry(port_frame, textvariable=port_var, width=8,
                bg=THEME["card_bg"], fg=THEME["fg"]).pack(side=tk.LEFT, padx=(10, 0))
        
        # Health URL
        url_frame = tk.Frame(dialog, bg=THEME["bg"])
        url_frame.pack(fill=tk.X, pady=5, padx=20)
        tk.Label(url_frame, text="Health URL:", font=THEME["font_main"], 
                bg=THEME["bg"], fg=THEME["fg"]).pack(side=tk.LEFT)
        url_var = tk.StringVar(value=svc.get("health_url", ""))
        tk.Entry(url_frame, textvariable=url_var, width=30,
                bg=THEME["card_bg"], fg=THEME["fg"]).pack(side=tk.LEFT, padx=(10, 0))
        
        # Script path
        script_frame = tk.Frame(dialog, bg=THEME["bg"])
        script_frame.pack(fill=tk.X, pady=5, padx=20)
        tk.Label(script_frame, text="Script:", font=THEME["font_main"], 
                bg=THEME["bg"], fg=THEME["fg"]).pack(side=tk.LEFT)
        script_var = tk.StringVar(value=svc.get("script", ""))
        tk.Entry(script_frame, textvariable=script_var, width=35,
                bg=THEME["card_bg"], fg=THEME["fg"]).pack(side=tk.LEFT, padx=(10, 0))
        
        # Category
        cat_frame = tk.Frame(dialog, bg=THEME["bg"])
        cat_frame.pack(fill=tk.X, pady=5, padx=20)
        tk.Label(cat_frame, text="Category:", font=THEME["font_main"], 
                bg=THEME["bg"], fg=THEME["fg"]).pack(side=tk.LEFT)
        cat_var = tk.StringVar(value=svc.get("category", "custom"))
        cats = ["core", "orchestration", "agents", "sub-agents", "other", "custom"]
        ttk.Combobox(cat_frame, textvariable=cat_var, values=cats, 
                    state="readonly", width=15).pack(side=tk.LEFT, padx=(10, 0))
        
        def save_settings():
            self.services[key]["port"] = int(port_var.get() or 0)
            self.services[key]["health_url"] = url_var.get()
            self.services[key]["script"] = script_var.get()
            self.services[key]["category"] = cat_var.get()
            self.save_config()
            self.log(f"Updated settings for {svc['name']}")
            dialog.destroy()
        
        ModernButton(dialog, "💾 Save", save_settings, 
                    bg_color=THEME["accent"], width=100).pack(pady=20)
    
    def stop_service(self, key):
        svc = self.services[key]
        self.log(f"Stopping {svc['name']}...", service_key=key)
        
        # Show spinner
        if key in self.spinners:
            self.spinners[key].start()
        
        def do_stop():
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
                self.log(f"  Stop command sent to {svc['name']}", service_key=key)
            except Exception as e:
                self.log(f"  Error stopping {svc['name']}: {e}", service_key=key)
            finally:
                if key in self.spinners:
                    self.spinners[key].stop()
        
        threading.Thread(target=do_stop, daemon=True).start()
    
    def restart_service(self, key, silent=False):
        svc = self.services[key]
        if not silent:
            self.log(f"Restarting {svc['name']}...", service_key=key)
        
        # Show spinner
        if key in self.spinners:
            self.spinners[key].start()
        
        def do_restart():
            try:
                self.stop_service(key)
                time.sleep(1)
                
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
                    self.log(f"  Restart command sent to {svc['name']}", service_key=key)
            except Exception as e:
                self.log(f"  ERROR restarting {svc['name']}: {e}", service_key=key)
            finally:
                time.sleep(2)
                if key in self.spinners:
                    self.spinners[key].stop()
        
        threading.Thread(target=do_restart, daemon=True).start()
    
    def launch_all(self):
        enabled = [k for k, v in self.services.items() if v.get("enabled", True)]
        
        if not enabled:
            messagebox.showwarning("No Services", "No services enabled. Please check at least one service.")
            return
        
        self.log(f"Launching all enabled services: {', '.join(enabled)}")
        
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
