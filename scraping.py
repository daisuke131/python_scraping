from pathlib import Path
from time import sleep

import pandas as pd
from dotenv import load_dotenv

from driver_setting import set_driver
from log_setting import log_setting

log = log_setting()
load_dotenv()


def main():
    # ログ出力設定
    log.debug("===== start =====")

    # ヘッドレスフラグを渡す。Trueならブラウザを立ち上げない。
    driver = set_driver(True)
    driver.get("https://job.mynavi.jp/2022/")
    sleep(3)

    # 検索ワード入力
    search_word = input("検索ワード>>")
    search_word = search_word.split()
    search_word = " ".join(search_word)
    textbox = driver.find_element_by_xpath('//*[@id="srchWord"]')
    textbox.send_keys(search_word)

    # URL クエリパラメータ
    # search_word = "%20".join(search_word)
    # search_query_url = (
    #     "https://job.mynavi.jp/22/pc/corpinfo/searchCorpListByGenCond/index?q="
    #     + search_word
    # )
    # driver = set_driver(False)
    # driver.get(search_query_url + search_word)
    # sleep(3)

    # 検索ボタン押下
    search_button = driver.find_element_by_xpath('//*[@id="srchButton"]/span')
    search_button.click()

    log.info(f"{search_word}で検索")

    search_count = 0
    data_count = 0

    corp_data_list = []

    while 1:
        # 会社名リスト追加
        corps_list = driver.find_elements_by_class_name("js-add-examination-list-text")
        search_count += len(corps_list)

        for corp in corps_list:
            # 画面下部までスクロール(これがないと画面に写ってないリンクが使えない。)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            corp.click()
            sleep(1)

            # アクティブ画面(タブ)切り替え
            driver.switch_to.window(driver.window_handles[-1])

            # タブを切り替えないと情報が見れないのでリンクまでスクロール
            element = driver.find_element_by_xpath('//*[@id="headerEmploymentTabLink"]')
            # 指定した要素までスクロール
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            # タブリンククリック
            element.click()
            sleep(1)

            # 会社データ取得
            corp_data = get_corp_data(driver)
            # リストに追加
            corp_data_list.append(corp_data)

            # アクティブ画面(タブ)切り替え⇨元画面へ
            driver.switch_to.window(driver.window_handles[0])

            data_count += 1
            log.info(f"{data_count}件書き込み完了")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 次のページへ
        try:
            driver.find_element_by_link_text("次の100社").click()
            sleep(1)
        except Exception:
            break

    # CSVに書き込み
    if data_count > 0:
        write_csv(search_word, corp_data_list)
        log.info(f"{data_count}件出力しました。")
        print(f"{search_count}件見つかりました。")
    else:
        log.info(f"{data_count}件です。")

    log.debug("===== end =====")
    # ブラウザ閉じる
    driver.quit()


# CSV書き込み
def write_csv(search_word, corp_data_list):
    # ディレクトリがないとエラーになるため作成
    dir = Path("./csv")
    dir.mkdir(parents=True, exist_ok=True)

    # csvファイル名に検索ワードを加える。
    csv_path = f"./csv/{search_word}_data.csv"
    # ヘッダー作成
    Column = ["会社名", "基本給", "勤務時間", "URL"]
    df = pd.DataFrame(corp_data_list, columns=Column)
    # 行番号なしで出力
    df.to_csv(csv_path, index=False, encoding="CP932")


# 会社データ取得
def get_corp_data(driver):
    # get_data_judgeでエラーならpass
    corp_name = get_data_judge(
        driver, "会社名", '//*[@id="companyHead"]/div[1]/div/div/div[1]/h1'
    )
    corp_income = get_data_judge(
        driver, "基本給", '//*[@id="employTreatmentListDescText3190"]'
    )
    corp_work_hours = get_data_judge(
        driver, "勤務時間", '//*[@id="employTreatmentListDescText3270"]'
    )
    corp_URL = driver.current_url
    return [corp_name, corp_income, corp_work_hours, corp_URL]


# データ取得できない場合はスルー
def get_data_judge(driver, data_name, xpath):
    try:
        return driver.find_element_by_xpath(xpath).text
    except Exception:
        log.critical(f"{data_name}が取得できませんでした。")
        pass


if __name__ == "__main__":
    main()
