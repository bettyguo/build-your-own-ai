# Structured / constrained decoding — from scratch

> **[original]** · part of [`build-your-own-ai/originals/`](README.md).
> _A short, runnable starter guide for a build target where no good public
> from-scratch guide exists today._

**Index entry:** [Inference → Structured / constrained decoding](../README.md#inference)

---

## The one-line promise

LLMs don't "know" how to output JSON. The *sampler* does — by masking
every invalid next-token to `-inf` at every step. This is the trick
behind Outlines, XGrammar, vLLM's guided decoding, and OpenAI's strict
JSON mode. You can write it in ~80 lines.

## What you'll understand after

- Why constrained decoding is **not** prompting — the constraint
  enforces correctness at sampling time, not generation time.
- Why an FSM over the *vocabulary* is the right data structure (not an
  FSM over characters).
- The exact failure mode every constrained-decoding system shares:
  *vocabulary-mismatch dead ends*, and how to detect them.

## The mental model

Decoding is a loop: model emits logits over the vocab, sampler picks
one. Constrained decoding adds one step in the middle:

```
logits = model(prefix)
mask   = fsm.valid_next_tokens(state)   # the new line
logits[~mask] = -inf
next_token = sample(softmax(logits))
state = fsm.advance(state, next_token)
```

That's it. The interesting work is in `fsm.valid_next_tokens(state)` —
which tokens, given the current FSM state, would not violate the
constraint?

## Step 1 — A toy: constrain to `yes` or `no`

Two tokens. The FSM is trivial: the only valid first-step tokens are
the ones that *start* one of `{"yes", "no"}`. After committing to one,
the FSM accepts only continuations of that word.

```python
import torch

class YesNoFSM:
    """Accepts exactly 'yes' or 'no' then EOS."""
    ACCEPT = {"yes", "no"}

    def __init__(self, tokenizer, eos_token_id: int):
        self.tok = tokenizer
        self.eos = eos_token_id

    def valid_next_token_ids(self, prefix_text: str) -> set[int]:
        """Return the set of token IDs that would keep us on a valid path."""
        valid: set[int] = set()
        # If the prefix already matches an accepted word, only EOS is valid.
        if prefix_text in self.ACCEPT:
            valid.add(self.eos)
            return valid
        # Otherwise: any token whose decode keeps the prefix on a path to
        # one of the ACCEPT strings is valid.
        for token_id in range(self.tok.vocab_size):
            candidate = prefix_text + self.tok.decode([token_id])
            if any(w.startswith(candidate) for w in self.ACCEPT):
                valid.add(token_id)
        return valid
```

Two things to notice already:

- We walk the entire vocabulary per step. For a 50k-vocab model that's
  fine — modern libraries cache this lookup as a trie indexed by FSM
  state, but the brute-force version is the same idea.
- We work in *decoded text* space, not token-string space. This matters
  because byte-pair tokens split words unintuitively (`" no"` and `"no"`
  are different tokens; spaces matter; multi-byte unicode tokens exist).

## Step 2 — The masking step

This is the line that does the actual work:

```python
def apply_mask(logits: torch.Tensor, valid_ids: set[int]) -> torch.Tensor:
    """logits: (vocab,). Returns logits with all-but-valid set to -inf."""
    mask = torch.full_like(logits, float("-inf"))
    if valid_ids:
        idx = torch.tensor(sorted(valid_ids), device=logits.device)
        mask[idx] = logits[idx]
    return mask
```

After `softmax`, every invalid token has probability exactly zero. The
model can no longer hallucinate a token that breaks the constraint.

## Step 3 — Wire it into a generation loop

```python
@torch.no_grad()
def constrained_generate(model, tokenizer, prompt: str, fsm,
                         max_new_tokens: int = 16) -> str:
    ids = tokenizer.encode(prompt, return_tensors="pt").to(model.device)
    completion_text = ""
    for _ in range(max_new_tokens):
        logits = model(ids).logits[0, -1, :]           # (vocab,)
        valid  = fsm.valid_next_token_ids(completion_text)
        if not valid:
            break                                       # dead end (see step 5)
        logits = apply_mask(logits, valid)
        next_id = torch.argmax(logits).item()           # greedy for the example
        if next_id == tokenizer.eos_token_id:
            break
        ids = torch.cat([ids, torch.tensor([[next_id]], device=ids.device)], 1)
        completion_text += tokenizer.decode([next_id])
    return completion_text
```

Run it on a small instruct model with the prompt `"Is the sky blue? Answer yes or no:"`
and watch it emit exactly `yes` or `no`, never anything else, regardless of how
weird the underlying logits are.

## Step 4 — From `yes`/`no` to a regex

The exact same shape generalizes. Replace `YesNoFSM` with one that
walks a compiled regex's state machine:

```python
import re

class RegexFSM:
    """Accepts strings that match a regex; uses prefix-matching for the FSM step."""
    def __init__(self, pattern: str, tokenizer, eos_token_id: int):
        self.full = re.compile(pattern)
        self.partial = re.compile(pattern + r"$", re.DOTALL)  # accepts prefixes
        self.tok = tokenizer
        self.eos = eos_token_id

    def valid_next_token_ids(self, prefix_text: str) -> set[int]:
        if self.full.fullmatch(prefix_text):
            return {self.eos}                # complete match → accept EOS only
        valid: set[int] = set()
        for tid in range(self.tok.vocab_size):
            cand = prefix_text + self.tok.decode([tid])
            # A token is valid if some completion of `cand` matches the regex.
            # Cheap conservative proxy: the regex with `.*` appended matches `cand`.
            if re.match(self.full.pattern + r".*", cand, re.DOTALL):
                valid.add(tid)
        return valid
```

This is the "naive Outlines" — slow because of the per-step vocab walk
and the prefix-completion check, but algorithmically correct. Outlines'
real contribution is *caching*: for each FSM state, precompute the set
of valid token IDs once. That turns the per-step cost from O(vocab)
into O(|valid|), and is what makes structured decoding fast enough for
production.

## Step 5 — JSON schema in 30 lines

JSON Schema → regex is a well-defined translation. For a simple schema
like `{"name": str, "age": int}`:

```python
import re

JSON_SCHEMA_REGEX = (
    r'\{"name": "[^"]+", "age": \d+\}'
)

fsm = RegexFSM(JSON_SCHEMA_REGEX, tokenizer, tokenizer.eos_token_id)
out = constrained_generate(model, tokenizer, "Return JSON: ", fsm, max_new_tokens=64)
# out: {"name": "Alice", "age": 30}  ← always valid JSON, always matches the schema
```

Production systems use a proper JSON-Schema → regex compiler (or, better,
a JSON-Schema → context-free grammar → pushdown automaton, which is
what XGrammar does for nested structures). The principle is the same.

## Step 6 — The failure mode: vocabulary-mismatch dead ends

The mode that bites every constrained-decoding system: **the constraint
is satisfiable in character-space but not in *token*-space.**

Example. Constrain to the regex `[0-9]{4}`. Some tokenizers have a
single token for `2024`. If, midway, the model has emitted `20` and the
next valid characters are `[0-9]{2}`, but the only tokens whose decodes
start with `[0-9]` are `2024`, `2025`, `2026` — there's no token that
extends the prefix `20` by exactly 1 or 2 digits without committing to
a longer one. The FSM accepts in character space; vocab space dead-ends.

Detect it:

```python
valid = fsm.valid_next_token_ids(prefix)
if not valid and not fsm.is_complete(prefix):
    raise RuntimeError(f"Vocabulary-mismatch dead end at prefix {prefix!r}")
```

Mitigations: looser regexes; tokenizer-aware constraint design; pushing
the constraint into a pre-tokenized grammar (XGrammar's PDA over
tokens, not characters).

## Three honest gotchas

1. **Greedy vs sampling under a mask.** Greedy on top of a mask is
   *not* the same as argmax of an unconstrained model. The model may
   strongly want a token you've masked out. Always log the *masked-out
   top-1* — if the model's actual preference is consistently masked,
   your constraint is misaligned with the model's distribution and the
   outputs will be subtly wrong (e.g. JSON values that satisfy the
   schema but ignore the question).
2. **EOS is a token too.** A constraint that requires more text than
   the model wants to produce can mask out EOS forever and rely on
   `max_new_tokens` for termination — fine for tests, dangerous in
   production.
3. **Cache the per-state token lists.** The toy code above is O(vocab)
   per step. A real implementation precomputes, per FSM state, the set
   of valid token IDs once (a trie keyed by FSM state). This is what
   makes Outlines fast.

## What to read next

- The [sampling entry](../README.md#inference) — structured decoding is
  a sampler-level intervention; understanding sampling first makes the
  mask line obvious.
- The [tool-layer original](tool-layer.md) — once you can guarantee
  valid JSON, the tool-layer's "broken JSON" failure mode collapses.
- Brandon Willard, *Efficient Guided Generation for Large Language
  Models* (Outlines paper, 2023) — the canonical theoretical reference
  for the FSM-over-vocab approach.
- XGrammar (MLC, 2024) — the PDA-over-tokens generalization, with a
  good intro to why CFGs (not just regex) matter for nested JSON.
