# EDR Writing Guide

## What is an EDR?

An Engineering Decision Record (EDR) documents a significant technical decision — what you chose, why you chose it, what you rejected, and when to revisit. It captures **reasoning**, not just outcomes. Six months from now, when you or someone else asks "why is retry a decorator instead of a base class method?", the EDR answers immediately without archaeology.

---

## When to Write an EDR

Write one when:

- You chose between two or more plausible approaches and the choice wasn't obvious
- The decision affects multiple modules or will constrain future versions
- You rejected a "standard" approach for a specific reason
- A future reader might reasonably ask "why not X?"

Do **not** write one for:

- Trivial implementation choices (variable names, loop style)
- Decisions forced by a single constraint with no real alternative
- Temporary scaffolding you plan to remove

---

## File Naming Convention

```
docs/adr/EDR-NNN-short-description-in-kebab-case.md
```

Number sequentially. Use a descriptive slug that answers "what decision?" at a glance.

Examples:
- `EDR-001-module-layout-and-responsibility-boundaries.md`
- `EDR-004-logging-configuration-strategy.md`
- `EDR-005-http-status-code-classification.md`

---

## Template

```markdown
# EDR-NNN: [Title — the decision, not the topic]

## Status
[Proposed | Accepted | Superseded by EDR-NNN | Deprecated]

## Problem
[One paragraph. What question needed answering? What forced this decision?]

## Context
[Background a reader needs. What exists today, what constraints apply, what's changing.
Keep it factual — save opinions for the "Why" sections below.]

## Possible Solutions
1. **[Option A]** — [one-line description]
2. **[Option B]** — [one-line description]
3. **[Option C]** — [one-line description]

## Chosen Solution
Option N — [restate briefly]

## Why This Solution Was Selected
[The core argument. Multiple bullet points, each making one clear claim.
Ground every claim in something concrete: a principle, a future requirement,
a specific cost, a specific benefit. Avoid "it felt right."]

## Trade-offs Accepted
[What you gave up or what could go wrong. Every design choice has costs —
being honest about them is what separates engineering from guessing.]

## Why Alternatives Were Rejected
[For each rejected option: one paragraph explaining the specific problem with it.
Don't just say "worse" — say why, concretely.]

## When to Revisit
[Under what future conditions should this decision be re-evaluated?
Name specific triggers: "If X happens, reconsider Y."]
```

---

## Writing Principles

### 1. Document the decision, not the topic

Bad title: "Retry Logic"
Good title: "Why a Decorator for Retry Logic"

The title should tell a reader what was decided without opening the file.

### 2. Enumerate alternatives honestly

If you can't name at least two real alternatives, either the decision is too obvious for an EDR, or you haven't thought hard enough. The alternatives should be approaches a reasonable engineer might choose — not strawmen.

### 3. Ground reasoning in specifics

Bad: "Composition is more flexible."
Good: "Adding a third site requires creating one `SiteConfig` instance and zero code changes to existing modules. With inheritance, it requires a new file, a new class, and potentially duplicated logic in overridden methods."

### 4. Name the trade-offs

Every decision has costs. If your EDR has no "Trade-offs Accepted" section, you haven't thought about it deeply enough. Common trade-offs:

- Simplicity now vs. flexibility later
- More boilerplate vs. better separation
- Custom code vs. external dependency
- Type safety vs. ease of change

### 5. Include "When to Revisit"

Decisions aren't permanent. Naming the conditions under which this decision should be reconsidered prevents two failure modes:
- Cargo-culting a stale decision long after circumstances changed
- Relitigating every old decision without trigger criteria

### 6. Write for a future reader who disagrees

The most valuable EDR is one that convinces a skeptic — someone who would have chosen differently. If your reasoning only makes sense to someone who already agrees, it's not doing its job.

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| Writing after the fact with post-hoc rationalization | Write during or immediately after the decision, when trade-offs are fresh |
| Listing only the chosen solution | Always enumerate at least 2–3 alternatives with honest analysis |
| Vague reasoning ("cleaner", "better", "simpler") | Quantify or give a concrete scenario that demonstrates the claim |
| No trade-offs section | Every choice has costs — find them and state them |
| Overly long context section | Context should be enough to understand the decision, not a tutorial |
| Forgetting "When to Revisit" | Name specific triggers, not "if requirements change" |

---

## Quality Check

Before considering an EDR done, verify:

- [ ] A reader can understand the problem without reading any other document
- [ ] All listed alternatives are approaches a reasonable engineer would consider
- [ ] The "Why" section makes concrete claims, not vague assertions
- [ ] Trade-offs are honest — you named what you gave up
- [ ] Rejected alternatives have specific, concrete reasons for rejection
- [ ] "When to Revisit" names a testable condition, not "someday"
- [ ] The EDR is short enough to read in 2–3 minutes

---

## Revisiting Existing EDRs

During this review week, re-read EDR-001 through EDR-003 with these questions:

1. **Does reality match the record?** Did you actually follow through on what the EDR says? If not, either update the code or update the EDR.
2. **Are the trade-offs still accurate?** Now that you've lived with the decision for a few weeks, have the predicted costs materialized? Were there unexpected costs?
3. **Have any "When to Revisit" triggers fired?** If so, it's time to either reaffirm the decision with updated reasoning or supersede it with a new EDR.
4. **Is any reasoning post-hoc?** Did you write the EDR after implementing, then unconsciously reverse-engineer justification? If the reasoning doesn't match your actual thought process, revise to be honest — it's more useful that way.
