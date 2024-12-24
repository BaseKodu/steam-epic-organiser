import os
import shutil
import json
from config import STEAM_CONTENT_PATH, EPIC_GAMES_MODS_PATH
from helpers import path_exists, get_abs_path, copytree_with_skip

def detect_content_type(folder_path):
    """
    Detect if a folder contains a mod, asset, or map by checking its contents.
    Returns 'mod', 'asset', or 'map' accordingly.
    """
    # List all files in the directory
    files = os.listdir(folder_path)
    
    # Look for common indicators
    for file in files:
        lower_file = file.lower()
        if lower_file.endswith('.dll') or 'modinfo.xml' in lower_file:
            return 'mod'
        elif lower_file.endswith('.crp'):
            return 'map'
        elif lower_file.endswith('.asset'):
            return 'asset'
    
    # Default to mod if unable to determine
    return 'mod'

def organize_content():
    """
    Organize content from Steam Workshop to Epic Games folders.
    Copies entire folders based on their content type.
    """
    # Load JSON file with mod information
    with open('steam_workshop_mods.json', 'r') as f:
        data = json.load(f)

    # Get absolute paths
    steam_content_path = get_abs_path(STEAM_CONTENT_PATH)
    epic_games_mods_path = get_abs_path(EPIC_GAMES_MODS_PATH)
    
    # Create Epic Games directories if they don't exist
    os.makedirs(epic_games_mods_path, exist_ok=True)
    
    # Iterate through directories in the Steam content folder
    for item in os.listdir(steam_content_path):
        source_path = os.path.join(steam_content_path, item)
        
        # Skip if not a directory
        if not os.path.isdir(source_path):
            continue
            
        # Skip if not in our JSON data
        if item not in data['mods']:
            print(f"Skipping {item} - not found in JSON data")
            continue
            
        # Detect content type
        content_type = detect_content_type(source_path)
        
        # Determine destination path based on content type
        if content_type == 'mod':
            destination_base = epic_games_mods_path
        else:
            print(f"Skipping {item} - unsupported content type: {content_type}")
            continue
        
        # Create the destination folder path
        destination_path = os.path.join(destination_base, item)
        
        # Copy the entire folder
        if not os.path.exists(destination_path):
            print(f"Copying {item} ({data['mods'][item]['name']}) to {destination_path}")
            shutil.copytree(source_path, destination_path)
        else:
            print(f"Skipping {item} - already exists in destination")

if __name__ == "__main__":
    organize_content()
    print("Finished copying content.")