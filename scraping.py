from selenium import webdriver
import time


def main():
  driver = webdriver.Chrome()
  driver.get("https://job.mynavi.jp/2022/")
  time.sleep(3)

  # 検索ワード入力
  textbox = driver.find_element_by_xpath('//*[@id="srchWord"]')
  textbox.send_keys("高収入")

  # 検索ボタン押下
  search_button = driver.find_element_by_xpath('//*[@id="srchButton"]/span')
  search_button.click()
  time.sleep(3)

  # 会社名リスト追加
  corps_list = driver.find_elements_by_class_name('js-add-examination-list-text')

  for corp in corps_list:
    print(corp.text)

  # ブラウザ閉じる
  time.sleep(5)
  driver.quit()


if __name__ == "__main__":
  main()
