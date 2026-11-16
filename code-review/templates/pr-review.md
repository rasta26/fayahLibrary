# Template: PR review

## 1. Purpose
A mentoring review of a teammate's pull request: find what must change and teach the principle behind it.
For the PR author. The growth notes at the end are for me only. Full method: `mentoring-code-review` skill.

## 2. Inputs
- PR link or diff (required; ask for it if missing)
- Author's level: junior / mid / senior (if missing, assume mid and say so)
- Linked ticket or spec (if missing, skip the spec check and say so)
- Anything from past reviews to watch for (optional)

## 3. Steps
1. Read the PR description, ticket and tests before the code. Write the intent in one sentence.
2. Check out the branch, run the tests, and try the happy path plus one edge case.
3. Go through the diff for correctness, tests, naming and security.
4. Put each finding in a tier: Blocking, Should or Consider (at most 3 Consider).
5. Write each comment in the comment format below.
6. Decide: any Blocking comment means request changes; otherwise approve.
7. Write the private growth notes separately.

## 4. Output format
```
## Review: <PR title> (#<n>)
Intent: <one sentence>
Ran: <test command> → <pass/fail counts>. Tried: <happy path>; <edge case>
Decision: Approve | Request changes

### Comments
[Blocking|Should|Consider] <one-line title>
What I see: <file:line or short quote>
Why it matters: <failure, future cost or principle>
One option: <small concrete change>
Your call: <question about their reasoning>

### Summary for the author
Done well: <specific, with file or line>
Carry forward: <one pattern>
Retire: <one pattern>
```
Then, outside the PR text: **Growth notes (private)** with strengths (evidence), recurring gaps
(evidence, count) and the next suggested kata.
Tone: direct and collegial; praise only if specific. Summary: 5 lines or fewer.

## 5. Finished example
None on file yet. Save the first review you're happy with to `code-review/examples/`
with names removed (this repo is public), and link it here.

## 6. Done check
- [ ] The tests were run and the result is stated.
- [ ] Every comment has a tier and all five lines.
- [ ] Every Blocking comment points at a file and line.
- [ ] The decision matches the tiers (any Blocking → request changes).
- [ ] Growth notes are not in the PR text.
