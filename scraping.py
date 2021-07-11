from selenium import webdriver
from time import sleep


def main():
  driver = webdriver.Chrome("chromedriver")
  driver.get("https://job.mynavi.jp/2022/")
  sleep(3)

  # 検索ワード入力
  textbox = driver.find_element_by_xpath('//*[@id="srchWord"]')
  textbox.send_keys("高収入")

  # 検索ボタン押下
  search_button = driver.find_element_by_xpath('//*[@id="srchButton"]/span')
  search_button.click()
  # sleep(3)

  # 会社名リスト追加
  corps_list = driver.find_elements_by_class_name('js-add-examination-list-text')

  for corp in corps_list:
    # 画面下部までスクロール(これがないと画面に写ってないリンクが使えない。)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    corp.click()
    # sleep(3)

    # アクティブ画面(タブ)切り替え
    driver.switch_to.window(driver.window_handles[-1])
    # sleep(3)

    # タブを切り替えないと情報が見れないのでリンクまでスクロール
    element = driver.find_element_by_xpath('//*[@id="headerEmploymentTabLink"]')
    # 指定した要素までスクロール
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    # タブリンククリック
    element.click()
    # sleep(3)

    get_corp_data(driver)

    # アクティブ画面(タブ)切り替え⇨元画面へ
    driver.switch_to.window(driver.window_handles[0])
    # sleep(3)

  driver.quit()


def get_corp_data(driver):
  corp_name = driver.find_element_by_xpath('//*[@id="companyHead"]/div[1]/div/div/div[1]/h1').text
  corp_income = driver.find_element_by_xpath('//*[@id="employTreatmentListDescText3190"]').text
  corp_work_hours = driver.find_element_by_xpath('//*[@id="employTreatmentListDescText3270"]').text
  print(f"会社名:{corp_name}")
  print(f"基本給:{corp_income}")
  print(f"勤務時間:{corp_work_hours}")


if __name__ == "__main__":
  main()
