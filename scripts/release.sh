#!/bin/bash

# /release.admin の削除手順を自動化するスクリプト
# このスクリプトは、課題リポジトリをリリース可能な状態にするため、
# 不要なファイルを削除し、必要なファイルを整理します。

set -e  # エラーが発生したら即座に終了

# カラー出力用
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# リポジトリのルートディレクトリに移動
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}リリース準備スクリプト${NC}"
echo -e "${GREEN}========================================${NC}"

# バックアップの推奨
echo -e "\n${BLUE}【重要】実行前の確認事項${NC}"
echo -e "このスクリプトは多数のファイルを削除・移動します。"
echo -e "実行前に以下を確認してください："
echo -e "  1. すべての変更がコミット済みであること"
echo -e "  2. 必要に応じてバックアップを取得していること"
echo -e "  3. release/evac.AGENTS.md と release/README.md が存在すること"
echo -e ""
read -p "続行しますか？ (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}スクリプトを中止しました。${NC}"
    exit 0
fi

echo -e "\n${GREEN}リポジトリをリリース可能な状態にします...${NC}"

# 事前チェック: 必須ファイルの存在確認
echo -e "\n${YELLOW}[事前チェック] 必須ファイルの確認中...${NC}"
MISSING_FILES=0

if [ ! -f "release/evac.AGENTS.md" ]; then
    echo -e "${RED}エラー: release/evac.AGENTS.md が見つかりません。${NC}"
    MISSING_FILES=1
fi

if [ ! -f "release/README.md" ]; then
    echo -e "${RED}エラー: release/README.md が見つかりません。${NC}"
    MISSING_FILES=1
fi

if [ $MISSING_FILES -eq 1 ]; then
    echo -e "${RED}必須ファイルが不足しています。スクリプトを中止します。${NC}"
    exit 1
fi

echo -e "${GREEN}必須ファイルの確認が完了しました。${NC}"

# 作業ツリーの状態確認
GIT_STATUS=$(git status --porcelain)
if [ -n "$GIT_STATUS" ]; then
    echo -e "${YELLOW}警告: 未コミットの変更があります。${NC}"
    echo "$GIT_STATUS" | head -10
    echo -e ""
    read -p "未コミットの変更がありますが続行しますか？ (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}スクリプトを中止しました。変更をコミットしてから再実行してください。${NC}"
        exit 0
    fi
fi

# 1. 作業用ブランチの作成
echo -e "\n${YELLOW}[1/9] 作業用ブランチを作成中...${NC}"
BRANCH_NAME="feature/remove-admin-prompts"

# 既に同名のブランチが存在する場合の処理
if git show-ref --quiet refs/heads/${BRANCH_NAME}; then
    echo -e "${YELLOW}警告: ブランチ '${BRANCH_NAME}' は既に存在します。${NC}"
    echo -e "選択肢:"
    echo -e "  1) 既存のブランチを削除して新規作成（推奨）"
    echo -e "  2) 既存のブランチに切り替えて続行"
    echo -e "  3) スクリプトを中止"
    read -p "選択してください (1-3): " -n 1 -r
    echo
    case $REPLY in
        1)
            echo -e "${YELLOW}既存のブランチを削除します...${NC}"
            CURRENT_BRANCH=$(git branch --show-current)
            if [ "$CURRENT_BRANCH" = "$BRANCH_NAME" ]; then
                git checkout main || git checkout master
            fi
            git branch -D ${BRANCH_NAME}
            git checkout -b ${BRANCH_NAME}
            echo -e "${GREEN}ブランチ '${BRANCH_NAME}' を新規作成しました。${NC}"
            ;;
        2)
            echo -e "${YELLOW}既存のブランチに切り替えます...${NC}"
            git checkout ${BRANCH_NAME}
            echo -e "${GREEN}ブランチ '${BRANCH_NAME}' に切り替えました。${NC}"
            ;;
        3)
            echo -e "${YELLOW}スクリプトを中止しました。${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}無効な選択です。スクリプトを中止します。${NC}"
            exit 1
            ;;
    esac
else
    git checkout -b ${BRANCH_NAME}
    echo -e "${GREEN}ブランチ '${BRANCH_NAME}' を作成しました。${NC}"
fi

# 2. 管理者用プロンプトファイルの削除
echo -e "\n${YELLOW}[2/9] 管理者用プロンプトファイルを削除中...${NC}"
if ls .github/prompts/*.admin.prompt.md 1> /dev/null 2>&1; then
    git rm .github/prompts/*.admin.prompt.md
    echo -e "${GREEN}管理者用プロンプトファイルを削除しました。${NC}"
else
    echo -e "${YELLOW}管理者用プロンプトファイルが見つかりません。スキップします。${NC}"
fi

# 3. agent-input ディレクトリの削除
echo -e "\n${YELLOW}[3/9] agent-input ディレクトリを削除中...${NC}"
if [ -d "agent-input" ]; then
    git rm -r agent-input
    echo -e "${GREEN}agent-input ディレクトリを削除しました。${NC}"
else
    echo -e "${YELLOW}agent-input ディレクトリが見つかりません。スキップします。${NC}"
fi

# 4. agent-output ディレクトリの削除
echo -e "\n${YELLOW}[4/9] agent-output ディレクトリを削除中...${NC}"
if [ -d "agent-output" ]; then
    git rm -r agent-output
    echo -e "${GREEN}agent-output ディレクトリを削除しました。${NC}"
else
    echo -e "${YELLOW}agent-output ディレクトリが見つかりません。スキップします。${NC}"
fi

# 5. templates ディレクトリの削除
echo -e "\n${YELLOW}[5/9] templates ディレクトリを削除中...${NC}"
if [ -d "templates" ]; then
    git rm -r templates
    echo -e "${GREEN}templates ディレクトリを削除しました。${NC}"
else
    echo -e "${YELLOW}templates ディレクトリが見つかりません。スキップします。${NC}"
fi

# 6. 開発用 AGENTS.md と README.md の削除
echo -e "\n${YELLOW}[6/9] 開発用 AGENTS.md と README.md を削除中...${NC}"
if [ -f "AGENTS.md" ]; then
    git rm AGENTS.md
    echo -e "${GREEN}AGENTS.md を削除しました。${NC}"
else
    echo -e "${YELLOW}AGENTS.md が見つかりません。スキップします。${NC}"
fi

if [ -f "README.md" ]; then
    git rm README.md
    echo -e "${GREEN}README.md を削除しました。${NC}"
else
    echo -e "${YELLOW}README.md が見つかりません。スキップします。${NC}"
fi

# 7. 空の TUTORIAL.md の削除（存在し、かつ空の場合のみ）
echo -e "\n${YELLOW}[7/9] 空の TUTORIAL.md を確認中...${NC}"
if [ -f "TUTORIAL.md" ]; then
    # ファイルサイズが0バイト、または空白文字のみの場合は削除
    if [ ! -s "TUTORIAL.md" ] || ! grep -q '[^[:space:]]' TUTORIAL.md; then
        git rm TUTORIAL.md
        echo -e "${GREEN}空の TUTORIAL.md を削除しました。${NC}"
    else
        echo -e "${GREEN}TUTORIAL.md にコンテンツがあるため、保持します。${NC}"
    fi
else
    echo -e "${YELLOW}TUTORIAL.md が見つかりません。スキップします。${NC}"
fi

# 8. tests/infrastructure ディレクトリの削除
echo -e "\n${YELLOW}[8/9] tests/infrastructure ディレクトリを削除中...${NC}"
if [ -d "tests/infrastructure" ]; then
    git rm -r tests/infrastructure
    echo -e "${GREEN}tests/infrastructure ディレクトリを削除しました。${NC}"
else
    echo -e "${YELLOW}tests/infrastructure ディレクトリが見つかりません。スキップします。${NC}"
fi

# 9. リリース用ファイルの移動
echo -e "\n${YELLOW}[9/9] リリース用ファイルを移動中...${NC}"

# release/student.AGENTS.md → AGENTS.md
if [ -f "release/student.AGENTS.md" ]; then
    git mv release/student.AGENTS.md AGENTS.md
    echo -e "${GREEN}release/student.AGENTS.md を AGENTS.md に移動しました。${NC}"
else
    echo -e "${RED}エラー: release/student.AGENTS.md が見つかりません。${NC}"
    echo -e "${RED}リリース準備を中止します。${NC}"
    echo -e "${YELLOW}ロールバック方法：${NC}"
    echo -e "  git reset --hard"
    echo -e "  git clean -fd"
    exit 1
fi

# release/README.md → README.md
if [ -f "release/README.md" ]; then
    git mv release/README.md README.md
    echo -e "${GREEN}release/README.md を README.md に移動しました。${NC}"
else
    echo -e "${RED}エラー: release/README.md が見つかりません。${NC}"
    echo -e "${RED}リリース準備を中止します。${NC}"
    echo -e "${YELLOW}ロールバック方法：${NC}"
    echo -e "  git reset --hard"
    echo -e "  git clean -fd"
    exit 1
fi

# 10. 変更をコミット
echo -e "\n${YELLOW}変更をコミット中...${NC}"
# Note: At this point, git rm and git mv operations have already staged changes,
# so we can proceed directly to commit
git commit -m "fix: remove admin prompt files"
echo -e "${GREEN}変更をコミットしました。${NC}"

# 11. リモートリポジトリにプッシュ
echo -e "\n${YELLOW}リモートリポジトリにプッシュ中...${NC}"
if git push origin ${BRANCH_NAME}; then
    echo -e "${GREEN}リモートリポジトリにプッシュしました。${NC}"
else
    echo -e "${RED}エラー: プッシュに失敗しました。${NC}"
    echo -e "${YELLOW}以下のコマンドでロールバックできます：${NC}"
    echo -e "  git reset --hard HEAD~1"
    echo -e "  git checkout main"
    echo -e "  git branch -D ${BRANCH_NAME}"
    exit 1
fi

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}リリース準備が完了しました！${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "次のステップ:"
echo -e "1. GitHub上でプルリクエストを作成してください"
echo -e "2. レビュー後、main ブランチにマージしてください"
echo -e ""
echo -e "${BLUE}【トラブルシューティング】${NC}"
echo -e "問題が発生した場合は以下のコマンドでロールバックできます："
echo -e "  ${YELLOW}git checkout main${NC}"
echo -e "  ${YELLOW}git branch -D ${BRANCH_NAME}${NC}"
echo -e "  ${YELLOW}git push origin --delete ${BRANCH_NAME}${NC}  # リモートブランチも削除する場合"
