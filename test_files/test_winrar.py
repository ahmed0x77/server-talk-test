import os
import sys
import requests
import tempfile
import shutil
from pathlib import Path
import time # Import the time module




import sys
sys.path.append(r"C:\Users\Zeroseven\Desktop\lvnex librarry\database\v6\update_system-3d-sapcey")

import platform
from functools import lru_cache
import shutil
import subprocess
import os
import sys
sys.path.append(r"C:\Users\Zeroseven\Desktop\lvnex librarry\database\v6\update_system-3d-sapcey")

import platform
from functools import lru_cache
import shutil
import subprocess
import os

IS_LINUX = platform.system().lower()  in ['linux', 'darwin']

@lru_cache(maxsize=1)
def ensure_rar_installed():
    """Ensure rar is installed on Linux systems (cached to avoid repeated checks)"""
    if not IS_LINUX:
        return  # Skip on Windows
    
    if not shutil.which("rar"):
        print("RAR not found, attempting to install...")
        #raise Exception("RAR is not installed. Please install RAR to use this feature. please check out `DOC\coolify-rar-unrar-deployment-troubleshooting.md` in the repository for more information.")
    else:
        print("RAR is available")

@lru_cache(maxsize=1)
def ensure_7z_installed():
    """Ensure 7z is installed on Linux systems (cached to avoid repeated checks)"""
    if not IS_LINUX:
        return  # Skip on Windows
    
    if not shutil.which("7z") and not shutil.which("7za"):
        print("7-Zip not found, attempting to install...")
        raise Exception("7-Zip is not installed. Please install p7zip-full package to use this feature, if you are using nixpacks you can add it to your `NIXPACKS.toml` like this:\n\n``nixpacks.toml\n[phases]\n  nixPkgs = [\"p7zip-full\"]")
    else:
        print("7-Zip is available")


def compress_files_rar(items_to_compress, output_archive, compression_level=3):
    """
        Compress files using RAR format
        
        Args:
            items_to_compress: List of files/folders to compress
            output_archive: Path to output RAR file
            compression_level: Compression level:
            0: Store (Add files to archive without compression)
            1: Fastest (Fastest method, least compressive)
            2: Fast (Fast compression method)
            3: Normal (Default compression method)
            4: Good (Good compression method, more compressive)
            5: Best (Best compression method, most compressive but also most slow)
        """
    if os.path.exists(output_archive):
        os.remove(output_archive)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_archive), exist_ok=True)
    
    # Validate compression level
    compression_level = max(0, min(5, compression_level))
    
    # Path to the RAR command line tool
    if IS_LINUX:
        rar_exe = shutil.which("rar") or "rar"
        command = [rar_exe, 'a', '-ep1', f'-m{compression_level}', output_archive]
        startupinfo = None
    else:
        winrar_exe = r"C:\Program Files\WinRAR\WinRAR.exe"
        command = [winrar_exe, 'a', '-ep1', '-ibck', f'-m{compression_level}', output_archive]
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    # Execute the compression command
    try:
        # Add each desired item to the command
        command.extend(items_to_compress)
        
        # Run the command with platform-specific parameters
        if IS_LINUX:
            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        else:
            result = subprocess.run(command, check=True, startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        print(f"Compression successful. The .rar file is located at: {output_archive}")
        return output_archive
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during compression: {e.stderr}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



def compress_files_7z(items_to_compress, output_archive, compression_level=5, exclude=[]):
    if os.path.exists(output_archive):
        os.remove(output_archive)
    """
    5 is normal and 9 is ultra
    :param compression_level: Compression level (0-9), default is 1 (fastest).
    :param exclude: List of files or directories to exclude from compression.
    """
    # Path to the 7z command line tool
    if IS_LINUX:
        seven_zip_exe = shutil.which("7z") or shutil.which("7za") or "7z"
    else:
        seven_zip_exe = r"C:\Users\Zeroseven\Desktop\lvnex librarry\database\v6\app_backend\app_resources\7z.exe"
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_archive), exist_ok=True)

    # Create a temporary directory for excluded items
    temp_dir = os.path.join(os.path.dirname(output_archive), "temp_exclude")
    os.makedirs(temp_dir, exist_ok=True)

    # Move excluded items to the temporary directory
    for item in exclude:
        if os.path.exists(item):
            shutil.move(item, temp_dir)

    # Update the items to compress by removing excluded items
    updated_items = [item for item in items_to_compress if item not in exclude]

    # Create the base command for 7z
    command = [seven_zip_exe, 'a', f'-mx={compression_level}', output_archive]

    # Execute the compression command
    try:
        # Add each desired item to the command
        command.extend(updated_items)
        
        # Run the command
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Compression successful. The .7z file is located at: {output_archive}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during compression: {e.stderr}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Optionally, move excluded items back to their original location
    for item in exclude:
        moved_item = os.path.join(temp_dir, os.path.basename(item))
        original_path = item
        if os.path.exists(moved_item):
            shutil.move(moved_item, original_path)
    
    # Remove the temporary directory if empty
    if not os.listdir(temp_dir):
        os.rmdir(temp_dir)

    return output_archive








def compress_files(items_to_compress, output_archive, compression_level=None, exclude=[]):
    """
    Compress files to RAR or 7z format
    
    Args:
        items_to_compress: List of files/folders to compress
        output_archive: Path to output archive file
        compression_level: Compression level 0-5 for RAR (0=store, 1=fastest, 3=normal, 5=maximum)
                          or 0-9 for 7z (0=store, 1=fastest, 5=normal, 9=ultra)
        exclude: List of files to exclude from compression
    """
    print("compressing files...")
    
    output_archive = output_archive.lower()
    
    if output_archive.endswith(".rar"):
        # Ensure rar is installed on Linux systems (cached check)
        ensure_rar_installed()
        compression_level = compression_level or 3
        return compress_files_rar(items_to_compress, output_archive, compression_level)
    elif output_archive.endswith(".7z") or output_archive.endswith(".zip"):
        # Ensure 7z is installed on Linux systems (cached check)
        ensure_7z_installed()
        compression_level = compression_level or 5
        return compress_files_7z(items_to_compress, output_archive, compression_level, exclude)
    else:
        raise ValueError(f"Unsupported archive format. Supported formats: .rar, .7z")


















import shutil
import subprocess
import sys;sys.path.append(r"c:\Users\Zeroseven\Desktop\lvnex librarry\database\v6\app_backend")

import os
import time
import pyzipper
import rarfile
from concurrent.futures import ThreadPoolExecutor, as_completed

import threading

def global_memory(key, value=None):
    pass
def force2remove(path):
    """Forcefully remove a directory and its contents."""
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
            print(f"Removed directory: {path}")
        except Exception as e:
            print(f"Error removing directory {path}: {e}")
    else:
        print(f"Directory does not exist: {path}")


rarfile.UNRAR_TOOL = r"C:\Users\Zeroseven\Desktop\lvnex librarry\database\v6\app_backend\app_resources\UnRAR.exe"
unrar_path = shutil.which("unrar") or shutil.which("unrar-free")
if IS_LINUX:
    rarfile.UNRAR_TOOL = unrar_path

#https://claude.ai/chat/95759287-6361-48a2-b397-deb271517af6  on modyzerosix08@gmail.com
def extract_zip_file(zip_file, file, extract_path, passwords):
    out_path = os.path.join(extract_path, file)
    if os.path.exists(out_path):
        return  # Skip if file already exists

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    for password in passwords:
        try:
            zip_file.extract(file, path=extract_path, pwd=password.encode())
            return password  # Return the successful password
        except (RuntimeError, pyzipper.BadZipFile):
            continue
    
    raise ValueError(f"No valid password found for {file}")

def extract_zip(archive_path, extract_path, files_to_extract, passwords, monitor_progress_id=False, max_progress=100):
    try:
        with pyzipper.AESZipFile(archive_path) as zip_file:
            files = [f for f in zip_file.namelist() if f in files_to_extract]
            total_files = len(files)
            
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = [executor.submit(extract_zip_file, zip_file, file, extract_path, passwords) for file in files]
                
                for i, future in enumerate(as_completed(futures), 1):
                    try:
                        password = future.result()
                        if password and password != passwords[0]:
                            passwords.insert(0, password)  # Move successful password to front
                        print(f"Progress: {i/total_files*max_progress:.2f}% completed")
                        if monitor_progress_id:
                            if global_memory(monitor_progress_id) == "extract_cancel": #if not exist that means that the user has clicked canceled 
                                for future in futures:
                                    future.cancel()
                                return False
                            global_memory(monitor_progress_id, int(i/total_files*max_progress))


                    except ValueError as e:
                        if monitor_progress_id:
                            global_memory(monitor_progress_id, "error_password")
                        print(str(e))
                        return False  # Stop if no valid password found
    
    except:
        if monitor_progress_id:
            global_memory(monitor_progress_id, "error_badfile")
        print(f"Failed to open ZIP file: {archive_path}. It may be corrupted or invalid.")
        return False

    return True





#https://chatgpt.com/share/66fc3ef3-7da4-800a-91c4-c1897aa81335    --> ITS NOT POSIBLE TO OUTPUT new_path_mapping WITHOUT MOVING THE FILES
def extract_rar_file(rar, file, extract_path, passwords):
    print(f"Extracting {file.filename} to {extract_path} with passwords: {passwords}")
    #time.sleep(1)
    out_path = os.path.join(extract_path, file.filename)
    if os.path.exists(out_path):
        return  # Skip if file already exists

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    for password in passwords:
        try:
            rar.extract(file, path=extract_path, pwd=password)
            return password  # Return the successful password
        except Exception as e:
            print(f"Error extracting000 : {e}")

    raise ValueError(f"No valid password found for {file.filename}")

def extract_rar(archive_path, extract_path, files_to_extract, passwords, monitor_progress_id=False, max_progress=100):
    try:
        with rarfile.RarFile(archive_path) as rar:
            files = [f for f in rar.infolist() if f.filename in files_to_extract]
            total_files = len(files)
            
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = [executor.submit(extract_rar_file, rar, file, extract_path, passwords) for file in files]
                
                for i, future in enumerate(as_completed(futures), 1):
                    try:
                        password = future.result()
                        if password and password != passwords[0]:
                            passwords.insert(0, password)  # Move successful password to front
                        print(f"Progress: {i/total_files*max_progress:.2f}% completed")
                        if monitor_progress_id:
                            if global_memory(monitor_progress_id) == "extract_cancel": #if not exist that means that the user has clicked canceled 
                                return False
                            global_memory(monitor_progress_id, int(i/total_files*max_progress))

                            
                    except ValueError as e:
                        if monitor_progress_id:
                            global_memory(monitor_progress_id, "error_password")
                        print(str(e))
                        return False  # Stop if no valid password found
    
    except Exception as e:
        if monitor_progress_id:
            global_memory(monitor_progress_id, "error_badfile")
        print(f"Failed to open RAR file: {archive_path}. It may be corrupted or invalid." , 'Error07:', e)
        return False

    return True





def get_archive_list_files(archive_path, monitor_progress_id=False):
    try:
        if archive_path.endswith('.zip'):
            with pyzipper.AESZipFile(archive_path) as zip_file:
                return zip_file.namelist()
        elif archive_path.endswith('.rar'):
            with rarfile.RarFile(archive_path) as rar:
                return [f.filename for f in rar.infolist()]
        else:
            print(f"Unsupported archive format: {archive_path}")
            return []
    except Exception as e:
        print(f"Failed to open archive file: {archive_path}. It may be corrupted or invalid.", 'Error07:', e)
        if monitor_progress_id:
            global_memory(monitor_progress_id, "error_badfile")
        return False

def get_archive_file_size(archive_path, filename=None):
    """ if filename = None, then return all files with their sizes """
    if archive_path.endswith('.zip'):
        with pyzipper.AESZipFile(archive_path) as zip_file:
            if filename is None:
                return {name: zip_file.getinfo(name).file_size for name in zip_file.namelist()}
            else:
                file_info = zip_file.getinfo(filename)
                return file_info.file_size
    elif archive_path.endswith('.rar'):
        with rarfile.RarFile(archive_path) as rar:
            if filename is None:
                return {f.filename: f.file_size for f in rar.infolist()}
            else:
                file_info = rar.getinfo(filename)
                return file_info.file_size
    else:
        print(f"Unsupported archive format: {archive_path}")
        return None
    




import os
import threading

def extract_archive(archive_path, extract_path, files_to_extract, passwords=[], monitor_progress_id=None, max_progress=100, Threading=False):
    if not passwords:
        passwords = ['Empty']
    os.makedirs(extract_path, exist_ok=True)

    def extraction_thread():
        if archive_path.endswith('.zip'):
            results = extract_zip(archive_path, extract_path, files_to_extract, passwords, monitor_progress_id, max_progress)
            if not results:
                force2remove(extract_path)
        elif archive_path.endswith('.rar'):
            results = extract_rar(archive_path, extract_path, files_to_extract, passwords, monitor_progress_id, max_progress)
            if not results:
                force2remove(extract_path)
        else:
            print(f"Unsupported archive format: {archive_path}")
            return False
        return results

    if Threading:
        thread = threading.Thread(target=extraction_thread)
        thread.start()
        return thread
    else:
        return extraction_thread()























def download_file(url, destination):
    # shutil.copy(r"C:\Users\Zeroseven\Downloads\sad\3063037.5f7e85f466473\COFFEE_SHOP_4\Coffee_shop_4_vray.max", destination)
    # print(f"File downloaded to: {destination}")
    # #time.sleep(20)  # Simulate download time
    # return True


    """Download a file from URL to destination path"""
    try:
        print(f"Downloading {url}...")
        start_time = time.time() # Record start time
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        end_time = time.time() # Record end time
        download_time = end_time - start_time # Calculate download time
        
        print(f"Downloaded successfully to: {destination}")
        print(f"Download time: {download_time:.2f} seconds") # Print download time
        
        file_size = get_file_size(destination)
        if file_size > 1024 * 1024:  # If file size is larger than 1MB
            print(f"File size: {file_size / (1024 * 1024):.2f} MB")
        else:
            print(f"File size: {file_size / 1024:.2f} KB")
        
        return True
    except requests.exceptions.RequestException as e:
        print(f"Download failed: {e}")
        return False
    except Exception as e:
        print(f"An error occurred during download: {e}")
        return False

def get_file_size(file_path):
    """Get file size in bytes"""
    try:
        return os.path.getsize(file_path)
    except:
        return 0

def test_image_compression():
    """Test function to download and compress an image"""
    
    # URL of the image to download
    image_url = "https://pub-8addd2ede87b415ea57517ed15658c5b.r2.dev/Coffee_shop_4_vray.max"
    compress_extension = ".zip"  
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Using temporary directory: {temp_dir}")
        
        # Define file paths
        downloaded_image_path = os.path.join(temp_dir, "max.max")
        compressed_archive_path = os.path.join(temp_dir, f"compressed_image{compress_extension}")
        extracted_path = os.path.join(temp_dir, "extracted")  # Define extraction path
        
        # Step 1: Download the image
        print("\n=== STEP 1: DOWNLOADING IMAGE ===")
        download_success = download_file(image_url, downloaded_image_path)

        
        if not download_success:
            print("❌ Test failed: Could not download the image")
            return False
        
        # Check if downloaded file exists and get its size
        if not os.path.exists(downloaded_image_path):
            print("❌ Test failed: Downloaded file does not exist")
            return False
        
        original_size = get_file_size(downloaded_image_path)
        print(f"✅ Image downloaded successfully")
        
        # Display original size in MB if it's larger than 1MB, otherwise in KB
        if original_size > 1024 * 1024:
            print(f"   Original file size: {original_size / (1024 * 1024):.2f} MB")
        else:
            print(f"   Original file size: {original_size / 1024:.2f} KB")
        
        # Step 2: Compress the image
        print("\n=== STEP 2: COMPRESSING IMAGE ===")
        start_time = time.time() # Record start time for compression
        try:
            result = compress_files(
                items_to_compress=[downloaded_image_path],
                output_archive=compressed_archive_path,
                compression_level=5
            )

            # Check if compression was successful
            if os.path.exists(compressed_archive_path):
                end_time = time.time() # Record end time for compression
                compression_time = end_time - start_time # Calculate compression time
                
                compressed_size = get_file_size(compressed_archive_path)
                compression_ratio = (1 - compressed_size / original_size) * 100 if original_size > 0 else 0
                
                print("✅ Compression completed successfully!")
                print(f"   Compressed file: {compressed_archive_path}")
                
                # Display compressed size in MB if it's larger than 1MB, otherwise in KB
                if compressed_size > 1024 * 1024:
                    print(f"   Compressed size: {compressed_size / (1024 * 1024):.2f} MB")
                else:
                    print(f"   Compressed size: {compressed_size / 1024:.2f} KB")
                
                print(f"   Compression ratio: {compression_ratio:.1f}% reduction")
                print(f"   Compression time: {compression_time:.2f} seconds") # Print compression time
                
                if compressed_size < original_size:
                    print("✅ File was successfully compressed (size reduced)")
                else:
                    print("⚠️  File was compressed but size increased (image already optimized)")
                
                # Step 3: Extract the archive
                print("\n=== STEP 3: EXTRACTING ARCHIVE ===")
                try:
                    os.makedirs(extracted_path, exist_ok=True)
                    
                    # Extract the archive using the extract_archive function
                    files_to_extract = get_archive_list_files(compressed_archive_path)
                    print(f"Files to extract: {files_to_extract}")
                    if files_to_extract is False:
                        print("❌ Extraction failed: Could not list files in archive")
                        return False
                    
                    extraction_result = extract_archive(
                        archive_path=compressed_archive_path,
                        extract_path=extracted_path,
                        files_to_extract=files_to_extract,
                        passwords=[]  # Provide passwords if needed
                    )
                    
                    if extraction_result:
                        print(f"✅ Archive extracted successfully to: {extracted_path}")
                        print(f"Extracted items: {os.listdir(extracted_path)}")
                        return True
                    else:
                        print("❌ Extraction failed")
                        return False
                    
                except Exception as e:
                    print(f"❌ Extraction failed with error: {e}")
                    return False
            else:
                print("❌ Compression failed: Output archive was not created")
                return False
                
        except Exception as e:
            print(f"❌ Compression failed with error: {e}")
            return False

def main():
    """Main function to run the test"""
    print("🚀 Starting Image Download and Compression Test")
    print("=" * 50)
    
    # Check if requests is available
    try:
        import requests
    except ImportError:
        print("❌ Error: 'requests' module is not installed")
        print("   Please install it using: pip install requests")
        return
    
    # Run the test
    success = test_image_compression()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 TEST PASSED: Image was downloaded and compressed successfully!")
    else:
        print("💥 TEST FAILED: Check the error messages above")

if __name__ == "__main__":
    main()
