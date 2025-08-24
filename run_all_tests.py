"""
Complete Test Runner for AI Band Backend
Created by Sergie Code

Runs all test suites and provides comprehensive validation.
"""

import sys
import subprocess
from pathlib import Path


def run_test_suite(test_file, suite_name):
    """Run a specific test suite and return results."""
    print(f"\n{'='*20} {suite_name} {'='*20}")
    
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
    
    except Exception as e:
        print(f"❌ Error running {suite_name}: {e}")
        return False


def validate_app_functionality():
    """Validate that the main app works."""
    print(f"\n{'='*20} APPLICATION VALIDATION {'='*20}")
    
    try:
        # Test main application
        result = subprocess.run(
            [sys.executable, "src/main.py"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        
        if result.returncode == 0:
            print("Main application runs successfully")
            print("MIDI files generated successfully")
            return True
        else:
            print("Main application failed")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
    
    except Exception as e:
        print(f"Error validating application: {e}")
        return False


def check_output_files():
    """Check that output files are created."""
    print(f"\n{'='*20} OUTPUT FILE VALIDATION {'='*20}")
    
    output_dir = Path(__file__).parent / "src" / "output"
    expected_files = ["bass_track.mid", "drum_track.mid"]
    
    all_files_exist = True
    
    for file_name in expected_files:
        file_path = output_dir / file_name
        if file_path.exists() and file_path.stat().st_size > 0:
            print(f"[OK] {file_name} exists and has content ({file_path.stat().st_size} bytes)")
        else:
            print(f"[FAIL] {file_name} missing or empty")
            all_files_exist = False
    
    if all_files_exist:
        print("All expected output files are present and valid")
    
    return all_files_exist


def main():
    """Run all tests and validations."""
    print("AI Band Backend - Complete Test Suite")
    print("Created by Sergie Code")
    print("=" * 60)
    
    test_results = []
    
    # Test suites to run
    test_suites = [
        ("test_ai_band.py", "Basic Tests"),
        ("test_advanced.py", "Advanced Tests"),
        ("test_integration.py", "Integration Tests"),
    ]
    
    # Run all test suites
    for test_file, suite_name in test_suites:
        test_path = Path(__file__).parent / test_file
        if test_path.exists():
            success = run_test_suite(test_file, suite_name)
            test_results.append((suite_name, success))
        else:
            print(f"Test file {test_file} not found")
            test_results.append((suite_name, False))
    
    # Validate application functionality
    app_success = validate_app_functionality()
    test_results.append(("Application Validation", app_success))
    
    # Check output files
    files_success = check_output_files()
    test_results.append(("Output Files", files_success))
    
    # Final summary
    print(f"\n{'='*60}")
    print("FINAL TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, success in test_results:
        status = "[PASSED]" if success else "[FAILED]"
        print(f"{test_name:<25} {status}")
        if success:
            passed += 1
    
    print("-" * 60)
    print(f"Total: {passed}/{total} test suites passed")
    
    if passed == total:
        print("\nALL TESTS PASSED!")
        print("The AI Band Backend is working perfectly!")
        print("Ready for production use!")
        print("Ready for integration with other projects!")
        print("\nNext steps:")
        print("  - Use the backend in your AI music projects")
        print("  - Integrate with ai-band-plugin for VST/AU support")
        print("  - Add more AI models for enhanced generation")
        print("  - Create real-time audio processing features")
        return True
    else:
        print(f"\n{total - passed} test suite(s) failed")
        print("Please fix the issues before using in production")
        return False


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nTests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nTest runner error: {e}")
        sys.exit(1)
