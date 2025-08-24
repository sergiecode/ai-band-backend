"""
Setup Script for AI Band Backend
Created by Sergie Code

This script helps set up the development environment and verify installation.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error during {description}: {e}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible")
        print("Please install Python 3.8 or higher")
        return False


def setup_virtual_environment():
    """Set up virtual environment if it doesn't exist."""
    venv_path = Path("venv")
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    print("🔧 Creating virtual environment...")
    if os.name == 'nt':  # Windows
        command = "python -m venv venv"
    else:  # macOS/Linux
        command = "python3 -m venv venv"
    
    return run_command(command, "Virtual environment creation")


def install_dependencies():
    """Install required dependencies."""
    if os.name == 'nt':  # Windows
        pip_command = "venv\\Scripts\\pip.exe"
    else:  # macOS/Linux
        pip_command = "venv/bin/pip"
    
    command = f"{pip_command} install -r requirements.txt"
    return run_command(command, "Dependencies installation")


def test_installation():
    """Test if the installation works."""
    print("🧪 Testing installation...")
    
    # Test imports
    test_script = '''
import sys
sys.path.append("src")

try:
    from chord_detection import ChordDetector
    from midi_generator import MidiGenerator
    print("✅ All modules imported successfully")
    
    # Test basic functionality
    detector = ChordDetector()
    generator = MidiGenerator()
    
    # Test chord detection
    sample_chords = [
        {"chord": "C", "start_time": 0.0, "duration": 2.0},
        {"chord": "Am", "start_time": 2.0, "duration": 2.0},
    ]
    
    tempo = detector.detect_tempo(sample_chords)
    key = detector.detect_key(sample_chords)
    print(f"✅ Chord detection works - Tempo: {tempo}, Key: {key}")
    
    print("✅ Installation test completed successfully!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Test error: {e}")
    sys.exit(1)
'''
    
    # Write test script to temporary file
    with open("test_installation.py", "w") as f:
        f.write(test_script)
    
    # Run test
    if os.name == 'nt':  # Windows
        python_command = "venv\\Scripts\\python.exe"
    else:  # macOS/Linux
        python_command = "venv/bin/python"
    
    success = run_command(f"{python_command} test_installation.py", "Installation test")
    
    # Clean up
    try:
        os.remove("test_installation.py")
    except Exception:
        pass
    
    return success


def main():
    """Main setup function."""
    print("🎸 AI Band Backend Setup")
    print("=" * 40)
    print("Created by Sergie Code - AI Tools for Musicians")
    print()
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Set up virtual environment
    if not setup_virtual_environment():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Test installation
    if not test_installation():
        return False
    
    print()
    print("🎉 Setup completed successfully!")
    print()
    print("Next steps:")
    print("1. Activate the virtual environment:")
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\activate")
    else:  # macOS/Linux
        print("   source venv/bin/activate")
    print("2. Run the example:")
    print("   cd src")
    print("   python main.py")
    print()
    print("Check the README.md for more information!")
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        sys.exit(1)
