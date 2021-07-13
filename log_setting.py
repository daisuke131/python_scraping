import logging
import logging.handlers
from pathlib import Path


def log_setting():
    dir = Path("./log")
    dir.mkdir(parents=True, exist_ok=True)
    log = logging.getLogger(__name__)
    # ログ出力レベルの設定
    log.setLevel(logging.DEBUG)

    # ローテーティングファイルハンドラを作成
    rh = logging.handlers.RotatingFileHandler(
        r"./log/app.log", encoding="utf-8", maxBytes=100
    )

    # ロガーに追加
    log.addHandler(rh)
    return log
