import json
import os
import ujson as json


def filter_and_save_data(input_folder_path, kd_output_folder_path, ch_output_file_path):
    # カテゴリーのフィルタリング用セット
    kd_categories = {"playerKilled", "playerDamaged"}
    ch_categories = {"playerConnected"}

    # 出力フォルダの作成
    os.makedirs(kd_output_folder_path, exist_ok=True)

    # 出力ファイルの初期化
    all_ch_filtered_data = []

    for file_name in os.listdir(input_folder_path):
        if file_name.endswith(".json"):
            file_path = os.path.join(input_folder_path, file_name)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    json_data = json.load(file)

                    # gameStateChangedがPostmatchの場合は無視
                    if any(
                        event.get("category") == "gameStateChanged"
                        and event.get("state") == "Postmatch"
                        for event in json_data
                    ):
                        continue

                    # 'playerKilled' または 'playerDamaged' のカテゴリーに基づいてエントリーをフィルタリング
                    kd_filtered_data = [
                        event
                        for event in json_data
                        if event["category"] in ("playerKilled", "playerDamaged")
                    ]
                    if kd_filtered_data:
                        # 新しいJSONファイルにフィルタリングされたデータを保存
                        kd_output_file_path = os.path.join(
                            kd_output_folder_path, file_name
                        )
                        with open(
                            kd_output_file_path, "w", encoding="utf-8"
                        ) as outfile:
                            json.dump(
                                kd_filtered_data, outfile, indent=4, ensure_ascii=False
                            )
                        print(
                            f"Kill and damage data has been saved to {kd_output_file_path}."
                        )

                    # 'playerConnected' のカテゴリーに基づいてエントリーをフィルタリング
                    ch_filtered_data = [
                        event
                        for event in json_data
                        if event["category"] in ch_categories
                    ]
                    if ch_filtered_data:
                        all_ch_filtered_data.extend(ch_filtered_data)

            except json.JSONDecodeError as e:
                print(f"Error reading {file_name}: {e}")

    # フィルタリングされたデータを保存
    with open(ch_output_file_path, "w", encoding="utf-8") as ch_outfile:
        json.dump(all_ch_filtered_data, ch_outfile, ensure_ascii=False, indent=4)
        print(f"Character data has been saved to {ch_output_file_path}.")
