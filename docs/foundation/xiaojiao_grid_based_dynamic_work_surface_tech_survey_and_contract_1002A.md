# 1002A Xiaojiao Grid Based Dynamic Work Surface Tech Survey and Contract

Stage:

`	ext
1002A_XIAOJIAO_GRID_BASED_DYNAMIC_WORK_SURFACE_TECH_SURVEY_AND_CONTRACT
`

Final status target:

`	ext
XIAOJIAO_GRID_BASED_DYNAMIC_WORK_SURFACE_TECH_SURVEY_AND_CONTRACT_PASS
`

## Product Judgment

Xiaojiao should not be one fixed page. It should be a progressive dynamic work surface:

`	ext
light entry -> focus surface -> grid based deep studio -> analysis board
`

Default entry stays light. Complex teaching work can expand into a bounded grid studio. Analysis tasks can become dashboard-like boards.

## Technology Survey

Primary candidate: React-Grid-Layout.

Reason: it directly matches draggable, resizable, responsive React grid workspaces, including static widgets, bounded layouts, saved layouts, responsive breakpoint layouts, and dashboard-like grids.

Secondary candidate: dnd-kit.

Reason: it is better for semantic drag/drop rules, tool docks, card insertion, cross-zone movement, and accessible sensors. It should supplement the grid engine rather than replace it.

Backup candidate: Gridstack.js.

Reason: it is a mature TypeScript dashboard grid engine, but it may push the product toward a dashboard feel.

Panel split candidate: react-resizable-panels.

Reason: useful for split panes inside a studio, not enough as the core grid surface.

Not recommended for core surface: React Flow and Craft.js.

Reason: React Flow is for node-based editors and diagrams. Craft.js is for page editors. Both may be useful later, but they should not define the main Xiaojiao work surface.

## Contract

Must define:

`	ext
surface_mode
grid_layout_schema
zone_type
card_type
card_registry
business_pack_layout_preset
layout_memory_policy
system_recommended_layout
teacher_override_layout
restore_default_layout
card_allowed_zone_rules
drag_resize_boundary_rules
`

## Boundary

This is a tech survey and contract only. It does not install dependencies, modify real frontend files, connect runtime, call provider/model, write database or memory, write Feishu, create formal export, or implement production UI.

## Sources

- React-Grid-Layout: https://github.com/react-grid-layout/react-grid-layout
- Gridstack.js: https://gridstackjs.com/
- dnd-kit: https://dndkit.com/
- react-resizable-panels: https://github.com/bvaughn/react-resizable-panels
- React Flow: https://reactflow.dev/
- Craft.js: https://github.com/prevwong/craft.js/