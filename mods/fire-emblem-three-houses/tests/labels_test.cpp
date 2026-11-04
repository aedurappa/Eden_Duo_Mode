#include "fe3h_labels.h"
#include <cstdio>
#include <cstring>
#include <set>
#include <string>
using namespace fe3h_labels;
static int fails = 0;
#define CHECK(c) do { if (!(c)) { std::printf("FAIL line %d: %s\n", __LINE__, #c); ++fails; } } while (0)
int main() {
    std::set<std::string> keys;
    size_t own_entries = 0, game_entries = 0;
    for (size_t i = 0; i < EntryCount(); ++i) {
        const Entry& e = Entries()[i];
        CHECK(keys.insert(e.key).second);
        CHECK(e.own[En] && *e.own[En]);
        if (e.part >= 0) { ++game_entries; for (int c = 1; c < ColumnCount; ++c) CHECK(!e.own[c]); CHECK(e.index >= 0); }
        else { ++own_entries; for (int c = 0; c < ColumnCount; ++c) CHECK(e.own[c] && *e.own[c]); }
    }
    std::printf("%zu entries: %zu from the game, %zu own\n", EntryCount(), game_entries, own_entries);
    CHECK(ColumnOf(1) == En && ColumnOf(2) == En && ColumnOf(-1) == En && ColumnOf(12) == En);
    CHECK(ColumnOf(0) == Ja && ColumnOf(3) == De && ColumnOf(4) == Fr && ColumnOf(5) == Fr);
    CHECK(ColumnOf(6) == Es && ColumnOf(7) == Es && ColumnOf(8) == It);
    CHECK(ColumnOf(9) == Ko && ColumnOf(10) == Twn && ColumnOf(11) == Chn);
    for (size_t i = 0; i < EntryCount(); ++i) {
        const Entry& e = Entries()[i];
        if (!std::strcmp(e.key, "academy")) { CHECK(!std::strcmp(Own(e, 9), "사관학교")); CHECK(!std::strcmp(Own(e, 1), "Academy")); CHECK(!std::strcmp(Own(e, 11), "士官学校")); CHECK(!std::strcmp(Own(e, 10), "士官學校")); }
        if (!std::strcmp(e.key, "str")) CHECK(e.part == 1 && e.index == 266 && !std::strcmp(Own(e, 9), "Str"));
    }
    CHECK(CleanGameText(std::string("a\x1b" "b\nc")) == "abc");
    std::printf(fails ? "FAILED %d\n" : "ALL OK\n", fails);
    return fails != 0;
}
