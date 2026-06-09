# English AI Pattern Library

> Merged from [humanizer_academic](https://github.com/matsuikentaro1/humanizer_academic) (99 stars), [slopbuster](https://github.com/gabelul/slopbuster) (16 stars), and [humanize-academic-writing](https://github.com/momo2young/humanize-academic-writing) (14 stars).
> Covers content-level, language-level, style, and structural AI patterns in English academic writing.

---

## I. Content-Level Patterns (from humanizer_academic)

### Pattern 1: Significance Inflation

**Trigger words:** stands/serves as, is a testament/reminder, a vital/significant/crucial/pivotal/key role/moment, underscores/highlights its importance, reflects broader, symbolizing its ongoing, contributing to the, setting the stage for, marking/shaping the, represents/marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted

**Before:**
> Heart failure represents a pivotal challenge in the evolving landscape of type 2 diabetes care. This stark reality underscores the critical importance of addressing cardiovascular comorbidities.

**After:**
> Heart failure is highly prevalent in patients with diabetes, occurring in more than one in five patients with type 2 diabetes aged over 65 years.

**Rule:** Delete inflated modifiers. If the sentence still makes sense without "important/crucial/significant," the modifier was AI-added padding.

---

### Pattern 2: Notability Name-Dropping

**Trigger words:** independent coverage, local/regional/national media outlets, written by a leading expert, active social media presence, landmark trial, renowned investigators, prestigious academic centers

**Before:**
> This landmark trial, led by renowned investigators at prestigious academic centers, enrolled an impressive 7020 patients across 590 sites in 42 countries.

**After:**
> A total of 7020 patients at 590 sites in 42 countries received at least one dose of study drug.

**Rule:** Remove superlatives about the research itself; state facts plainly.

---

### Pattern 3: Superficial -ing Analyses

**Trigger words:** highlighting, underscoring, emphasizing, ensuring, reflecting, symbolizing, contributing to, cultivating, fostering, encompassing, showcasing, suggesting, demonstrating, prompting

**Before:**
> Hospitalization for heart failure occurred in 2.7% of empagliflozin patients, highlighting the cardioprotective effects. This effect was consistent across subgroups, underscoring broad applicability.

**After:**
> Hospitalization for heart failure occurred in 2.7% of empagliflozin patients (HR 0.65; P = 0.002). The effect was consistent across subgroups.

**Rule:** Delete -ing phrases that restate what the data already show. If the causal link matters, restore an explicit connective ("therefore," "accordingly").

---

### Pattern 4: Promotional Language

**Trigger words:** boasts a, vibrant, rich (figurative), profound, enhancing its, showcasing, exemplifies, commitment to, groundbreaking, renowned, breathtaking, stunning, remarkable, exciting

**Before:**
> This groundbreaking study showcases the profound impact of empagliflozin and reflects a renewed commitment to improving cardiovascular care.

**After:**
> In patients with type 2 diabetes and high cardiovascular risk, empagliflozin reduced heart failure hospitalization and cardiovascular death.

**Rule:** Academic papers do not advertise. Replace promotional adjectives with data.

---

### Pattern 5: Vague Attributions

**Trigger words:** Industry reports, Observers have cited, Experts argue, Some critics argue, several sources/publications, Studies have shown (without citation)

**EXCEPTION:** "Prior studies have shown that...", "Previous research has demonstrated..." are standard when followed by citations. Only flag when unsupported.

**Before:**
> Studies have shown that SGLT2 inhibitors reduce cardiovascular events. Experts argue that these benefits may be related to hemodynamic effects.

**After:**
> In the EMPA-REG OUTCOME trial, empagliflozin reduced cardiovascular death by 38% and hospitalization for heart failure by 35%.

**Rule:** Replace vague authority with specific citation or the paper's own analysis.

---

### Pattern 6: Formulaic Challenges Section

**Trigger words:** Despite its... faces several challenges..., Despite these challenges, Future Outlook, Challenges and Legacy

**Before:**
> Despite its rigorous methodology, this trial faces several challenges typical of large clinical studies. Despite these limitations, the trial's design continues to provide valuable insights.

**After:**
> The diagnosis of heart failure at baseline was based solely on investigator reports, with no measures of cardiac function or biomarkers recorded.

**Rule:** Replace template "Despite X... still valuable" with specific limitation statement.

---

### Pattern 7: AI Vocabulary (English)

**High-frequency AI words:** Additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate/intricacies, key (adjective), landscape (abstract), pivotal, showcase, tapestry (abstract), testament, underscore (verb), valuable, vibrant, multifaceted, nuanced, navigate, robust (non-statistical), leverage (non-engineering), holistic, paradigm, synergy, seamless, innovative, transformative

**Before:**
> Additionally, empagliflozin reduced the risk by 34%, a pivotal finding in the evolving therapeutic landscape.

**After:**
> Empagliflozin reduced the risk by 34%.

---

### Pattern 8: Copula Avoidance

**Trigger words:** serves as, stands as, marks, represents [a], boasts, features, offers [a]

**Before:**
> Heart failure serves as the leading cause of hospitalization, standing as a major clinical burden and representing a significant unmet need.

**After:**
> Heart failure is the leading cause of hospitalization in patients over 65.

**Rule:** Use "is/are" when that's what you mean.

---

### Pattern 9: Negative Parallelisms

**Trigger words:** Not only...but also..., It's not just about...it's..., Not merely...but rather...

**Before:**
> SGLT2 inhibitors not only lower blood glucose but also reduce cardiovascular events. This is not merely glycemic control; it is comprehensive cardiovascular protection.

**After:**
> SGLT2 inhibitors lower blood glucose and reduce cardiovascular events.

---

### Pattern 10: Rule of Three

**Before:**
> SGLT2 inhibitors lower glucose, reduce cardiovascular events, and improve renal outcomes. These agents offer efficacy, safety, and tolerability.

**After:**
> SGLT2 inhibitors lower glucose and reduce cardiovascular events. They also slow kidney disease progression.

**Rule:** Break triads into pairs or quads. Let importance dictate length.

---

### Pattern 11: Synonym Cycling (Elegant Variation)

**Before:**
> Patients had lower hospitalization rates. Participants demonstrated reduced mortality. Subjects experienced decreased all-cause death rates.

**After:**
> Patients had lower rates of hospitalization (2.7% vs. 4.1%), cardiovascular death (3.7% vs. 5.9%), and all-cause mortality (5.7% vs. 8.3%).

**Rule:** One term per concept. Consistency > variety.

---

### Pattern 12: False Ranges

**Trigger words:** from X to Y (where X and Y aren't on a meaningful scale), spanning from...to..., ranging from...to...across

**Before:**
> The benefits span from improved renal function to enhanced cardiac outcomes, from better metabolic control to reduced hospitalization rates.

**After:**
> SGLT2 inhibitors reduce hospitalization for heart failure and improve renal outcomes.

---

### Pattern 13: Em Dash Overuse (ZERO TOLERANCE in humanizer_academic)

**Rule:** Replace ALL em dashes (—). Commas, parentheses, or periods.

**Before:**
> SGLT2 inhibitors—a relatively new drug class—have transformed treatment. The benefits—a 35% reduction—appeared early—within months.

**After:**
> SGLT2 inhibitors, a relatively new drug class, have transformed treatment. The benefits (a 35% reduction) appeared within months.

---

### Pattern 14: Filler Phrases

| Before | After |
|--------|-------|
| In order to assess | To assess |
| Due to the fact that | Because |
| At the present time | Currently / omit |
| It is important to note that | [delete] |
| The study has the ability to | The study can |
| A growing body of evidence | [cite specific studies] |
| It is worth noting that | [delete] |

---

### Pattern 15: Redundant Multi-layered Hedging

**Before (4-5 layers):**
> These findings may suggest that SGLT2 inhibitors have the potential to confer beneficial effects in select patient populations.

**After (1-2 layers):**
> These findings suggest that SGLT2 inhibitors may reduce cardiovascular events.

**Key distinction:**
- RCT with significant result → direct statement: "Empagliflozin reduced death."
- Observational/exploratory → keep one hedge: "may reduce", "was associated with"
- LLM-style multi-hedge → simplify: "may suggest... have the potential to" → "suggest... may"

---

### Pattern 16: Overly Assertive Causal Claims (Insufficient Hedging)

**Before:**
> Addressing fatigue may reduce the risk of developing depressive symptoms.

**After:**
> Addressing fatigue may help reduce the risk of developing depressive symptoms.

**Rule:** Observational claims need cushion words ("may help reduce", "could potentially contribute to").

---

### Pattern 17: Generic Positive Conclusions

**Before:**
> The future looks bright for patients as these exciting findings continue to reshape clinical practice.

**After:**
> Empagliflozin reduced heart failure hospitalization. The benefit was consistent in patients with and without heart failure at baseline.

**Rule:** Replace vague optimism with specific, verifiable statements.

---

## II. LLM-Specific Word Choice Patterns (from humanizer_academic)

### Pattern 18: Informal "linked to"

**Before:** EDS has been linked to shorter sleep duration.
**After:** EDS has been reported to be associated with shorter sleep duration.

### Pattern 19: Overuse of "Beyond"

**Before:** Beyond the association with sleep disturbances, EDS was also related to impaired functioning.
**After:** In addition to the association with sleep disturbances, EDS was also related to impaired functioning.

### Pattern 20: Overuse of "via"

**Before:** Consent was obtained via the online form.
**After:** Consent was obtained through an online form.

### Pattern 21: "where" as Non-locative Connector

**Before:** Women were overrepresented at the most intensive level, where almost daily use was more than twice as common.
**After:** Women were overrepresented at the most intensive level, with almost daily use more than twice as common.

**Rule:** Keep "where" for physical locations and datasets only. Prefer "with" for loose connections.

### Pattern 22: "yield" as Result Verb

**Before:** Analyses did not yield stable estimates.
**After:** Analyses failed to produce stable estimates.

**Rule:** Replace "yield" with "produce/provide/generate" (except chemical yields).

---

## III. Classical Academic Term Restoration (from humanizer_academic)

LLMs have shifted away from classical academic expressions. Restoring them makes writing sound more established.

### Word-Level Restorations

| AI Version | Restore To |
|------------|-----------|
| proportion of | percentage of |
| aim of | purpose of |
| was assessed | was measured |
| With regard to | With respect to |
| to elucidate | to determine |
| a growing body of research | a growing number of studies |

### Phrasing-Level Restorations

| AI Version | Restore To |
|------------|-----------|
| These findings suggest | The results suggest |
| ultimately (sentence-end) | after all (sentence-end) |
| First (discourse marker) | To begin with |

### Structural Restorations

- **Verb → Noun (nominalization):** "We hypothesized that X" → "We tested the hypothesis that X"
- **Adj+Noun → Adverb:** "A clear dose-response relationship was observed" → "The dose-response relationship was clearly observed"

---

## IV. Structural Patterns (from slopbuster, 10 groups)

### Group A: Meaning & Accuracy (Hard Boundaries)

1. Preserve meaning exactly — never invent claims, citations, or results
2. Never alter numbers — p-values, gene names, technical terms are untouchable
3. Never convert correlation to causation
4. Soften causal language in observational contexts — "demonstrates" → "suggests"

### Group B: Generic Filler

5. Kill transition padding: "moreover," "furthermore," "notably," "importantly," "it is worth noting"
6. Kill significance filler: "plays a crucial role," "provides valuable insights," "highlights the importance of," "underscores," "sheds light on"
7. Kill meta-language: "The present study aims to...", "The results reveal that..."
8. Kill vague intensifiers: "robust" (non-statistical), "comprehensive," "novel," "nuanced," "pivotal," "vital"
9. Kill "leverage" outside engineering contexts

### Group C: Punctuation Habits

10. No em dashes as parenthetical insertions — rewrite as comma, parentheses, or separate sentence
11. No colons introducing bullet-style lists mid-paragraph — integrate into prose
12. No semicolons connecting sentences that should be separate
13. No scare-quotes around technical terms

### Group D: Sentence & Paragraph Patterns

14. Vary sentence length — after two long sentences, insert one short one
15. No consecutive sentences opening with identical word or structure
16. No repeated "This suggests/highlights/indicates/demonstrates" openers
17. No mandatory significance statement at end of every paragraph
18. No symmetric "On the one hand... on the other hand..." unless genuinely balanced
19. No First/Second/Third/Finally enumeration — integrate into prose
20. No stacking multiple qualifying clauses in one sentence — split instead

### Group E: Voice & Reasoning

21. Replace vague wording with concrete phrasing when data supports it
22. Keep disciplinary vocabulary — do not oversimplify technical terms
23. Make reasoning researcher-driven — grounded in observation, not abstract claims
24. Vary paragraph structures — not every paragraph: claim → evidence → implication

### Group F: Deep AI Syntax Patterns

25. Eliminate abstract noun subjects — "This finding suggests..." → "The 40% reduction in..."
26. Front main claims in main clauses — subordinate supporting information
27. Reduce "While X, Y" overuse — vary concessive clause placement
28. Eliminate relative clause stacking — chains of "that" clauses
29. Replace nominalizations — "the examination of" → "examining"; "the occurrence of" → "when"
30. Question parallel list padding — delete items unless truly equal-weight and necessary

### Group G: Creative Grammar & Rhythm

31. Allow deliberate fragments for emphasis — not every sentence needs a verb
32. Allow syntactic tension between adjacent sentences without transitional connectors
33. Vary sentence "weight" within paragraphs — some brief, some observational
34. Occasional inverted constructions — "What the data do not show is equally telling"
35. Some abruptness signals judgment — not mechanical flow

### Group H: Metaphor & Sentence Architecture

36. No self-commentary pattern — use the accurate term directly
37. No explanatory metaphors that frame technical processes in lay terms then self-correct
38. No "does more than X; it Y" pattern — state the primary function first
39. No two equal-weight clauses joined by "and" when one logically depends on the other
40. Prefer active over passive when agent is known (except in Methods)
41. Kill participial closers that restate what the sentence already said

### Group I: Logical Closure & Argument

42. Don't close every causal chain — trust the reader to complete obvious inferences
43. Don't use exclusively forward-moving structure — foreground contrast and unexpected findings
44. Don't always open paragraphs with the broadest generalization — sometimes start specific

### Group J: Subject Variety & Implicit Logic

45. If 2+ consecutive sentences begin with "This/These/The results/The analysis," vary subjects
46. Break chains where every sentence has an abstract process as subject — use concrete actors
47. Remove "therefore/thus/consequently" where causal relationship is already clear
48. Concentrate hedging at genuinely uncertain claims — write directly at well-supported ones
49. After fixing individual patterns, run structural pass (see below)

### Structural Pass (Post-Rule)

| # | Pattern | Fix |
|---|---------|-----|
| S1 | Equal-weight sentences throughout | Elevate main claim; compress support |
| S2 | Every chain closed with "thereby"/"thus" | Remove where inference is obvious |
| S3 | Only forward-moving argument | Lead from unexpected findings or contrasts |
| S4 | Opens with broadest generalization | Try specific observation first |
| S5 | 2+ sentences share same subject type | Introduce concrete actor or finding |
| S6 | Every sentence S-V-O with no variation | Break the pattern |
| S7 | "Therefore/thus/consequently" obvious | Remove; let juxtaposition carry meaning |
| S8 | Uncertainty spread evenly | Concentrate at genuinely uncertain claims |
| S9 | Juxtaposed sentences unclear | Add one precise connective |
| S10 | Final sentence summarizes | Replace with: next-idea opener, implication, or specific claim |

---

## V. What NOT to Change

- Sentences that already read naturally
- Passive voice in Methods sections (disciplinary convention)
- Technical jargon and disciplinary vocabulary
- Hedging on genuinely uncertain claims
- Complete and necessary lists (experimental conditions, molecular components)
- Statistical language backed by actual statistics
- Legitimate academic transitions followed by citations (Notably, Prior studies have shown, etc.)

---

## VI. Hard Constraints (English)

| Constraint | Hard Limit | Description |
|------------|------------|-------------|
| AI high-freq words | ≤ 3 per paragraph | Replace excess |
| Em dashes | 0 in entire text | Replace with commas/parentheses |
| Rule of Three | ≤ 1 per paragraph | Break symmetry |
| "This suggests/highlights" openers | ≤ 2 per page | Vary subjects |
| Filler phrases | 0 in entire text | Delete |
| Generic conclusions | 0 in entire text | Replace with specific claim |
| Vague attribution | 0 in entire text | Cite or delete |
| Significance filler | ≤ 2 per page | Delete or replace with data |
