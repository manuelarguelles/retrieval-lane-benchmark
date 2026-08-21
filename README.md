# Hand-built versus managed retrieval

I built the same research agent twice over a corpus of academic papers: once **by hand**,
owning the chunking and the character offsets, and once **delegated** to a managed
retrieval service. Same corpus, same 70 questions, same generating model.

The question was never which one retrieves more. It was **what you give up by delegating**.

> The corpus is in English and the questions are in Spanish — this was built for
> Spanish-speaking readers querying English-language research. Queries are
> machine-translated into the corpus language before retrieval, which is why a multilingual
> embedding model is required rather than optional.

## Results

| | recall@8 | MRR | p50 |
|---|---|---|---|
| Lane A · dense + lexical, hand-built | **53/70 (76 %)** | 0.460 | 0.015 s |
| Lane B · managed service | **43/70 (61 %)** | 0.367 | 0.400 s |
| Lane A · with reranking | **60/70 (86 %)** | 0.69 | +1.4 s |

Delegating the whole pipeline costs 10 questions out of 70 and 27× the latency. The
breakdown matters more than the total: delegating **the search engine** costs 0; losing
**the lexical leg** costs 11.

## What you lose isn't recall — it's the pointer

Of the 560 passages the managed lane returned, **560 carry a page number and none carries a
character offset**. And the returned text is no longer ours: the service extracts the PDF
with its own extractor, so the same passage comes out differently from each.

Compared **literally** against our document, the managed lane's recall drops to 5/70. The
38-question gap is line breaks, not missing evidence.

⇒ With a managed service, deterministic citation checking **cannot run as written**: it
forces whitespace normalisation, and normalising is exactly what welds non-contiguous text
together and lets something absent pass as present.

## The ceiling trap

The union of both lanes is 58/70, which invites building a hybrid. **It doesn't pay.** At 8
slots every split loses to the hand-built lane alone and captures **0 of the 5** gains. At
16 slots it doesn't either: A alone reaches 57, the hybrid 55.

Three of the five questions the managed lane rescues sit at positions 5–6 of its list, and
the hand-built lane has 10 hits in slots 5–8. **Giving up four slots kills ten to gain two.**
The union is what a selector that knew in advance which lane is right would achieve — and no
such selector exists.

The page ships a simulator: move the split, and recall recomputes from each question's real
measured positions.

## A correction worth reading

Sources that didn't make it into the corpus were listed as "no access". That status came
from a service answering a narrower question — *is there an open-access PDF for this DOI?* —
and a "no" there was stored as "the content can't be read".

Auditing all 23 with a real browser: **4 have an open version ingestion never took**, two
verified by hand with the full article on screen. The corpus could grow ~30 % without paying
for a single subscription. Nothing was re-ingested, because changing the corpus would
invalidate all 70 questions and every measurement here.

The auditor was wrong first, too: its initial version read only the main frame and reported
"abstract only" for a page whose full article sat inside a cross-origin iframe.

## Repository layout

```
site/
  index.html       ← the page (for embedded publishing)
  standalone.html  ← the same page, opens directly in a browser
  build.py         ← assembles both from the parts
  data.json        ← the measurements, already sanitised
  _*.html          ← the parts: tokens, styles, sections, behaviour
```

One page, no dependencies, no server. `python3 site/build.py` rebuilds it.

## What isn't here, and why

- **The corpus PDFs.** Academic articles under their own licences; the catalogue links each
  to its original source.
- **The experiment code.** It lives in a private repository: it touches resources in the
  account where the measurement ran.
- **That account's identifiers.** This ran on a client's infrastructure. Account names,
  buckets, roles and personal data are deliberately outside this publication, and an
  automated gate fails data generation if any of them leak in.

## What this experiment does not prove

- The generating model isn't the one I'd have chosen: the provider had the main model family
  quota-blocked throughout. The judges run on the same model that generates — the largest
  bias still standing.
- Thirteen documents and seventy questions separate lanes differing by ten points, not
  differences of two.
- Results hold for English-language papers queried in Spanish. Internal documents with tables
  and forms are a different problem.
- The managed service's chunking ran at default settings. Tuning it would likely move its
  recall; it would not move the loss of the pointer, which is structural.

---

Manuel Argüelles · August 2026
