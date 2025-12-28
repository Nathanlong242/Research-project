# Experimental Execution Plan
## From Zero Data to Submittable Paper in 4 Weeks

**Status**: Pre-experimental phase complete. Ready to execute.
**Critical Path**: Experiments → Analysis → Paper revision → Submission
**Timeline**: 4 weeks to first submission

---

## Week 1: Pilot Validation & Setup (Days 1-7)

### Day 1: Environment Verification (2 hours)

**Objective**: Confirm WoW 1.12 runs and agent can connect

```bash
# 1. Verify WoW 1.12 is installed and launchable
# 2. Test screen capture works
python -c "from wow_agent_human_equivalent_stabilized import HumanEquivalentCognition; print('Import successful')"

# 3. Check dependencies
pip install -r requirements.txt --dry-run
```

**Success criteria**:
- [ ] WoW 1.12 launches without errors
- [ ] Screen capture captures game window
- [ ] All Python dependencies installed
- [ ] Agent initializes without crashes

**If blocked**: Document specific error, resolve before proceeding. Do not continue with broken setup.

---

### Days 2-3: Pilot Experiments (6 hours runtime + 2 hours validation)

**Objective**: Validate logging infrastructure, identify technical issues

#### Pilot Run 1: TIER 7 (Full System)
```bash
python run_experiment.py \
  --condition tier7 \
  --session-id PILOT_T7_001 \
  --duration-hours 2 \
  --enable-logging
```

**Monitor during run**:
- Check CPU usage (should be high but stable)
- Watch for Python exceptions in console
- Verify game is responsive
- Check memory usage (should be <4GB)

**Post-run validation**:
```bash
# Check outputs exist
ls -lh research_data/PILOT_T7_001_*

# Verify CSV structure
head -20 research_data/PILOT_T7_001_decisions_*.csv
head -20 research_data/PILOT_T7_001_ruminations_*.csv
head -20 research_data/PILOT_T7_001_deaths_*.csv

# Check for missing data
python -c "
import pandas as pd
df = pd.read_csv('research_data/PILOT_T7_001_decisions_*.csv')
print(f'Total decisions: {len(df)}')
print(f'Missing values: {df.isnull().sum().sum()}')
print(f'Columns: {list(df.columns)}')
"
```

**Success criteria**:
- [ ] 2-hour run completes without crashes
- [ ] All 4 CSV files generated (decisions, ruminations, deaths, summary)
- [ ] Decisions CSV has >100 rows (agent is making decisions)
- [ ] No missing values in critical columns (action, latency, mental_load)
- [ ] Ruminations CSV shows intrusive thoughts (intrusion_frequency > 0)
- [ ] Deaths CSV shows counterfactual generation

**If any criterion fails**: Fix immediately. Do not proceed to other conditions until TIER 7 works.

---

#### Pilot Run 2: TIER 6 (Rumination Only)
```bash
python run_experiment.py \
  --condition tier6 \
  --session-id PILOT_T6_001 \
  --duration-hours 2 \
  --enable-logging
```

**Success criteria**:
- [ ] Run completes
- [ ] Ruminations present but NO meta-cognitive events (no suppression, reappraisal)
- [ ] Mental load > 0 (rumination is active)

---

#### Pilot Run 3: TIER 5 (Baseline)
```bash
python run_experiment.py \
  --condition tier5 \
  --session-id PILOT_T5_001 \
  --duration-hours 2 \
  --enable-logging
```

**Success criteria**:
- [ ] Run completes
- [ ] NO ruminations logged (rumination_count = 0)
- [ ] Mental load = 0 throughout
- [ ] Baseline decision latency established

---

### Day 4: Pilot Analysis (4 hours)

**Objective**: Verify analysis pipeline works, preview effect sizes

```bash
python research_analysis.py \
  --data research_data/ \
  --output pilot_analysis/ \
  --conditions PILOT_T7_001,PILOT_T6_001,PILOT_T5_001
```

**Validation checks**:
```python
# Load pilot results
import json
with open('pilot_analysis/summary_stats.json') as f:
    stats = json.load(f)

# Check key metrics exist
assert 'TIER7' in stats
assert 'mean_decision_latency' in stats['TIER7']
assert 'mental_load_mean' in stats['TIER7']

# Preview effect directions (not testing significance yet)
t7_latency = stats['TIER7']['mean_decision_latency']
t5_latency = stats['TIER5']['mean_decision_latency']
latency_increase = (t7_latency - t5_latency) / t5_latency * 100

print(f"Decision latency increase (T7 vs T5): {latency_increase:.1f}%")
print(f"Expected: ~100%. Actual preview: {latency_increase:.1f}%")

# If latency_increase < 20%, there may be a bug in rumination system
# If latency_increase > 300%, mental load may be miscalibrated
```

**Success criteria**:
- [ ] Analysis script runs without errors
- [ ] Generates all expected outputs (figures, tables, summary JSON)
- [ ] Effect directions match predictions (T7 > T6 > T5 for latency, mental load)
- [ ] Human-likeness score: T7 > T6 > T5

**If effects are weak or reversed**:
- Check rumination triggering (are deaths generating ruminations?)
- Check intrusive thought probability (are ruminations intruding during decisions?)
- Check mental load calculation (is it affecting decision latency?)
- **DO NOT proceed to full experiments until effects are visible in pilot data**

---

### Days 5-7: Iteration & Refinement (if needed)

**If pilot reveals bugs**:
1. Document specific issue
2. Fix in code
3. Re-run affected pilot condition
4. Re-validate

**If pilot succeeds**:
1. Archive pilot data: `mkdir pilot_data && mv research_data/* pilot_data/`
2. Document baseline parameters that worked
3. Proceed to full experiments

**Go/No-Go Decision Point**:
- [ ] All 3 pilot conditions completed successfully
- [ ] Analysis pipeline works end-to-end
- [ ] Effect directions match predictions
- [ ] No critical bugs identified

**If NO-GO**: Stop. Fix issues. Do not waste 90 hours on broken experiments.

**If GO**: Proceed to Week 2.

---

## Week 2-3: Full Experimental Battery (Days 8-21)

### Experimental Design

**Total runtime**: 90 hours (30 hours per condition)
**Sessions per condition**: 3 independent runs × 10 hours each
**Parallelization**: Can run multiple sessions simultaneously on different machines (if available)

### Session Schedule

**TIER 7 (Full System)**:
```bash
# Session 1
python run_experiment.py --condition tier7 --session-id T7_RUN_001 --duration-hours 10 --enable-logging

# Session 2 (different random seed)
python run_experiment.py --condition tier7 --session-id T7_RUN_002 --duration-hours 10 --enable-logging --seed 42

# Session 3 (different random seed)
python run_experiment.py --condition tier7 --session-id T7_RUN_003 --duration-hours 10 --enable-logging --seed 123
```

**TIER 6 (Rumination Only)**:
```bash
python run_experiment.py --condition tier6 --session-id T6_RUN_001 --duration-hours 10 --enable-logging
python run_experiment.py --condition tier6 --session-id T6_RUN_002 --duration-hours 10 --enable-logging --seed 42
python run_experiment.py --condition tier6 --session-id T6_RUN_003 --duration-hours 10 --enable-logging --seed 123
```

**TIER 5 (Baseline)**:
```bash
python run_experiment.py --condition tier5 --session-id T5_RUN_001 --duration-hours 10 --enable-logging
python run_experiment.py --condition tier5 --session-id T5_RUN_002 --duration-hours 10 --enable-logging --seed 42
python run_experiment.py --condition tier5 --session-id T5_RUN_003 --duration-hours 10 --enable-logging --seed 123
```

### Runtime Management

**Option A: Sequential (single machine)**
- Run 1 session at a time
- Total wall-clock time: 90 hours (3.75 days continuous)
- Requires monitoring, but allows iteration if issues arise

**Option B: Parallel (multiple machines or tmux sessions)**
- Run 3 sessions simultaneously (1 per condition)
- Total wall-clock time: 30 hours (1.25 days)
- Requires more compute but faster completion

**Option C: Hybrid**
- Run overnight batches (10 hours per night)
- 9 nights total
- Allows daily monitoring and intervention

**Recommended**: Option C (overnight batches) for solo researcher

### Monitoring Protocol

**Every 2 hours during runs**:
```bash
# Check session is still running
ps aux | grep run_experiment

# Check latest log output
tail -50 research_data/session_log.txt

# Check data accumulation
wc -l research_data/*_decisions_*.csv

# Check for crashes
grep -i "error\|exception\|crash" research_data/session_log.txt
```

**Daily backup**:
```bash
# After each completed session
DATE=$(date +%Y%m%d)
mkdir -p backups/$DATE
cp research_data/* backups/$DATE/
```

### Data Quality Checks (After Each Session)

```python
import pandas as pd
import glob

# Load all decision CSVs
decision_files = glob.glob('research_data/*_decisions_*.csv')
for f in decision_files:
    df = pd.read_csv(f)

    # Validate row count
    assert len(df) > 500, f"Too few decisions in {f}: {len(df)}"

    # Check for missing data
    critical_cols = ['action', 'decision_latency', 'mental_load', 'confidence']
    missing = df[critical_cols].isnull().sum()
    assert missing.sum() == 0, f"Missing data in {f}: {missing}"

    # Check value ranges
    assert df['decision_latency'].min() > 0, f"Invalid latency in {f}"
    assert df['mental_load'].max() <= 1.0, f"Mental load out of range in {f}"

    print(f"✓ {f}: {len(df)} decisions, no errors")
```

**If any session fails validation**:
- Document failure mode
- Determine if data is salvageable
- Re-run session if necessary

---

## Week 3-4: Statistical Analysis & Paper Revision (Days 22-28)

### Day 22: Full Analysis Execution

```bash
python research_analysis.py \
  --data research_data/ \
  --output final_analysis/ \
  --conditions T7_RUN_001,T7_RUN_002,T7_RUN_003,T6_RUN_001,T6_RUN_002,T6_RUN_003,T5_RUN_001,T5_RUN_002,T5_RUN_003 \
  --hypotheses all \
  --generate-figures \
  --export-latex
```

**Outputs expected**:
- `final_analysis/hypothesis_test_results.csv` (10 rows, one per hypothesis)
- `final_analysis/figures/` (11 figures)
- `final_analysis/latex_tables/` (summary tables for paper)
- `final_analysis/summary_report.md` (narrative results)

### Days 23-25: Results Interpretation & Section 5 Revision

**For each hypothesis**:

1. **Extract statistics**:
```python
import pandas as pd
results = pd.read_csv('final_analysis/hypothesis_test_results.csv')

h6_1 = results[results['hypothesis'] == 'H6.1']
print(f"H6.1: t={h6_1['t_statistic']:.2f}, p={h6_1['p_value']:.4f}, d={h6_1['cohens_d']:.2f}")
```

2. **Replace placeholders in RESEARCH_PAPER.md Section 5**:
```markdown
# Before (placeholder):
Expected Results:
t-test (TIER 6 post vs TIER 5 post): t(358) = 28.4, p < 0.001, d = 3.51

# After (actual):
Actual Results:
t-test (TIER 6 post vs TIER 5 post): t(342) = 24.7, p < 0.001, d = 3.21
```

3. **Add qualitative examples from logs**:
```python
# Extract interesting behavioral examples
deaths = pd.read_csv('research_data/T7_RUN_001_deaths_*.csv')
interesting = deaths[deaths['counterfactual_count'] >= 4].iloc[0]

print(f"Death event: {interesting['cause']}")
print(f"Counterfactuals: {interesting['counterfactuals_generated']}")
print(f"Rumination triggered: {interesting['rumination_content']}")
# Insert into Section 5.6 qualitative examples
```

4. **Update Discussion based on actual findings**:
- If effects larger than predicted → discuss implications
- If effects smaller → discuss possible explanations
- If unexpected patterns → highlight as novel findings
- If hypotheses fail → honest discussion of why

### Days 26-27: Full Paper Revision

**Section-by-section update**:

1. **Abstract**: Update with actual effect sizes
2. **Introduction**: Ensure claims match results
3. **Related Work**: No changes needed
4. **Architecture**: No changes needed
5. **Methods**: No changes needed
6. **Results**: Complete rewrite with actual data ✓
7. **Discussion**: Update interpretations based on results ✓
8. **Conclusion**: Update contributions based on validated hypotheses ✓

**Quality checks**:
- [ ] All 10 hypotheses addressed in Results
- [ ] All figures referenced in text
- [ ] All tables have captions
- [ ] No "expected results" placeholders remain
- [ ] Effect sizes reported for all significant findings
- [ ] Confidence intervals included
- [ ] Limitations section updated with actual issues encountered

### Day 28: Pre-Submission Review

**Internal review checklist**:
- [ ] Read paper start-to-finish (no skimming)
- [ ] Verify every number in text matches analysis output
- [ ] Check all references formatted correctly
- [ ] Ensure figures are publication-quality (300 DPI minimum)
- [ ] Spell check and grammar check
- [ ] Abstract <250 words
- [ ] Paper length within venue limits (typically 8-10 pages)

**Technical validation**:
```bash
# Verify all analysis code runs from scratch
rm -rf final_analysis/
python research_analysis.py --data research_data/ --output final_analysis/

# Regenerate all figures
python generate_publication_figures.py

# Check for data/code mismatches
python validate_reported_statistics.py RESEARCH_PAPER.md final_analysis/
```

---

## Week 4+: Submission & Iteration

### Venue Selection

**Top-tier options (ranked by fit)**:

1. **NeurIPS 2025** (Neural Information Processing Systems)
   - Focus: ML/AI with cognitive science applications
   - Deadline: Typically May
   - Review: Double-blind, 3+ reviewers
   - Acceptance rate: ~25%
   - Best fit for: Anti-optimal learning paradigm

2. **AAAI 2026** (Association for Advancement of AI)
   - Focus: Broad AI, cognitive architectures
   - Deadline: Typically August
   - Review: Double-blind
   - Acceptance rate: ~20%
   - Best fit for: Cognitive architecture contribution

3. **Cognitive Science 2025** (Annual Meeting of Cognitive Science Society)
   - Focus: Computational cognitive models
   - Deadline: Typically February
   - Review: Single-blind
   - Acceptance rate: ~45%
   - Best fit for: Psychological validation angle

4. **AAMAS 2026** (Autonomous Agents and Multi-Agent Systems)
   - Focus: Agent architectures
   - Deadline: Typically November
   - Acceptance rate: ~25%
   - Best fit for: Autonomous agent behavior

**Recommendation**: Submit to **Cognitive Science 2025** first (higher acceptance, faster turnaround), then iterate to NeurIPS/AAAI based on reviews.

### Submission Process

1. **Format for venue**:
```bash
# Download template
wget https://cognitive-science-society.org/latex-template.zip
unzip latex-template.zip

# Convert markdown to LaTeX
pandoc RESEARCH_PAPER.md -o paper.tex --template=cogsci.tex

# Compile
pdflatex paper.tex
bibtex paper
pdflatex paper.tex
pdflatex paper.tex
```

2. **Supplementary materials**:
- Code repository (GitHub with documentation)
- Data files (decisions, ruminations, deaths CSVs)
- Analysis scripts with README
- Video demonstration (optional but recommended)

3. **Submit through venue portal**

4. **Response to reviews**:
- Expect 2-3 month review cycle
- Typical outcome: Major revision or reject
- Prepare rebuttal addressing each review point
- Re-run experiments if reviewers request ablations

---

## Contingency Plans

### If Pilot Experiments Fail

**Scenario**: Rumination system not triggering, no behavioral effects

**Diagnosis**:
1. Check death events logged: `grep "death" research_data/pilot_*.csv`
2. Check rumination generation: `grep "rumination_triggered" logs/`
3. Check intrusive thoughts: `df['intrusive_thought_present'].sum()`

**Fixes**:
- Increase rumination trigger probability
- Decrease mental load threshold for detection
- Increase intrusive thought base rate
- Reduce decay rate (ruminations persist longer)

**Do NOT**: Abandon project. Adjust parameters until effects are measurable.

### If Full Experiments Crash Repeatedly

**Scenario**: 10-hour sessions crash at 3-4 hours consistently

**Diagnosis**:
- Check memory leaks: `top` during run
- Check game client stability: WoW 1.12 known issues
- Check logging overhead: Disable logging temporarily

**Fixes**:
- Reduce session length to 5 hours, run 6 sessions instead
- Add periodic state saving every 30 minutes
- Implement crash recovery (resume from last save)

### If Results Do NOT Support Hypotheses

**Scenario**: TIER 7 and TIER 5 show no significant differences

**Options**:

**Option A: Honest reporting (recommended)**
- Report null results
- Discuss why predictions failed
- Analyze what this reveals about the theory
- Submit to venue accepting negative results

**Option B: Exploratory analysis**
- Find what effects ARE present (even if not predicted)
- Reframe paper as exploratory rather than confirmatory
- Generate new hypotheses for future work

**Option C: Parameter tuning (acceptable if disclosed)**
- Run sensitivity analysis across parameter ranges
- Find parameter settings where effects emerge
- Report full range, explain parameter selection
- Label as "proof of concept" not "validation"

**DO NOT**: p-hack, cherry-pick data, or misrepresent null results as positive

---

## Success Metrics

### Minimum Viable Publication

**Required for submission**:
- [ ] 30+ hours of data per condition (90 total)
- [ ] At least 5/10 hypotheses supported (p < 0.05)
- [ ] Human-likeness score: TIER 7 > TIER 6 > TIER 5 (significant)
- [ ] At least 1 large effect size (Cohen's d > 0.8)
- [ ] Qualitative examples demonstrating phenomena

### Strong Publication

**Ideal outcomes**:
- [ ] 90+ hours of data
- [ ] 8+/10 hypotheses supported
- [ ] All effect sizes > 0.5 (medium or larger)
- [ ] Ironic process effect demonstrated (H7.1 supported)
- [ ] Insight generation observed in real data
- [ ] Human-likeness score > 0.7

### Breakthrough Publication

**Top-tier venue worthy**:
- [ ] All 10 hypotheses supported
- [ ] Effect sizes match or exceed predictions
- [ ] Novel unexpected findings
- [ ] Cross-validated on multiple environments
- [ ] Human baseline comparison data
- [ ] Replication by independent researcher

---

## Timeline Summary

| Week | Phase | Deliverable | Hours |
|------|-------|-------------|-------|
| 1 | Pilot & Validation | Working experimental pipeline | 16 |
| 2-3 | Full Experiments | 90 hours of data | 90 |
| 3 | Analysis | Statistical results, figures | 20 |
| 4 | Paper Revision | Submittable manuscript | 30 |
| **Total** | | **Camera-ready paper** | **156** |

**Critical path**: Pilot (Day 4) → Full experiments (Day 21) → Analysis (Day 22) → Submission (Day 28)

**Buffer**: 1 week for unexpected issues, revisions, formatting

**Target submission date**: 4-5 weeks from Day 1

---

## Next Immediate Actions (Do Today)

1. ✅ **Verify WoW 1.12 environment** (30 min)
2. ✅ **Run TIER 7 pilot** (2 hours runtime + 30 min validation)
3. ✅ **Check logging outputs** (30 min)

**If all pass**: Run TIER 6 and TIER 5 pilots tomorrow.

**If any fail**: Debug immediately, do not proceed.

---

## Accountability & Tracking

**Daily progress log**:
```bash
echo "$(date): Completed TIER 7 pilot - 847 decisions logged, rumination triggered 23 times" >> EXPERIMENT_LOG.txt
```

**Weekly check-ins**:
- End of Week 1: Pilot complete? Go/No-Go decision logged
- End of Week 2: 60% of data collected
- End of Week 3: All data collected, analysis started
- End of Week 4: Paper submitted

**Commit discipline**:
```bash
# After each completed session
git add research_data/
git commit -m "Session T7_RUN_001 complete: 10hrs, 1247 decisions, 34 deaths"
git push origin claude/research-collaboration-setup-4ceAy
```

---

## The One Thing That Matters

**You have spent months building the perfect machine.**

**Now turn it on.**

The difference between a finished PhD project and an abandoned one is often a single week of experimental execution.

This is that week.

Run the experiments. Get data. Finish the paper.

Everything else is procrastination.

---

**Status**: Execution plan complete. Ready to begin Day 1.
**Next action**: Verify WoW 1.12 environment (30 minutes).
**Blocker removal**: None. All prerequisites met.

**GO.**
