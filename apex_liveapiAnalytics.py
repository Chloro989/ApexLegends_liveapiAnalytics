import json
import os
import csv
from collections import defaultdict
import argparse

# コマンドライン引数の設定
parser = argparse.ArgumentParser(description='Process some paths.')
parser.add_argument('--input_folder', '-i', type=str, default=os.path.dirname(os.path.realpath(__file__)),
                    help='Path to the folder containing JSON files. Defaults to the directory of this script.')
parser.add_argument('--output_csv', '-o', type=str, default=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'player_stats.csv'),
                    help='Path to the output CSV file. Defaults to the same directory as this script with name player_stats.csv.')

# 引数を解析
args = parser.parse_args()

# パスを設定
folder_path = args.input_folder
output_csv_path = args.output_csv

# Dict
player_stats = defaultdict(lambda: {"total_damage": 0, "file_counts": 0, "character_counts": defaultdict(int)})

# Load Json
for file_name in os.listdir(folder_path):
    if file_name.endswith(".json"):
        file_path = os.path.join(folder_path, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
                file_processed_players = set()
                file_processed_characters = set()
                for event in json_data:
                    if event.get("category") == "playerDamaged" and "attacker" in event:
                        attacker = event["attacker"]
                        name = attacker.get("name")
                        character = attacker.get("character")
                        damage_str = event.get("damageInflicted")  # Get damage as a string
                        
                        if name and damage_str is not None:
                            damage = int(damage_str)  
                            stats = player_stats[name]
                            if character not in file_processed_characters:
                                stats["character_counts"][character] += 1
                                file_processed_characters.add(character)
                            stats["total_damage"] += damage
                            if name not in file_processed_players:
                                stats["file_counts"] += 1
                                file_processed_players.add(name)
        except json.JSONDecodeError as e:
            print(f"Error reading {file_name}: {e}")

# Print Data
            
"""for player, stats in player_stats.items():
    avg_damage = stats["total_damage"] / stats["file_counts"] if stats["file_counts"] > 0 else 0
    print(f"Player: {player}, Average Damage: {avg_damage:.2f}, Matches Joined: {stats['file_counts']}")
    for character, count in stats["character_counts"].items():
        print(f"  Character: {character}, Count: {count}")

"""

# Write CSV
with open(output_csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['Player', 'Average Damage', 'Matches Joined']  
    # Make a List of Chractres
    all_characters = set(character for stats in player_stats.values() for character in stats["character_counts"])
    fieldnames.extend(all_characters) 

    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for player, stats in player_stats.items():
        avg_damage = stats["total_damage"] / stats["file_counts"] if stats["file_counts"] > 0 else 0
        row = {
            'Player': player,
            'Average Damage': f"{avg_damage:.2f}",
            'Matches Joined': stats['file_counts'],
        }
        for character in all_characters:
            row[character] = stats["character_counts"].get(character, 0)
        writer.writerow(row)

print("CSV Written!")
