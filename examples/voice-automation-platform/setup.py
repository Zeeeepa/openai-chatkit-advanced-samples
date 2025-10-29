#!/usr/bin/env python3
"""
Voice Automation Platform - Deployment Setup
============================================

Comprehensive deployment script that:
1. Validates environment and dependencies
2. Configures backend and frontend
3. Installs all required packages
4. Starts both services
5. Provides health checks and monitoring

Usage:
    python3 setup.py --mode=dev          # Development mode
    python3 setup.py --mode=prod         # Production mode
    python3 setup.py --mode=demo         # Demo with Z.ai vision
    python3 setup.py --check             # Check environment only
"""

import os
import sys
import subprocess
import time
import argparse
import json
import shutil
from pathlib import Path
from typing import Optional, Dict, List, Tuple
import signal


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
    UNDERLINE = '\033[4m'


class DeploymentManager:
    """Manages the complete deployment lifecycle"""
    
    def __init__(self, mode: str = "dev"):
        self.mode = mode
        self.root_dir = Path(__file__).parent
        self.backend_dir = self.root_dir / "backend"
        self.frontend_dir = self.root_dir / "frontend"
        self.backend_process = None
        self.frontend_process = None
        
    def print_header(self, text: str):
        """Print styled header"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.END}")
        print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.END}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.END}\n")
        
    def print_success(self, text: str):
        """Print success message"""
        print(f"{Colors.GREEN}✅ {text}{Colors.END}")
        
    def print_error(self, text: str):
        """Print error message"""
        print(f"{Colors.RED}❌ {text}{Colors.END}")
        
    def print_warning(self, text: str):
        """Print warning message"""
        print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")
        
    def print_info(self, text: str):
        """Print info message"""
        print(f"{Colors.CYAN}ℹ️  {text}{Colors.END}")
        
    def run_command(self, cmd: str, cwd: Optional[Path] = None, 
                   capture_output: bool = False, check: bool = True) -> Tuple[bool, str]:
        """Run shell command and return success status and output"""
        try:
            if capture_output:
                result = subprocess.run(
                    cmd, 
                    shell=True, 
                    cwd=cwd, 
                    capture_output=True, 
                    text=True,
                    check=check
                )
                return True, result.stdout
            else:
                subprocess.run(cmd, shell=True, cwd=cwd, check=check)
                return True, ""
        except subprocess.CalledProcessError as e:
            return False, str(e)
            
    def check_python_version(self) -> bool:
        """Check if Python version is compatible"""
        self.print_info("Checking Python version...")
        version = sys.version_info
        
        if version.major >= 3 and version.minor >= 8:
            self.print_success(f"Python {version.major}.{version.minor}.{version.micro} - Compatible")
            return True
        else:
            self.print_error(f"Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.8+")
            return False
            
    def check_node_version(self) -> bool:
        """Check if Node.js is installed"""
        self.print_info("Checking Node.js version...")
        success, output = self.run_command("node --version", capture_output=True, check=False)
        
        if success and output:
            version = output.strip()
            self.print_success(f"Node.js {version} - Available")
            return True
        else:
            self.print_warning("Node.js not found - Frontend will need Node.js 18+")
            return False
            
    def check_npm_version(self) -> bool:
        """Check if npm is installed"""
        self.print_info("Checking npm version...")
        success, output = self.run_command("npm --version", capture_output=True, check=False)
        
        if success and output:
            version = output.strip()
            self.print_success(f"npm {version} - Available")
            return True
        else:
            self.print_warning("npm not found - Required for frontend")
            return False
            
    def create_backend_env(self) -> bool:
        """Create backend .env file"""
        self.print_info("Configuring backend environment...")
        
        env_file = self.backend_dir / ".env"
        env_example = self.backend_dir / ".env.example"
        
        if env_file.exists():
            self.print_warning(".env already exists - skipping creation")
            return True
            
        if not env_example.exists():
            self.print_error(".env.example not found")
            return False
            
        # Read example and create .env
        with open(env_example, 'r') as f:
            content = f.read()
            
        # Add demo configuration for Z.ai if in demo mode
        if self.mode == "demo":
            content += "\n# Z.ai Vision Configuration\n"
            content += "ANTHROPIC_MODEL=glm-4.5V\n"
            content += "ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic\n"
            content += "ANTHROPIC_AUTH_TOKEN=665b963943b647dc9501dff942afb877.A47LrMc7sgGjyfBJ\n"
            
        with open(env_file, 'w') as f:
            f.write(content)
            
        self.print_success("Backend .env created")
        self.print_warning("⚠️  IMPORTANT: Update OPENAI_API_KEY in backend/.env")
        
        if self.mode == "demo":
            self.print_info("Demo mode: Z.ai vision credentials added")
            
        return True
        
    def create_frontend_env(self) -> bool:
        """Create frontend .env.local file"""
        self.print_info("Configuring frontend environment...")
        
        env_file = self.frontend_dir / ".env.local"
        env_example = self.frontend_dir / ".env.example"
        
        if env_file.exists():
            self.print_warning(".env.local already exists - skipping creation")
            return True
            
        if not env_example.exists():
            self.print_error(".env.example not found")
            return False
            
        # Copy example to .env.local
        shutil.copy(env_example, env_file)
        
        self.print_success("Frontend .env.local created")
        self.print_warning("⚠️  IMPORTANT: Update NEXT_PUBLIC_CHATKIT_WORKFLOW_ID in frontend/.env.local")
        return True
        
    def install_backend_dependencies(self) -> bool:
        """Install Python backend dependencies"""
        self.print_info("Installing backend dependencies...")
        
        req_file = self.backend_dir / "requirements.txt"
        if not req_file.exists():
            self.print_error("requirements.txt not found")
            return False
            
        success, _ = self.run_command(
            f"pip install -r requirements.txt", 
            cwd=self.backend_dir
        )
        
        if success:
            self.print_success("Backend dependencies installed")
            return True
        else:
            self.print_error("Failed to install backend dependencies")
            return False
            
    def install_frontend_dependencies(self) -> bool:
        """Install Node.js frontend dependencies"""
        self.print_info("Installing frontend dependencies...")
        
        package_file = self.frontend_dir / "package.json"
        if not package_file.exists():
            self.print_error("package.json not found")
            return False
            
        success, _ = self.run_command("npm install", cwd=self.frontend_dir)
        
        if success:
            self.print_success("Frontend dependencies installed")
            return True
        else:
            self.print_error("Failed to install frontend dependencies")
            return False
            
    def start_backend(self) -> bool:
        """Start FastAPI backend server"""
        self.print_info("Starting backend server...")
        
        cmd = "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
        
        try:
            self.backend_process = subprocess.Popen(
                cmd.split(),
                cwd=self.backend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait a bit and check if it started
            time.sleep(3)
            
            if self.backend_process.poll() is None:
                self.print_success("Backend server started on http://localhost:8000")
                return True
            else:
                self.print_error("Backend server failed to start")
                return False
                
        except Exception as e:
            self.print_error(f"Failed to start backend: {e}")
            return False
            
    def start_frontend(self) -> bool:
        """Start Next.js frontend server"""
        self.print_info("Starting frontend server...")
        
        cmd = "npm run dev"
        
        try:
            self.frontend_process = subprocess.Popen(
                cmd.split(),
                cwd=self.frontend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait a bit and check if it started
            time.sleep(5)
            
            if self.frontend_process.poll() is None:
                self.print_success("Frontend server started on http://localhost:3000")
                return True
            else:
                self.print_error("Frontend server failed to start")
                return False
                
        except Exception as e:
            self.print_error(f"Failed to start frontend: {e}")
            return False
            
    def check_backend_health(self) -> bool:
        """Check if backend is healthy"""
        self.print_info("Checking backend health...")
        
        try:
            import requests
            response = requests.get("http://localhost:8000/health", timeout=5)
            
            if response.status_code == 200:
                self.print_success("Backend is healthy ✓")
                return True
            else:
                self.print_warning(f"Backend returned status {response.status_code}")
                return False
                
        except Exception as e:
            self.print_warning(f"Backend health check failed: {e}")
            return False
            
    def check_frontend_health(self) -> bool:
        """Check if frontend is accessible"""
        self.print_info("Checking frontend health...")
        
        try:
            import requests
            response = requests.get("http://localhost:3000", timeout=5)
            
            if response.status_code == 200:
                self.print_success("Frontend is accessible ✓")
                return True
            else:
                self.print_warning(f"Frontend returned status {response.status_code}")
                return False
                
        except Exception as e:
            self.print_warning(f"Frontend health check failed: {e}")
            return False
            
    def print_status_panel(self):
        """Print system status panel"""
        self.print_header("SYSTEM STATUS")
        
        # Backend status
        if self.backend_process and self.backend_process.poll() is None:
            print(f"Backend:  {Colors.GREEN}●{Colors.END} Running on http://localhost:8000")
            print(f"          {Colors.CYAN}📚 API Docs: http://localhost:8000/docs{Colors.END}")
        else:
            print(f"Backend:  {Colors.RED}●{Colors.END} Not running")
            
        # Frontend status
        if self.frontend_process and self.frontend_process.poll() is None:
            print(f"Frontend: {Colors.GREEN}●{Colors.END} Running on http://localhost:3000")
            print(f"          {Colors.CYAN}🌐 App: http://localhost:3000{Colors.END}")
        else:
            print(f"Frontend: {Colors.RED}●{Colors.END} Not running")
            
        print()
        
    def print_quick_start_guide(self):
        """Print quick start guide"""
        self.print_header("QUICK START GUIDE")
        
        print(f"{Colors.BOLD}1. Open the application:{Colors.END}")
        print(f"   {Colors.CYAN}http://localhost:3000{Colors.END}\n")
        
        print(f"{Colors.BOLD}2. Test the backend API:{Colors.END}")
        print(f"   {Colors.CYAN}http://localhost:8000/docs{Colors.END}\n")
        
        print(f"{Colors.BOLD}3. Configuration files:{Colors.END}")
        print(f"   Backend:  {Colors.CYAN}backend/.env{Colors.END}")
        print(f"   Frontend: {Colors.CYAN}frontend/.env.local{Colors.END}\n")
        
        print(f"{Colors.BOLD}4. Stop the servers:{Colors.END}")
        print(f"   Press {Colors.YELLOW}Ctrl+C{Colors.END} to stop\n")
        
        if self.mode == "demo":
            print(f"{Colors.BOLD}5. Vision Testing:{Colors.END}")
            print(f"   Run: {Colors.CYAN}python3 tests/test_vision_integration.py{Colors.END}\n")
            
    def cleanup(self):
        """Cleanup processes on exit"""
        self.print_info("\nShutting down services...")
        
        if self.backend_process:
            self.backend_process.terminate()
            self.backend_process.wait(timeout=5)
            self.print_success("Backend stopped")
            
        if self.frontend_process:
            self.frontend_process.terminate()
            self.frontend_process.wait(timeout=5)
            self.print_success("Frontend stopped")
            
        print(f"\n{Colors.GREEN}Goodbye! 👋{Colors.END}\n")
        
    def run_checks_only(self) -> bool:
        """Run environment checks only"""
        self.print_header("ENVIRONMENT CHECKS")
        
        checks = [
            ("Python Version", self.check_python_version()),
            ("Node.js", self.check_node_version()),
            ("npm", self.check_npm_version()),
        ]
        
        all_passed = all(result for _, result in checks)
        
        print()
        if all_passed:
            self.print_success("All checks passed! ✓")
        else:
            self.print_warning("Some checks failed - review output above")
            
        return all_passed
        
    def deploy(self) -> bool:
        """Run complete deployment"""
        try:
            # Header
            self.print_header(f"VOICE AUTOMATION PLATFORM - {self.mode.upper()} MODE")
            
            # Environment checks
            if not self.run_checks_only():
                self.print_error("Environment checks failed - cannot proceed")
                return False
                
            # Configuration
            self.print_header("CONFIGURATION")
            if not self.create_backend_env():
                return False
            if not self.create_frontend_env():
                return False
                
            # Dependencies
            self.print_header("INSTALLING DEPENDENCIES")
            if not self.install_backend_dependencies():
                return False
                
            if self.check_node_version():
                if not self.install_frontend_dependencies():
                    return False
            else:
                self.print_warning("Skipping frontend installation - Node.js not available")
                
            # Start services
            self.print_header("STARTING SERVICES")
            
            if not self.start_backend():
                return False
                
            # Wait for backend to be ready
            time.sleep(3)
            self.check_backend_health()
            
            if self.check_node_version():
                if not self.start_frontend():
                    return False
                    
                # Wait for frontend to be ready
                time.sleep(5)
                self.check_frontend_health()
            else:
                self.print_warning("Skipping frontend start - Node.js not available")
                
            # Status
            self.print_status_panel()
            self.print_quick_start_guide()
            
            # Keep running
            self.print_info("Services are running. Press Ctrl+C to stop.")
            
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n")
            self.cleanup()
            return True
            
        except Exception as e:
            self.print_error(f"Deployment failed: {e}")
            self.cleanup()
            return False


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Voice Automation Platform Deployment Tool"
    )
    parser.add_argument(
        "--mode",
        choices=["dev", "prod", "demo"],
        default="dev",
        help="Deployment mode (default: dev)"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Run environment checks only"
    )
    
    args = parser.parse_args()
    
    manager = DeploymentManager(mode=args.mode)
    
    # Setup signal handlers
    signal.signal(signal.SIGINT, lambda s, f: manager.cleanup() or sys.exit(0))
    signal.signal(signal.SIGTERM, lambda s, f: manager.cleanup() or sys.exit(0))
    
    if args.check:
        success = manager.run_checks_only()
    else:
        success = manager.deploy()
        
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

