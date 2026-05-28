"""Simple test to verify MVC architecture works."""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all MVC components can be imported."""
    print("Testing imports...")

    try:
        from model import APP_DIR, TEMPLATES, NC_FLAVORS
        print("[OK] Model imports successful")
    except Exception as e:
        print(f"[FAIL] Model imports failed: {e}")
        return False

    try:
        from model.payload_transformer import payload_to_printf
        from model.command_builder import build_command
        from model.profile_manager import ProfileManager
        print("[OK] Model functions imported successfully")
    except Exception as e:
        print(f"[FAIL] Model functions failed: {e}")
        return False

    try:
        from controller import AppController, PayloadController, ProfileController, CommandController
        print("[OK] Controller imports successful")
    except Exception as e:
        print(f"[FAIL] Controller imports failed: {e}")
        return False

    try:
        from view import MainWindow, TargetPanel, PayloadEditor, Sidebar, CommandPreview, HelpersPanel
        print("[OK] View imports successful")
    except Exception as e:
        print(f"[FAIL] View imports failed: {e}")
        return False

    return True

def test_basic_functionality():
    """Test basic functionality without GUI."""
    print("\nTesting basic functionality...")

    try:
        from controller import AppController

        # Create controller
        controller = AppController()
        print("[OK] AppController created successfully")

        # Test basic command generation
        controller.host = "127.0.0.1"
        controller.port = "1337"
        controller.raw_payload = "hello"
        command = controller.get_command()

        if "nc" in command and "1337" in command:
            print("[OK] Command generation works")
        else:
            print(f"[FAIL] Command generation failed")
            return False

        # Test GET mode
        controller.editor_mode = "get"
        controller.update_get_params(path="/test", params={"flag": "pwn"})
        get_command = controller.get_command()

        if "GET" in get_command and "/test" in get_command:
            print("[OK] GET mode works")
        else:
            print(f"[FAIL] GET mode failed")
            return False

        # Test POST mode
        controller.editor_mode = "post"
        controller.update_post_params(path="/submit", content_type="application/x-www-form-urlencoded", params={"data": "test"})
        post_command = controller.get_command()

        if "POST" in post_command and "Content-Length" in post_command:
            print("[OK] POST mode works")
        else:
            print(f"[FAIL] POST mode failed")
            return False

        return True

    except Exception as e:
        print(f"[FAIL] Basic functionality test failed: {e}")
        return False

def test_payload_modes():
    """Test different payload modes."""
    print("\nTesting payload modes...")

    try:
        from model.payload_transformer import payload_to_printf

        # Test plain text
        result = payload_to_printf("hello", "Plain text")
        if "hello" in result:
            print("[OK] Plain text mode works")
        else:
            print(f"[FAIL] Plain text mode failed: {result}")
            return False

        # Test escapes mode
        result = payload_to_printf("hello\\nworld", "Escapes (\\r\\n, \\x41)")
        if "hello" in result and "world" in result:
            print("[OK] Escapes mode works")
        else:
            print(f"[FAIL] Escapes mode failed: {result}")
            return False

        # Test hex mode
        result = payload_to_printf("41 42 43", "Hex (41 42 43)")
        if "ABC" in result:
            print("[OK] Hex mode works")
        else:
            print(f"[FAIL] Hex mode failed: {result}")
            return False

        return True

    except Exception as e:
        print(f"[FAIL] Payload modes test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 50)
    print("MVC Architecture Test Suite")
    print("=" * 50)

    results = []

    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Basic Functionality", test_basic_functionality()))
    results.append(("Payload Modes", test_payload_modes()))

    # Print results
    print("\n" + "=" * 50)
    print("Test Results:")
    print("=" * 50)

    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")

    # Overall result
    all_passed = all(result for _, result in results)
    print("=" * 50)
    if all_passed:
        print("[SUCCESS] All tests passed!")
    else:
        print("[FAILURE] Some tests failed")

    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)