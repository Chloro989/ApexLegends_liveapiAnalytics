import csv
import os

def calculate_match_results():
    # ファイルパスの定義
    input_dir = './match_2_aggregate/output'
    team_kills_file = os.path.join(input_dir, 'teamKills.csv')
    team_ranks_file = os.path.join(input_dir, 'teamRanks.csv')
    output_file = os.path.join(input_dir, 'result.csv')

    # チームのキル数とランクを読み込む
    team_kills = {}
    with open(team_kills_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            team_kills[row['team ID']] = row['kills']

    team_ranks = {}
    with open(team_ranks_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        match_columns = reader.fieldnames[2:]  # 最初の2列以外はマッチのランク
        for row in reader:
            team_ranks[row['team ID']] = row

    # マッチポイントのルールに基づいてポイントを計算
    points_for_rank = {1: 12, 2: 9, 3: 7, 4: 5, 5: 4, 6: 3, 7: 3, 8: 2, 9: 2, 10: 2, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0}

    # 結果のリストを作成
    results = []
    for team_id, team_info in team_ranks.items():
        if team_id in team_kills:
            match_points = int(team_kills[team_id])  # Killsの数だけポイントを加算
            for key in match_columns:
                if team_info[key].isdigit():
                    rank = int(team_info[key])
                    match_points += points_for_rank.get(rank, 0)
            row = {'team ID': team_id, 'team name': team_info['team name'], 'kills': team_kills[team_id], 'match point': match_points}
            row.update({key: team_info[key] for key in match_columns})  # 各マッチのランクを追加
            results.append(row)

    # match pointの降順で結果をソート
    results_sorted = sorted(results, key=lambda x: x['match point'], reverse=True)

    # 結果をCSVファイルに出力
    fieldnames = ['team ID', 'team name', 'kills', 'match point'] + match_columns
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results_sorted)

    print(f'Result has been saved to {output_file}. ')
