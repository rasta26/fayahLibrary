---
name: mentoring-code-review
description: Review a pull request or diff as a principal engineer mentoring the author. Use when asked to review code for a developer, give PR feedback, prepare for a 1:1 about someone's code, or turn review findings into growth points.
---

# Mentoring Code Review

Review to make the author better, not only the code. Every comment teaches a reusable
principle and leaves the decision with the author where it is theirs to make.

## Procedure

1. **Understand intent first.** Read the PR description, linked spec/issue, and tests
   before the implementation. State the intent back in one sentence at the top of the review.
2. **Run it.** Check out, run tests, try the happy path and one edge case. A review without
   running the code is a reading, not a review.
3. **Triage findings** into three tiers; label every comment with its tier:
   - **Blocking:** correctness, security, data loss, contract violation, missing test for a
     requirement. Must be fixed before merge.
   - **Should:** maintainability, naming, duplication, missing edge-case test. Fix now or
     file a follow-up with the author's agreement.
   - **Consider:** style, alternative approaches, learning pointers. Author decides.
4. **Write each comment** as: *observation → why it matters → one concrete option →
   question that invites the author's reasoning.* Never only "change this".
5. **Close with a summary:** what was done well (specific, not generic), the one pattern
   to carry forward, and the one pattern to retire.

## Comment template

```
[Blocking|Should|Consider] <one-line title>
What I see: <quote or line ref>
Why it matters: <failure mode, future cost, or principle>
One option: <small concrete change or snippet>
Your call / question: <what did you weigh here?>
```

## Calibration

- Max ~3 "Consider" comments per review; more dilutes the blocking ones.
- If a Blocking issue recurs from a previous review, say so plainly and propose a
  practice (a kata, a checklist, a lint rule) rather than repeating the fix.
- Praise is specific or omitted: "the retry wrapper isolates the flaky dependency cleanly"
  rather than "nice work".
- Review the tests as hard as the code: assert on behaviour, not implementation; one
  concept per test; names that read as requirements.

## Growth notes (for 1:1s)

After the review, append to a private note for the author:
- strengths observed (evidence)
- recurring gaps (evidence, count)
- suggested next kata or reading (see `coding-kata`)
Do not put growth notes in the PR itself.
