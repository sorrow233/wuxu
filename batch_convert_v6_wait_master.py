
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
    return inf_path

def optimize_and_unify_v2(cape_path, safe_name):
    """
    1. Fixes XML headers.
    2. Sets HiDPI=True, CapeVersion=2.0, CapeName.
    3. Resizes to 32pt.
    4. UNIFIES Arrow and IBeam to the 'WAIT/BUSY' animation.
    """
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
        plist_data['Author'] = "Master Character Pack"
        plist_data['HiDPI'] = True
        plist_data['CapeVersion'] = 2.0
        
        cursors = plist_data.get('Cursors', {})
        
        # FIND THE CHARACTER master (WAIT or BUSY)
        master_key = None
        
        # CRITICAL: Prioritize Wait/Busy which usually holds the character animation
        priority_keys = [
            "com.apple.coregraphics.Wait",
            "com.apple.coregraphics.Busy",
            "com.apple.coregraphics.AppStarting"
        ]
        
        for k in priority_keys:
            if k in cursors:
                # Check if it has frames (ani)
                if int(cursors[k].get('FrameCount', 0)) > 1:
                    master_key = k
                    break
        
        # If no animated wait found, fall back to max frames anywhere
        if not master_key:
            max_f = -1
            for k, v in cursors.items():
                fc = int(v.get('FrameCount', 1))
                if fc > max_f:
                    max_f = fc
                    master_key = k
        
        if master_key:
            print(f"  - MASTER SOURCE: {master_key} ({cursors[master_key].get('FrameCount')} frames)")
            master_data = dict(cursors[master_key])
            
            # CLONE to common interaction states
            cursors['com.apple.coregraphics.Arrow'] = dict(master_data) # 选中
            cursors['com.apple.coregraphics.IBeam'] = dict(master_data) # 输入
            # Wait itself is already correct if it was the master
            
        # Global Post-processing: Resize to 32pt
        for k, v in cursors.items():
            ph = float(v.get('PointsHigh', 0))
            pw = float(v.get('PointsWide', 0))
            if ph > 40:
                scale = TARGET_HEIGHT / ph
                v['PointsHigh'] = TARGET_HEIGHT
                v['PointsWide'] = pw * scale
                if 'HotSpotX' in v: v['HotSpotX'] = float(v.get('HotSpotX', 0)) * scale
                if 'HotSpotY' in v: v['HotSpotY'] = float(v.get('HotSpotY', 0)) * scale

        with open(cape_path, 'wb') as f:
            plistlib.dump(plist_data, f)
        print(f"Successfully Re-Unified from Wait: {display_name}")
            
    except Exception as e:
        print(f"Error: {e}")

def convert_folder(folder_path):
    # Find INF
    inf_file = None
    for f in os.listdir(folder_path):
        if f.lower().endswith('.inf'):
            inf_file = f
            break
    if not inf_file: return
    
    name = os.path.basename(folder_path)
    if "安装" in name or "Install" in name:
        name = os.path.basename(os.path.dirname(folder_path))
    safe_name = re.sub(r'[\\/*?:"<>|]', "", name).replace(" ", "_")
    output_cape = os.path.join(OUTPUT_DIR, f"{safe_name}.cape")
    
    cmd = [CAPEIFY_BIN, "convert", "--path", folder_path, "--inf-file", inf_file, "--out", output_cape]
    try:
        subprocess.run(cmd, env=ENV, cwd=folder_path, check=True)
        optimize_and_unify_v2(output_cape, safe_name)
    except: pass

def main():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    for root, dirs, files in os.walk(SOURCE_DIR):
        if OUTPUT_DIR in root: continue
        if any(f.lower().endswith('.inf') for f in files):
            convert_folder(root)

if __name__ == "__main__":
    main()
