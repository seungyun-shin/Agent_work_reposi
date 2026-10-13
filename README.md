# 30일 수익화 프로젝트 — AI 업무자동화 키트

직장인을 위한 복붙용 <strong>AI 프롬프트 키트(PDF)</strong>를 판매하고, 매일 자동으로 검색 유입용 글과 SNS 초안을 쌓는 시스템입니다.

```
[매일 자동 루틴] → 블로그 글 1편 + SNS 초안 → 검색·SNS 유입 → 사이트 → 결제(Gumroad/크몽) → 판매 기록
```

## 구성

| 경로 | 내용 |
|---|---|
| `docs/` | 판매 사이트 (GitHub Pages): 랜딩, 무료 샘플, 블로그 |
| `docs/assets/config.js` | **결제 링크·가격 설정** — 여기만 바꾸면 사이트 전체 반영 |
| `automation/ROUTINE.md` | 매일 실행되는 AI 루틴의 작업 지침 |
| `automation/content_calendar.md` | 30일 글 주제 (검색 키워드 순) |
| `automation/posts/` | 블로그 원고 (Markdown) → `build_site.py`가 HTML로 변환 |
| `automation/sns/` | 날짜별 SNS 게시 초안 (스레드·인스타·숏폼) |
| `automation/sales_report.py` | Gumroad 판매 조회 → `metrics.csv` |
| `automation/reports/` | 주간 점검 리포트 |
| `product/` | PDF 빌드 도구 (원고·PDF 자체는 저장소에 없음) |

## 소유자가 한 번만 해주실 일 (약 1시간)

1. **Gumroad 상품 등록** (gumroad.com 가입)
   - 상품 PDF 업로드, 가격 12,900원 (또는 $9.9), 지급(Payout) 정보 등록
   - 상품 링크(`https://….gumroad.com/l/…`)를 알려주시면 `config.js`에 넣습니다
2. **크몽 전자책 등록** (선택, 강력 추천) — 크몽 자체 검색 유입이 있어 첫 판매가 가장 빨리 나올 수 있는 채널입니다. 심사에 며칠 걸립니다
3. **GitHub Pages 켜기** — 저장소 Settings → Pages → Source: *Deploy from a branch* → 운영 브랜치 / `/docs`
   - 주소: https://seungyun-shin.github.io/Agent_work_reposi/
4. **판매 조회 토큰** — Gumroad → Settings → Advanced → Applications 에서 액세스 토큰 발급 →
   이 클라우드 환경 설정(세션 제목줄의 환경 메뉴 → Edit)에 `GUMROAD_ACCESS_TOKEN` 으로 저장 (채팅에 붙여넣지 마세요)
5. **검색 등록** (선택) — Google Search Console, 네이버 서치어드바이저에 사이트와 `sitemap.xml` 제출
6. **매일 5분** — `automation/sns/오늘날짜.md` 초안을 운영 중인 SNS 채널에 복사해 게시

## 정직한 기대치

- 판매는 보장되지 않습니다. 30일 안에 **첫 매출**을 내는 것이 1차 목표입니다.
- 검색 유입은 보통 수 주~수 개월 걸립니다. 30일 안의 매출은 주로 **기존 SNS 채널**과 **크몽 마켓 유입**에서 나옵니다.
- 루틴은 매일 한 번 실행되며 실행할 때마다 Claude 사용량을 씁니다.
- 결제·환불·세금(해외 플랫폼 수입도 종합소득세 신고 대상)은 소유자 계정에서 처리됩니다.
