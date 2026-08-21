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

## Access is not a property of the document

The corpus table went through three versions and the first two were wrong the same way. They
said *"no access"* and *"closed"* — claims about the world, written from what a program with
no signed-in session managed to fetch.

Both fell to someone checking **a single source by eye**. First, a conference record marked
"no access" whose full article rendered on its own page — inside a cross-origin iframe my
auditor never entered. Then one marked "closed" that JSTOR serves in full on a free account,
ten articles a month.

| Who asks JSTOR | What it returns |
|---|---|
| an automated browser, no session | **83 characters** |
| a person with a free account | the full 10-page article |

**Access is a relation, not an attribute.** It depends on who is asking, with what session,
from which institution, from which country. A pipeline without credentials sees a more closed
world than the one that exists — and writing that down as the document's status publishes
your own limitation as a fact about the world.

The second flaw was subtler: the auditor asked *where the DOI points* — the publisher and its
paywall — instead of *which venues hold the work*. Querying every indexed location surfaces
copies the DOI never mentions: university repositories at CSUN, DePaul and SMU, plus JSTOR
and PubMed.

So the status column now has two values only — `in the corpus` and `not ingested` — because
those are the only two things this pipeline can verify. Of the 24 not ingested, 3 were read
in full by hand and 4 have a copy elsewhere. How much the corpus could grow is no longer
estimated: the previous estimate came from the same kind of inference that failed twice.

Four venues answer automation with a bot check or a 403. **No attempt was made to get around
any of them.** What was verified was verified by reading it in an ordinary browser.

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
