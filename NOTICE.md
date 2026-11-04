# Notice, attribution and license / 고지, 출처 표기, 라이선스

This repository is a collection of modifications to Eden Duo companions ("mods"). Everything in
it is free software under the **GNU General Public License v3.0 or later** (see [LICENSE](LICENSE)).
It is not affiliated with or endorsed by Eden Duo, the Eden project, Nintendo, Koei Tecmo or
Intelligent Systems. All trademarks belong to their respective owners.

이 저장소는 Eden Duo 컴패니언(모드)을 수정한 결과물을 모아 둔 곳입니다. 모든 내용은
**GNU GPL v3.0 이상**으로 배포되며([LICENSE](LICENSE)), Eden Duo·Eden 프로젝트·닌텐도·코에이테크모·
인텔리전트 시스템즈와 제휴하거나 승인받은 것이 아닙니다. 모든 상표는 각 소유자의 것입니다.

## What this work is based on / 바탕이 된 것

| Work | Where | Author / owner (as shown by the source) | License |
|---|---|---|---|
| **Fire Emblem: Three Houses companion** (package 1.0.0, native module, manifest) | <https://github.com/igawa6/eden-duo-companions>, commit `fc0f85e` | `igawa6` (repository owner and commit author of record). Per-file copyright line: "Eden DSMod fork". | GPL-3.0-or-later |
| **Eden Duo** (the runtime the companion runs on; this work only builds against its public module headers `core/mods/dsmod_module_abi.h` etc. and ships none of its code) | <https://github.com/igawa6/eden-duo>, tag `v1.2.0` | `igawa6`, as an independent fork of Eden. | GPL-3.0 (see its `LICENSE.txt`) |
| **Eden** and its predecessors (yuzu), the emulator Eden Duo is forked from | <https://git.eden-emu.dev/eden-emu/eden> | The Eden project and the yuzu contributors | GPL-3.0-or-later |
| **Original companion author** (the one to credit for the Fire Emblem: Three Houses companion this work modifies) | <https://github.com/igawa6> | `igawa6` | GPL-3.0-or-later |

The companion's own copyright and license notices are kept as they are in every upstream file
that this work modifies (the patch changes lines, it does not remove headers). Files that this
work adds carry "Copyright 2026 Eden_Duo_Mode contributors" and the same license.

수정한 업스트림 파일의 저작권·라이선스 표기는 모두 그대로 유지했습니다(패치는 줄만 바꾸고 헤더를
지우지 않습니다). 새로 추가한 파일에는 "Copyright 2026 Eden_Duo_Mode contributors"와 같은
라이선스를 표기했습니다.

## What was changed / 변경 내용 (GPL §5a)

Modified on **2026-11-05**, against upstream `eden-duo-companions` commit `fc0f85e`.
The change is `mods/fire-emblem-three-houses/patches/0001-fe3h-cjk-glyphs-and-language-labels.patch`
(12 files, +698 −6 lines). In short:

- the module reads the game's own Korean / Japanese / Chinese font atlases and code tables (from
  the player's romfs, at run time) in addition to the Latin one, so those scripts are drawn;
- the font atlas is split into one-cell-row pages so one screen fits the host's page cache;
- the language is found by comparing a few words from the game's memory with the game's
  message data, and the companion's fixed labels are published in that language;
- the manifest's fixed English labels are bound to those published labels (`gen_labels.py`) or,
  for the Korean-only package, replaced by Korean (`gen_ko.py`).
- the top-bar turn label and number are smaller and the number is right aligned before the phase
  text, so the game's wider words (TURN, TURNO) and a two digit number do not overlap
  (`layout_fix.py`).

Both packages in the Releases were built from exactly this source (see the README of the mod for
the build steps).

## Game assets / 게임 자산

Nothing from the game is shipped: no art, fonts, text, audio or keys. Fonts, glyphs and text
are read at run time from the player's own game files, as in the original companion. The words
the labels use are looked up by index in the player's own message data; only this work's own
translations of the companion's own phrases are included (`tools/own.py`).

게임의 그림·글꼴·문구·소리·키는 포함하지 않습니다. 글꼴과 글자 모양, 게임 용어는 모두 실행 중 사용자의
게임 파일에서 읽습니다. 모드 고유 문구의 번역(`tools/own.py`)만 이 저장소의 것입니다.

## Source for the binaries / 바이너리의 소스 (GPL §6)

The `.so` libraries inside the packages in the Releases are built from: upstream
`eden-duo-companions` at `fc0f85e` **plus** the patch in this repository, against Eden Duo `v1.2.0`
headers. That is the complete corresponding source; `mods/fire-emblem-three-houses/tools/build.sh`
is the build script that was used.

## AI assistance / AI 도움

This work was made with the help of an AI coding assistant (Claude, by Anthropic). The
translations of the companion's own phrases in `tools/own.py` were written with that help and have
not been reviewed by native speakers of every language.
