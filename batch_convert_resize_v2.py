
import os
import zipfile
import subprocess
import shutil
import re
import plistlib
import sys

# Configuration
SOURCE_DIR = "/Users/kang/Downloads/MYGO母鸡卡指针合集"
OUTPUT_DIR = "/Users/kang/Downloads/MYGO母鸡卡指针合集/MYGO_Cape_Output"
CAPEIFY_BIN = "/private/tmp/capeify_work/myenv/bin/capeify"

ENV = os.environ.copy()
ENV["MAGICK_HOME"] = "/opt/homebrew/opt/imagemagick"
ENV["DYLD_LIBRARY_PATH"] = f"/opt/homebrew/opt/imagemagick/lib:{ENV.get('DYLD_LIBRARY_PATH', '')}"
ENV["PATH"] = f"/opt/homebrew/opt/imagemagick/bin:{ENV.get('PATH', '')}"

def fix_inf(inf_path):
    # Read file with tolerant encoding
    content = ""
    try:
        with open(inf_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(inf_path, 'r', encoding='gbk') as f:
                content = f.read()
        except:
            return None # Cannot read

    lines = content.splitlines()
    new_lines = []
    fixed = False
    
    for line in lines:
        if line.strip().lower().startswith("addreg"):
            parts = line.split("=")
            if len(parts) > 1:
                key = parts[0]
                value = parts[1]
                # Split value by comma
                vals = [v.strip() for v in value.split(",")]
                if len(vals) > 1:
                     # Keep only the first one
                     new_line = f"{key} = {vals[0]}"
                     new_lines.append(new_line)
                     fixed = True
                     continue
        new_lines.append(line)
        
    if fixed:
        new_path = inf_path + ".fixed.inf"
        with open(new_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(new_lines))
        return new_path
    return inf_path

def resize_cape_plist(cape_path):
    """
    Parses the Cape Plist and scales cursors down to 32.0 points height.
    Scales HotSpots accordingly to maintain correct click position.
    """
    TARGET_HEIGHT = 32.0
    
    try:
        with open(cape_path, 'rb') as f:
            plist_data = plistlib.load(f)
        
        cursors = plist_data.get('Cursors', {})
        modified = False
        
        for cursor_key, cursor_data in cursors.items():
            # Get current dimensions
            points_high = float(cursor_data.get('PointsHigh', 0))
            points_wide = float(cursor_data.get('PointsWide', 0))
            
            # If it's significantly larger than 32 (e.g. > 40), scale it down
            if points_high > 40:
                scale_factor = TARGET_HEIGHT / points_high
                
                # Update Dimensions
                cursor_data['PointsHigh'] = TARGET_HEIGHT
                cursor_data['PointsWide'] = points_wide * scale_factor
                
                # Update Hotspots
                if 'HotSpotX' in cursor_data:
                    cursor_data['HotSpotX'] = float(cursor_data['HotSpotX']) * scale_factor
                if 'HotSpotY' in cursor_data:
                    cursor_data['HotSpotY'] = float(cursor_data['HotSpotY']) * scale_factor
                    
                modified = True
                print(f"  - Scaled {cursor_key}: {points_high}->{TARGET_HEIGHT} (Factor: {scale_factor:.4f})")

        if modified:
            with open(cape_path, 'wb') as f:
                plistlib.dump(plist_data, f)
            print(f"Successfully resized cursors in {os.path.basename(cape_path)}")
        else:
            print(f"No resizing needed for {os.path.basename(cape_path)}")
            
    except Exception as e:
        print(f"Error processing plist {cape_path}: {e}")

def convert_folder(folder_path):
    # Find .inf file
    inf_file = None
    for f in os.listdir(folder_path):
        if f.lower().endswith('.inf') and not f.endswith('.fixed.inf'):
            inf_file = os.path.join(folder_path, f)
            break
    
    if not inf_file:
        return

    print(f"Found INF in {folder_path}...")
    
    # Fix INF if needed
    fixed_inf = fix_inf(inf_file)
    if not fixed_inf:
        print("Could not read INF file")
        return

    # Determine output name
    folder_name = os.path.basename(folder_path)
    # Sanitize name
    safe_name = re.sub(r'[\\/*?:"<>|]', "", folder_name).replace(" ", "_")
    output_cape = os.path.join(OUTPUT_DIR, f"{safe_name}.cape")
    
    cmd = [
        CAPEIFY_BIN,
        "convert",
        "--path", folder_path,
        "--inf-file", os.path.basename(fixed_inf),
        "--out", output_cape
    ]
    
    print(f"Converting {os.path.basename(inf_file)} to {safe_name}.cape...")
    try:
        subprocess.run(cmd, env=ENV, cwd=folder_path, check=True)
        
        # POST-PROCESS: FIX SIZE AND HOTSPOTS
        resize_cape_plist(output_cape)
        
    except subprocess.CalledProcessError as e:
        print(f"Conversion failed for {folder_path}: {e}")

def main():
    # Ensure output dir exists
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    # 1. We assume unzipping is already done from previous step. 
    # If not, the folders should still be there. 
    # Just in case, we focus on the existing directories.

    # 2. Walk directories and convert
    for root, dirs, files in os.walk(SOURCE_DIR):
        # Skip output dir
        if OUTPUT_DIR in root:
            continue
            
        # Check if this dir has an INF file
        has_inf = any(f.lower().endswith('.inf') for f in files)
        if has_inf:
            convert_folder(root)

if __name__ == "__main__":
    main()
