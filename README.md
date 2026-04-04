# understory-cover-analysis

下層植生の解析についてまとめます。

## Rの環境について

[renv](https://rstudio.github.io/renv/articles/renv.html)というパッケージを使うことで、プロジェクトごとのR環境を管理しています。
このリポジトリをクローンした場合は、以下のスクリプトを実行してください。

```r
renv::restore()
```

これで、プロジェクトに必要なパッケージがインストールされ、適切なバージョンが設定されます。

## Pythonの環境について

Pythonの解析は、仮想環境を作成して管理しています。
仮想環境やパッケージの管理には、[uv](https://docs.astral.sh/uv/)を使用しています。

```bash
uv venv
```

仮想環境の作成後、有効化します。

Mac/Linux: 

```bash
source .venv/bin/activate
```

無効化する際は、以下のコマンドを実行します。

```bash
deactivate
```

## Webページのビルドについて

ローカル確認:

```bash
quarto preview
```

本番ビルド:

```bash
quarto render
```

GitHub Pagesの機能を利用して公開しています。
