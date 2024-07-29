import os
import shutil
import json
from config import STEAM_CONTENT_PATH, EPIC_GAMES_MODS_PATH
from helpers import path_exists, get_abs_path, copytree_with_skip

# Define paths
steam_content_path = get_abs_path(STEAM_CONTENT_PATH)
epic_games_mods_path = get_abs_path(EPIC_GAMES_MODS_PATH)
#epic_games_assets_path = 'path/to/your/epic/games/Assets'
#epic_games_maps_path = 'path/to/your/epic/games/Maps'

# Debug: Print paths to ensure they are correct
print(f"Steam content path: {steam_content_path}")
#print(f"Epic Games mods path: {epic_games_mods_path}")

'''
if path_exists(steam_content_path):
    print("Steam content path exists")
else:
    print("Steam content path does not exist")
    
if path_exists(epic_games_mods_path):
    print("Epic Games mods path exists")
else:
    print("Epic Games mods path does not exist")
'''


# TODO: Make sure you copy entire mod folders, not just the contents
# Load JSON file with mod information
with open('steam_workshop_mods.json', 'r') as f:
    data = json.load(f)

# Function to organize content
def organize_content():
    # Iterate through directories in the Steam content folder
    for item in os.listdir(steam_content_path):
        item_path = os.path.join(steam_content_path, item)
        
        if os.path.isdir(item_path) and item in data['mods']:
            mod_info = data['mods'][item]
            
            # Determine destination path based on the type
            destination_path = epic_games_mods_path  # Default to mods path
            
            # Copy the directory to the corresponding folder in the Epic Games version
            copytree_with_skip(item_path, destination_path)
            print(f"Copied {item} ({mod_info['name']}) to {destination_path}")
        else:
            # Handle files if necessary
            print(f"Item {item} not found in JSON data or is not a directory")
            pass
        
 


       
if __name__ == "__main__":
    ...
    organize_content()







