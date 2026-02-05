
import os
import zipfile
import subprocess
import shutil
import re
import sys

# Configuration
SOURCE_DIR = "/Users/kang/Downloads/MYGO母鸡卡指针合集"
OUTPUT_DIR = "/Users/kang/Downloads/MYGO母鸡卡指针合集/MYGO_Cape_Output"
VENV_PYTHON = "/private/tmp/capeify_work/myenv/bin/python"
CAPEIFY_BIN = "/private/tmp/capeify_work/myenv/bin/capeify"

ENV = os.environ.copy()
ENV["MAGICK_HOME"] = "/opt/homebrew/opt/imagemagick"
ENV["DYLD_LIBRARY_PATH"] = f"/opt/homebrew/opt/imagemagick/lib:{ENV.get('DYLD_LIBRARY_PATH', '')}"
ENV["PATH"] = f"/opt/homebrew/opt/imagemagick/bin:{ENV.get('PATH', '')}"

def unzip_gbk(zip_path, extract_to):
    print(f"Unzipping {zip_path}...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            for file_info in z.infolist():
                try:
                    filename = file_info.filename.encode('cp437').decode('gbk')
                except:
                    filename = file_info.filename

                if filename.startswith('__MACOSX'):
                    continue
                    
                target_path = os.path.join(extract_to, filename)
                
                if file_info.is_dir() or filename.endswith('/'):
                    os.makedirs(target_path, exist_ok=True)
                else:
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    with open(target_path, 'wb') as f:
                        f.write(z.read(file_info))
    except Exception as e:
        print(f"Error unzipping {zip_path}: {e}")

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
    Reads the Generated Cape XML and forces the size to 32.0 if it's too large.
    """
    try:
        with open(cape_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Regex to find <key>PointsHigh</key>\n\t<real>96.0</real> pattern
        # We replace any size > 48 with 32.0 (standard Mac cursor size)
        
        def replace_size(match):
            val = float(match.group(1))
            if val > 48:
                return f"<real>32.0</real>"
            return match.group(0)

        # Replace PointsHigh
        content = re.sub(r'<key>PointsHigh</key>\s*<real>([\d\.]+)</real>', 
                         lambda m: f"<key>PointsHigh</key>\n\t\t<real>{'32.0' if float(m.group(1)) > 40 else m.group(1)}</real>", 
                         content)
        
        # Replace PointsWide
        content = re.sub(r'<key>PointsWide</key>\s*<real>([\d\.]+)</real>', 
                         lambda m: f"<key>PointsWide</key>\n\t\t<real>{'32.0' if float(m.group(1)) > 40 else m.group(1)}</real>", 
                         content)
        
        # Also fix Resolution if needed, but usually points is the key
        
        with open(cape_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Resized cursors in {os.path.basename(cape_path)}")
        
    except Exception as e:
        print(f"Error resizing plist {cape_path}: {e}")

def convert_folder(folder_path):
    # Find .inf file
    inf_file = None
    for f in os.listdir(folder_path):
        if f.lower().endswith('.inf') and not f.endswith('.fixed.inf'):
            inf_file = os.path.join(folder_path, f)
            break
    
    if not inf_file:
        return

    print(f"Processing {folder_path}...")
    
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
    
    print(f"Running conversion for {os.path.basename(inf_file)}...")
    try:
        subprocess.run(cmd, env=ENV, cwd=folder_path, check=True)
        print(f"Created {output_cape}")
        
        # POST-PROCESS: FIX SIZE
        resize_cape_plist(output_cape)
        
    except subprocess.CalledProcessError as e:
        print(f"Conversion failed for {folder_path}: {e}")

def main():
    # Ensure output dir exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 1. Unzip all zips in source dir
    for root, dirs, files in os.walk(SOURCE_DIR):
        for f in files:
            file_path = os.path.join(root, f)
            # Skip output dir
            if OUTPUT_DIR in file_path:
                continue
                
            if f.lower().endswith('.zip'):
                zip_path = file_path
                # Unzip to a folder with same name (without extension)
                extract_name = os.path.splitext(f)[0]
                extract_path = os.path.join(root, extract_name)
                
                # Only extract if not already there (simple check)
                if not os.path.exists(extract_path):
                    unzip_gbk(zip_path, extract_path)

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
