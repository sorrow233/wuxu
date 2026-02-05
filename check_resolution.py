
import os
import sys
from PIL import Image

# Add venv to path to use Pillow
sys.path.append("/private/tmp/capeify_work/myenv/lib/python3.11/site-packages")

def check_ani_size(path):
    try:
        # Pillow might not open ANI directly out of the box without plugin, 
        # but let's try or use a workaround if needed.
        # Often .ani is a RIFF container with .ico/.cur inside.
        # If Pillow fails, we can try to find a .cur file or just read bytes if we know the offset (hard).
        # Actually usually these packs have .cur files too.
        
        with Image.open(path) as img:
            print(f"File: {os.path.basename(path)}")
            print(f"Format: {img.format}")
            print(f"Size: {img.size}")
            print(f"Info: {img.info}")
    except Exception as e:
        print(f"Failed to open {os.path.basename(path)}: {e}")

# Check a few files
base_dir = "/Users/kang/Downloads/MYGO母鸡卡指针合集/GO_cursors/Chihaya Anon 千早爱音"
files_to_check = ["Normal Select.ani", "Work.ani", "Link.ani"]

for f in files_to_check:
    full_path = os.path.join(base_dir, f)
    if os.path.exists(full_path):
        check_ani_size(full_path)
    else:
        print(f"File not found: {f}")
