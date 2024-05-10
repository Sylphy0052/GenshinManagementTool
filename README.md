# 原神素材管理ツール

## 機能

キャラをあるLv,天賦に育成するまでに必要な素材数の計算
武器をあるLvに育成するまでに必要な素材枢の計算
残り必要素材確認

## exe化

Windowsで実施。
gradio,sqlalchemy,pyinstallerをインストール。

1. `pyi-makespec --collect-data=gradio_client --collect-data=gradio app.py` で `app.spec` を作成
2. `app.spec` で `a=Analysis(...)` を編集

```bash
a = Analysis(
    ...
    module_collection_mode={
        'gradio': 'py',  # Collect gradio package as source .py files
    },
)
```

3. `pyinstaller app.spec` でexeファイル作成
