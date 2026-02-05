
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
    content = ""
    try:
        with open(inf_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(inf_path, 'r', encoding='gbk') as f:
                content = f.read()
        except:
            return None 

    lines = content.splitlines()
    new_lines = []
    fixed = False
    
    for line in lines:
        if line.strip().lower().startswith("addreg"):
            parts = line.split("=")
            if len(parts) > 1:
                key = parts[0]
                value = parts[1]
                vals = [v.strip() for v in value.split(",")]
                if len(vals) > 1:
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
    1. Fixes missing XML headers if present (manual text patch).
    2. Parses the Cape Plist using plistlib.
    3. Sets HiDPI = True and CapeVersion = 2.0.
    4. Scales cursors down to 32.0 points height if they are large.
    """
    TARGET_HEIGHT = 32.0
    
    # 1. FIX HEADER (Text mode)
    with open(cape_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if not content.strip().startswith("<?xml"):
        print(f"  - Adding missing XML headers to {os.path.basename(cape_path)}")
        new_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
        new_content += '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n'
        new_content += '<plist version="1.0">\n'
        new_content += content
        new_content += '\n</plist>'
        with open(cape_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    
    # 2. LOAD PLIST
    try:
        with open(cape_path, 'rb') as f:
            plist_data = plistlib.load(f)
        
        # 3. SET METADATA
        plist_data['HiDPI'] = True
        plist_data['CapeVersion'] = 2.0
        
        # 4. RESIZE LOGIC
        cursors = plist_data.get('Cursors', {})
        modified = True # Always save because we changed metadata
        
        for cursor_key, cursor_data in cursors.items():
            points_high = float(cursor_data.get('PointsHigh', 0))
            points_wide = float(cursor_data.get('PointsWide', 0))
            
            # If significantly larger than 32 (e.g. > 40), scale it down
            if points_high > 40:
                scale_factor = TARGET_HEIGHT / points_high
                
                cursor_data['PointsHigh'] = TARGET_HEIGHT
                cursor_data['PointsWide'] = points_wide * scale_factor
                
                if 'HotSpotX' in cursor_data:
                    cursor_data['HotSpotX'] = float(cursor_data.get('HotSpotX', 0)) * scale_factor
                if 'HotSpotY' in cursor_data:
                    cursor_data['HotSpotY'] = float(cursor_data.get('HotSpotY', 0)) * scale_factor
        
        # Check FrameDuration (Fix for animation speed if needed) - Keeping logic simple for now
        
        with open(cape_path, 'wb') as f:
            plistlib.dump(plist_data, f)
        print(f"Successfully optimized {os.path.basename(cape_path)} (HiDPI + Resized)")
            
    except Exception as e:
        print(f"Error processing plist {cape_path}: {e}")

def convert_folder(folder_path):
    inf_file = None
    for f in os.listdir(folder_path):
        if f.lower().endswith('.inf') and not f.endswith('.fixed.inf'):
            inf_file = os.path.join(folder_path, f)
            break
    
    if not inf_file:
        return

    fixed_inf = fix_inf(inf_file)
    if not fixed_inf:
        return

    folder_name = os.path.basename(folder_path)
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
        resize_cape_plist(output_cape)
    except subprocess.CalledProcessError as e:
        print(f"Conversion failed for {folder_path}: {e}")

def main():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    for root, dirs, files in os.walk(SOURCE_DIR):
        if OUTPUT_DIR in root:
            continue
        has_inf = any(f.lower().endswith('.inf') for f in files)
        if has_inf:
            convert_folder(root)

if __name__ == "__main__":
    main()
