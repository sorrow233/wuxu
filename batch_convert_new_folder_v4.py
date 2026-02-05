
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
    
    # 1. FIND ALL ADDREG SECTIONS
    reg_sections = []
    for line in lines:
        if line.strip().lower().startswith("addreg"):
            parts = line.split("=")
            if len(parts) > 1:
                vals = [v.strip() for v in parts[1].split(",")]
                reg_sections.extend(vals)
    
    # 2. ANALYZE EACH SECTION FOR QUALITY
    # We want a section that has explicit keys like IBeam, Arrow, etc.
    best_section = None
    max_score = -1
    
    sections_map = {}
    current_section = None
    for line in lines:
        line = line.strip()
        if line.startswith("[") and line.endswith("]"):
            current_section = line[1:-1]
            sections_map[current_section] = []
        elif current_section and line and "=" in line:
            sections_map[current_section].append(line)
            
    for sec_name in reg_sections:
        if sec_name not in sections_map:
            continue
        
        score = 0
        keywords = ["arrow", "ibeam", "appstarting", "wait", "busy", "link", "hand", "help"]
        for line in sections_map[sec_name]:
            if any(k in line.lower() for k in keywords):
                score += 1
        
        if score > max_score:
            max_score = score
            best_section = sec_name
            
    # 3. GENERATE NEW INF
    new_lines = []
    for line in lines:
        if line.strip().lower().startswith("addreg"):
            key = line.split("=")[0]
            # Replace with our best one
            target = best_section if best_section else reg_sections[0] if reg_sections else ""
            new_lines.append(f"{key} = {target}")
        else:
            new_lines.append(line)
            
    new_path = inf_path + ".fixed.inf"
    with open(new_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(new_lines))
    return new_path

def resize_cape_plist(cape_path, safe_name):
    TARGET_HEIGHT = 32.0
    
    with open(cape_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if not content.strip().startswith("<?xml"):
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
        
        display_name = safe_name
        match = re.search(r'指针-(.+?)--', safe_name)
        if match:
            display_name = match.group(1)
        
        plist_data['CapeName'] = display_name
        plist_data['Author'] = "AI Converted (v4 Mapping Fix)"
        plist_data['HiDPI'] = True
        plist_data['CapeVersion'] = 2.0
        
        cursors = plist_data.get('Cursors', {})
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
            plist_data = plistlib.dump(plist_data, f)
        print(f"Successfully optimized {safe_name} (Name: {display_name})")
            
    except Exception as e:
        print(f"Error processing plist {cape_path}: {e}")

def get_smart_name(folder_path):
    name = os.path.basename(folder_path)
    if "安装" in name or "Install" in name or "cursor" == name.lower():
        parent = os.path.basename(os.path.dirname(folder_path))
        if parent:
            name = parent
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

    safe_name = get_smart_name(folder_path)
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
        resize_cape_plist(output_cape, safe_name)
    except subprocess.CalledProcessError as e:
        print(f"Conversion failed for {folder_path}: {e}")

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for root, dirs, files in os.walk(SOURCE_DIR):
        if OUTPUT_DIR in root:
            continue
        has_inf = any(f.lower().endswith('.inf') for f in files)
        if has_inf:
            convert_folder(root)

if __name__ == "__main__":
    main()
