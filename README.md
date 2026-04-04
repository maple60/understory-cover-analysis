# understory-cover-analysis

下層植生の解析についてまとめます。

## Rの環境について

[renv](https://rstudio.github.io/renv/articles/renv.html)というパッケージを使うことで、プロジェクトごとのR環境を管理しています。
このリポジトリをクローンした場合は、以下のスクリプトを実行してください。

```r
renv::restore()
```

これで、プロジェクトに必要なパッケージがインストールされ、適切なバージョンが設定されます。

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
