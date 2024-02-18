import ujson as json
import csv
import os
from collections import defaultdict
from datetime import datetime, timedelta


def calculate_team_ranks(input_dir, output_dir):

    output_file = os.path.join(output_dir, "teamRanks.csv")

    # 出力フォルダがなければ作成
    os.makedirs(output_dir, exist_ok=True)

    # ファイル名から日付を解析する関数
    def parse_date_from_filename(filename):
        date_str = filename.split(".")[0]  # 拡張子を除去
        try:
            return datetime.strptime(date_str, "%m-%d-%Y-%H-%M-%S")
        except ValueError:
            return datetime.now() - timedelta(
                days=365
            )  # 解析できない場合はデフォルト値を返す

    # ファイル名に基づいてソート
    sorted_filenames = sorted(
        os.listdir(input_dir), key=lambda x: parse_date_from_filename(x)
    )

    # 各JSONファイルごとにランクを計算
    ranks = defaultdict(list)
    for filename in sorted_filenames:
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

                teams = defaultdict(
                    lambda: {"teamName": None, "timestamp": float("inf")}
                )
                for event in data:
                    if event["category"] == "squadEliminated":
                        for player in event["players"]:
                            teamId = player["teamId"]
                            timestamp = int(event["timestamp"])
                            teamName = player["teamName"]
                            if timestamp < teams[teamId]["timestamp"]:
                                teams[teamId]["timestamp"] = timestamp
                                teams[teamId]["teamName"] = teamName
                team_count = len(teams)
                ranked_teams = sorted(teams.items(), key=lambda x: x[1]["timestamp"])
                for i, (teamId, teamInfo) in enumerate(ranked_teams, start=1):
                    rank = team_count - i + 1
                    ranks[teamId].append(rank)

    # teamIdで降順に並び替えてCSVに出力
    sorted_teams_by_id = sorted(ranks.items(), key=lambda x: x[0])

    with open(output_file, "w", newline="") as csvfile:
        fieldnames = ["team ID", "team name"] + [
            f"match{i+1} rank" for i in range(len(sorted_filenames))
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for teamId, rank_list in sorted_teams_by_id:
            row = {"team ID": teamId, "team name": teams[teamId]["teamName"]}
            row.update({f"match{i+1} rank": rank for i, rank in enumerate(rank_list)})
            writer.writerow(row)

    print(f"Result was saved to {output_file} .")
