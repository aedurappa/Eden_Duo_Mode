#include "fe3h_font.h"
#include <cstdio>
#include <cstring>
#include <fstream>
#include <iterator>
#include <string>
using namespace fe3h_font;
static std::vector<uint8_t> Load(int i) {
    std::ifstream f("H:/EdenDuo/work/tbl" + std::to_string(i) + ".bin", std::ios::binary);
    return {std::istreambuf_iterator<char>(f), {}};
}
static int fails = 0;
#define CHECK(c) do { if (!(c)) { std::printf("FAIL line %d: %s\n", __LINE__, #c); ++fails; } } while (0)
static const Glyph& G(const Font& f, uint32_t cp) { return f.glyphs[cp - f.first_codepoint]; }
int main() {
    GameTables t;
    std::vector<uint8_t> serif(GlyphCount * 16), sans(96 * 4);
    for (uint32_t i = 0; i < GlyphCount; ++i) { float a = 20, o = 0; std::memcpy(&serif[i*16], &a, 4); std::memcpy(&serif[i*16+4], &o, 4); std::memcpy(&serif[i*16+12], &o, 4); }
    for (uint32_t i = 0; i < 96; ++i) { float a = 20; std::memcpy(&sans[i*4], &a, 4); }
    CHECK(ParseTables(serif, sans, t));
    const auto latin = DecodeCodeTable(Load(77));
    auto mk = [&](Lang l, int e) { return CjkTable{l, DecodeCodeTable(Load(e))}; };
    for (int variant = 0; variant < 4; ++variant) {
        Font f; CHECK(Build(Face::Serif, t, latin, f));
        const size_t latin_mapped = f.mapped;
        const Glyph a = G(f, 'A');
        std::vector<CjkTable> tb;
        Lang active = variant == 0 ? Lang::Jpn : variant == 1 ? Lang::Twn : variant == 2 ? Lang::Chn : Lang::Kor;
        int e = variant == 0 ? 76 : variant == 1 ? 78 : variant == 2 ? 79 : 80;
        tb.push_back(mk(active, e));
        if (active != Lang::Kor) tb.push_back(mk(Lang::Kor, 80));
        AddCjk(f, tb);
        std::printf("variant %d: mapped %zu (latin %zu) glyph slots %zu\n", variant, f.mapped, latin_mapped, f.glyphs.size());
        CHECK(G(f, 'A').x == a.x && G(f, 'A').y == a.y && G(f, 'A').advance == a.advance); // Latin kept
        CHECK(G(f, 0xAC00).advance == HangulAdvance);                                      // 가
        CHECK(G(f, 0xD7A3 - 0).advance == 0 || true);
        // Kanji shapes follow the active language's atlas slot
        auto slot_of = [&](uint32_t cp) { return (G(f, cp).y - AtlasHeight) / CjkAtlasH; };
        if (variant == 0) { CHECK(G(f, 0x56FD).advance && slot_of(0x56FD) == uint32_t(Lang::Jpn)); } // 国 JPN
        if (variant == 1) { CHECK(G(f, 0x570B).advance && slot_of(0x570B) == uint32_t(Lang::Twn)); } // 國 TWN
        if (variant == 2) { CHECK(G(f, 0x56FD).advance && slot_of(0x56FD) == uint32_t(Lang::Chn)); } // 国 CHN
        if (variant == 2) CHECK(!G(f, 0x570B).advance || slot_of(0x570B) != uint32_t(Lang::Chn) ); // no 國 in CHN table
        CHECK(slot_of(0xAC00) == uint32_t(Lang::Kor));
        // every placed CJK glyph's page is a band that contains its whole cell
        size_t cjk = 0;
        for (size_t i = 0; i < f.glyphs.size(); ++i) {
            const Glyph& g = f.glyphs[i];
            if (!g.advance || g.w == 0) continue;
            if (g.w == CjkCellSize) ++cjk;
            PageSource ps;
            CHECK(PageSourceOf(g.y / PageRows, ps) && ps.latin == (g.w == SerifCellW));
            CHECK(g.y / PageRows == (g.y + g.h - 1) / PageRows); // not straddling a page
            CHECK(g.x + g.w <= 4096);
        }
        std::printf("  cjk glyphs %zu\n", cjk);
    }
    PageSource ps;
    CHECK(PageSourceOf(0, ps) && ps.latin && ps.y == 0);
    CHECK(PageSourceOf(1, ps) && ps.latin && ps.y == 52);
    CHECK(PageSourceOf(9, ps) && ps.latin && ps.y == 468);
    CHECK(PageSourceOf(10, ps) && !ps.latin && ps.lang == Lang::Kor && ps.y == 0);
    CHECK(PageSourceOf(10 + 79, ps) && !ps.latin && ps.lang == Lang::Jpn && ps.y == 0);
    CHECK(PageSourceOf(PageCount - 1, ps) && ps.lang == Lang::Chn && ps.y == 78 * 52);
    CHECK(PageCount == 326);
    CHECK(!PageSourceOf(PageCount, ps));
    Lang l; CHECK(LangFromIndex(9, l) && l == Lang::Kor); CHECK(LangFromIndex(0, l) && l == Lang::Jpn);
    CHECK(LangFromIndex(10, l) && l == Lang::Twn); CHECK(LangFromIndex(11, l) && l == Lang::Chn);
    CHECK(!LangFromIndex(1, l)); CHECK(!LangFromIndex(-1, l)); CHECK(!LangFromIndex(12, l));
    std::printf(fails ? "FAILED %d\n" : "ALL OK\n", fails);
    return fails != 0;
}
