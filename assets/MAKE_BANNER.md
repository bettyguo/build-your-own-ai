# Banner / social card spec

This repository's `assets/banner.png` and `assets/social-card.png` are
intentionally absent from the initial commit — they should be rendered by
a designer (or image generator) using the spec below, then committed.

## `banner.png` — README hero

- **Size:** 1500 × 500 px, PNG, < 200 KB.
- **Headline (left-aligned, ~96pt):** `build-your-own-ai`
- **Sub-headline (left-aligned, ~36pt):** `Master modern AI by building it from scratch.`
- **Visual motif (right):** a small isometric / line-art stack of "build blocks" suggesting:
  tokenizer → attention → training loop → RAG → agent. Five labeled blocks
  stacked or arranged in a clear vertical/diagonal flow. Subtle, monochrome
  with one accent color.
- **Palette:** background `#0B1020` (deep indigo) · text `#F5F7FF` ·
  accent `#7EE0B8` (mint) · secondary `#9AA3C7` (cool grey).
- **Type:** Inter or Source Sans 3 for both lines.
- **Footer (bottom-left, ~14pt, muted):** `curated by Betty Guo (HKU)`

## `social-card.png` — Open Graph / Twitter

- **Size:** 1200 × 630 px, PNG, < 200 KB.
- Same palette + type.
- **Title:** `build-your-own-ai`
- **Sub-title:** `The curated index of build-it-from-scratch guides for the modern AI stack.`
- **Below sub-title (smaller):** `Tokenizers · Attention · Training · RAG · Agents · Evals · Diffusion`
- **Bottom strip:** the URL `github.com/bettyguo/build-your-own-ai`

## Reference inspiration

- `build-your-own-x` does not use a banner — its formatting alone carries
  the visual identity. This repo wants to go one click further: a banner
  that reinforces "stack of things you'll build" rather than a stylized AI
  illustration.
- Avoid anything resembling a brain, robot, neural-network blob, or a
  ChatGPT-style bubble. Visual language: blueprint, not mascot.
