import ujson as json
import csv
import csv


def analyze_characters():
    # Read the contents of characters.json
    with open("characters.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    # Aggregate the "character" field using the "name" field and count occurrences
    characters_count = {}
    all_characters = set()

    for entry in data:
        name = entry["player"]["name"]
        character = entry["player"]["character"]
        all_characters.add(character)  # Update the set of all characters
        if name not in characters_count:
            characters_count[name] = {}
        if character in characters_count[name]:
            characters_count[name][character] += 1
        else:
            characters_count[name][character] = 1

    # Create a sorted list of all characters to define the columns in the CSV
    sorted_characters = sorted(all_characters)

    # Write the aggregated and counted data to a CSV file
    with open("characters_count.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Write header with player and character names
        writer.writerow(["Player"] + sorted_characters)
        for name, characters in characters_count.items():
            # Prepare a row for each player with counts for each character (0 if not used)
            row = [name] + [
                characters.get(character, 0) for character in sorted_characters
            ]
            writer.writerow(row)
