import csv


def sort_csv_data():
    # 最初のCSVファイルからプレイヤーリストを読み込む
    players_order = []
    with open("characters_count.csv", "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # ヘッダーをスキップ
        for row in reader:
            players_order.append(row[0])  # プレイヤー名をセットに追加

    # 二つ目のCSVファイルのデータを読み込む
    players_data = {}
    with open("killndamages.csv", "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            player_name = row["Player"]
            players_data[player_name] = row

    # プレイヤーリストの順序に基づいて二つ目のCSVファイルのデータを並び替える
    sorted_data = [
        players_data[player] for player in players_order if player in players_data
    ]

    # 並び替えたデータを新しいCSVファイルに書き込む
    with open("sorted_killndamages.csv", "w", newline="", encoding="utf-8") as csvfile:
        if sorted_data:  # ソートされたデータがある場合のみ
            fieldnames = reader.fieldnames  # ヘッダーを取得
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sorted_data)

    print("Sorted data has been saved to 'sorted_killndamages.csv' ")
