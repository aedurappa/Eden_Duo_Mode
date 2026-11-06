# Eden_Duo_Mode

[Eden Duo](https://github.com/igawa6/eden-duo) 컴패니언(세컨드 스크린 모드)을 수정·한글화한 결과물을 모아 두는 저장소입니다.
한 모드 전용이 아니라, 앞으로 만드는 수정 모드를 `mods/` 아래에 하나씩 추가합니다.

> 이 저장소는 Eden Duo 및 원 컴패니언 제작자의 공식 저장소가 아닙니다.
> 바탕이 된 작품과 라이선스, 변경 내용은 [NOTICE.md](NOTICE.md)에 있습니다.

## 모드 목록

| 모드 | 게임 | Title ID | 게임 버전 | 상태 | 다운로드 |
|---|---|---|---|---|---|
| [Fire Emblem: Three Houses — 한글/다국어](mods/fire-emblem-three-houses/) | 파이어 엠블렘 풍화설월 | `010055D009F78000` | 1.2.0 | 글자 표시: 공식 1.0.1에 반영됨 / 라벨: [PR #23](https://github.com/igawa6/eden-duo-companions/pull/23) 검토 중 | [Releases](../../releases) |

## 규칙

- **게임 자산을 넣지 않습니다.** 그림·글꼴·문구·소리·키는 저장소에도, 패키지에도 없습니다. 모두 실행 중 사용자의
  게임 파일에서 읽습니다.
- 모든 코드와 패키지는 **GPL-3.0 이상**입니다([LICENSE](LICENSE)). 바이너리(Releases의 zip)는 같은 저장소의
  소스와 패치로 빌드한 것입니다.
- 바탕이 된 컴패니언의 저작권·라이선스 표기는 그대로 유지합니다.

## 구조

```
mods/<모드 이름>/
  README.md     무엇을 바꿨는지, 설치·빌드 방법, 한계
  patches/      업스트림 소스에 적용하는 패치 (기준 커밋은 README에 명시)
  tools/        패키지를 만드는 스크립트와 데이터
  tests/        PC에서 도는 확인용 테스트
NOTICE.md       출처, 저작자, 라이선스, 변경 고지
```
