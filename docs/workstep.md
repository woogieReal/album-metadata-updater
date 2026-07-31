# 앨범 메타데이터 자동 갱신 TUI 앱 — 단계별 작업 항목

---

## Phase 1. 프로젝트 초기 설정

- [X] Python 가상환경 생성 및 활성화
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```
- [X] `requirements.txt` 파일 생성 (아래 내용 작성)
  ```
  textual
  mutagen
  ```
- [X] 의존성 설치
  ```bash
  pip install -r requirements.txt
  ```
- [X] 프로젝트 디렉터리 구조 생성
  - `main.py` (진입점)
  - `app.py` (AlbumTagApp)
  - `screens/explorer.py` (ExplorerScreen)
  - `screens/metadata.py` (MetadataScreen)
  - `services/metadata_service.py` (MetadataService)
- [X] `.gitignore`에 `.venv/` 추가

---

## Phase 2. MetadataService 구현

- [X] `mutagen`을 이용한 ID3 태그 읽기 메서드 구현 (`TALB`, `TPE1`, `TDRC`, `TIT2`, `TRCK`)
- [X] 파일명 정제(트랙명 추출) 로직 구현
  - 정규표현식 `r'^\s*(\d+|\[\d+\])[\s._\-)]*'` 기반으로 앞부분 트랙번호 패턴 제거
  - `.mp3` 확장자 제거 후 정제된 트랙명 반환
- [X] 트랙번호 부여 로직 구현
  - 파일명 기준 오름차순 정렬 후 `1, 2, 3 ...` 순번 반환
- [X] ID3 태그 일괄 쓰기 메서드 구현 (`TALB`, `TPE1`, `TDRC`, `TIT2`, `TRCK`)
  - 성공/실패 결과 반환 처리 포함

---

## Phase 3. AlbumTagApp (메인 앱 클래스) 구현

- [X] `textual.app.App` 기반 `AlbumTagApp` 클래스 작성
- [X] 앱 전역 상태 관리 속성 정의
  - 선택된 폴더 경로
  - 체크된 MP3 파일 목록
- [X] 초기 화면을 `ExplorerScreen`으로 설정

---

## Phase 4. ExplorerScreen 구현

### 4-1. 상태 1: 디렉터리 탐색 모드 (최초 실행)

- [X] `DirectoryTree` 위젯으로 전체 파일시스템 탐색 가능하도록 구성
- [X] 하단에 `현재 폴더 사용하기` 버튼 배치
- [X] `DirectoryTree`에서 디렉터리 선택 시 현재 선택 경로 상태 갱신

### 4-2. 상태 2: 대상 폴더 선택 후 (사용 버튼 클릭 시)

- [X] 선택된 폴더 하위에서 `.mp3` 파일만 필터링하여 목록 추출
- [X] 최상단 `전체 선택/해제` 체크박스 구현 (토글 시 하위 전체 연동)
- [X] 추출된 MP3 파일명 목록 및 개별 체크박스 렌더링 (기본값: 모두 선택)
- [X] `현재 폴더 사용하기` 버튼을 `설정할 메타데이터 고르기` 버튼으로 교체

### 4-3. MetadataScreen 전환 (설정 버튼 클릭 시)

- [X] 체크된 MP3 파일 목록을 수집하여 `MetadataScreen`으로 전달
- [X] `app.push_screen(MetadataScreen(...))` 방식으로 화면 전환

---

## Phase 5. MetadataScreen 구현

### 5-1. 레이아웃 및 공통 컨트롤

- [X] 우상단 `닫기` 버튼 구현 (클릭 시 `app.pop_screen()`으로 탐색 화면 복귀)
- [X] 하단 `메타데이터 수정하기` 버튼 배치

### 5-2. 메타데이터 설정 목록 영역

- [X] 최상단 `전체 항목 선택/해제` 체크박스 구현 (기본값: 모두 선택)
- [X] `앨범명` 입력 필드 + 체크박스
  - 전달받은 MP3의 `TALB` 태그 1차 읽기, 없으면 현재 폴더명으로 자동 매핑
- [X] `아티스트` 입력 필드 + 체크박스
  - 전달받은 MP3의 `TPE1` 태그 1차 읽기, 없으면 빈칸
- [X] `연도` 입력 필드 + 체크박스
  - 전달받은 MP3의 `TDRC` 태그 1차 읽기, 없으면 빈칸
- [X] `트랙명` 항목 + 체크박스 (입력창 없음, 자동 정제 적용 예정 안내 표기)
- [X] `트랙번호` 항목 + 체크박스 (입력창 없음, 파일명 오름차순 순번 적용 예정 안내 표기)

---

## Phase 6. 메타데이터 적용 및 결과 처리

- [X] 수정 버튼 클릭 시 체크된 항목만 선별하여 `MetadataService` 호출
  - 체크된 필드(`앨범명`, `아티스트`, `연도`, `트랙명`, `트랙번호`)만 ID3 태그에 반영
- [X] 성공 시: 성공 알림 메시지(Toast/Modal) 표시 후 탐색 화면으로 자동 복귀
- [X] 실패 시: 실패 알림 메시지 표시 후 메타 화면 상태 유지

---

## Phase 7. 통합 테스트 및 마무리

- [X] 전체 플로우 통합 수동 테스트 (디렉터리 탐색 → 파일 선택 → 메타데이터 설정 → 수정)
- [X] 엣지 케이스 처리
  - 선택 폴더에 MP3 파일이 없는 경우 안내 처리
  - 체크된 파일이 없는 상태에서 설정 버튼 클릭 방지
  - 체크된 항목이 없는 상태에서 수정 버튼 클릭 방지
- [X] UI 스타일 및 레이아웃 최종 정리
