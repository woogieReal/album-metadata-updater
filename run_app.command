#!/bin/bash

# 현재 스크립트가 위치한 디렉토리로 이동
cd -- "$(dirname "$0")"

# 가상환경 경로 설정
VENV_PATH="./.venv"

# 가상환경이 존재하는지 확인
if [ -d "$VENV_PATH" ]; then
    echo "가상환경을 활성화하는 중..."
    source "$VENV_PATH/bin/activate"
else
    echo "오류: 가상환경($VENV_PATH)을 찾을 수 없습니다."
    echo "의존성 설치가 완료되었는지 확인해주세요."
    read -p "종료하려면 엔터를 누르세요..."
    exit 1
fi

echo "앨범 메타데이터 업데이터를 시작합니다..."
python main.py
