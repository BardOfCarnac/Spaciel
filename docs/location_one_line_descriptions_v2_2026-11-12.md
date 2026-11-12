# Spaciel one-line descriptions V2 — draft coverage complete (12 November 2026)

**Status: 661/661 descriptions populated in a private editorial review bundle. Not approved for production.**

| Locations | Existing edited Vend-R copy | New original sourcebook-grounded descriptions | Blank | Total |
|---|---:|---:|---:|---:|
| 556 primary places | 82 | 474 | 0 | 556 |
| 105 individual outlet pins | 58 | 47 | 0 | 105 |
| **Total** | **140** | **521** | **0** | **661** |

- V1 had 490 descriptions and 171 gaps. V2 fills all **124 missing main locations** and **47 missing outlet pins**. Every original V1 line was preserved unchanged (140 Vend-R edited lines and 350 original sourcebook summary drafts).
- The 171 new one-line drafts were written from the user's private *Night City 2045* sourcebook, including nested places that had been missed by the earlier heading extractor. All 521 sourcebook-derived summaries remain pending editorial approval.
- Canonical ID equality was validated across all **556 primary IDs plus 105 Vend-R outlet IDs**: 661 unique records, 0 gaps. Main/child relationships, positions, category colour, 28 subtypes, optional tags and animations are untouched.
- The complete texts and the 31MB viewer remain **private**, not in this public repository. See conversation attachments named `Spaciel_661_One_Line_Descriptions_V2_Complete_Review.json`, `Spaciel_661_One_Line_Descriptions_V2_Complete_Review.csv`, `Spaciel_661_Descriptions_V2_Editorial_Reviewer.html`, and `Spaciel_V19_661_Pins_Descriptions_V2_Complete_Review.html`.
- Use [the canonical-ID integration helper](../src/locations/one-line-descriptions.js) for future main viewer builds. All records have nonempty descriptions; no fallback to category, subtype, tag or affiliation is allowed.
- Six new lines have focused editorial caution flags where multi-column formatting made a source passage less straightforward. The complete 521 original summary drafts still require an editorial sign-off.
- JavaScript syntax checks passed for all ten viewer blocks and the standalone reviewer. No real-device WebGL2 visual acceptance or live Supabase deployment has been claimed.

Earlier coverage estimates and the original V1 report remain historical snapshots, not the current status. This is a **completed writing pass**, not a user-approved publication or a live software release.
