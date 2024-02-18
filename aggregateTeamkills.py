import ujson as json
import csv
import os
from collections import defaultdict


def aggregate_team_kills(input_dir, output_dir):
    # 出力フォルダがなければ作成
    os.makedirs(output_dir, exist_ok=True)

    # チームのキル数を保持する辞書
    team_kills = defaultdict(int)

    # チーム名を保持する辞書
    team_names = {}

    # フォルダ内の全JSONファイルを処理
    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(input_dir, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

                # gameStateChangedがPostmatchの場合は無視
                if any(
                    event.get("category") == "gameStateChanged"
                    and event.get("state") == "Postmatch"
                    for event in data
                ):
                    continue

                for event in data:
                    if event["category"] == "playerKilled":
                        attacker = event.get("attacker", {})
                        teamId = attacker.get("teamId")
                        teamName = attacker.get("teamName")
                        if teamId and teamName:
                            team_kills[teamId] += 1
                            if teamId not in team_names:
                                team_names[teamId] = teamName

    # 結果をCSVファイルに出力
    output_file = os.path.join(output_dir, "teamKills.csv")
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["team ID", "team name", "kills"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for teamId, kills in sorted(team_kills.items(), key=lambda x: x[0]):
            writer.writerow(
                {"team ID": teamId, "team name": team_names[teamId], "kills": kills}
            )

    print(f"Result was saved to {output_file} .")
