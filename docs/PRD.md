# Product Requirements Document (PRD)

**Product:** Mercari Smart Listing Agent   
**Status:** Draft v0.1 | **Updated:** 2026-10-26

## 1. User and problem

**User:** A non-native Japanese speaker (initial persona: around JLPT N3) who can photograph a second-hand item but struggles to write a clear Japanese listing.

**Job to be done:** Help me turn my item photo and the facts I provide into an accurate Japanese draft, so I can review and finish a listing with less effort.

A listing requires a category, title, description, condition, and price. A one-shot LLM prompt may invent a brand or size, use inconsistent fields, exceed the title limit, or suggest a price without evidence. Fluent text is not necessarily trustworthy. This is an independent learning project, not a Mercari product or integration.

## 2. What we will build

A **local-first, human-in-the-loop workflow**:

1. The seller selects an item photo and can enter known facts such as brand, size, defects, and accessories.
2. A local vision-language model extracts only reasonably visible facts. Unknown or uncertain details are marked `unknown` or asked of the seller, never guessed.
3. A fixed workflow asks for essential missing facts, then a local text model drafts the category, Japanese title, and description from visible and seller-confirmed information.
4. Pydantic validates the structured output. A title check enforces the project's 40-character target; the current marketplace counting rule must be verified before release.
5. The seller can review, edit, and copy the draft. **The MVP never submits or publishes a listing.** Price guidance is optional and is shown only if a defensible source of comparable data exists.
6. Representative photos and reviewed expected facts become test fixtures for reproducible evaluation.

**Technical direction:** Python, Ollama/local inference, Pydantic, and automated tests. Qwen3-VL 4B and a small local text model are candidates to benchmark, not assumed to be good enough without testing. Photos should not leave the machine in the MVP. Start with a predictable workflow; add agent-like decisions only when justified by a requirement.

## 3. Success metrics

**Offline evaluation:** Use a manually reviewed set of approximately 40-60 item photos. Track each metric separately:

- **Schema validity:** Report the raw model-output pass rate; 100% of accepted outputs must pass validation.
- **Title validity:** Track raw title-limit violations; 100% of accepted titles must pass the configured length check.
- **Groundedness:** Track and reduce claims unsupported by the image or seller.
- **Category quality:** Top-1 accuracy against reviewed labels.
- **Japanese quality:** Human rubric for naturalness, clarity, and factual fidelity; back-translation/model judging can assist but cannot replace human review.
- **Price quality:** Report error only when defensible reference prices exist.
- **Performance:** Response time and resource use on the target laptop.

Set realistic quality thresholds after measuring the first baseline, then keep the test set and thresholds fixed between comparisons.

**Supervised pilot:** There is no production deployment in the MVP. Measure task completion, time to a review-ready draft, amount of manual editing, corrections for false claims, and seller confidence. These measure usability—not sales or conversion.

## 4. Non-goals

- No scraping Mercari or other marketplaces for listing or price data.
- No automatic publishing, account actions, or direct Mercari integration.
- No photo-only guarantee of authenticity, safety, or defect-free condition.
- No authoritative “true market price” or promise of perfect Japanese.
- No required paid cloud API or remote upload of private item photos.
- No autonomous agent acting without seller confirmation.
- No guarantee of marketplace-policy compliance or sales improvement.

## 5. Risks and open questions

- **Hallucinations/Japanese quality:** Local models may misidentify items or write unnatural text. Measure unsupported claims and use a documented Japanese-quality rubric; seek proficient-speaker review when available.
- **Pricing evidence:** What lawful, reproducible comparison dataset can support price guidance? Until decided, keep pricing optional.
- **Marketplace rules:** Verify the current title-counting method, required fields, categories, and policies before release.
- **Privacy:** Decide whether photos/drafts are discarded or saved locally with explicit user control; do not silently retain images in logs.
- **Scope/hardware:** Decide whether the first interface is CLI or a local web UI. Benchmark candidate model versions for quality, speed, and memory use on the actual Windows laptop.

## 6. MVP done when

The local workflow runs reproducibly; accepted drafts pass schema and title checks; uncertainty is visible; sellers can edit and copy results; tests run; and the README documents evaluation and limitations. Nothing is published automatically.
