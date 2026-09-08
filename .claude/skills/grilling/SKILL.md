---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea until nothing is silently assumed. Use when the user wants to stress-test their thinking, when starting a new level or puzzle, or on any 'grill' trigger phrase.
---

Interview the user relentlessly until you reach a shared understanding. Map this as a
**design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are
already settled — the questions you can ask *now* without guessing at answers you have not
heard yet. Ask the whole frontier in one round: number each question and give your
recommended answer. Then wait for the user's answers before the next round.

Format a round like so:

```
❓ **Q1** — **<question title>**: <question body, may be multiple paragraphs, may include choices>

➡️ <your recommended answer, and why>

---

❓ **Q2** — **<question title>**: <question body>

➡️ <your recommended answer, and why>
```

Each round of answers reshapes the tree: settled decisions push the frontier outward and
unblock questions that depended on them. Recompute the frontier and ask the next round. A
question whose answer depends on another question still open in this round belongs to a
*later* round, not this one.

Finding **facts** is your job, never the user's. When a frontier question needs a fact from
the environment — what a file contains, what a library supports, what an astronomy source
says — dispatch a sub-agent to find it; never ask the user for something you could look up.
Do not block on it: a running exploration is an unsettled prerequisite, so only the
questions downstream of it wait. Ask the rest of the frontier now.

The **decisions** are the user's. Put each to them and wait.

The session is done when the frontier is empty: every branch visited, nothing left silently
assumed. Do not act on it until the user confirms you have reached a shared understanding.

## Branches this project keeps forgetting to ask about

When grilling a new level or puzzle, the frontier almost always includes these — they are
cheap to decide up front and expensive to retrofit:

- **What is the astronomy claim, exactly?** And is it already in `docs/sources.md` as
  VERIFIED? A puzzle built on a NEEDS SOURCE claim cannot ship.
- **How does this hide the math?** What does the player manipulate, and what do they see
  change? If the answer contains a number, the design is not finished.
- **Which of the five puzzle types is this?** If the honest answer is "none of them", that
  is a scope decision, not an implementation detail — surface it.
- **What does a wrong attempt teach?** If the answer is "nothing, it just fails", the
  puzzle is a lock, not a lesson.
- **What Bulgarian text does this need**, and does it read naturally for an 11-12 year old
  rather than as translated English?
- **What does this cost on the target hardware?** New textures, a new 3D moment, a new
  dependency.
- **Does it need new generated data?** If so, which script produces it, and does the
  `dataRef` seam already exist?
- **What is deliberately NOT in this?** The scope boundary is easier to hold when it is
  stated out loud.
