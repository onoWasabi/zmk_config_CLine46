# CLine46 NICOLA v10 — 2026-09-30

Keyball39 2026-09-29 FUNC priority and 2026-09-10 FUNC mouse controls port.

- Keep existing layer IDs 0–7 and add FUNC_SCROLL=8.
- `src/func_priority.c` removes AML on FUNC entry, including queued reactivation.
- FUNC cursor override skips AML; vertical/horizontal scrolling retains precedence.
- FUNC_2 positions 19/20/21: left click, right click, held scroll. Position 22 stays Ctrl.
- FUNC scroll: hold position 21, then a Shift position (34/35/45) for horizontal scroll.
- Existing MOUSE scroll gestures, JIS symbols, NICOLA and Bluetooth system controls remain.

Run host regression checks: `python3 tests/test_func_priority.py`.
Build with the existing GitHub Actions workflow (right, left, settings_reset).
Flash the matching L/R UF2 to each half after double-tapping its reset button.
`settings_reset` erases stored settings/pairing; it is not a normal firmware update step.
Actual keyboard/BLE behavior still requires hardware verification.

See `keymap_design_CLine46.md` for the layout.

## Boot mode (2026-10-01)

Move the ball to activate MOUSE, then hold position 1 (Q) or 10 (P) for 1.5 seconds to enter DFU on the left or right half respectively. A shorter press does nothing. Flash the matching new UF2 on both halves. Other key presses cannot trigger boot early. Physical double-reset remains available.
