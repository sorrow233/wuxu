
import os
import zipfile
import subprocess
import shutil
import re
import plistlib
import sys
import copy

# Configuration
SOURCE_DIR = "/Users/kang/Downloads/未命名文件夹 2"
OUTPUT_DIR = "/Users/kang/Downloads/未命名文件夹 2/Output_Cape"
CAPEIFY_BIN = "/private/tmp/capeify_work/myenv/bin/capeify"

ENV = os.environ.copy()
ENV["MAGICK_HOME"] = "/opt/homebrew/opt/imagemagick"
ENV["DYLD_LIBRARY_PATH"] = f"/opt/homebrew/opt/imagemagick/lib:{ENV.get('DYLD_LIBRARY_PATH', '')}"
ENV["PATH"] = f"/opt/homebrew/opt/imagemagick/bin:{ENV.get('PATH', '')}"

NAME_MAP = {
    "Bocchi": "后藤一里 (Bocchi)",
    "喜多郁代": "喜多郁代",
    "山田凉": "山田凉",
    "拉普兰德": "拉普兰德",
    "德克萨斯": "德克萨斯",
    "异德": "德克萨斯 - 异德",
    "谧默": "德克萨斯 - 缄默",
    "缄默": "德克萨斯 - 缄默",
    "缪尔赛思": "缪尔赛思",
    "澄闪": "澄闪-喜夜侍者",
    "荒芜": "拉普兰德 - 荒芜"
}

def fix_inf(inf_path):
    content = ""
    try:
        with open(inf_path, 'r', encoding='utf-8') as f: content = f.read()
    except:
        try:
            with open(inf_path, 'r', encoding='gbk') as f: content = f.read()
        except: return None 

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
            if any(k in line.lower() for k in keywords): score += 1
        if score > max_score:
            max_score = score
            best_section = sec_name
            
    new_lines = []
    for line in lines:
        if line.strip().lower().startswith("addreg"):
            key = line.split("=")[0]
            target = best_section if best_section else reg_sections[0] if reg_sections else ""
            new_lines.append(f"{key} = {target}")
        else: new_lines.append(line)
            
    new_path = inf_path + ".fixed.inf"
    with open(new_path, 'w', encoding='utf-8') as f: f.write("\n".join(new_lines))
    return new_path

def optimize_and_correct(cape_path, safe_name):
    TARGET_HEIGHT = 32.0
    
    with open(cape_path, 'r', encoding='utf-8') as f: content = f.read()
    if not content.strip().startswith("<?xml"):
        new_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
        new_content += '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n'
        new_content += '<plist version="1.0">\n'
        new_content += content
        new_content += '\n</plist>'
        with open(cape_path, 'w', encoding='utf-8') as f: f.write(new_content)
    
    try:
        with open(cape_path, 'rb') as f: plist_data = plistlib.load(f)
        
        display_name = safe_name
        for key, val in NAME_MAP.items():
            if key in safe_name:
                display_name = val
                break
        
        plist_data['CapeName'] = display_name
        plist_data['Author'] = "Master Pixel Cursors v15"
        plist_data['HiDPI'] = True
        plist_data['CapeVersion'] = 2.0
        
        cursors = plist_data.get('Cursors', {})
        
        # CLONING LOGIC v15
        master_key = None
        for k in ["com.apple.coregraphics.Wait", "com.apple.coregraphics.Busy"]:
            if k in cursors and int(cursors[k].get('FrameCount', 1)) > 1:
                master_key = k
                break
        
        if master_key:
            ibeam_key = "com.apple.coregraphics.IBeam"
            ibeam_frames = int(cursors.get(ibeam_key, {}).get('FrameCount', 0))
            if ibeam_frames <= 1:
                print(f"  - Replacing Static IBeam for {display_name}")
                master_data = copy.deepcopy(cursors[master_key])
                cursors[ibeam_key] = master_data
                cursors["com.apple.cursor.4"] = copy.deepcopy(master_data)
        
        # RESIZE ALL
        for k, v in cursors.items():
            ph = float(v.get('PointsHigh', 0))
            if ph > 40:
                scale = TARGET_HEIGHT / ph
                v['PointsHigh'] = TARGET_HEIGHT
                v['PointsWide'] = float(v.get('PointsWide', 0)) * scale
                if 'HotSpotX' in v: v['HotSpotX'] = float(v.get('HotSpotX', 0)) * scale
                if 'HotSpotY' in v: v['HotSpotY'] = float(v.get('HotSpotY', 0)) * scale

        with open(cape_path, 'wb') as f: plistlib.dump(plist_data, f)
        print(f"Successfully Corrected v15: {display_name}")
            
    except Exception as e: print(f"Error: {e}")

def convert_item(name, folder_path):
    """Recursively search for INF in folder_path and convert."""
    inf_file = None
    search_dir = folder_path
    
    for root, dirs, files in os.walk(folder_path):
        for f in files:
            if f.lower().endswith('.inf') and not f.endswith('.fixed.inf'):
                inf_file = os.path.join(root, f)
                break
        if inf_file: break
    
    if not inf_file: 
        print(f"No INF found in {folder_path}")
        return

    fixed_inf = fix_inf(inf_file)
    if not fixed_inf: return

    safe_name = re.sub(r'[\\/*?:"<>|]', "", name).replace(" ", "_")
    output_cape = os.path.join(OUTPUT_DIR, f"{safe_name}.cape")
    
    cmd = [CAPEIFY_BIN, "convert", "--path", os.path.dirname(fixed_inf), "--inf-file", os.path.basename(fixed_inf), "--out", output_cape]
    try:
        subprocess.run(cmd, env=ENV, cwd=os.path.dirname(fixed_inf), check=True)
        optimize_and_correct(output_cape, safe_name)
    except Exception as e: print(f"Error converting {name}: {e}")

def main():
    if os.path.exists(OUTPUT_DIR): shutil.rmtree(OUTPUT_DIR) # RESET FOR CLEAN START
    os.makedirs(OUTPUT_DIR)
    # Process each top-level folder in SOURCE_DIR
    for item in os.listdir(SOURCE_DIR):
        p = os.path.join(SOURCE_DIR, item)
        if os.path.isdir(p) and item != "Output_Cape":
            convert_item(item, p)

if __name__ == "__main__":
    main()
