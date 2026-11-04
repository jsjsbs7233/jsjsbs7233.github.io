#!/usr/bin/env python3
"""빌드 결과(public/)의 링크·자산 경로를 점검한다. Python 3.9+, 외부 패키지 없음.

사용법 (저장소 최상위에서):
    py .github/pages_build.py --build
    py tools/check_site.py

점검 항목
- 내부 링크와 이미지·CSS·JS 경로가 public/ 안의 실제 파일을 가리키는지 (대소문자 포함)
- localhost, 127.0.0.1, file: 주소나 개인 PC 경로가 남아 있는지
- http:// 로 불러오는 자산(혼합 콘텐츠)이 있는지
- href가 비어 있거나 의미 없는 "#"인 링크가 있는지
- alt 속성이 없는 이미지가 있는지
"""
from __future__ import annotations

import sys
import urllib.parse
from html.parser import HTMLParser
from pathlib import Path

PUBLIC = Path(__file__).resolve().parent.parent / 'public'
LOCAL_MARKERS = ('localhost', '127.0.0.1', 'file:', 'C:\\', 'C:/', '/Users/')


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []      # (태그, 속성, 값)
        self.problems = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for name in ('href', 'src'):
            if name in attrs:
                self.refs.append((tag, name, attrs[name] or ''))
        if tag == 'img' and 'alt' not in attrs:
            self.problems.append(f'alt 없는 이미지: {attrs.get("src")}')
        if tag == 'a' and 'href' in attrs and (attrs['href'] or '').strip() in ('', '#'):
            self.problems.append(f'빈 링크: <a href="{attrs["href"]}">')


def target_exists(path: str) -> bool:
    rel = urllib.parse.unquote(path).lstrip('/')
    candidates = [rel, rel.rstrip('/') + '/index.html'] if rel else ['index.html']
    for candidate in candidates:
        file = PUBLIC / candidate
        # Windows는 대소문자를 구분하지 않으므로 실제 파일명과 한 글자씩 비교한다.
        if file.is_file() and file.resolve().as_posix().endswith(candidate):
            return True
    return False


def check_page(page: Path) -> list[str]:
    parser = PageParser()
    parser.feed(page.read_text(encoding='utf-8'))
    problems = list(parser.problems)
    base = '/' + page.relative_to(PUBLIC).as_posix()
    for tag, name, value in parser.refs:
        if any(marker in value for marker in LOCAL_MARKERS):
            problems.append(f'개인 PC/로컬 주소: {value}')
            continue
        parsed = urllib.parse.urlsplit(value)
        if parsed.scheme == 'http' and (tag != 'a'):
            problems.append(f'HTTP 자산(혼합 콘텐츠): {value}')
        if parsed.scheme in ('http', 'https', 'mailto', 'tel', 'data', 'javascript') or value.startswith(('//', '#')):
            continue
        path = urllib.parse.urlsplit(urllib.parse.urljoin(base, value)).path
        if not target_exists(path):
            problems.append(f'없는 파일을 가리킴: <{tag} {name}="{value}">')
    return problems


def main() -> int:
    if not (PUBLIC / 'index.html').is_file():
        print('public/index.html이 없습니다. 먼저 py .github/pages_build.py --build 를 실행하세요.')
        return 1
    pages = sorted(PUBLIC.rglob('*.html'))
    total = 0
    for page in pages:
        problems = check_page(page)
        for problem in problems:
            print(f'[{page.relative_to(PUBLIC).as_posix()}] {problem}')
        total += len(problems)
    print(f'점검한 HTML {len(pages)}개, 발견한 문제 {total}개')
    return 1 if total else 0


if __name__ == '__main__':
    sys.exit(main())
