
import zipfile
import os
import sys

def unzip_gbk(zip_path, extract_to):
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            for file_info in z.infolist():
                # 尝试修复文件名编码
                try:
                    # Windows zip 默认可能是 cp437，尝试将其作为 raw bytes 读取然后用 gbk 解码
                    filename = file_info.filename.encode('cp437').decode('gbk')
                except:
                    # 如果失败，保留原样
                    filename = file_info.filename

                # 排除 __MACOSX 目录
                if filename.startswith('__MACOSX'):
                    continue
                    
                target_path = os.path.join(extract_to, filename)
                
                # 如果是目录
                if file_info.is_dir() or filename.endswith('/'):
                    os.makedirs(target_path, exist_ok=True)
                else:
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    with open(target_path, 'wb') as f:
                        f.write(z.read(file_info))
        print(f"Successfully extracted {zip_path}")
    except Exception as e:
        print(f"Error extracting {zip_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python unzip_gbk.py <zip_file> <dest_dir>")
        sys.exit(1)
    
    unzip_gbk(sys.argv[1], sys.argv[2])
