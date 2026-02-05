
import os
import zipfile
import subprocess
import shutil
import re
import plistlib
import sys

# Configuration
SOURCE_DIR = "/Users/kang/Downloads/未命名文件夹"
OUTPUT_DIR = "/Users/kang/Downloads/未命名文件夹/Output_Cape"
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
    TARGET_HEIGHT = 32.0
    
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
    
    try:
        with open(cape_path, 'rb') as f:
            plist_data = plistlib.load(f)
        
        plist_data['HiDPI'] = True
        plist_data['CapeVersion'] = 2.0
        
        cursors = plist_data.get('Cursors', {})
        modified = True
        
        for cursor_key, cursor_data in cursors.items():
            points_high = float(cursor_data.get('PointsHigh', 0))
            points_wide = float(cursor_data.get('PointsWide', 0))
            
            if points_high > 40:
                scale_factor = TARGET_HEIGHT / points_high
                
                cursor_data['PointsHigh'] = TARGET_HEIGHT
                cursor_data['PointsWide'] = points_wide * scale_factor
                
                if 'HotSpotX' in cursor_data:
                    cursor_data['HotSpotX'] = float(cursor_data.get('HotSpotX', 0)) * scale_factor
                if 'HotSpotY' in cursor_data:
                    cursor_data['HotSpotY'] = float(cursor_data.get('HotSpotY', 0)) * scale_factor
        
        with open(cape_path, 'wb') as f:
            plistlib.dump(plist_data, f)
        print(f"Successfully optimized {os.path.basename(cape_path)} (HiDPI + Resized)")
            
    except Exception as e:
        print(f"Error processing plist {cape_path}: {e}")

def get_smart_name(folder_path):
    # If folder name is generic, go up one level
    name = os.path.basename(folder_path)
    if "安装" in name or "Install" in name or "cursor" == name.lower():
        parent = os.path.basename(os.path.dirname(folder_path))
        if parent:
            name = parent
    
    # Clean name
    safe_name = re.sub(r'[\\/*?:"<>|]', "", name).replace(" ", "_")
    return safe_name

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

    # Use SMART NAME logic
    safe_name = get_smart_name(folder_path)
    
    # Handle duplicates by appending _v2, etc if needed? 
    # For now let's hope zip folders are unique.
    
    output_cape = os.path.join(OUTPUT_DIR, f"{safe_name}.cape")
    
    # Check if exists, append random if needed to avoid overwrite?
    # Actually user might want overwrite if re-running.
    
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
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 2. Convert recursively (Unzip already done manually or by previous run)
    for root, dirs, files in os.walk(SOURCE_DIR):
        if OUTPUT_DIR in root:
            continue
        has_inf = any(f.lower().endswith('.inf') for f in files)
        if has_inf:
            convert_folder(root)

if __name__ == "__main__":
    main()
