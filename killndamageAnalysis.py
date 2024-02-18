import ujson as json  # ujsonを利用
import csv
import os
from collections import defaultdict


def analyze_kill_and_damage(folder_path, csv_file_path):
    # プレイヤーデータを格納するためのdefaultdict
    players_data = defaultdict(lambda: {"kills": 0, "damage": 0})

    # フォルダ内の全JSONファイルを処理
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json"):
            file_path = os.path.join(folder_path, file_name)

            with open(file_path, "r", encoding="utf-8") as file:
                events = json.load(file)  # JSONファイルからリストを読み込む

                # ファイル内の各イベントを処理
                for event in events:
                    # playerDamaged カテゴリの処理
                    if event["category"] == "playerDamaged":
                        attacker_name = event["attacker"]["name"]
                        damage = int(event["damageInflicted"])
                        players_data[attacker_name]["damage"] += damage

                    # playerKilled カテゴリの処理
                    elif event["category"] == "playerKilled":
                        attacker_name = event["attacker"]["name"]
                        players_data[attacker_name]["kills"] += 1

    # 結果をCSVファイルに書き込む
    with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Player", "Total Damage", "Kills"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for player, stats in players_data.items():
            writer.writerow(
                {
                    "Player": player,
                    "Total Damage": stats["damage"],
                    "Kills": stats["kills"],
                }
            )

    print("CSV written successfully.")
