/* SPDX-License-Identifier: MIT */
#include <zmk/event_manager.h>
#include <zmk/events/layer_state_changed.h>
#include <zmk/keymap.h>

/* Keep the existing layer IDs, including Studio and NICOLA settings. */
#define FUNC_1 2
#define FUNC_2 3
#define MOUSE 4

static int func_priority_listener(const zmk_event_t *eh) {
    const struct zmk_layer_state_changed *ev = as_zmk_layer_state_changed(eh);
    if (ev && ev->state &&
        (ev->layer == FUNC_1 || ev->layer == FUNC_2 || ev->layer == MOUSE) &&
        (zmk_keymap_layer_active(FUNC_1) || zmk_keymap_layer_active(FUNC_2)) &&
        zmk_keymap_layer_active(MOUSE)) {
        /* Also rejects an AML activation already queued before FUNC was pressed.
         * The stock temp-layer listener observes this deactivation and cancels
         * its timer/state. ZMK retains press-time bindings for key releases. */
        zmk_keymap_layer_deactivate(MOUSE);
    }
    return ZMK_EV_EVENT_BUBBLE;
}

ZMK_LISTENER(cline_func_priority, func_priority_listener);
ZMK_SUBSCRIPTION(cline_func_priority, zmk_layer_state_changed);
