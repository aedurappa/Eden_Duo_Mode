"""Layout fixes the localized words need, shared by gen_labels.py and gen_ko.py.

The top bar of the battle pages draws the label "Turn" (left aligned, text_scale 8) and the turn
number 78 units to its right, left aligned. The game's own words are wider than the English one:
about 84 units for TURN (Korean, Japanese, Chinese) and 105 for TURNO (Spanish, Italian) at
text_scale 7, against about 70 for "Turn" at 8, so the number was drawn over the last letter.

The label gets text_scale 6 (TURNO then ends about 90 units from its start) and the number is
right aligned at 124 units from the label's start, which is 7 units before the "PLAYER PHASE" text
next to it. A right aligned number grows to the left, so whatever the width of the word or the
number, the number never runs into the phase text, and one digit leaves room for the longest word.
"""

LABEL_SCALE = 6
NUMBER_SHIFT = 46  # 124 - 78: the number's right edge, from where its left edge was


def fix_turn_overlap(manifest):
    """Applies the fix to every page; returns the number of widgets changed."""
    changed = 0

    def walk(o):
        nonlocal changed
        if isinstance(o, dict):
            if o.get('type') == 'label' and o.get('text') == 'Turn' and o.get('text_scale') == 8 \
                    and o.get('align') != 'center':
                o['text_scale'] = LABEL_SCALE
                changed += 1
            elif o.get('type') == 'value' and o.get('bind') == 'bt.turn' and o.get('text_scale') == 10:
                rect = o['rect']
                o['rect'] = [rect[0] + NUMBER_SHIFT] + rect[1:]
                o['align'] = 'right'
                changed += 1
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    for page in manifest['pages']:
        walk(page['widgets'])
    return changed
