import csv
import sys
import chardet

""" デフォルト出力行番号 """
DEFAULT_OUTPUT_ROW_NUM = 100
""" デフォルト出力パス """
DEFAULT_OUTPUT_FILE_PATH = './output.csv'


def get_encoding(file_path):
    """
    ファイルパスからファイルのエンコーディングを取得する
    :param file_path ファイルパス
    :return ファイルのエンコーディング
    """
    detector = chardet.UniversalDetector()
    with open(file_path, mode='rb') as f:
        for binary in f:
            detector.feed(binary)
            if detector.done:
                break
    detector.close()
    return detector.result['encoding']


def get_input_rows_and_header(input_file_path, encoding, is_header):
    """
    入力ファイルの各行とヘッダーを取得する
    :param input_file_path ファイルパス
    :param encoding ファイルパス
    :param is_header ファイルパス
    :return 入力元csv行一覧、ヘッダー行
    """
    input_rows = []
    # ヘッダーをinput_rowsに入れると
    # 先頭行に戻って出力を継続する処理がややこしくなるので明示的にヘッダーを分けた
    header = None

    with open(input_file_path, 'r', encoding=encoding) as f:
        rows = csv.reader(f)

        if is_header:
            header = next(rows)

        for row in rows:
            input_rows.append(row)

    return input_rows, header


def output_csv(output_file_path, encoding, input_rows, output_row_num, header):
    """
    csvファイルを出力する
    :param output_file_path 出力ファイルパス
    :param encoding 出力ファイルエンコーディング
    :param input_rows 入力元csvの行一覧
    :param output_row_num 出力したい行数
    :param header ヘッダー行
    """
    with open(output_file_path, 'w', encoding=encoding) as f:
        # 出力したい行数と入力元のcsv行の何行目を出力しているかは別で管理したい
        input_row_current_index = 0

        csv_writer = csv.writer(f)
        for i in range(0, output_row_num):
            if i == 0 and header:
                csv_writer.writerow(header)

            csv_writer.writerow(input_rows[input_row_current_index])
            input_row_current_index += 1

            if input_row_current_index >= len(input_rows):
                # 入力元のcsv行一覧を最終行まで出力したら先頭行から出力し直す
                input_row_current_index = 0


def main():
    input_file_path = sys.argv[1]
    # 引数がなければデフォルト行数出力
    output_row_num = int(sys.argv[2]) if len(sys.argv) >= 3 else DEFAULT_OUTPUT_ROW_NUM
    # 引数がなければデフォルト出力パスにファイルを出力
    output_file_path = sys.argv[3] if len(sys.argv) >= 4 else DEFAULT_OUTPUT_FILE_PATH
    # 引数がなければヘッダーありとみなす
    is_header = bool(sys.argv[4]) if len(sys.argv) >= 5 else True

    encoding = get_encoding(input_file_path)
    input_rows, header = get_input_rows_and_header(input_file_path, encoding, is_header)
    output_csv(output_file_path, encoding, input_rows, output_row_num, header)


main()
