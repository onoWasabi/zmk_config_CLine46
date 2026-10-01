"""Host regression tests for the actual C listener and DTS keymap structure."""
import pathlib, re, subprocess, tempfile
root = pathlib.Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as d:
    d = pathlib.Path(d)
    (d / "zmk/events").mkdir(parents=True)
    (d / "zmk/event_manager.h").write_text("#pragma once\n#include <stdbool.h>\n#include <stdint.h>\ntypedef struct zmk_event_t { uint8_t layer; bool state; } zmk_event_t;\n#define ZMK_EV_EVENT_BUBBLE 0\n#define ZMK_LISTENER(a,b)\n#define ZMK_SUBSCRIPTION(a,b)\n")
    (d / "zmk/events/layer_state_changed.h").write_text("#include <zmk/event_manager.h>\n#define zmk_layer_state_changed zmk_event_t\n#define as_zmk_layer_state_changed(e) (e)\n")
    (d / "zmk/keymap.h").write_text("#include <stdbool.h>\nbool zmk_keymap_layer_active(int layer);\nint zmk_keymap_layer_deactivate(int layer);\n")
    harness = r'''#include <assert.h>
#include "SOURCE"
static unsigned layers;
bool zmk_keymap_layer_active(int layer) { return (layers & (1u << layer)) != 0; }
static void change(int layer, bool active) {
    if (active) layers |= 1u << layer; else layers &= ~(1u << layer);
    zmk_event_t ev = {layer, active};
    assert(func_priority_listener(&ev) == ZMK_EV_EVENT_BUBBLE);
}
int zmk_keymap_layer_deactivate(int layer) { change(layer, false); return 0; }
int main(void) {
    for (int mode = 0; mode <= 1; mode++) {
        for (int fn = 2; fn <= 3; fn++) {
            layers = 1u << mode;
            change(4, true); assert(zmk_keymap_layer_active(4));
            change(fn, true); assert(!zmk_keymap_layer_active(4));
            assert(zmk_keymap_layer_active(mode));
            change(4, true); assert(!zmk_keymap_layer_active(4));
            change(5, true); change(7, true); change(8, true);
            assert(zmk_keymap_layer_active(5) && zmk_keymap_layer_active(7) && zmk_keymap_layer_active(8));
            change(fn, false); change(4, true); assert(zmk_keymap_layer_active(4));
        }
    }
    layers = 1; change(2, true); change(3, true); change(2, false);
    change(4, true); assert(!zmk_keymap_layer_active(4));
    change(3, false); change(4, true); assert(zmk_keymap_layer_active(4));
    return 0;
}
'''.replace("SOURCE", str(root / "src/func_priority.c"))
    (d / "test.c").write_text(harness)
    subprocess.run(["cc", "-std=c11", "-Wall", "-Wextra", "-Werror", "-I", str(d), str(d / "test.c"), "-o", str(d / "test")], check=True)
    subprocess.run([str(d / "test")], check=True)
text = (root / "config/CLine46.keymap").read_text()
keymap = text[text.index("    keymap {"):]
keymap = re.sub(r"//[^\n]*", "", keymap)
layers = {}
for name, bindings in re.findall(r"(\w+)\s*\{\s*bindings\s*=\s*<(.*?)>;", keymap, re.S):
    entries = [x.strip() for x in re.findall(r"&[^&]+", bindings)]
    assert len(entries) == 46, (name, len(entries))
    layers[name] = entries
assert len(layers) == 9
assert layers["FUNC_2"][19:23] == ["&mkp MB1", "&mkp MB2", "&mo 8", "&kp LCTRL"]
assert layers["FUNC_SCROLL"][22] == "&trans"
assert layers["FUNC_2"][11] == "&mo 6"
assert layers["FUNC_1"][18:22] == ["&kp LEFT", "&kp DOWN", "&kp UP", "&kp RIGHT"]
overlay = (root / "boards/shields/CLine46/CLine46_R.overlay").read_text()
assert overlay.index("hscroller {") < overlay.index("scroller {") < overlay.index("function_cursor {")
assert "layers = <5 8>;" in overlay
function = overlay[overlay.index("function_cursor {"):]
assert "layers = <2 3>;" in function and "zip_temp_layer" not in function
print("PASS: FUNC priority, queued AML, NICOLA preservation, scroll preservation, 9 x 46 bindings, click/arrows/BT mappings, processor priority")
