
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
    # Keep it simple, just let capeify do its best, then we fix the mappings in the PLIST
    return inf_path

def optimize_and_unify_animations(cape_path, safe_name):
    """
    1. Fixes XML headers.
    2. Sets HiDPI=True, CapeVersion=2.0, CapeName.
    3. Resizes to 32pt.
    4. UNIFIES Arrow, IBeam, and Wait to the BEST animation found.
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
        plist_data['Author'] = "Unified Character Pack"
        plist_data['HiDPI'] = True
        plist_data['CapeVersion'] = 2.0
        
        cursors = plist_data.get('Cursors', {})
        
        # FIND THE BEST master animation
        master_key = None
        max_frames = -1
        
        # Priority for searching the "character" animation
        search_keys = [
            "com.apple.coregraphics.Arrow",
            "com.apple.coregraphics.Wait",
            "com.apple.coregraphics.Busy",
            "com.apple.coregraphics.IBeam"
        ]
        
        for k in search_keys:
            if k in cursors:
                fcount = int(cursors[k].get('FrameCount', 1))
                if fcount > max_frames:
                    max_frames = fcount
                    master_key = k
                    
        # If still none (unlikely), take the first one with max frames
        if not master_key or max_frames <= 1:
            for k, v in cursors.items():
                fcount = int(v.get('FrameCount', 1))
                if fcount > max_frames:
                    max_frames = fcount
                    master_key = k
        
        if master_key:
            print(f"  - Using animation from {master_key} ({max_frames} frames) for all core types.")
            master_data = dict(cursors[master_key])
            
            # UNIFY: Arrow, IBeam, Wait
            cursors['com.apple.coregraphics.Arrow'] = dict(master_data)
            cursors['com.apple.coregraphics.IBeam'] = dict(master_data)
            cursors['com.apple.coregraphics.Wait'] = dict(master_data)
            
        # Global Post-processing: Resize 96px -> 32pt
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
        print(f"Successfully Unified: {display_name}")
            
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
    
    # We use a smart name for output
    name = os.path.basename(folder_path)
    if "安装" in name or "Install" in name:
        name = os.path.basename(os.path.dirname(folder_path))
    safe_name = re.sub(r'[\\/*?:"<>|]', "", name).replace(" ", "_")
    output_cape = os.path.join(OUTPUT_DIR, f"{safe_name}.cape")
    
    cmd = [CAPEIFY_BIN, "convert", "--path", folder_path, "--inf-file", inf_file, "--out", output_cape]
    try:
        subprocess.run(cmd, env=ENV, cwd=folder_path, check=True)
        optimize_and_unify_animations(output_cape, safe_name)
    except: pass

def main():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    for root, dirs, files in os.walk(SOURCE_DIR):
        if OUTPUT_DIR in root: continue
        if any(f.lower().endswith('.inf') for f in files):
            convert_folder(root)

if __name__ == "__main__":
    main()
