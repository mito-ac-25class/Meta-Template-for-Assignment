#!/bin/bash

# /release.admin の削除手順を自動化するスクリプト
# このスクリプトは、課題リポジトリをリリース可能な状態にするため、
# 不要なファイルを削除し、必要なファイルを整理します。

set -e  # エラーが発生したら即座に終了

# カラー出力用
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# リポジトリのルートディレクトリに移動
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

echo -e "${GREEN}リポジトリをリリース可能な状態にします...${NC}"

# 1. 作業用ブランチの作成
echo -e "\n${YELLOW}[1/8] 作業用ブランチを作成中...${NC}"
BRANCH_NAME="feature/remove-admin-prompts"

# 既に同名のブランチが存在する場合の処理
if git show-ref --quiet refs/heads/${BRANCH_NAME}; then
    echo -e "${YELLOW}警告: ブランチ '${BRANCH_NAME}' は既に存在します。${NC}"
    echo -e "${YELLOW}既存のブランチに切り替えます...${NC}"
    git checkout ${BRANCH_NAME}
else
    git checkout -b ${BRANCH_NAME}
    echo -e "${GREEN}ブランチ '${BRANCH_NAME}' を作成しました。${NC}"
fi

# 2. 管理者用プロンプトファイルの削除
echo -e "\n${YELLOW}[2/8] 管理者用プロンプトファイルを削除中...${NC}"
if ls .github/prompts/*.admin.prompt.md 1> /dev/null 2>&1; then
    git rm .github/prompts/*.admin.prompt.md
    echo -e "${GREEN}管理者用プロンプトファイルを削除しました。${NC}"
else
    echo -e "${YELLOW}管理者用プロンプトファイルが見つかりません。スキップします。${NC}"
fi

# 3. agent-input ディレクトリの削除
echo -e "\n${YELLOW}[3/8] agent-input ディレクトリを削除中...${NC}"
if [ -d "agent-input" ]; then
    git rm -r agent-input
    echo -e "${GREEN}agent-input ディレクトリを削除しました。${NC}"
else
    echo -e "${YELLOW}agent-input ディレクトリが見つかりません。スキップします。${NC}"
fi

# 4. agent-output ディレクトリの削除
echo -e "\n${YELLOW}[4/8] agent-output ディレクトリを削除中...${NC}"
if [ -d "agent-output" ]; then
    git rm -r agent-output
    echo -e "${GREEN}agent-output ディレクトリを削除しました。${NC}"
else
    echo -e "${YELLOW}agent-output ディレクトリが見つかりません。スキップします。${NC}"
fi

# 5. templates ディレクトリの削除
echo -e "\n${YELLOW}[5/8] templates ディレクトリを削除中...${NC}"
if [ -d "templates" ]; then
    git rm -r templates
    echo -e "${GREEN}templates ディレクトリを削除しました。${NC}"
else
    echo -e "${YELLOW}templates ディレクトリが見つかりません。スキップします。${NC}"
fi

# 6. 開発用 AGENTS.md と README.md の削除
echo -e "\n${YELLOW}[6/8] 開発用 AGENTS.md と README.md を削除中...${NC}"
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
echo -e "\n${YELLOW}[7/8] 空の TUTORIAL.md を確認中...${NC}"
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

# 8. リリース用ファイルの移動
echo -e "\n${YELLOW}[8/8] リリース用ファイルを移動中...${NC}"

# release/evac.AGENTS.md → AGENTS.md
if [ -f "release/evac.AGENTS.md" ]; then
    git mv release/evac.AGENTS.md AGENTS.md
    echo -e "${GREEN}release/evac.AGENTS.md を AGENTS.md に移動しました。${NC}"
else
    echo -e "${RED}エラー: release/evac.AGENTS.md が見つかりません。${NC}"
    exit 1
fi

# release/README.md → README.md
if [ -f "release/README.md" ]; then
    git mv release/README.md README.md
    echo -e "${GREEN}release/README.md を README.md に移動しました。${NC}"
else
    echo -e "${RED}エラー: release/README.md が見つかりません。${NC}"
    exit 1
fi

# 9. 変更をコミット
echo -e "\n${YELLOW}変更をコミット中...${NC}"
git commit -m "fix: remove admin prompt files"
echo -e "${GREEN}変更をコミットしました。${NC}"

# 10. リモートリポジトリにプッシュ
echo -e "\n${YELLOW}リモートリポジトリにプッシュ中...${NC}"
git push origin ${BRANCH_NAME}
echo -e "${GREEN}リモートリポジトリにプッシュしました。${NC}"

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}リリース準備が完了しました！${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "次のステップ:"
echo -e "1. GitHub上でプルリクエストを作成してください"
echo -e "2. レビュー後、main ブランチにマージしてください"
