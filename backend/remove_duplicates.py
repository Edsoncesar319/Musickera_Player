import os
import re
from pathlib import Path

def clean_song_name(filename):
    """Remove file extension and clean the song name for comparison"""
    # Remove file extension
    name = os.path.splitext(filename)[0]
    # Remove common suffixes like (Ao Vivo), etc.
    name = re.sub(r'\s*\([^)]*\)\s*$', '', name)
    return name.strip().lower()

def find_duplicates(music_dir):
    """Find duplicate music files based on song names"""
    music_path = Path(music_dir)
    if not music_path.exists():
        print(f"Directory {music_dir} does not exist!")
        return
    
    # Get all music files
    music_files = []
    for ext in ['.mp3', '.m4a', '.mp4', '.wav', '.flac', '.aac']:
        music_files.extend(music_path.glob(f'*{ext}'))
    
    # Group files by cleaned song name
    song_groups = {}
    for file in music_files:
        clean_name = clean_song_name(file.name)
        if clean_name not in song_groups:
            song_groups[clean_name] = []
        song_groups[clean_name].append(file)
    
    # Find duplicates
    duplicates = {}
    for song_name, files in song_groups.items():
        if len(files) > 1:
            duplicates[song_name] = files
    
    return duplicates

def remove_duplicates(music_dir, dry_run=True):
    """Remove duplicate music files, keeping the best quality version"""
    duplicates = find_duplicates(music_dir)
    
    if not duplicates:
        print("No duplicate music files found!")
        return
    
    print(f"Found {len(duplicates)} songs with duplicates:")
    print("-" * 50)
    
    # Priority order for file formats (higher index = higher priority)
    format_priority = {
        '.flac': 5,  # Lossless
        '.wav': 4,   # Lossless
        '.m4a': 3,   # AAC codec
        '.mp3': 2,   # MP3
        '.mp4': 1,   # Video format (lower priority for audio)
        '.aac': 0    # AAC
    }
    
    files_to_remove = []
    
    for song_name, files in duplicates.items():
        print(f"\nSong: {song_name}")
        print("Files:")
        
        # Sort files by priority
        sorted_files = sorted(files, key=lambda f: format_priority.get(f.suffix.lower(), -1), reverse=True)
        
        # Keep the highest priority file, mark others for removal
        keep_file = sorted_files[0]
        remove_files = sorted_files[1:]
        
        print(f"  KEEP: {keep_file.name} ({keep_file.suffix})")
        for file in remove_files:
            print(f"  REMOVE: {file.name} ({file.suffix})")
            files_to_remove.append(file)
    
    if not dry_run and files_to_remove:
        print(f"\nRemoving {len(files_to_remove)} duplicate files...")
        for file in files_to_remove:
            try:
                file.unlink()
                print(f"Removed: {file.name}")
            except Exception as e:
                print(f"Error removing {file.name}: {e}")
        print("Duplicate removal completed!")
    elif dry_run:
        print(f"\nDRY RUN: Would remove {len(files_to_remove)} duplicate files")
        print("Run with dry_run=False to actually remove the files")

if __name__ == "__main__":
    music_directory = "musics"
    
    print("Music Duplicate Remover")
    print("=" * 30)
    
    # First, show what would be removed (dry run)
    remove_duplicates(music_directory, dry_run=True)
    
    # Ask for confirmation
    response = input("\nDo you want to proceed with removing the duplicates? (y/N): ")
    if response.lower() in ['y', 'yes']:
        remove_duplicates(music_directory, dry_run=False)
    else:
        print("Operation cancelled.")
