"""
https://kamedassou.com/python_seireki_to_wareki/
西暦を受け取り、元号で返します。
Args:
    date (str): 処理する西暦の文字列
    format_type(int):1 元号を漢字で返す 平成、令和 等,2 元号を記号で返す H R等
Returns:
    str: 処理済みの文字列
"""

#元号情報
GENGO_DATA = "明治,M,18681023,大正,T,19120730,昭和,S,19261225,平成,H,19890108,令和,R,20190501"

# 改訂版関数（ゼロ埋めを削除したバージョン）
def seireki_to_wareki(date, format_type=1):

    eras = GENGO_DATA.split(',')

    date_int = int(date)

    for i in range(len(eras) - 1, 1, -3):
        era_start = int(eras[i])

        if date_int >= era_start:
            era_name = eras[i - 2] if format_type == 1 else eras[i - 1]

            # 年号を計算
            year = date_int // 10000 - era_start // 10000 + 1
            year_str = str(year)

            # 元年の場合、年号を "元年" にする
            if year == 1:
                year_str = "元年"
            else:
                year_str += "年"  # 年号の後ろに "年" を追加

            # 月日部分をフォーマット
            month_day = date[4:6].lstrip("0") + "月" + date[6:].lstrip("0") + "日" if format_type == 1 else date[4:]

            if format_type == 2:
                # format_type が 2 の場合、年を2桁ゼロ埋め
                year_str = str(year).zfill(2)

            return era_name + year_str + month_day

    return "元号情報を登録してください。"
