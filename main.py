import flet as ft
import threading
import sys

# 既存の関数をインポートする
import jsonCutter, charactersAnalysis, killndamageAnalysis, csvFormatt, makePlayerStats, aggregateTeamkills, matchAggregate, makeResult

input_folder_path = "./raw_data"
input_dir = "./match_2_aggregate"
output_dir = "./match_2_aggregate/output"
kd_output_folder_path = "./kill_and_damages"
ch_output_file_path = "characters.json"

# カスタム出力クラス
class CustomOutput:
    def __init__(self, log_area):
        self.log_area = log_area
        self.standard_output = sys.stdout

    def write(self, message):
        # GUIのログエリアにメッセージを追加
        self.log_area.value += message
        self.log_area.update()
        # 標準出力にもメッセージを送る
        self.standard_output.write(message)

    def flush(self):
        # フラッシュメソッドは、標準出力のフラッシュに委譲する
        self.standard_output.flush()

# プレイヤーデータの集計を実行する関数
def aggregate_player_data(log_area):
    sys.stdout = CustomOutput(log_area)
    # 処理を実行
    jsonCutter.filter_and_save_data(input_folder_path, kd_output_folder_path, ch_output_file_path)
    charactersAnalysis.analyze_characters()
    killndamageAnalysis.analyze_kill_and_damage(kd_output_folder_path, "killndamages.csv")
    csvFormatt.sort_csv_data()
    makePlayerStats.make_player_stats()
    print("Player data processing completed!")
    sys.stdout = sys.__stdout__

# マッチデータの集計を実行する関数
def aggregate_match_data(log_area):
    sys.stdout = CustomOutput(log_area)
    # 処理を実行
    aggregateTeamkills.aggregate_team_kills(input_dir, output_dir)
    matchAggregate.calculate_team_ranks(input_dir, output_dir)
    makeResult.calculate_match_results()
    print("Match data processing completed!")
    sys.stdout = sys.__stdout__

def app(page: ft.Page):
    page.title = "Data Aggregator"
    page.vertical_alignment = ft.MainAxisAlignment.START

    # ログエリアの定義
    log_area = ft.TextField(value="", expand=True, multiline=True, read_only=True, label="Logs")

    # プレイヤーデータ集計ボタン
    aggregate_player_data_button = ft.CupertinoButton(
        content=ft.Text("Aggregate Player Data", color=ft.colors.PINK_900),
        bgcolor=ft.colors.INDIGO_100,
        disabled_color=ft.colors.DEEP_PURPLE,
        filled=True,
        on_click=lambda e: threading.Thread(target=aggregate_player_data, args=(log_area,)).start()
        
    )

    # マッチデータ集計ボタン
    aggregate_match_data_button = ft.CupertinoButton(
        content=ft.Text("Aggregate Match Data", color=ft.colors.PINK_900),
        bgcolor=ft.colors.INDIGO_100,
        disabled_color=ft.colors.DEEP_PURPLE,
        filled=True,
        on_click=lambda e: threading.Thread(target=aggregate_match_data, args=(log_area,)).start()
    )

    page.add(aggregate_player_data_button, aggregate_match_data_button, log_area)

if __name__ == "__main__":
    ft.app(target=app)

