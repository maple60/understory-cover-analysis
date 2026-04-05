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

Windows:

```powershell
.venv\Scripts\activate
```

その後、以下のコマンドを実行します。

```bash
uv sync
```

無効化する際は、以下のコマンドを実行します。

```bash
deactivate
```

## 下層植生分類プログラムの実行

仮想環境を有効化した状態で、以下のコマンドを実行してください。

```bash
uv run python app/classify_quadrat_regions.py
```

アプリケーションが立ち上がります。
解析したい下層植生の撮影画像を選択し、分類を実行してください。

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

## アプリのビルドについて

[pyinstaller](https://pyinstaller.org/en/stable/)を使って、スタンドアロンのアプリケーションを作成できるようにしました。
手動で解析アプリをビルドする場合は、ターミナルから以下のコマンドを実行してください。

```bash
pyinstaller --onedir --windowed app/classify_quadrat_regions.py
```

また、`spec`ファイルからビルドすることもできます。

```bash
pyinstaller classify_quadrat_regions.spec
```
