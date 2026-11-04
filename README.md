# 김우현 개인 포트폴리오 사이트

정보보안을 공부하는 김우현의 개인 소개 웹사이트입니다. [Hugo](https://gohugo.io/)와 [Coder 테마](https://github.com/luizdepra/hugo-coder)로 만들고, GitHub Actions로 GitHub Pages에 자동 배포합니다.

- 공개 주소: https://jsjsbs7233.github.io/
- 저장소: https://github.com/jsjsbs7233/jsjsbs7233.github.io
- 배포 실행 기록: https://github.com/jsjsbs7233/jsjsbs7233.github.io/actions

## 폴더 구조

실제로 빌드되는 사이트는 `site/` 폴더입니다. 저장소 최상위의 `layouts/`, `assets/`, `exampleSite/` 등은 내려받은 원본 테마 ZIP을 그대로 보존한 것이며 빌드에는 쓰이지 않습니다.

```text
.
├── .github/
│   ├── workflows/hugo-pages.yml   # main push 시 빌드·배포하는 워크플로
│   └── pages_build.py             # 워크플로가 호출하는 빌드 스크립트(수업 제공)
├── .github-pages.json             # 빌드 설정(Hugo 버전, 설정 파일, 테마 이름)
├── site/                          # ← 실제 사이트
│   ├── hugo.toml                  # 사이트 설정(이름, 메뉴, 링크)
│   ├── pages.json                 # 배포용 baseURL 등 추가 설정(스크립트 생성)
│   ├── content/                   # 페이지 글(Markdown)
│   ├── layouts/                   # 테마 화면 일부를 덮어쓴 파일
│   ├── assets/css/                # 직접 작성한 CSS
│   ├── static/images/             # 아바타, 파비콘, 본문 이미지
│   ├── archetypes/                # 새 활동 페이지 양식
│   └── themes/template/           # Coder 테마(원본 보존)
├── tools/check_site.py            # 빌드 결과 링크·자산 점검 스크립트
├── prepare_github_pages.py        # 수업 제공 준비 스크립트
├── THEME_README.md                # 원본 테마의 README
└── LICENSE.md                     # 원본 테마 라이선스(MIT)
```

## 필요한 도구와 버전

| 도구 | 버전 | 용도 |
|---|---|---|
| Hugo **extended** | 배포: `0.167.0` (`.github-pages.json`에서 지정) / 로컬 확인: `0.169.0` | 사이트 빌드 |
| Python | 3.9 이상 (작성자는 3.13.7 사용) | 빌드 스크립트 실행 |
| Git | 2.x (작성자는 2.54.0 사용) | 버전 관리, push |
| 운영체제 | Windows 11 (작성 환경), GitHub Actions는 `ubuntu-latest` | |

### 설치 (Windows)

```powershell
winget install --id Hugo.Hugo.Extended -e
winget install --id Python.Python.3.13 -e
winget install --id Git.Git -e
```

설치 후 새 터미널을 열고 `hugo version`, `py --version`, `git --version`으로 확인합니다.
Windows에서는 `python` 대신 `py` 명령을 사용합니다.

## 로컬에서 확인하기

저장소를 내려받은 뒤 최상위 폴더에서 실행합니다.

```powershell
git clone https://github.com/jsjsbs7233/jsjsbs7233.github.io.git
cd jsjsbs7233.github.io
```

**미리보기 서버** (글을 고치면 브라우저가 자동으로 새로고침됨)

```powershell
cd site
hugo server --config hugo.toml,pages.json --theme template --themesDir themes
```

브라우저에서 http://localhost:1313/ 을 엽니다. 종료는 `Ctrl + C`입니다.

**배포와 같은 방식으로 빌드** (결과는 최상위 `public/` 폴더에 생김)

```powershell
py .github/pages_build.py --build
```

마지막 줄에 `빌드 완료`가 나오고 `public/index.html`이 생기면 성공입니다. `public/`은 `.gitignore`로 제외되어 커밋되지 않습니다.

**링크·자산 경로 점검** (빌드 후 실행)

```powershell
py tools/check_site.py
```

`public/`의 모든 HTML에서 없는 파일을 가리키는 링크·이미지, localhost·`file:` 주소, `http://` 자산, 빈 `#` 링크, alt 없는 이미지를 찾아 출력합니다. 마지막 줄이 `발견한 문제 0개`이면 통과입니다.

## 내용을 수정하려면

| 바꾸고 싶은 것 | 파일 |
|---|---|
| 이름, 홈 화면 소개 문구, 아바타 경로 | `site/hugo.toml`의 `[params]` (`author`, `info`, `avatarURL`) |
| 상단 메뉴 | `site/hugo.toml`의 `[[languages.ko.menu.main]]` |
| 홈 화면 GitHub 아이콘 링크 | `site/hugo.toml`의 `[[params.social]]` |
| 소개 페이지 | `site/content/about.md` |
| 활동 목록 안내 문구 | `site/content/projects/_index.md` |
| 활동 상세 페이지 | `site/content/projects/*.md` |
| 연락처 페이지 | `site/content/contact.md` |
| 이미지 | `site/static/images/` (글에서는 `/images/파일명`으로 참조) |
| 직접 추가한 스타일 | `site/assets/css/custom.css`, `site/assets/css/a11y.css` |
| 테마 화면을 바꾼 부분 | `site/layouts/` (테마의 같은 경로 파일을 덮어씀) |

**새 활동 페이지 추가**

```powershell
cd site
hugo new content projects/새-활동-이름.md --kind projects
```

생성된 파일의 `draft = true`를 `false`로 바꿔야 사이트에 표시됩니다.

## 배포하고 확인하기

1. 파일을 고친 뒤 커밋하고 main에 push합니다.
   ```powershell
   git add 고친파일
   git commit -m "변경 내용을 설명하는 메시지"
   git push
   ```
2. 저장소의 [Actions 탭](https://github.com/jsjsbs7233/jsjsbs7233.github.io/actions)에서 **Deploy Hugo to GitHub Pages** 실행이 자동으로 시작되는지 확인합니다. `build`와 `deploy` 두 단계가 모두 초록색(✅)이면 배포 완료입니다(보통 1~3분).
3. https://jsjsbs7233.github.io/ 를 열고 `Ctrl + Shift + R`(캐시 무시 새로고침)로 변경 내용이 반영됐는지 확인합니다.

**실패했을 때**

- Actions의 빨간 단계를 열어 오류 메시지를 확인하고, 위의 로컬 빌드 명령으로 같은 오류가 나는지 확인합니다.
- 처음 설정할 때는 저장소 **Settings → Pages → Build and deployment → Source**가 **GitHub Actions**로 되어 있어야 합니다.

## 출처와 이용 조건

| 자료 | 사용 위치 | 출처 | 이용 조건 |
|---|---|---|---|
| Coder 테마 | `site/themes/template/`, 저장소 최상위 원본 파일 | https://github.com/luizdepra/hugo-coder | MIT License (`LICENSE.md` 유지, 사이트 푸터에 고지) |
| Font Awesome Free 아이콘·글꼴 | 테마에 포함(`site/themes/template/static/fonts/`) | https://fontawesome.com | 아이콘 CC BY 4.0, 글꼴 SIL OFL 1.1 (`LICENSE.txt` 유지) |
| Hugo | 사이트 빌드 도구 | https://gohugo.io | Apache License 2.0 |
| 준비 스크립트 `prepare_github_pages.py`, `.github/pages_build.py`, 워크플로 | 배포 구성 | 수업 제공 | 수업 과제용 |
| 해커톤 시연 화면 `site/static/images/projects/golden-time-map.jpg` | 해커톤 활동 페이지 | 직접 캡처(팀 프로젝트 화면), 아래쪽 일부를 잘라냄 | 직접 제작 |

## 직접 제작과 AI 활용 구분

이 사이트는 AI 코딩 도구(Claude Code)의 도움을 받아 만들었습니다. 모든 결과는 직접 확인한 뒤 커밋했습니다.

| 구분 | 대상 |
|---|---|
| **본인 제공 정보 + AI가 문장 정리** (본인이 사실 확인·수정) | `site/content/about.md`, `site/content/projects/golden-time.md`, `site/content/projects/portfolio-site.md`, `site/content/contact.md` |
| **AI 생성** (본인이 화면에서 동작 확인) | `site/static/images/avatar.svg`, 파비콘(`favicon.svg`, `favicon-*.png`, `apple-touch-icon.png`), `site/assets/css/*.css`, `site/layouts/` 아래 재정의 파일, `site/static/site.webmanifest`, `site/static/images/safari-pinned-tab.svg`, `tools/check_site.py`, 이 README 초안 |
| **직접 제작** | 해커톤 시연 화면 캡처, 해커톤 프로젝트 자체(팀 작업), 모든 커밋과 배포·검증 작업 |
| **외부 자료** | Coder 테마, Font Awesome, 수업 제공 스크립트 (위 표 참고) |
