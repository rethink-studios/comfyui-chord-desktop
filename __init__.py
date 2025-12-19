import os
import sys
import traceback

# Add chord subdirectory to path (insert at beginning for priority)
current_dir = os.path.dirname(os.path.abspath(__file__))
chord_dir = os.path.join(current_dir, "chord")
# Use insert(0) instead of append to ensure this path is checked first
# This helps with ComfyUI Desktop which may have different path handling
if chord_dir not in sys.path:
    sys.path.insert(0, chord_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

print(f"[ComfyUI-Chord] Debug: current_dir = {current_dir}")
print(f"[ComfyUI-Chord] Debug: chord_dir = {chord_dir}")
print(f"[ComfyUI-Chord] Debug: sys.path entries = {[p for p in sys.path if 'chord' in p.lower() or 'ComfyUI-Chord' in p]}")

# Import nodes module - use importlib to ensure we get the local nodes.py file
try:
    import importlib.util
    nodes_path = os.path.join(current_dir, "nodes.py")
    print(f"[ComfyUI-Chord] Debug: Loading nodes from: {nodes_path}")
    
    spec = importlib.util.spec_from_file_location("chord_nodes", nodes_path)
    chord_nodes = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(chord_nodes)
    
    print(f"[ComfyUI-Chord] Debug: nodes module imported successfully")
    print(f"[ComfyUI-Chord] Debug: NODE_CLASS_MAPPINGS type: {type(chord_nodes.NODE_CLASS_MAPPINGS)}")
    print(f"[ComfyUI-Chord] Debug: NODE_CLASS_MAPPINGS keys: {list(chord_nodes.NODE_CLASS_MAPPINGS.keys())}")
    
    NODE_CLASS_MAPPINGS = chord_nodes.NODE_CLASS_MAPPINGS
    NODE_DISPLAY_NAME_MAPPINGS = chord_nodes.NODE_DISPLAY_NAME_MAPPINGS
    
    print(f"[ComfyUI-Chord] Successfully loaded {len(NODE_CLASS_MAPPINGS)} Chord nodes")
    print(f"[ComfyUI-Chord] Chord nodes registered: {list(NODE_CLASS_MAPPINGS.keys())}")
except Exception as e:
    print(f"[ComfyUI-Chord] ERROR loading nodes: {e}")
    traceback.print_exc()
    NODE_CLASS_MAPPINGS = {}
    NODE_DISPLAY_NAME_MAPPINGS = {}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
