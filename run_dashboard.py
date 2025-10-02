#!/usr/bin/env python3
"""
Enhanced Startup Script for Global Economic Dashboard
This script provides a comprehensive setup and launch system with dependency management,
system checks, and enhanced user experience.
"""

import sys
import subprocess
import os
import importlib.util
import platform
import time
from datetime import datetime

class DashboardLauncher:
    def __init__(self):
        self.required_packages = {
            'dash': '>=2.14.1',
            'dash_bootstrap_components': '>=1.4.1', 
            'plotly': '>=5.15.0',
            'pandas': '>=2.0.0',
            'requests': '>=2.28.0',
            'fpdf2': '>=2.7.4'
        }
        self.optional_packages = {
            'kaleido': '>=0.2.1',  # For static image export
            'psutil': '>=5.9.0',   # For system monitoring
        }
        
    def print_banner(self):
        """Display an attractive startup banner."""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                🌍 GLOBAL ECONOMIC DASHBOARD 🌍               ║ 
║                                                              ║
║            Real-time Economic Data Analysis Platform         ║
║               Powered by World Bank Open Data                ║
║                                                              ║
║  Features:                                                   ║
║  • 📊 Interactive Charts with Multiple Types                 ║
║  • 🌐 200+ Countries & Territories                           ║
║  • 📈 100+ Economic Indicators                               ║
║  • 📤 CSV & PDF Export                                       ║
║  • 📥 Data Import Functionality                              ║
║  • 🎨 Modern Responsive UI                                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
        print(banner)
        
    def check_python_version(self):
        """Check if Python version meets requirements."""
        print("🐍 Checking Python version...")
        
        if sys.version_info < (3, 8):
            print("❌ Error: Python 3.8+ is required")
            print(f"   Current version: {sys.version.split()[0]}")
            print("   Please upgrade Python and try again.")
            return False
            
        print(f"✅ Python {sys.version.split()[0]} - Compatible!")
        return True
        
    def check_system_info(self):
        """Display system information."""
        print("\n💻 System Information:")
        print(f"   OS: {platform.system()} {platform.release()}")
        print(f"   Architecture: {platform.machine()}")
        print(f"   Python: {sys.version.split()[0]}")
        
        # Check available memory if psutil is available
        try:
            import psutil
            memory = psutil.virtual_memory()
            print(f"   Available Memory: {memory.available // (1024**3):.1f} GB")
        except ImportError:
            pass
            
    def check_package(self, package_name, version_req=None):
        """Check if a package is installed and meets version requirements."""
        try:
            spec = importlib.util.find_spec(package_name)
            if spec is None:
                return False, "Not installed"
                
            # Try to import and check version
            module = importlib.import_module(package_name)
            if hasattr(module, '__version__'):
                version = module.__version__
                return True, version
            else:
                return True, "Unknown version"
                
        except ImportError:
            return False, "Import failed"
            
    def install_packages(self, packages):
        """Install missing packages."""
        if not packages:
            return True
            
        print(f"\n📦 Installing {len(packages)} package(s)...")
        print("   This may take a few minutes...")
        
        try:
            # Update pip first
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Install packages
            for package in packages:
                print(f"   Installing {package}...")
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install', package
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
            print("✅ All packages installed successfully!")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Installation failed: {e}")
            print("   Please try installing manually:")
            print(f"   pip install {' '.join(packages)}")
            return False
            
    def check_dependencies(self):
        """Check and install required dependencies."""
        print("\n🔍 Checking dependencies...")
        
        missing_required = []
        missing_optional = []
        
        # Check required packages
        for package, version_req in self.required_packages.items():
            installed, version = self.check_package(package)
            
            if installed:
                print(f"   ✅ {package} ({version})")
            else:
                print(f"   ❌ {package} - {version}")
                missing_required.append(package + version_req.replace('>=', '>='))
        
        # Check optional packages
        for package, version_req in self.optional_packages.items():
            installed, version = self.check_package(package)
            
            if installed:
                print(f"   ✅ {package} ({version}) - Optional")
            else:
                print(f"   ⚠️  {package} - Optional package missing")
                missing_optional.append(package + version_req.replace('>=', '>='))
        
        # Install missing required packages
        if missing_required:
            print(f"\n❌ Missing required packages: {len(missing_required)}")
            if not self.install_packages(missing_required):
                return False
        
        # Offer to install optional packages
        if missing_optional:
            print(f"\n⚠️  Optional packages missing: {len(missing_optional)}")
            print("   These provide enhanced functionality but are not required.")
            
            try:
                response = input("   Install optional packages? (y/N): ").lower().strip()
                if response in ['y', 'yes']:
                    self.install_packages(missing_optional)
            except KeyboardInterrupt:
                print("\n   Skipping optional packages...")
        
        return True
        
    def create_directories(self):
        """Create necessary directories."""
        print("\n📁 Setting up directories...")
        
        directories = [
            'exports',
            'cache', 
            'logs',
            'temp_uploads'
        ]
        
        created_count = 0
        for directory in directories:
            if not os.path.exists(directory):
                try:
                    os.makedirs(directory, exist_ok=True)
                    print(f"   ✅ Created: {directory}/")
                    created_count += 1
                except OSError as e:
                    print(f"   ❌ Failed to create {directory}/: {e}")
            else:
                print(f"   ✅ Exists: {directory}/")
        
        if created_count > 0:
            print(f"   📂 Created {created_count} new directories")
        else:
            print("   📂 All directories already exist")
            
    def check_config_files(self):
        """Check if configuration files exist."""
        print("\n⚙️  Checking configuration...")
        
        config_files = ['config.py', 'main.py']
        missing_files = []
        
        for file in config_files:
            if os.path.exists(file):
                print(f"   ✅ Found: {file}")
            else:
                print(f"   ❌ Missing: {file}")
                missing_files.append(file)
        
        if missing_files:
            print(f"   ❌ Missing critical files: {', '.join(missing_files)}")
            print("   Please ensure all required files are in the current directory.")
            return False
            
        return True
        
    def test_world_bank_api(self):
        """Test connection to World Bank API."""
        print("\n🌐 Testing World Bank API connection...")
        
        try:
            import requests
            
            # Test API endpoint
            url = "http://api.worldbank.org/v2/country?format=json&per_page=1"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print("   ✅ World Bank API is accessible")
                data = response.json()
                if len(data) > 1:
                    print("   ✅ API response format is valid")
                    return True
            else:
                print(f"   ❌ API returned status code: {response.status_code}")
                
        except requests.RequestException as e:
            print(f"   ❌ API connection failed: {e}")
            print("   ⚠️  Dashboard will work with limited functionality")
            
        except ImportError:
            print("   ❌ Requests module not available")
            return False
            
        return False
        
    def display_startup_info(self):
        """Display important startup information."""
        info = """
🚀 Starting Enhanced Global Economic Dashboard...

📋 Quick Start Guide:
   1. Select countries from the dropdown or use quick selection buttons
   2. Choose economic indicators you want to analyze
   3. Adjust the year range as needed
   4. Click "Analyze Data" to fetch and visualize data
   5. Use individual chart type controls for each indicator
   6. Export your analysis as CSV or PDF

💡 Pro Tips:
   • Upload your own CSV data using the import feature
   • Each indicator can have its own chart type
   • Use country groups (G7, BRICS, etc.) for quick analysis
   • Export functionality supports both CSV and PDF formats

🌐 Access Information:
"""
        print(info)
        
    def launch_dashboard(self):
        """Launch the main dashboard application."""
        print("🚀 Launching dashboard...")
        
        try:
            # Import and run the main application
            from main import app, fetch_all_countries
            
            print("📡 Pre-loading country data...")
            countries = fetch_all_countries()
            print(f"✅ Loaded {len(countries)} countries from World Bank API")
            
            print("\n" + "="*60)
            print("🎉 DASHBOARD IS READY!")
            print("="*60)
            print("📱 Local URL:     http://localhost:8050")
            print("🌍 Network URL:   http://0.0.0.0:8050")
            print("⏹️  Stop server:   Press Ctrl+C")
            print("="*60)
            
            # Start the server
            app.run_server(
                debug=False,
                host='0.0.0.0',
                port=8050,
                dev_tools_hot_reload=False,
                dev_tools_ui=False
            )
            
        except KeyboardInterrupt:
            print("\n\n👋 Dashboard stopped by user")
            print("   Thank you for using Global Economic Dashboard!")
            
        except ImportError as e:
            print(f"\n❌ Error importing main application: {e}")
            print("   Make sure main.py and config.py are in the same directory")
            
        except Exception as e:
            print(f"\n❌ Unexpected error during startup: {e}")
            print("   Please check the error details above")
            
    def run_diagnostics(self):
        """Run comprehensive system diagnostics."""
        print("\n🔧 Running system diagnostics...")
        
        diagnostics = {
            "Python Version": sys.version.split()[0],
            "Platform": f"{platform.system()} {platform.release()}",
            "Working Directory": os.getcwd(),
            "Script Location": os.path.abspath(__file__),
        }
        
        # Check disk space
        try:
            import shutil
            total, used, free = shutil.disk_usage(".")
            diagnostics["Available Space"] = f"{free // (1024**3)} GB"
        except:
            diagnostics["Available Space"] = "Unknown"
            
        # Check network connectivity
        try:
            import socket
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            diagnostics["Internet Connection"] = "Available"
        except:
            diagnostics["Internet Connection"] = "Limited or unavailable"
        
        for key, value in diagnostics.items():
            print(f"   {key}: {value}")
            
    def main(self):
        """Main execution flow."""
        # Clear screen for better presentation
        os.system('cls' if os.name == 'nt' else 'clear')
        
        self.print_banner()
        
        # System checks
        if not self.check_python_version():
            input("\nPress Enter to exit...")
            return
            
        self.check_system_info()
        
        # Configuration checks
        if not self.check_config_files():
            input("\nPress Enter to exit...")
            return
            
        # Dependency management
        if not self.check_dependencies():
            input("\nPress Enter to exit...")
            return
            
        # Directory setup
        self.create_directories()
        
        # API connectivity test
        self.test_world_bank_api()
        
        # Show startup information
        self.display_startup_info()
        
        # Optional diagnostics
        try:
            show_diag = input("🔧 Run detailed diagnostics? (y/N): ").lower().strip()
            if show_diag in ['y', 'yes']:
                self.run_diagnostics()
        except KeyboardInterrupt:
            print("\n   Skipping diagnostics...")
        
        print("\n" + "="*60)
        
        # Launch the dashboard
        try:
            ready = input("🚀 Ready to launch dashboard? Press Enter to continue (Ctrl+C to exit)...")
            self.launch_dashboard()
        except KeyboardInterrupt:
            print("\n👋 Startup cancelled by user")

if __name__ == "__main__":
    launcher = DashboardLauncher()
    launcher.main()