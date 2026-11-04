#include "fe3h_labels.h"

#include <cstdio>
#include <fstream>
#include <map>
#include <sstream>
#include <string>

using namespace fe3h_labels;

static int fails = 0;
#define CHECK(c)                                                                  \
    do {                                                                          \
        if (!(c)) {                                                               \
            std::printf("FAIL line %d: %s\n", __LINE__, #c);                      \
            ++fails;                                                              \
        }                                                                         \
    } while (0)

// real data: lang \t index \t text (message part 1 of msgdata, the probe indices)
static std::map<std::pair<int, uint32_t>, std::string> Texts;

static bool Get(int language, uint32_t index, std::string& out) {
    const auto it = Texts.find({language, index});
    if (it == Texts.end())
        return false;
    out = it->second;
    return true;
}

int main() {
    std::ifstream f("H:/EdenDuo/work/probe_texts.tsv", std::ios::binary);
    std::string line;
    while (std::getline(f, line)) {
        std::istringstream ls(line);
        std::string l, i, t;
        std::getline(ls, l, '\t');
        std::getline(ls, i, '\t');
        std::getline(ls, t);
        Texts[{std::stoi(l), uint32_t(std::stoul(i))}] = t;
    }
    CHECK(Texts.size() == 12 * std::size(ProbeIndices));

    std::map<int, std::string> probe;
    for (int l = 0; l < LanguageCount; ++l) {
        probe[l] = BuildProbe([&](uint32_t index, std::string& out) { return Get(l, index, out); });
        CHECK(!probe[l].empty());
    }
    // the groups of regional variants have equal words here: 1 = 2, 4 = 5, 6 = 7
    const int group_first[LanguageCount] = {0, 1, 1, 3, 4, 4, 6, 6, 8, 9, 10, 11};
    for (int l = 0; l < LanguageCount; ++l) {
        // no hint: the first of the equal ones
        CHECK(MatchLanguage(probe[l], -1, Get) == group_first[l]);
        // the right hint wins, including a variant after its twin
        CHECK(MatchLanguage(probe[l], l, Get) == l);
        // a wrong hint (another language, even a CJK one) does not fool it
        for (int hint : {0, 1, 9, 10, 11, 99})
            CHECK(MatchLanguage(probe[l], hint, Get) == (hint == l ? l : (probe[hint % LanguageCount == hint ? hint : 0] == probe[l] && hint < LanguageCount ? hint : group_first[l])));
    }
    // the CJK ones tell each other apart (same Han words, different shapes of code points)
    CHECK(probe[10] != probe[11] && probe[0] != probe[10] && probe[0] != probe[9]);
    CHECK(MatchLanguage("", 9, Get) == -1);
    CHECK(MatchLanguage("nothing|like|it|", 9, Get) == -1);
    // an unreadable romfs finds nothing
    CHECK(MatchLanguage(probe[9], 9, [](int, uint32_t, std::string&) { return false; }) == -1);
    // the probe is empty while any word is missing (the text manager is not loaded)
    CHECK(BuildProbe([](uint32_t, std::string&) { return false; }).empty());
    CHECK(BuildProbe([](uint32_t index, std::string& out) { out = index == 257 ? "x" : ""; return true; }).empty());
    // control codes do not matter
    CHECK(BuildProbe([](uint32_t, std::string& out) { out = "a\x1b" "b"; return true; }) == "ab|ab|ab|ab|ab|");
    std::printf(fails ? "FAILED %d\n" : "ALL OK\n", fails);
    return fails != 0;
}
