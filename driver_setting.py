import os

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.utils import ChromeType


def set_driver(headless_flg):
    # 使用ブラウザの管理は.envで行う
    # firefox or chromium指定以外はchromeで起動
    browser_name = os.getenv("BROWSER")
    if "firefox" in browser_name:
        options = webdriver.FirefoxOptions()
    else:
        options = webdriver.ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg is True:
        options.add_argument("--headless")

    # 起動オプションの設定
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        + "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    )
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    options.add_argument("--incognito")

    if "firefox" in browser_name:
        return webdriver.Firefox(
            executable_path=GeckoDriverManager().install(), options=options
        )
    elif "chromium" in browser_name:
        return webdriver.Chrome(
            ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(),
            options=options,
        )
    else:
        return webdriver.Chrome(ChromeDriverManager().install(), options=options)
