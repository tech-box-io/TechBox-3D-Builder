# Review v12: Lee's notes of 16 Oct 2026

Three independent reviewers (the player; the generator and the step-text tool, tried on scratch copies with the cases a
curriculum director's spreadsheet can bring; the result in the browser at desktop and phone widths), then an adversarial
verifier for each medium or high finding. Workflow run `wf_bcd3df46-8a1`.

The reviewers confirmed: the view reset returns exactly to the step's own camera (title page, flipped and isolated steps,
Completed View; after a real drag with its spin, a wheel zoom and a pan), does nothing during a step animation, is hidden on note
cards and the parts list, adds no work when idle; the Parts List tiles match the page's layout and load no picture before the
step list opens (and work with the bundle's packed pictures); the joysticks are named Left / Right on hover and click
everywhere; only the joystick names and the wood bands changed in steps.json; `_runthrough()` 211 views, 0 problems.

| Finding | Severity | Outcome |
|---|---|---|
| Steps 56 and 66 have the same wording, so they shared a key: an edit to one would land on both | high, verified | Fixed: each step's key is a short code from its wording and which step with that wording it is (`text_key`, in every step's views). Tested: an edit to Step 56 alone changes Step 56 only. |
| A whole-sheet Replace All also rewrote the key (the wording), so the edits were lost | medium, verified | Fixed by the code key. Tested: 'servo horn' to 'servo arm' throughout keeps all 7 edits. |
| A renamed or missing column was read as empty cells (cautions silently deleted, or nothing imported) | medium, verified (low) | Fixed: the columns are found by name (loosely); a missing one stops the import with a message before anything is written. UTF-16 files are refused with advice. |
| Excel for Mac's plain CSV was read as Windows text (garbled); CR-only lines stopped the import | medium, verified | Fixed: UTF-8 if it is UTF-8, else Windows or Mac text, whichever leaves more rows reading as the guide does; lines read with any line ending. Tested both. |
| Every edited step pinned its caution, so a later caution change in guide.py would be ignored | medium, verified | Fixed: only the edited fields are stored; an edited caution keeps the guide's caution it replaced, and if guide.py's caution has changed since, the generator keeps guide.py's and warns. Tested. |
| Keyboard focus was lost when the focused reset button was hidden (stepping onto a card or the parts list) | medium, verified (low) | Fixed: the button is hidden after the player notes the focus, so focus moves on as for the other buttons (to Next, or the card's speaker). Tested. |
| An edit copying another step's wording moved that step's key | low | Fixed: the key comes from the step itself. |
| Rows with no key (a new step) or an unknown key were dropped with their comments; an emptied instruction was silently kept | low | Fixed: such rows are reported with their text and comment; the emptied instruction is reported (and in How to edit.txt). |
| Rest steps never showed a caution (latent) | low | Fixed. |
| With Review notes shown (?review=1) the switch covered the caption's corner at 701 - 729 px wide | low | Fixed: the caption keeps clear of it then. Tested at 704 px. |
| Embedded without full screen, the reset button left an empty slot in the corner | low | Fixed: it moves into the corner. |
| The Parts List tiles always use an 1100 px window's layout (at 1400 px or on a phone the page itself is laid out differently) | low | Kept (the tile is a fixed size); reported to Lee with the trial. |
| The wood groups' icons are still orange | low | Kept: only the bands were asked for; reported. |
