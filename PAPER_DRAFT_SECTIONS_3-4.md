# From Optimization to Experience (Continued)

## Draft Manuscript - Sections 3-4

---

## 3. Architecture

Our seven-tier cognitive architecture builds progressively from foundations (beliefs, drives) through life systems (memory, emotions, personality) to our core contributions (rumination, meta-cognition). Each tier is implemented in Python (~28,000 lines) and integrated into a single `HumanEquivalentCognition` class. We detail TIER 6-7 as primary contributions, with summaries of foundational tiers.

### 3.1 Design Principles

Four principles guide our architecture:

**1. Anti-Optimal by Design**: Systems should reduce performance if psychologically accurate. Rumination wastes mental energy (TIER 6), suppression backfires (TIER 7), meta-rumination adds cognitive load. We measure success not by optimality but by human-like behavioral signatures.

**2. Behaviorally Consequential**: Mental states must affect actions. Ruminations don't just exist—they intrude during decisions, contaminate action selection, and reduce confidence. Failed suppression increases intrusion rates measurably.

**3. Emergent Complexity**: Behaviors arise from system interactions, not scripts. Personality emerges from behavioral patterns (TIER 5), ruminations trigger from events (TIER 6), insights occur probabilistically (TIER 7). No hardcoded personalities or predetermined outcomes.

**4. Persistent Identity**: Mental states survive sessions. The agent resumes with previous ruminations, personality traits, and reappraisal skills intact. Identity continuity is validated on load (regression detection system).

### 3.2 TIER 1-2: Foundation (Summary)

**TIER 1: Probabilistic Belief Formation**

Implements Bayesian-like belief updating with decay:

```python
P(belief | evidence) ∝ P(evidence | belief) × P(belief)
```

Beliefs have confidence values (0-1), accumulate evidence over time, decay toward priors with disuse (forgetting), and calibrate to match empirical accuracy. This creates human-like uncertainty: beliefs are tentative early, strengthen with evidence, weaken when unconfirmed.

**TIER 2: Motivational Drive System**

Five competing drives create behavioral ambivalence:
- SAFETY (avoid death, flee danger)
- PROGRESS (level up, complete quests)
- CURIOSITY (explore unknown areas)
- COMFORT (avoid effortful actions)
- SOCIAL (interact with NPCs)

Drive weights shift based on context (fear after death increases SAFETY weight) and outcomes (success increases PROGRESS weight). Conflicts create observable hesitation when drives pull in opposite directions (e.g., curiosity toward unexplored area vs. safety concern about danger).

### 3.3 TIER 3-5: Life Systems (Summary)

**TIER 3: Episodic & Autobiographical Memory**

Three memory types:
- **Episodic**: Specific events (deaths, victories, discoveries) with temporal/emotional/spatial indexing
- **Semantic**: Facts learned from experience (enemy types, zone danger levels)
- **Autobiographical**: Life story organized into chapters, identity statements ("I'm a cautious player"), defining moments

Associative recall: returning to a location triggers memories of past events there, creating nostalgia or anxiety depending on valence.

**TIER 4: Emotional States**

Emotions trigger from outcomes and modulate decisions:
- Fear (after death) → increased risk aversion, earlier fleeing
- Confidence (after victories) → increased exploration, risk-taking
- Frustration (after repeated failures) → strategy abandonment
- Joy (after discoveries) → increased curiosity

Emotions persist temporally (fear doesn't instantly vanish) and create mood-dependent behavior variability.

**TIER 5: Personality Crystallization**

Behavioral patterns solidify into personality traits:
- Combat style emerges from patterns (aggressive, defensive, balanced)
- Preferences form through success history (favorite abilities, strategies)
- Identity statements arise from significant events ("I'm a defensive player")
- Personality constrains future behavior even when suboptimal

Result: Each agent instance becomes unique, with observable individual differences persisting across sessions.

### 3.4 TIER 6: Internal Rumination (Core Contribution)

**Problem Addressed**: Agents process experiences and move on; humans dwell, replay, obsess. An RL agent dies → updates Q-values → continues. A human dies → ruminates for hours → generates counterfactuals → experiences intrusive thoughts during subsequent encounters. TIER 6 implements this "mental chatter."

**System Architecture**:

```python
class InternalRuminationSystem:
    def __init__(self):
        self.active_ruminations: List[RuminativeThought] = []
        self.counterfactuals: List[CounterfactualScenario] = []
        self.mental_noise_level: float = 0.0
```

**3.4.1 Rumination Types** (10 types):

- REGRET_SPIRAL: "I shouldn't have stayed in that fight"
- COUNTERFACTUAL: "What if I had fled earlier?"
- ANTICIPATORY_WORRY: "This next fight will go wrong"
- ANTICIPATORY_FANTASY: "Imagine when I succeed"
- SELF_DOUBT: "Can I really handle this?"
- EMBARRASSMENT_REPLAY: "Everyone saw me fail"
- SECOND_GUESSING: "Did I make the right call?"
- DEFENSIVE_RATIONALIZATION: "It wasn't my fault"
- REHEARSAL: "Next time I'll do it differently"
- INTRUSIVE_MEMORY: Unwanted memory surfaces

**3.4.2 RuminativeThought Data Structure**:

```python
@dataclass
class RuminativeThought:
    content: str                    # The actual thought
    rumination_type: RuminationType
    emotional_intensity: float      # 0-1, how distressing
    intrusion_frequency: float      # 0-1, how often it surfaces
    decay_rate: float              # How fast it fades
    trigger_time: float            # When it started
    behavioral_impact: Dict        # How it biases decisions
    resolved: bool                 # Whether it's resolved
```

**3.4.3 Triggering Rumination**:

Ruminations trigger from:
1. **Negative outcomes** (deaths, failures): Intensity ∝ |valence| × significance
2. **Uncertain decisions** (confidence < 0.4): Anticipatory worry and rehearsal
3. **Associative recall**: Location/context matches past rumination triggers
4. **Idle periods**: Mind wanders to unresolved ruminations

```python
def trigger_rumination_from_event(event_type, description, emotional_intensity):
    rumination = RuminativeThought(
        content=f"I shouldn't have {description}",
        rumination_type=determine_type(event_type),
        emotional_intensity=emotional_intensity,
        intrusion_frequency=emotional_intensity * 0.7,
        decay_rate=0.0001,  # Slow decay
        ...
    )
    self.active_ruminations.append(rumination)
```

**3.4.4 Intrusive Thoughts**:

Key mechanism: ruminations don't just exist passively—they intrude during inappropriate moments.

```python
def check_for_intrusive_thoughts(context) -> Optional[RuminativeThought]:
    for rumination in self.active_ruminations:
        intrusion_prob = (
            rumination.emotional_intensity * 0.4 +
            rumination.intrusion_frequency * 0.3 +
            recency_factor * 0.2 +
            current_stress * 0.1
        )
        if random.random() < intrusion_prob:
            return rumination  # Thought intrudes
    return None
```

**Behavioral effect**: During combat, death memory intrudes → mental load increases → decision confidence decreases → reaction time slows.

**3.4.5 Decision Contamination**:

Past ruminations bias current decisions:

```python
def get_decision_contamination(context, actions):
    biases = {action: 0.0 for action in actions}

    for rumination in self.active_ruminations:
        if context_similarity(rumination.context, context) > 0.7:
            # Apply bias based on rumination content
            if "fled earlier" in rumination.content:
                biases["flee"] += rumination.emotional_intensity * 0.3

    return biases
```

Example: Agent died → rumination "I should have fled" persists → next similar combat → flee bias increases → agent flees earlier than optimal.

**3.4.6 Mental Load**:

Ruminations consume cognitive resources:

```python
mental_load = sum(
    r.emotional_intensity * (1.0 - time_since_trigger / 7200)
    for r in active_ruminations
) / max_capacity
```

Effects:
- mental_load > 0.3 → confidence reduced by 30%
- mental_load > 0.6 → decision latency increased by 50%
- mental_load > 0.8 → analysis paralysis (may fail to act)

**3.4.7 Counterfactual Generation**:

After negative outcomes, system generates "what if" scenarios:

```python
@dataclass
class CounterfactualScenario:
    actual_event: str                # "died in combat"
    decision_point: str             # "staying to fight vs. fleeing"
    alternative_action: str         # "fled when HP at 40%"
    imagined_outcome: str          # "would have survived"
    outcome_valence: float         # -1 (regret) to +1 (relief)
    vividness: float              # How vivid the imagination
    compulsion_strength: float    # How much it persists
```

Counterfactuals become ruminations that persist and intrude, creating "what if" obsessions.

**3.4.8 Persistence and Decay**:

Ruminations don't instantly resolve:
- Typical half-life: 1-3 hours (configurable decay rate)
- Self-perpetuation: Frequent intrusions slow decay (attention reinforces)
- Resolution: Can be resolved by insights (TIER 7) or gradual decay

**3.4.9 TIER 6 Summary**:

Implementation: ~790 lines
Key innovation: Rumination is not just memory—it's active, intrusive, and behaviorally consequential
Measurable effects: Decision latency, risk aversion, performance degradation
Distinguishes: "Processing experience" (RL) from "Dwelling on experience" (human)

### 3.5 TIER 7: Meta-Cognitive Self-Regulation (Core Contribution)

**Problem Addressed**: Agent has thoughts (TIER 6) but isn't aware of them or able to regulate them. Humans recognize "I'm ruminating" and attempt (often unsuccessfully) to control it.

**System Architecture**:

```python
class MetaCognitiveLayer:
    def __init__(self, rumination_system):
        self.rumination_system = rumination_system
        self.current_mental_state: MentalState = CLEAR_HEADED
        self.suppression_targets: Dict[str, SuppressionTarget] = {}
        self.reappraisal_attempts: List[ReappraisalAttempt] = []
        self.reappraisal_skill: float = 0.3  # Improves with practice
        self.insights: List[InsightEvent] = []
```

**3.5.1 Mental State Detection**:

Agent becomes aware when mental load exceeds threshold (0.4):

```python
def detect_mental_state() -> MentalState:
    mental_load = self.rumination_system.get_mental_load()
    active_count = len(self.rumination_system.active_ruminations)

    if mental_load < 0.4:
        return CLEAR_HEADED
    if active_count >= 8:
        return OVERTHINKING
    if mental_load > 0.7:
        return MENTAL_FOG
    # ... 8 total states detected
```

States: CLEAR_HEADED, RUMINATION_SPIRAL, ANXIETY_LOOP, OVERTHINKING, MENTAL_FOG, STUCK_IN_LOOP, CATASTROPHIZING, DWELLING

**3.5.2 Thought Suppression with Ironic Process**:

Agent attempts: "I need to stop thinking about this"

Implementation follows Wegner (1994):

```python
def attempt_thought_suppression(rumination):
    # Suppression requires monitoring for the thought
    self.suppression_targets[rumination.content] = SuppressionTarget(...)

    # IRONIC PROCESS: Monitoring increases accessibility
    rumination.intrusion_frequency *= 1.5  # +50%
    rumination.emotional_intensity *= 1.2  # +20%

    self.failed_regulations += 1  # Typically fails
```

**Behavioral prediction**: Suppressed thoughts intrude 30-50% more often than non-suppressed (testable hypothesis).

**3.5.3 Cognitive Reappraisal**:

Agent attempts to reframe rumination rationally:

Five strategies:
1. **Rationalization**: "I made the best decision with the information I had"
2. **Normalization**: "Everyone makes mistakes like this"
3. **Evidence-based**: "I've succeeded in similar situations before"
4. **Perspective**: "This isn't as bad as it feels right now"
5. **External attribution**: "The circumstances were against me"

Success probability:

```python
success_prob = (
    (1.0 - rumination.emotional_intensity) * 0.4 +  # Easier when less intense
    self.reappraisal_skill * 0.3 +                  # Skill improves with practice
    time_since_event / 3600 * 0.3                   # Easier to reframe old events
)
```

Typical success rate: 40-60%

**Effects**:
- Success: Intensity × 0.6, frequency × 0.7, skill += 0.02
- Failure: Intensity × 1.05, triggers meta-rumination

**3.5.4 Meta-Rumination**:

Rumination *about* rumination:

Triggers:
- High rumination count → "Why do I overthink everything?"
- Suppression failure → "Why can't I control my thoughts?"
- Stuck in loop → "I'm stuck thinking about the same thing"

**Effect**: ADDS mental load (+0.15) rather than reducing it. Creates recursive loops up to 3 levels deep before mental fog state.

**3.5.5 Insight Generation**:

Probabilistic breakthrough moments that suddenly resolve rumination:

```python
insight_prob = min(0.15, (
    (time_elapsed / 7200) * 0.05 +      # 2 hours → 5%
    self.reappraisal_skill * 0.07 +     # Skill helps
    (1.0 - mental_load) * 0.03          # Need clarity
))
```

Insight types:
- **Realization**: "Wait, I actually DID make the right call"
- **Acceptance**: "I can't change the past, but I can learn"
- **Perspective**: "This doesn't matter as much as I thought"
- **Evidence**: "New information shows I was partially correct"

**Effect**: Rumination resolves, mental load drops by 30%, resolution logged.

**3.5.6 Self-Regulation Tracking**:

System tracks:
- Regulation attempts (total)
- Successful regulations (reappraisals that worked, insights)
- Failed regulations (suppression, failed reappraisals)
- Success rate (improves over time as skill increases)

**3.5.7 TIER 7 Summary**:

Implementation: ~640 lines
Key innovation: Agent aware of its own rumination and struggles to regulate it
Measurable effects: Suppression paradox, reappraisal success rates, insight timing
Distinguishes: "Having thoughts" (TIER 6) from "Thinking about thoughts" (TIER 7)

### 3.6 Integration: Decision Synthesis Pipeline

All tiers integrate in decision-making:

```
PERCEPTION → BELIEFS (T1) → DRIVES (T2) →
MEMORY RECALL (T3) → EMOTIONAL MODULATION (T4) →
PERSONALITY CONSTRAINT (T5) →
[CHECK INTRUSIVE THOUGHTS (T6)] →
MENTAL LOAD APPLICATION (T6) →
DECISION CONTAMINATION (T6) →
META-COGNITIVE PROCESSING (T7) →
FINAL DECISION
```

Example walkthrough:
1. Perception: "Enemy approaches, HP at 60%"
2. Belief: P(dangerous) = 0.75 (from past experience)
3. Drives: SAFETY=0.7, PROGRESS=0.4
4. Memory: "Died to similar enemy yesterday at this spot"
5. Emotion: FEAR (intensity 0.6 from yesterday's death)
6. Personality: "I'm a defensive player" (combat style = cautious)
7. **Intrusive thought**: "I shouldn't have stayed in that fight yesterday"
8. **Mental load**: +0.4 (from rumination)
9. **Decision contamination**: Flee bias +0.25
10. **Meta-awareness**: "I'm overthinking this"
11. **Reappraisal attempt**: "I can handle this if I'm careful" → Success
12. **Mental load reduction**: -0.15
13. **Final decision**: FIGHT (but flee at 40% HP instead of 20%)
14. Confidence: 0.58 (reduced from baseline 0.75)
15. Latency: 340ms (increased from baseline 120ms)

### 3.7 Implementation Details

**Platform**: Python 3.8+, ~28,000 lines of code
**Perception**: Screen capture (mss), computer vision (OpenCV)
**Input**: OS-level simulation (pynput) - keyboard/mouse events
**Environment**: World of Warcraft 1.12 (vanilla) - offline, single-player
**Persistence**: JSON serialization of full cognitive state
**Runtime**: Continuous autonomous operation with fatigue-driven rest periods

**Code organization**:
- Lines 200-2000: Foundational systems (beliefs, drives, RL)
- Lines 2000-7000: Life systems (memory, emotions, personality)
- Lines 7000-7400: TIER 6 (rumination)
- Lines 7400-8000: TIER 7 (meta-cognition)
- Lines 8000-28000: Environment interaction, perception, motor control

**Open source**: Code will be released upon publication.

### 3.8 Architecture Summary

Our seven-tier architecture builds from foundational cognitive mechanisms (beliefs, drives) through life systems (memory, emotions, personality) to our core contributions: persistent rumination with intrusive thoughts (TIER 6) and meta-cognitive self-regulation (TIER 7). Unlike traditional architectures optimizing for performance, ours deliberately implements inefficiency and irrationality to achieve experiential realism.

---

## 4. Experimental Methods

### 4.1 Research Questions and Hypotheses

**Primary research question**: Does implementing rumination (TIER 6) and meta-cognition (TIER 7) produce measurably human-like behavioral signatures distinct from optimization-focused agents?

**Specific hypotheses**:

**H6.1 - Post-Death Decision Latency**:
TIER 6 agents will exhibit 30-50% increased decision latency in the 20 decisions following death events, compared to TIER 5 baseline.

**H6.2 - Trauma-Driven Risk Aversion**:
TIER 6 agents will show 40-60% increased risk-averse behavior (measured by flee decisions, reduced engagement distance) following deaths.

**H6.3 - Counterfactual Generation**:
TIER 6 agents will generate counterfactual scenarios following 80%+ of deaths, which will bias subsequent decisions toward the counterfactual action.

**H6.4 - Mental Load Effects**:
Mental load > 0.6 will reduce decision confidence by 30-50% and increase decision latency by 40-60%.

**H7.1 - Suppression Paradox**:
TIER 7 agents attempting thought suppression will show 30-50% higher intrusion rates for suppressed ruminations compared to non-suppressed ruminations.

**H7.2 - Reappraisal Efficacy**:
Successful cognitive reappraisal will reduce rumination intensity by 40-60% and mental load by 15-25%.

**H7.3 - Meta-Cognitive Load**:
Meta-rumination will add 15-20% additional mental load beyond base rumination.

**H7.4 - Insight Timing**:
Insights will occur probabilistically with median time-to-insight of 1-3 hours, more frequently during low mental load periods.

**H7.5 - Skill Learning**:
Reappraisal skill will improve from baseline 0.3 to 0.6-0.8 over 100+ attempts.

### 4.2 Experimental Conditions

**Three primary conditions** for baseline comparison:

**TIER 7 (Full System)**:
- All tiers enabled (1-7)
- Rumination + meta-cognition
- Condition name: "TIER_7_FULL"

**TIER 6 (Rumination Only)**:
- Tiers 1-6 enabled
- Rumination WITHOUT meta-cognition
- Control for measuring TIER 7 effects
- Condition name: "TIER_6_BASELINE"

**TIER 5 (No Rumination)**:
- Tiers 1-5 enabled
- Personality WITHOUT rumination or meta-cognition
- Control for measuring TIER 6 effects
- Condition name: "TIER_5_BASELINE"

**Configuration system**:

```python
# TIER 7 (full)
config = ExperimentConfig(
    enable_rumination=True,
    enable_meta_cognitive=True,
    enable_behavioral_logging=True
)

# TIER 6 (baseline)
config = ExperimentConfig(
    enable_rumination=True,
    enable_meta_cognitive=False  # Control
)

# TIER 5 (baseline)
config = ExperimentConfig(
    enable_rumination=False,     # Control
    enable_meta_cognitive=False
)
```

### 4.3 Behavioral Instrumentation

**BehavioralLogger** captures fine-grained data:

**Decision Events**:
- Timestamp, context (game state, HP, level)
- Action taken, alternatives considered
- Decision latency (ms), confidence (0-1)
- Mental load, active rumination count
- Intrusive thought present (boolean)
- Dominant emotion, fatigue level

**Rumination Events**:
- Timestamp, rumination type
- Content, emotional intensity
- Intrusion frequency, triggered by
- Mental load contribution
- Decision bias strength

**Death Events**:
- Timestamp, level, cause, location
- Pre-death decisions, confidence
- Ruminations triggered, counterfactuals generated
- Regret intensity
- Post-death behavioral changes (measured over 20 decisions)

**Session Summaries**:
- Aggregate statistics (total decisions, deaths, levels)
- Cognitive metrics (avg mental load, latency, confidence)
- Human-likeness indicators (sub-optimal rate, regret rate, etc.)

**Output format**: CSV files for pandas/R analysis, JSON for session summaries.

### 4.4 Metrics

**Performance metrics** (baseline):
- Deaths per hour
- Experience points per hour
- Level progression rate
- Combat success rate

**Cognitive metrics**:
- Decision latency (ms) - mean, variance, distribution
- Decision confidence (0-1) - mean, min/max, correlation with load
- Mental load (0-1) - mean, max, time spent above threshold
- Active rumination count - mean, max, duration
- Intrusive thought frequency - per decision, per minute

**Human-likeness indicators**:
- Sub-optimal decision rate: % decisions with confidence < 0.6
- Post-death regret rate: % deaths followed by rumination
- Analysis paralysis events: decisions with latency > 2× median
- Intrusive thought rate: % decisions with intrusion
- Decision contamination strength: magnitude of bias from rumination

**Composite score**:
```
Human-Likeness Index =
    sub_optimal_rate × 0.25 +
    regret_rate × 0.20 +
    paralysis_rate × 0.15 +
    intrusion_rate × 0.15 +
    rumination_frequency × 0.25
```

Range: 0 (pure optimizer) to 1 (maximal human characteristics)

### 4.5 Experimental Protocol

**Phase 1: Pilot Runs** (Week 1)
- Single instance per condition
- 10-hour runtime each
- Validate logging, identify issues
- Preliminary analysis

**Phase 2: Full Experiment** (Weeks 2-3)
- N=10 instances per condition (30 total)
- Different random seeds
- 10-hour runtime each (300 hours total)
- Aggregate statistics, hypothesis tests

**Phase 3: Hypothesis Testing** (Week 4)
- Statistical comparison across conditions
- Effect size calculations
- Visualization, interpretation

### 4.6 Statistical Analysis Plan

**Primary comparisons**:

TIER 7 vs. TIER 6:
- Paired t-tests on suppression effects, reappraisal success
- Effect sizes (Cohen's d)

TIER 6 vs. TIER 5:
- Paired t-tests on decision latency, risk aversion
- ANOVA for mental load effects

Three-way comparison:
- ANOVA: TIER 7 vs. TIER 6 vs. TIER 5
- Post-hoc tests with Bonferroni correction

**Significance threshold**: p < 0.05, two-tailed
**Corrections**: Bonferroni for multiple comparisons
**Effect sizes**: Cohen's d for all significant effects

### 4.7 Experimental Controls

**Randomization**:
- Random seeds for each instance
- Randomized order of condition execution

**Confound control**:
- Same environment, starting conditions
- Same perception/motor systems
- Only tier configuration varies

**Validation**:
- Logging verification (spot checks)
- State persistence validation
- Syntax validation (no runtime errors)

### 4.8 Data Analysis Pipeline

**research_analysis.py** automates:
1. Load CSVs from all sessions
2. Group by condition
3. Compute metrics (latency, load, confidence, etc.)
4. Run hypothesis tests (t-tests, ANOVA)
5. Calculate effect sizes
6. Generate visualizations
7. Export markdown report

**Visualizations**:
- Decision latency distributions (by condition)
- Mental load trajectories over time
- Post-death behavior changes (latency, confidence)
- Suppression effects (intrusion rates)
- Reappraisal success over time

### 4.9 Methods Summary

Our experimental methodology provides rigorous validation of the hypothesis that implementing rumination and meta-cognition produces measurably human-like behavioral signatures. Through controlled baseline comparisons (TIER 7 vs. 6 vs. 5), comprehensive behavioral logging, and statistical hypothesis testing, we can empirically demonstrate the functional effects of our psychological systems.

---

**[End of Sections 3-4]**

**Next sections (5-7) will cover Results, Discussion, and Conclusion.**

**Word count**: ~4,200 words (Sections 3-4)
**Total so far**: ~8,000 words (Sections 1-4)
**Target total**: 10,000-12,000 words (full paper)

---
