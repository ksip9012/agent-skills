# agent-skills

Claude Code 用の自作 skill 集です。GitHub Flow で開発するときの、ブランチ・Issue・PR の作業と、新しいプロジェクトの初期化を skill にしています。

自分の運用に合わせて書いているので、担当者（`ksip9012`）やひな形の場所（dotfiles の `templates/`）は、使うときに読み替えてください。

## 入っている skill

| skill | 内容 |
| --- | --- |
| [`github-branch`](./github-branch/SKILL.md) | Issue 番号からブランチ名を作り、main を最新にしてからブランチを切る |
| [`github-issue-create`](./github-issue-create/SKILL.md) | テンプレートに沿って Issue を作る |
| [`github-issue-comment`](./github-issue-comment/SKILL.md) | push のあと、作業が途中の Issue に進み具合をコメントする |
| [`github-pr`](./github-pr/SKILL.md) | 作業が終わったら PR を作り、関連する Issue を閉じる形にする |
| [`github-init`](./github-init/SKILL.md) | 新しいプロジェクトに、言語に合わせたひな形・テンプレート・ラベル・Dependabot を置く |

## 使い方

クローンして、`~/.claude/skills` からリンクします。

```zsh
git clone https://github.com/ksip9012/agent-skills.git ~/.claude-skills
ln -s ~/.claude-skills ~/.claude/skills
```

Claude Code で `/github-pr` のように呼び出すか、「PR を作って」のように頼むと動きます。

## skill の置き場所の方針

skill は性質によって置き場所を使い分けています。

- **このリポジトリ（`~/.claude/skills`）**: どのプロジェクトでも同じロジックで動く、プロジェクトに依存しない skill
- **各リポジトリの `.claude/skills/`**: そのプロジェクトのファイル構造やルールに結びついた skill。claude.ai/code のクラウドセッションはそのリポジトリしかクローンしないので、クラウドで使う skill もここに置く

Claude Code 以外のツールは、それぞれ別の場所から skill を探します。同じロジックを複数のツールで使いたいときは、実体を複製せず、薄いラッパーからルールの実体を参照する形にします。

## skill を作るときの参考

新しい skill を作る・直すときは [`SKILL_DESIGN_GUIDE.md`](./SKILL_DESIGN_GUIDE.md) のチェックリストを参照します。

## License

[MIT](./LICENSE)
