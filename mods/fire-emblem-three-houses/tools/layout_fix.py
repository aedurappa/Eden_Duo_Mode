"""Layout fixes the localized words need, shared by gen_labels.py and gen_ko.py.

The top bar of the battle pages draws the label "Turn" (left aligned, text_scale 8) and the turn
number 78 units to its right. The game's own words are wider than the English one: TURN (Korean,
Japanese, Chinese) is about 87 units, TURNO (Spanish, Italian) about 104, against about 70 for
"Turn". So the number was drawn over the last letter. The label gets text_scale 7 (TURNO is then
about 91 units) and the number moves 14 units to the right (92 units from the label), which still
ends before the "PLAYER PHASE" text next to it.
"""

LABEL_SCALE = 7
NUMBER_SHIFT = 14


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
                changed += 1
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    for page in manifest['pages']:
        walk(page['widgets'])
    return changed
