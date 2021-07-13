from pathlib import Path
from time import sleep

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def main():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome("chromedriver", options=options)
    driver.get("https://job.mynavi.jp/2022/")
    sleep(3)

    # 検索ワード入力
    textbox = driver.find_element_by_xpath('//*[@id="srchWord"]')
    search_word = input("検索ワード>>")
    textbox.send_keys(search_word)

    # 検索ボタン押下
    search_button = driver.find_element_by_xpath('//*[@id="srchButton"]/span')
    search_button.click()

    search_count = 0
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

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 次のページへ
        try:
            driver.find_element_by_link_text("次の100社").click()
            sleep(1)
        except Exception:
            break

    # CSVに書き込み
    write_csv(search_word, corp_data_list)
    # 件数確認用
    print(search_count)
    # ブラウザ閉じる
    driver.quit()


def write_csv(search_word, corp_data_list):
    # ディレクトリがないとエラーになるため作成
    dir = Path("./csv")
    dir.mkdir(parents=True, exist_ok=True)

    # csvファイル名に検索ワードを加える。
    csv_path = f"./csv/{search_word}_data.csv"
    # ヘッダー作成
    Coulum = ["会社名", "基本給", "勤務時間", "URL"]
    df = pd.DataFrame(corp_data_list, columns=Coulum)
    # 行番号なしで出力
    df.to_csv(csv_path, index=False, encoding="CP932")


def get_corp_data(driver):
    corp_name = get_data_judge(
        driver, '//*[@id="companyHead"]/div[1]/div/div/div[1]/h1'
    )
    corp_income = get_data_judge(driver, '//*[@id="employTreatmentListDescText3190"]')
    corp_work_hours = get_data_judge(
        driver, '//*[@id="employTreatmentListDescText3270"]'
    )
    corp_URL = driver.current_url
    return [corp_name, corp_income, corp_work_hours, corp_URL]


def get_data_judge(driver, xpath):
    try:
        return driver.find_element_by_xpath(xpath).text
    except Exception:
        # 個別ページから取得している為passではなく空白を返す。
        return ""


if __name__ == "__main__":
    main()
