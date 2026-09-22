# skillsの置き場所方針

skillは性質によって置き場所を使い分ける。個々のskill名の一覧は各`SKILL.md`のfrontmatter（name/description）で確認できるため、ここでは「どこに何を置くか」の方針のみを記す（個別skillの一覧は陳腐化しやすいためここには書かない）。

## 方針

- **グローバル（このリポジトリ, `~/.claude-skills/` = `~/.claude/skills`へのシンボリックリンク）**: どのプロジェクトでも同じロジックで動く、プロジェクト非依存のskill。例: `github-pr` `github-init` `github-issue-create` `github-branch` `github-issue-comment`
- **プロジェクトローカル（各リポジトリ内の`.claude/skills/`）**: そのプロジェクト固有のファイル構造・ルールに密結合したskill。特に、claude.ai/codeのクラウドセッションから使う必要があるskillは、クラウドセッションが対象リポジトリしかクローンしないため、必ずここに置く（グローバルに置くとクラウドセッションから見えなくなる）。例: `life`リポジトリの`inbox-triage`（`gtd/001_inbox.md`等、そのVault固有の構造に依存し、会社PC/携帯からのInbox整理に使うためプロジェクトローカルに置いている）

## 設計時の参考

新しいskillを作成・改修する際は `SKILL_DESIGN_GUIDE.md` のチェックリストを参照する。

## 他ツールとの関係

Claude Code以外のツール（Gemini CLI: `.gemini/skills/`、Termy: `.agents/skills/` 等）は、ツールごとに独自のskill発見場所を持つ。これらは統一できないため、同じロジックを複数ツールで使いたい場合は、実体を複製せず薄いラッパーからルールの実体（例: 各リポジトリの`005_rules/`等）を参照する形にする。

## 既知の課題

- `life`リポジトリの`.gemini/skills/skill-gtd-inbox/`が独自にルールを複製しており、パスの記述が古くなっている（未修正、2026-09-20時点）
