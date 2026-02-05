
import os
import zipfile
import subprocess
import shutil
import re
import plistlib
import sys
import copy

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
    except:
        try:
            with open(inf_path, 'r', encoding='gbk') as f:
                content = f.read()
        except:
            return None 

    lines = content.splitlines()
    reg_sections = []
    for line in lines:
        if line.strip().lower().startswith("addreg"):
            parts = line.split("=")
            if len(parts) > 1:
                vals = [v.strip() for v in parts[1].split(",")]
                reg_sections.extend(vals)
    
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
        if sec_name not in sections_map: continue
        score = 0
        keywords = ["arrow", "ibeam", "appstarting", "wait", "busy", "link", "hand", "help"]
        for line in sections_map[sec_name]:
            if any(k in line.lower() for k in keywords):
                score += 1
        if score > max_score:
            max_score = score
            best_section = sec_name
            
    new_lines = []
    for line in lines:
        if line.strip().lower().startswith("addreg"):
            key = line.split("=")[0]
            target = best_section if best_section else reg_sections[0] if reg_sections else ""
            new_lines.append(f"{key} = {target}")
        else:
            new_lines.append(line)
            
    new_path = inf_path + ".fixed.inf"
    with open(new_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(new_lines))
    return new_path

def optimize_and_correct(cape_path, safe_name, is_full_version=False):
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
        
        # IMPROVED NAMING
        display_name = safe_name
        if "Sangonomiya" in safe_name or "Kokomi" in safe_name: display_name = "珊格诺米亚·心海"
        elif "平泽唯" in safe_name or "Hirasawa" in safe_name: display_name = "平泽唯"
        
        match = re.search(r'指针-(.+?)--', safe_name)
        if match: display_name = match.group(1)
            
        plist_data['CapeName'] = display_name
        plist_data['Author'] = "Master Pixel Cursors"
        plist_data['HiDPI'] = True
        plist_data['CapeVersion'] = 2.0
        
        cursors = plist_data.get('Cursors', {})
        
        if not is_full_version:
            master_key = None
            priority_keys = ["com.apple.coregraphics.Wait", "com.apple.coregraphics.Busy", "com.apple.coregraphics.AppStarting"]
            for k in priority_keys:
                if k in cursors:
                    if int(cursors[k].get('FrameCount', 1)) > 1:
                        master_key = k
                        break
            if master_key:
                print(f"  - TRIAL: Syncing IBeam to {master_key}")
                master_data = copy.deepcopy(cursors[master_key])
                text_keys = ["com.apple.coregraphics.IBeam", "com.apple.cursor.4"]
                for k in text_keys:
                    cursors[k] = copy.deepcopy(master_data)
        else:
            print(f"  - FULL: Skipping animation sync for {display_name}")

        for k, v in cursors.items():
            ph = float(v.get('PointsHigh', 0))
            if ph > 40:
                scale = TARGET_HEIGHT / ph
                v['PointsHigh'] = TARGET_HEIGHT
                v['PointsWide'] = float(v.get('PointsWide', 0)) * scale
                if 'HotSpotX' in v: v['HotSpotX'] = float(v.get('HotSpotX', 0)) * scale
                if 'HotSpotY' in v: v['HotSpotY'] = float(v.get('HotSpotY', 0)) * scale

        with open(cape_path, 'wb') as f:
            plistlib.dump(plist_data, f)
        print(f"Successfully Corrected v13: {display_name}")
            
    except Exception as e:
        print(f"Error: {e}")

def convert_folder(folder_path):
    path_lower = folder_path.lower()
    is_full = "kokomi" in path_lower or "平泽唯" in path_lower or ("trial" not in path_lower and "试用" not in path_lower)

    inf_file = None
    for f in os.listdir(folder_path):
        if f.lower().endswith('.inf') and not f.endswith('.fixed.inf'):
            inf_file = os.path.join(folder_path, f)
            break
    if not inf_file: return
    
    fixed_inf = fix_inf(inf_file)
    if not fixed_inf: return

    # Smart Naming for Output Filename
    name = os.path.basename(folder_path)
    if "安装" in name or "Install" in name or "mouse" in name.lower():
        curr = folder_path
        while "安装" in os.path.basename(curr) or "Install" in os.path.basename(curr) or "mouse" in os.path.basename(curr).lower():
            parent = os.path.dirname(curr)
            if parent == curr: break
            curr = parent
        name = os.path.basename(curr)

    if "kokomi" in name.lower() or "sangonomiya" in name.lower(): 
        safe_name = "珊瑚宫心海"
    elif "平泽唯" in name:
        safe_name = "平泽唯"
    else:
        safe_name = re.sub(r'[\\/*?:"<>|]', "", name).replace(" ", "_")
        
    output_cape = os.path.join(OUTPUT_DIR, f"{safe_name}.cape")
    
    cmd = [CAPEIFY_BIN, "convert", "--path", folder_path, "--inf-file", os.path.basename(fixed_inf), "--out", output_cape]
    try:
        subprocess.run(cmd, env=ENV, cwd=folder_path, check=True)
        optimize_and_correct(output_cape, safe_name, is_full_version=is_full)
    except: pass

def main():
    if os.path.exists(OUTPUT_DIR): shutil.rmtree(OUTPUT_DIR) # Clean start
    os.makedirs(OUTPUT_DIR)
    
    for root, dirs, files in os.walk(SOURCE_DIR):
        if OUTPUT_DIR in root: continue
        if any(f.lower().endswith('.inf') for f in files):
            convert_folder(root)

if __name__ == "__main__":
    main()
