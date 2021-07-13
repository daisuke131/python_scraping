from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options


def main():
  options = Options()
  options.add_argument('--headless')

  driver = webdriver.Chrome("chromedriver", options=options)
  driver.get("https://job.mynavi.jp/2022/")

  # 検索ワード入力
  textbox = driver.find_element_by_xpath('//*[@id="srchWord"]')
  search_word = input("検索ワード>>")
  textbox.send_keys(search_word)

  # 検索ボタン押下
  search_button = driver.find_element_by_xpath('//*[@id="srchButton"]/span')
  search_button.click()

  search_count = 0

  while 1:
    # 会社名リスト追加
    corps_list = driver.find_elements_by_class_name('js-add-examination-list-text')
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

      get_corp_data(driver)

      # アクティブ画面(タブ)切り替え⇨元画面へ
      driver.switch_to.window(driver.window_handles[0])

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
      driver.find_element_by_link_text('次の100社').click()
      sleep(1)
    except Exception:
      break

  # 件数確認用
  print(search_count)
  # ブラウザ閉じる
  driver.quit()


def get_corp_data(driver):
  corp_name = driver.find_element_by_xpath('//*[@id="companyHead"]/div[1]/div/div/div[1]/h1').text
  corp_income = driver.find_element_by_xpath('//*[@id="employTreatmentListDescText3190"]').text
  corp_work_hours = driver.find_element_by_xpath('//*[@id="employTreatmentListDescText3270"]').text
  corp_URL = driver.current_url
  print(f"会社名:{corp_name}")
  print(f"基本給:{corp_income}")
  print(f"勤務時間:{corp_work_hours}")
  print(f"URL:{corp_URL}")


if __name__ == "__main__":
  main()
