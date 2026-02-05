
import plistlib
import io
from PIL import Image
import sys

def inspect_cape(cape_path):
    print(f"--- Inspecting {cape_path} ---")
    try:
        with open(cape_path, 'rb') as f:
            plist_data = plistlib.load(f)
            
        print(f"CapeVersion: {plist_data.get('CapeVersion')}")
        print(f"Cloud: {plist_data.get('Cloud')}")
        print(f"HiDPI: {plist_data.get('HiDPI')}") # Guessing
        
        cursors = plist_data.get('Cursors', {})
        print(f"Total Cursors: {len(cursors)}")
        
        # Check first cursor
        if cursors:
            first_key = list(cursors.keys())[0]
            c = cursors[first_key]
            print(f"Cursor: {first_key}")
            print(f"  Points: {c.get('PointsWide')} x {c.get('PointsHigh')}")
            reps = c.get('Representations', [])
            print(f"  Representation Count: {len(reps)}")
            
            for idx, r in enumerate(reps):
                img = Image.open(io.BytesIO(r))
                print(f"    Rep {idx}: {img.size} ({img.format})")
                
    except Exception as e:
        print(f"Error: {e}")

if len(sys.argv) > 1:
    inspect_cape(sys.argv[1])
