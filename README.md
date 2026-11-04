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
├── prepare_github_pages.py        # 수업 제공 준비 스크립트
├── THEME_README.md                # 원본 테마의 README
└── LICENSE.md                     # 원본 테마 라이선스(MIT)
```
