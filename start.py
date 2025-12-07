#!/usr/bin/env python3
"""
FIBO Command Center - Universal Startup Script
Starts both frontend and backend servers with a single command
"""

import subprocess
import sys
import os
import platform
import time
from pathlib import Path

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    """Print startup banner"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}╔═══════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}║                                                       ║{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}║          🚀 FIBO COMMAND CENTER 🚀                   ║{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}║     Professional AI Visual Production Suite           ║{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}║                                                       ║{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}╚═══════════════════════════════════════════════════════╝{Colors.END}\n")

def check_requirements():
    """Check if required dependencies are installed"""
    print(f"{Colors.BOLD}🔍 Checking requirements...{Colors.END}")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print(f"{Colors.RED}❌ Python 3.8+ required. Current: {sys.version}{Colors.END}")
        sys.exit(1)
    print(f"{Colors.GREEN}✅ Python {sys.version.split()[0]}{Colors.END}")
    
    # Check Node.js
    try:
        node_version = subprocess.check_output(['node', '--version'], 
                                               stderr=subprocess.DEVNULL,
                                               text=True).strip()
        print(f"{Colors.GREEN}✅ Node.js {node_version}{Colors.END}")
    except FileNotFoundError:
        print(f"{Colors.RED}❌ Node.js not found. Please install Node.js 16+{Colors.END}")
        sys.exit(1)
    
    # Check npm (try multiple ways for PowerShell compatibility)
    npm_found = False
    try:
        npm_version = subprocess.check_output(['npm', '--version'],
                                             stderr=subprocess.DEVNULL,
                                             text=True,
                                             shell=True).strip()
        print(f"{Colors.GREEN}✅ npm {npm_version}{Colors.END}")
        npm_found = True
    except:
        try:
            # Try with cmd /c for Windows
            npm_version = subprocess.check_output(['cmd', '/c', 'npm', '--version'],
                                                 stderr=subprocess.DEVNULL,
                                                 text=True).strip()
            print(f"{Colors.GREEN}✅ npm {npm_version}{Colors.END}")
            npm_found = True
        except:
            pass
    
    if not npm_found:
        print(f"{Colors.RED}❌ npm not found{Colors.END}")
        sys.exit(1)

def get_project_root():
    """Get the project root directory"""
    return Path(__file__).parent

def start_backend():
    """Start the FastAPI backend server"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}🔧 Starting Backend Server...{Colors.END}")
    
    project_root = get_project_root()
    backend_dir = project_root / "backend"
    
    # Check if virtual environment exists
    if platform.system() == "Windows":
        python_exe = backend_dir / "venv" / "Scripts" / "python.exe"
        activate_script = backend_dir / "venv" / "Scripts" / "activate.bat"
    else:
        python_exe = backend_dir / "venv" / "bin" / "python"
        activate_script = backend_dir / "venv" / "bin" / "activate"
    
    if not python_exe.exists():
        print(f"{Colors.YELLOW}⚠️  Virtual environment not found. Creating...{Colors.END}")
        subprocess.run([sys.executable, "-m", "venv", str(backend_dir / "venv")], 
                      cwd=backend_dir, check=True)
        print(f"{Colors.GREEN}✅ Virtual environment created{Colors.END}")
        
        # Install requirements
        print(f"{Colors.YELLOW}📦 Installing backend dependencies...{Colors.END}")
        subprocess.run([str(python_exe), "-m", "pip", "install", "--upgrade", "pip"],
                      cwd=backend_dir, check=True)
        subprocess.run([str(python_exe), "-m", "pip", "install", "-r", "requirements.txt"],
                      cwd=backend_dir, check=True)
        print(f"{Colors.GREEN}✅ Backend dependencies installed{Colors.END}")
    
    # Start uvicorn server
    print(f"{Colors.CYAN}🌐 Backend will be available at: http://localhost:8000{Colors.END}")
    print(f"{Colors.CYAN}📚 API Docs: http://localhost:8000/api/docs{Colors.END}")
    
    backend_cmd = [str(python_exe), "-m", "uvicorn", "main:app", 
                   "--reload", "--host", "0.0.0.0", "--port", "8000"]
    
    if platform.system() == "Windows":
        backend_process = subprocess.Popen(
            backend_cmd,
            cwd=backend_dir,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    else:
        backend_process = subprocess.Popen(
            backend_cmd,
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    
    return backend_process

def start_frontend():
    """Start the React frontend development server"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}⚛️  Starting Frontend Server...{Colors.END}")
    
    project_root = get_project_root()
    frontend_dir = project_root / "frontend"
    
    # Check if node_modules exists
    if not (frontend_dir / "node_modules").exists():
        print(f"{Colors.YELLOW}⚠️  node_modules not found. Installing dependencies...{Colors.END}")
        subprocess.run(["npm", "install", "--legacy-peer-deps"],
                      cwd=frontend_dir, check=True, shell=True)
        print(f"{Colors.GREEN}✅ Frontend dependencies installed{Colors.END}")
    
    # Start development server
    print(f"{Colors.CYAN}🌐 Frontend will be available at: http://localhost:3000{Colors.END}")
    
    if platform.system() == "Windows":
        frontend_process = subprocess.Popen(
            ["cmd", "/c", "npm", "start"],
            cwd=frontend_dir,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    else:
        frontend_process = subprocess.Popen(
            ["npm", "start"],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    
    return frontend_process

def main():
    """Main function to start both servers"""
    try:
        print_banner()
        check_requirements()
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}🚀 Starting FIBO Command Center...{Colors.END}\n")
        
        # Start backend
        backend_process = start_backend()
        time.sleep(2)  # Wait for backend to initialize
        
        # Start frontend
        frontend_process = start_frontend()
        time.sleep(2)  # Wait for frontend to initialize
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}✨ FIBO Command Center is running!{Colors.END}\n")
        print(f"{Colors.CYAN}Frontend: {Colors.BOLD}http://localhost:3000{Colors.END}")
        print(f"{Colors.CYAN}Backend:  {Colors.BOLD}http://localhost:8000{Colors.END}")
        print(f"{Colors.CYAN}API Docs: {Colors.BOLD}http://localhost:8000/api/docs{Colors.END}")
        print(f"\n{Colors.YELLOW}Press Ctrl+C to stop all servers{Colors.END}\n")
        
        # Keep the script running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}🛑 Shutting down servers...{Colors.END}")
            backend_process.terminate()
            frontend_process.terminate()
            
            # Wait for processes to terminate
            backend_process.wait(timeout=5)
            frontend_process.wait(timeout=5)
            
            print(f"{Colors.GREEN}✅ All servers stopped{Colors.END}")
    
    except Exception as e:
        print(f"{Colors.RED}❌ Error: {str(e)}{Colors.END}")
        sys.exit(1)

if __name__ == "__main__":
    main()
