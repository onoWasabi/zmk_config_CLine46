# Only the right (central) half owns keymap and pointing state.
if(CONFIG_ZMK_SPLIT_ROLE_CENTRAL AND CONFIG_ZMK_POINTING)
  target_sources(app PRIVATE src/func_priority.c)
endif()
