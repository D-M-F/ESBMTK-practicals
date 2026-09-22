# Notebook reading cues

Use these conventions in the active 00–04 instructor sources and their generated
student copies. The permanent maintenance rule lives in [AGENTS.md](../AGENTS.md).
Keep the existing **Choose and explain**, **Understand and run**, and
**Supplied implementation** code labels in 01–04: those identify the student's
role in code; these cues identify concepts, questions and written answers.

| Content | Appearance | Use |
| --- | --- | --- |
| Key term | Pale gold, bold text | Selected concepts at introduction or a key distinction; avoid highlighting every occurrence, whole paragraphs or every number |
| Student question | Pale blue panel, blue left border, explicit **Question — …** label | Existing predictions, scientific mappings, derivations, interpretations and completion prompts |
| Written instructor answer | Pale purple panel, purple left border, explicit **Instructor answer** label | Existing written solutions, including equations and result tables |
| Instructor-only reference/check | Same purple panel, accurate **Instructor reference** or **Instructor verification** label | Existing instructor-only guidance; do not relabel a software check as a scientific answer |

Keep general explanations, supplied run instructions and reference material in
ordinary Markdown. A blue panel may include the inputs or hints needed for its
question, but must not contain the instructor answer. Preserve question order,
wording, scope and timing. Do not add answers merely to fill a panel.

Add a short reading key near each notebook opening. Use explicit labels and bold
text as well as colour. Fix both text and background colours within panels for
contrast; surrounding notebook text can follow the reader's theme. The inline
styles need no setup cell, extension, external stylesheet or trusted code output.
Viewers that strip styling should still show the labels and content in order.

## Authoring patterns

Key terms use inline HTML; leave maths, code and Markdown links outside the mark
unless the rendered result has been checked. Do not wrap Markdown `**` inside HTML
`strong` elements.

```html
<mark style="background-color: #fff0b3; color: #513d00; padding: 0.05em 0.2em; border-radius: 3px;"><strong>carbon inventory</strong></mark>
```

Question panel (keep blank lines around the HTML boundaries and Markdown):

```markdown
<div style="background-color: #edf5ff; color: #173b61; border-left: 4px solid #3977b8; padding: 12px 16px; margin: 16px 0; border-radius: 4px;">

**Question — interpret the budget**

Existing question text goes here.

</div>
```

Instructor answer panel: **both HTML boundaries and the label must be inside
the solution markers** so student generation removes the whole panel.

```markdown
<!-- BEGIN SOLUTION -->
<div style="background-color: #f3eefb; color: #38224f; border-left: 4px solid #7952a8; padding: 12px 16px; margin: 16px 0; border-radius: 4px;">

**Instructor answer**

Existing answer text, equations or tables go here.

</div>
<!-- END SOLUTION -->
```

An existing `solution-only` Markdown cell can use the purple panel without adding
markers; its metadata already removes the entire cell. Keep executable solutions
in code cells with their existing solution markers/tags. Do not duplicate them
in styled Markdown. Separate table headers from preceding prose with a blank
line, and retain dollar-delimited mathematics.

## Maintenance checks

Edit instructor sources only, then regenerate the corresponding student copies
with `scripts/build_student_notebooks.py`. Check that questions and key terms
survive, written answers become placeholders, instructor-only cells disappear,
code solutions remain masked, and student outputs are cleared. Inspect rendered
panels, lists, links, tables and mathematical derivations. For a presentation-only
edit, compare code cells and existing instructor outputs with the starting
worktree; run the applicable generation and conservation checks.

Do not restyle dated archives. Optional extensions can adopt this convention in
a future edit; the initial rollout covers core 00–04 only.
