"""
HenParser.py
Author: pns
レセ電コード情報ファイル記録条件仕様 R6.8.23版
/opt/homebrew/bin/python3 (-V 3.13.1)
brew install python-tk@3.13
brew install tcl-tk
source ./.venv/bin/activate
pip install pyinstaller
pyinstaller HenParser.py --onefile
deactivate
"""
import sys
import tkinter.filedialog
import csv
import re
import Gengo
import Ref

product = []

# HEN, SAH ファイル選択
def get_path():
    path = tkinter.filedialog.askopenfilename()
    return path

# 日付文字列処理
def to_date(s):
    drop_0 = lambda d: re.sub("^0", "", d)
    if len(s) == 6:
        return [s[0:4], drop_0(s[4:6])]
    else:
        return [s[0:4], drop_0(s[4:6]), drop_0(s[6:8])]

#
# main
#
if __name__ == "__main__":
    path = get_path()
    if not path:
        sys.exit(1)

    with open(path, encoding="shift_jis") as f:
        reader = csv.reader(f)
        for item in reader:
            if len(item) < 4:
                continue

            # ヘッダ
            if item[0] == "HI":
                date = to_date(item[2])
                formatted = f"HI 返戻月: {date[0]}年 {date[1]}月"
                product.append(formatted)

            #  履歴管理情報: item[0] データ識別, item[1] 行番号, item[2] 枝番号
            match item[3]:
                case "MN":  # レセプト管理コード
                    continue
                case "IR":  # 医療機関情報レコード
                    continue

                case "RE":  # レセプト共通レコード
                    number = "\nレセプト " + item[4]
                    product.append(number)
                    date = to_date(item[6])
                    name = item[7]
                    kana = item[39]
                    birthday = Gengo.seireki_to_wareki(item[9])
                    sex = Ref.sex[item[8]]
                    karte_id = item[16]
                    formatted = f"{karte_id} {name} {kana} {sex} {birthday}生 診療月 {date[0]}年{date[1]}月"
                    product.append(formatted)

                case "HO":  # 保険者レコード
                    organization = item[4]
                    symbol = item[5]
                    number = item[6]
                    formatted = f"HO 保険者 {organization} 記号 {symbol} 番号 {number}"
                    product.append(formatted)

                case "KO":  # 公費レコード
                    funds = item[4]
                    number = item[5]
                    formatted = f"KO 公費負担者 {funds} 番号 {number}"
                    product.append(formatted)

                case "SN":  # 資格確認レコード
                    if item[0] != "1" and item[0] != "8": # 保険者で変更等あった場合
                        product.append("SN " + Ref.data_category[item[0]])
                        product.append("   負担者種別: " + Ref.payer_category[item[4]])
                        product.append("   確認区分: " + Ref.certify_category[item[5]])
                        organization = item[6]
                        symbol = item[7]
                        number = item[8]
                        branch = item[9]
                        recipient = item[10]
                        formatted = f"   保険者 {organization} 記号 {symbol} 番号 {number} {branch} 受給者番号 {recipient}"
                        product.append(formatted)

                case "JD":  # 受診日等レコード
                    continue
                case "MF":  # 窓口負担額レコード（記録は任意）
                    continue
                case "GR":  # 包括評価対象外理由レコード
                    continue
                case "SY":  # 傷病名レコード
                    continue
                case "SI":  # 診療行為レコード
                    continue
                case "IY":  # 医薬品レコード
                    continue
                case "TO":  # 特定器材レコード
                    continue
                case "CO":  # コメントレコード
                    continue
                case "SJ":  # 症状詳記レコード
                    continue
                case "TI":  # 臓器提供医療機関情報レコード
                    continue
                case "TR":  # 臓器提供者レセプト情報レコー
                    continue
                case "TS":  # 臓器提供者請求情報レコード
                    continue

                case "JY":  # 事由レコード
                    data = Ref.data_category[item[0]]
                    revision = "追加" if item[4] == "1" else "修正" if item[4] == "2" else "削除"
                    formatted = f"JY {data} - {revision}"
                    product.append(formatted)

                case "ON":  # 資格確認運用レコード
                    continue
                case "EX":  # 審査運用レコード
                    continue
                case "RC":  # レコード管理情報レコード
                    continue

                case "MD":  # 再審査申し出レコード
                    reason = Ref.reason.get(item[8], "?"+item[8])
                    formatted = f"MD 理由: {reason} {item[9]} {item[10]} {item[11]}"
                    product.append(formatted)
                    if item[12]:
                        reason_details = Ref.reason_details.get(item[12], "?"+item[12])
                        product.append(reason_details)
                    if item[14]:
                        product.append(item[14])
                    if item[15]:
                        product.append(item[15])
                    if item[16] == "1":
                        product.append("医療機関と連絡調整済み")

                case "RT":  # 理由対象レコード
                    continue

                case "JR":  # レセプト縦覧レコード
                    if item[4]:
                        if item[4] =="1":
                            product.append("JR 縦覧区分: 相手が電子レセプトの場合")
                        elif item[4] == "2":
                            product.append("JR 縦覧区分: 相手が紙レセプトの場合")
                        elif item[4] == "3":
                            product.append("JR 縦覧区分: 相手が紙の参考の場合")

                case "MK":  # 再審査申し出結果レコード
                    date = to_date(item[5])
                    claim_address = Ref.claim_address.get(item[6], "?"+item[6])
                    revise_date = to_date(item[7])
                    if item[8]:
                        reason = Ref.reason[item[8]]
                    if item[9]:
                        revise_result = Ref.revise_result.get(item[9], "?"+item[9])
                    formatted = f"MK {claim_address} 請求 {date[0]}年{date[1]}月{date[2]}日 審査 {revise_date[0]}年{revise_date[1]}月 {reason} {revise_result}"
                    product.append(formatted)
                    if item[10]: # 連絡
                        product.append("   " + item[10])
                    if item[11]: # 原審通り理由1
                        product.append(Ref.accept_reason["   " + item[11]])
                    if item[12]: # 原審通り理由2
                        product.append(Ref.accept_reason["   " + item[12]])
                    if item[13]: # 原審通り理由3
                        product.append(Ref.accept_reason["   " + item[13]])

                case "HR":  # 返戻理由レコード
                    date = to_date(item[4])
                    type = Ref.revise_type[item[5]]
                    reason = item[8] + " - " + item[9]
                    formatted = f"HR 返戻 {date[0]}年{date[1]}月 {type} 理由:{reason}"
                    product.append(formatted)

    file = open(path+".txt", "w")
    for line in product:
        print(line)
        file.write(line+"\n")
    file.close()

