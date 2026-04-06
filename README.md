# 下層植生の分類・解析について

下層植生の解析についてまとめます。

## リンク

* 解説Webページ: [https://maple60.github.io/understory-cover-analysis/](https://maple60.github.io/understory-cover-analysis/)
* 解析用スタンドアロンアプリ: [Releaseページ](https://github.com/maple60/understory-cover-analysis/releases)

## Pythonの環境について

解析には主に[Python](https://www.python.org/)を使用しています。
解析環境は、[uv](https://docs.astral.sh/uv/)を使用して、仮想環境を作成して管理しています。

もしuvをインストールされていない場合は、[Installation](https://docs.astral.sh/uv/#highlights:~:text=of%20Ruff.-,Installation,-Install%20uv%20with)を参照してインストールしてください。

インストール後、以下のコマンドを実行して仮想環境を作成します。

```bash
uv venv
```

仮想環境の作成後、有効化します。
OSによってコマンドが異なります。

* Mac/Linux: 

```bash
source .venv/bin/activate
```

* Windows:

```powershell
.venv\Scripts\activate
```

その後、以下のコマンドを実行すると、必要なライブラリがインストールされます。

```bash
uv sync
```

なお、無効化する際は、以下のコマンドを実行します。

```bash
deactivate
```

## 下層植生分類プログラムの実行

下層植生を分類するプログラムを作成しました。
仮想環境を有効化した状態で、以下のコマンドを実行してください。

```bash
uv run python app/classify_quadrat_regions.py
```

アプリケーションが立ち上がります。
解析したい下層植生の撮影画像を選択し、分類を実行してください。

## その他開発者向け情報

### Webページのビルドについて

Webページは[Quarto](https://quarto.org/)を使って作成しています。
以下のコマンドを使用してプレビューや公開用のレンダリングを行うことができます。
コマンドはルートディレクトリから実行します。

ローカル確認:

```bash
quarto preview
```

公開用のレンダリング:

```bash
quarto render
```

レンダリングが終了すると、`docs`フォルダにHTMLファイルが生成されます。
これがWebページに公開されます。

`docs`フォルダに生成されたファイルをcommit後、pushをすることでGitHub上で公開されます。
公開には、[GitHub Pages](https://docs.github.com/en/pages)の機能を利用しています。

公開されたWebページは、以下のURLから閲覧できます。

* [https://maple60.github.io/understory-cover-analysis/](https://maple60.github.io/understory-cover-analysis/)

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
