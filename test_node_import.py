#!/usr/bin/env python3
"""
Test script to verify that ReplaceColorAtNode can be imported correctly
This simulates how ComfyUI would load the extension
"""

import sys
import os

# Add the current directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def test_node_import():
    """Test importing the ReplaceColorAtNode"""
    try:
        # Import the node directly
        import importlib.util
        node_file = os.path.join(current_dir, "nodes", "palette", "replace_color_at_node.py")
        spec = importlib.util.spec_from_file_location("replace_color_at_node", node_file)

        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Check if the class exists
            if hasattr(module, 'ReplaceColorAtNode'):
                node_class = module.ReplaceColorAtNode
                print("✅ ReplaceColorAtNode imported successfully!")
                print(f"   Class: {node_class}")
                print(f"   Category: {node_class.CATEGORY}")
                print(f"   Function: {node_class.FUNCTION}")

                # Test INPUT_TYPES
                input_types = node_class.INPUT_TYPES()
                print(f"   Required inputs: {list(input_types.get('required', {}).keys())}")
                print(f"   Return types: {node_class.RETURN_TYPES}")

                return True
            else:
                print("❌ ReplaceColorAtNode class not found in module")
                return False
        else:
            print("❌ Could not create module spec")
            return False

    except Exception as e:
        print(f"❌ Node import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_main_init():
    """Test importing from main __init__.py using importlib"""
    try:
        # Import the main __init__.py using importlib
        import importlib.util
        init_file = os.path.join(current_dir, "__init__.py")
        spec = importlib.util.spec_from_file_location("pixel_palette_art", init_file)

        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Check NODE_CLASS_MAPPINGS
            if hasattr(module, 'NODE_CLASS_MAPPINGS'):
                mappings = module.NODE_CLASS_MAPPINGS
                print("✅ Main __init__.py loaded successfully!")
                print(f"   NODE_CLASS_MAPPINGS keys: {list(mappings.keys())}")

                if 'ReplaceColorAtNode' in mappings:
                    print("✅ ReplaceColorAtNode found in NODE_CLASS_MAPPINGS!")
                    return True
                else:
                    print("❌ ReplaceColorAtNode not found in NODE_CLASS_MAPPINGS")
                    return False
            else:
                print("❌ NODE_CLASS_MAPPINGS not found in main module")
                return False
        else:
            print("❌ Could not create module spec for __init__.py")
            return False

    except Exception as e:
        print(f"❌ Main __init__.py import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing ReplaceColorAtNode import...")
    print("=" * 50)

    node_ok = test_node_import()
    print()

    main_ok = test_main_init()
    print()

    if node_ok and main_ok:
        print("🎉 All tests passed! The node should work in ComfyUI.")
    else:
        print("❌ Some tests failed. Check the errors above.")