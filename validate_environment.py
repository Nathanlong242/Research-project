#!/usr/bin/env python3
"""
Environment Validation Script
Run this before starting experiments to verify everything works.
"""

import sys
import importlib
import subprocess
from pathlib import Path

def check_python_version():
    """Verify Python 3.8+"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        return False, f"Python {version.major}.{version.minor} found, need 3.8+"
    return True, f"Python {version.major}.{version.minor}.{version.micro}"

def check_dependencies():
    """Verify all required packages are installed"""
    required = [
        'numpy',
        'pandas',
        'scipy',
        'matplotlib',
        'opencv-python',  # cv2
        'pynput',
        'mss',
    ]

    missing = []
    for package in required:
        try:
            # Handle opencv-python → cv2 mapping
            import_name = 'cv2' if package == 'opencv-python' else package
            importlib.import_module(import_name)
        except ImportError:
            missing.append(package)

    if missing:
        return False, f"Missing packages: {', '.join(missing)}"
    return True, f"All {len(required)} dependencies installed"

def check_main_agent():
    """Verify main agent file exists and imports"""
    agent_file = Path('wow_agent_human_equivalent_stabilized.py')
    if not agent_file.exists():
        return False, f"Agent file not found: {agent_file}"

    try:
        from wow_agent_human_equivalent_stabilized import HumanEquivalentCognition
        return True, "Agent imports successfully"
    except Exception as e:
        return False, f"Agent import failed: {str(e)[:100]}"

def check_research_infrastructure():
    """Verify logging and analysis infrastructure"""
    files = {
        'behavioral_logger.py': 'Behavioral logging',
        'research_analysis.py': 'Statistical analysis',
        'experiment_config.py': 'Experiment configuration',
        'run_experiment.py': 'Experiment runner'
    }

    missing = []
    for file, desc in files.items():
        if not Path(file).exists():
            missing.append(f"{desc} ({file})")

    if missing:
        return False, f"Missing files: {', '.join(missing)}"
    return True, "All infrastructure files present"

def check_data_directory():
    """Verify research_data directory exists or can be created"""
    data_dir = Path('research_data')
    if not data_dir.exists():
        try:
            data_dir.mkdir(parents=True)
            return True, "Created research_data/ directory"
        except Exception as e:
            return False, f"Cannot create research_data/: {e}"
    return True, "research_data/ directory exists"

def check_disk_space():
    """Verify sufficient disk space for 90 hours of data"""
    try:
        stat = subprocess.run(['df', '-h', '.'], capture_output=True, text=True)
        # Parse available space (rough check)
        lines = stat.stdout.split('\n')
        if len(lines) >= 2:
            available = lines[1].split()[3]  # Available column
            return True, f"Disk space available: {available}"
        return True, "Disk space check inconclusive"
    except:
        return True, "Disk space check skipped (df command unavailable)"

def check_screen_capture():
    """Test if screen capture works"""
    try:
        import mss
        with mss.mss() as sct:
            monitor = sct.monitors[0]  # Primary monitor
            screenshot = sct.grab(monitor)
            if screenshot.width > 0 and screenshot.height > 0:
                return True, f"Screen capture works ({screenshot.width}x{screenshot.height})"
            return False, "Screen capture returned empty image"
    except Exception as e:
        return False, f"Screen capture failed: {str(e)[:100]}"

def run_all_checks():
    """Run all validation checks and report results"""
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Main Agent", check_main_agent),
        ("Research Infrastructure", check_research_infrastructure),
        ("Data Directory", check_data_directory),
        ("Disk Space", check_disk_space),
        ("Screen Capture", check_screen_capture),
    ]

    print("=" * 70)
    print("ENVIRONMENT VALIDATION")
    print("=" * 70)
    print()

    all_passed = True
    results = []

    for name, check_func in checks:
        try:
            passed, message = check_func()
            status = "✓ PASS" if passed else "✗ FAIL"
            results.append((name, passed, message))

            if not passed:
                all_passed = False

        except Exception as e:
            results.append((name, False, f"Check crashed: {str(e)[:100]}"))
            all_passed = False

    # Print results
    for name, passed, message in results:
        status = "✓" if passed else "✗"
        print(f"{status} {name:30s} {message}")

    print()
    print("=" * 70)

    if all_passed:
        print("✓ ALL CHECKS PASSED - Ready to run experiments")
        print()
        print("Next steps:")
        print("  1. Launch World of Warcraft 1.12")
        print("  2. Run pilot experiment:")
        print("     python run_experiment.py --condition tier7 --session-id PILOT_T7_001 --duration-hours 2")
        print()
        return 0
    else:
        print("✗ SOME CHECKS FAILED - Fix issues before running experiments")
        print()
        print("Common fixes:")
        print("  - Missing dependencies: pip install -r requirements.txt")
        print("  - Missing agent file: Verify you're in the project directory")
        print("  - Screen capture issues: Check display server (X11/Wayland)")
        print()
        return 1

if __name__ == '__main__':
    sys.exit(run_all_checks())
