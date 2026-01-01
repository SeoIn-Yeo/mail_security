# Git 히스토리에서 Credential 제거 가이드

## ⚠️ 중요: 이미 원격 저장소에 push된 경우

커밋 2edce2e에 포함된 credential을 Git 히스토리에서 완전히 제거하려면 다음 단계를 따르세요.

## 방법 1: git filter-branch 사용 (권장)

```bash
# docker-compose.yml 파일의 히스토리에서 credential 제거
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch docker-compose.yml" \
  --prune-empty --tag-name-filter cat -- --all

# 수정된 히스토리로 docker-compose.yml 복원 (현재 버전)
git checkout HEAD -- docker-compose.yml
git add docker-compose.yml
git commit -m "Fix: Remove credentials from docker-compose.yml, use .env file instead"

# 강제 푸시 (주의: 팀원들과 협의 필요!)
git push origin --force --all
git push origin --force --tags
```

## 방법 2: BFG Repo-Cleaner 사용 (더 빠름, 추천)

```bash
# BFG 설치 (Homebrew)
brew install bfg

# credential이 포함된 커밋의 파일 내용 치환
# docker-compose.yml에서 특정 문자열 제거
bfg --replace-text <(echo 'yeoseoin@naver.com==>REMOVED') 
bfg --replace-text <(echo '5KYNZ1HJJV8X==>REMOVED')

# Git 정리
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# 강제 푸시
git push origin --force --all
```

## 방법 3: 새 커밋으로 덮어쓰기 (가장 간단, 하지만 히스토리에 남음)

현재 작업한 내용을 커밋하고 push:

```bash
git add docker-compose.yml .env.example .gitignore
git commit -m "Security: Remove credentials from docker-compose.yml, use .env file instead"
git push
```

⚠️ 이 방법은 이전 커밋에 credential이 남아있지만, 현재 버전은 안전합니다.

## .env 파일 생성

`.env.example`을 복사하여 실제 `.env` 파일을 만드세요:

```bash
cp .env.example .env
```

그리고 `.env` 파일에 실제 credential을 입력하세요. (`.env`는 `.gitignore`에 이미 포함되어 있습니다)

## ⚠️ 추가 보안 조치

원격 저장소에 credential이 이미 노출되었다면:

1. **네이버 메일 앱 비밀번호 즉시 변경** (가장 중요!)
2. GitHub 저장소의 "Settings" → "Security" → "Secret scanning" 활성화
3. 해당 credential이 사용된 곳에서 모두 변경

