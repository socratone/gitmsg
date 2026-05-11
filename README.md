# gcm

`git add` 후 `gcm` 한 번으로 AI가 커밋 메시지를 작성하고 커밋까지 완료해주는 CLI 도구.

- OpenAI(`gpt-4.1-mini`)가 staged diff를 분석해 커밋 메시지 생성
- Conventional Commits 형식 (`feat`, `fix`, `refactor` 등)
- 모노레포 자동 감지 → `feat(web):`, `fix(api):` 형태로 scope 추가
- 커밋 메시지 한국어 작성
- Docker 기반 — 로컬에 Python 환경 불필요

## 요구사항

- [Docker](https://www.docker.com/get-started)
- OpenAI API 키

## 설치

```bash
git clone <this-repo>
cd gcm
./install.sh
source ~/.zshrc
```

`install.sh`가 하는 일:
1. Docker 설치 여부 확인
2. Docker 이미지(`gcm-tool`) 빌드
3. `~/.zshrc`에 `gcm` 함수 추가 (중복 추가 방지)
4. oh-my-zsh git 플러그인의 `gcm` alias 충돌 감지 시 경고 출력

> **oh-my-zsh 사용자 주의**: oh-my-zsh git 플러그인에 `gcm = git checkout main` alias가 기본 포함되어 있습니다. `install.sh`가 자동으로 `unalias gcm`을 삽입해 덮어씁니다.

## OpenAI API 키 설정

```bash
# ~/.zshrc에 추가
export OPENAI_API_KEY=sk-...
```

## 사용법

```bash
git add .
gcm
```

### 출력 예시

```
Commit message: feat(web): 로그인 페이지 컴포넌트 추가
[main 3f2a1b4] feat(web): 로그인 페이지 컴포넌트 추가
 2 files changed, 48 insertions(+)
```

### 커밋 메시지 형식

| 상황 | 예시 |
|------|------|
| 일반 레포 | `feat: 회원가입 기능 추가` |
| 모노레포 (단일 앱) | `fix(api): 토큰 만료 처리 수정` |
| 모노레포 (여러 앱) | `refactor(web): 공통 훅 분리` |

## 동작 원리

```
gcm
 └─ docker run -v $(pwd):/workspace gcm-tool   # diff 분석 + 메시지 생성
 └─ git commit -m "<생성된 메시지>"              # 호스트에서 커밋
```

Docker 컨테이너는 현재 디렉토리를 마운트해 `git diff --cached`를 읽고, OpenAI API 호출 후 커밋 메시지만 stdout에 출력. 실제 `git commit`은 호스트 shell 함수가 실행.

**첫 커밋 처리**: HEAD가 없는 레포(커밋이 한 번도 없는 경우)에서는 git의 빈 트리 해시(`4b825dc...`)를 기준으로 diff를 생성해 정상 동작합니다.

## 이미지 업데이트

`gcm.py` 수정 후에는 이미지를 재빌드해야 반영됩니다.

```bash
./install.sh
```
