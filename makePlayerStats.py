import csv


def make_player_stats():
    # ステップ 1: CSVファイルを読み込む
    def load_csv(filename):
        with open(filename, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            return list(reader)

    characters_data = load_csv(
        "characters_count.csv"
    )  # このファイル名が正しいか確認が必要です。
    sorted_killndamages_data = load_csv("sorted_killndamages.csv")

    # ステップ 2 & 3: 新しい列を追加し、Matches Joinedを計算する
    for character in characters_data:
        character["Matches Joined"] = sum(
            int(character[hero]) for hero in character if hero != "Player"
        )
        character["Total Damage"] = 0
        character["Kills"] = 0
        character["AVG Damage"] = 0

    # ステップ 4: Total DamageとKillsを更新する
    for damage_data in sorted_killndamages_data:
        for character in characters_data:
            if character["Player"] == damage_data["Player"]:
                character["Total Damage"] = damage_data["Total Damage"]
                character["Kills"] = damage_data["Kills"]

    # ステップ 5: AVG Damageを計算する
    for character in characters_data:
        if int(character["Matches Joined"]) > 0:
            character["AVG Damage"] = round(
                int(character["Total Damage"]) / int(character["Matches Joined"]), 2
            )

    # ステップ 6: 新しいCSVファイルを作成する
    fieldnames = ["Player", "Matches Joined", "Total Damage", "AVG Damage", "Kills"] + [
        hero
        for hero in characters_data[0]
        if hero
        not in ["Player", "Matches Joined", "Total Damage", "AVG Damage", "Kills"]
    ]
    with open("players_stats.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for character in characters_data:
            writer.writerow(character)

    print("Data has been saved to 'players_stats.csv' ")
