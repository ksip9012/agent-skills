---
name: github-init
description: 新規プロジェクトの土台を初期化する。git init や gh repo create の直後、または「プロジェクトを始めたい」「ひな形を置いて」と頼まれたときに呼び出す。dotfiles のひな形（mise.toml・pre-commit・CI・.gitignore・ADR）を言語に合わせて置き、Issue・PR テンプレートとラベル、Dependabot をセットアップする。
user-invocable: true
allowed-tools: Bash, Read, Glob, Write
---

# プロジェクト初期化スキル

新しいプロジェクトに、`~/.dotfiles/templates/` のひな形と GitHub まわりの設定を置く。ひな形の中身と決めた理由は dotfiles にある（`~/.dotfiles/templates/README.md`、`~/.dotfiles/decisions/`）。このスキルはそれを読んで置くだけにし、ひな形の中身をここに書かない（dotfiles の ADR 0001）。

## 目標

- 終わったときに、`mise run check` が通る状態になっている（言語のひな形があるとき）
- 既にあるファイルは壊さない

## 手順

### 1. 言語と場所を判定する

- 言語: 今あるファイルや、ユーザーの話から判定する（`pyproject.toml` → Python、`go.mod` → Go など）。空のフォルダなら聞く
- ひな形があるか: `~/.dotfiles/templates/<言語>/` があるかを見る（`ls ~/.dotfiles/templates/`）
- 場所: カレントディレクトリのパスで判定する（dotfiles の ADR 0004）
  - `~/Documents/codes/personal-products/` → CI を置く
  - `~/Documents/codes/playground/` → CI を置くか聞く
  - `~/Documents/codes/work/` → 仕事の相手のルールに従うので、CI を置くか聞く
  - それ以外 → 聞く

判定した結果（言語・ひな形の有無・CI を置くか）をユーザーに確認してから次に進む。

### 2. ひな形を置く

`templates/common/` と `templates/<言語>/` を置く。

- 既にあるファイルは上書きしない。ぶつかるものがあれば、一覧を見せて、どうするか聞く
- `.gitignore` は、common と言語のものを足し合わせる。既にあれば、ない行だけ足す
- 名前の置き換え: `package-name`（`pyproject.toml` の name）と `package_name`（`src/` の下のフォルダと、テストの import）を、プロジェクトの名前にする。Python のパッケージ名はハイフンをアンダースコアにする
- CI を置かないときは、`.github/workflows/` と `.github/dependabot.yml` を置かない
- **言語のひな形がないとき**: `mise run check` のタスクがないので、CI と pre-commit を置かない。common の残り（`.gitignore`・`decisions/`）だけ置き、「言語のひな形がないので、`mise.toml` に `[tasks.check]` を書いてから CI と pre-commit を置く」と知らせる

### 3. GitHub まわりを置く

- Issue テンプレート: `~/.dotfiles/github/ISSUE_TEMPLATE/` を `.github/ISSUE_TEMPLATE/` にコピーする。`bug_report.md` の環境欄に、言語の版を書く行を足す（例: `- Python Version: [e.g. 3.13]`）
- PR テンプレート: `~/.dotfiles/github/pull_request_template.md` を `.github/` にコピーする
- ラベル: GitHub のデフォルトのラベルを消し、次を作る

```bash
gh label list --json name | jq -r '.[].name' | xargs -I {} gh label delete "{}" --yes
gh label create "feat"     --color "#0075ca" --description "新機能・機能追加"
gh label create "fix"      --color "#d73a4a" --description "バグ修正"
gh label create "docs"     --color "#0052cc" --description "ドキュメント"
gh label create "chore"    --color "#e4e669" --description "保守・依存関係更新などの雑務"
gh label create "refactor" --color "#a2eeef" --description "リファクタリング"
gh label create "ci"       --color "#f9d0c4" --description "CI/CD 関連"
gh label create "idea"     --color "#d876e3" --description "アイデア・提案"
gh label create "research" --color "#fbca04" --description "技術調査・検証"
```

- Dependabot: アラートと自動の修正 PR をオンにする（全リポジトリでオンにすると決めている）

```bash
gh api -X PUT "repos/{owner}/{repo}/vulnerability-alerts"
gh api -X PUT "repos/{owner}/{repo}/automated-security-fixes"
```

### 4. 動かして確かめる

言語のひな形を置いたときは、`~/.dotfiles/templates/README.md` の「使い方」のとおりに、`mise trust`、依存のインストール、`pre-commit install`、`mise run check` まで動かす。通らなければ、直してから報告する。

### 5. 完了報告

- 判定した言語・場所と、CI を置いたか
- 置いたファイルの一覧と、置かなかったもの（ぶつかったもの、言語のひな形がないもの）
- セットアップしたラベルと、Dependabot をオンにしたか
- `mise run check` の結果

## 注意事項

- ひな形はコピーする（シンボリックリンクにしない）。プロジェクトごとに直せるようにするため
- ひな形を直したくなったら、プロジェクトではなく `~/.dotfiles/templates/` を直す（dotfiles の Issue → PR）

## Gotchas

- GitHub のリポジトリがまだないときは、ラベルと Dependabot を飛ばしてファイルだけ置く。報告で「`gh repo create` のあとに、ラベルと Dependabot だけもう一度」と伝える
- `gh label delete` が失敗する場合（権限不足など）は飛ばして先に進む
- `pyproject.toml` は `readme = "README.md"` なので、README.md がないと uv が失敗する。なければ見出しだけの README.md を置く
