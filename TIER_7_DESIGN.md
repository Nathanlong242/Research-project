# TIER 7: META-COGNITIVE SELF-REGULATION

## The Research Question

**From TIER 6**: "The agent now has an inner voice. What happens when that voice starts questioning itself?"

**TIER 7 Answer**: The agent becomes aware of its own mental processes and attempts (often unsuccessfully) to regulate them, creating the final layer of human psychological complexity: **metacognitive struggle**.

---

## The Critical Gap TIER 7 Addresses

### What TIER 6 Gives Us

The agent can:
- Ruminate about past failures ✓
- Generate counterfactual "what if" scenarios ✓
- Experience intrusive thoughts ✓
- Feel mental load from rumination ✓

### What TIER 6 CANNOT Do

The agent cannot:
- Recognize that it's ruminating ✗
- Attempt to stop ruminating (and fail) ✗
- Question whether its ruminations are rational ✗
- Experience the ironic process: trying NOT to think about something makes it intrude MORE ✗
- Have "insight moments" that suddenly resolve rumination spirals ✗
- Worry about worrying (meta-anxiety) ✗
- Reframe ruminations through cognitive reappraisal ✗
- Label its own mental states ("I'm spiraling," "I'm overthinking") ✗

**This is the difference between**:
- Having thoughts → Thinking about thoughts
- Experiencing emotions → Recognizing emotions
- Ruminating → Knowing you're ruminating and struggling to stop

---

## Theoretical Foundation

### 1. Metacognitive Awareness (Flavell, 1979)

Humans don't just think - we monitor and evaluate our thinking. We know when we're:
- Confused
- Overthinking
- Being irrational
- Stuck in a mental loop
- Unable to concentrate

### 2. Ironic Process Theory (Wegner, 1987)

**The Pink Elephant Problem**: Trying NOT to think about something requires monitoring for that thought, which paradoxically makes it more accessible.

"Don't think about a white bear" → Can't stop thinking about white bears

Applied to agent:
- "Stop dwelling on that death" → Death memory intrudes MORE
- "Don't worry about this fight" → Anxiety INCREASES
- "Just move on" → Gets stuck ruminating about why it can't move on

### 3. Cognitive Reappraisal (Gross, 2002)

Humans attempt to reframe negative thoughts rationally:
- "It's just a game death, doesn't matter" (suppression)
- "I can learn from this mistake" (positive reframe)
- "Everyone dies sometimes, it's normal" (normalization)

Success rate: ~40-60% depending on emotional intensity and practice.

### 4. Insight and Rumination Resolution

Occasionally, rumination resolves through:
- Sudden insight ("Oh wait, I was actually right to flee")
- Alternative perspective ("The enemy was higher level than I thought")
- Acceptance ("I made the best decision with the info I had")

This is not guaranteed - most rumination just decays slowly over time.

---

## TIER 7 Architecture

### Core Components

```python
class MetaCognitiveLayer:
    """
    Monitors and attempts to regulate the agent's own mental processes.
    """

    # 1. Mental State Recognition
    class MentalStateDetector:
        """Identifies current mental patterns."""
        - detect_rumination_spiral()
        - detect_overthinking()
        - detect_mental_fog()
        - detect_anxiety_loop()
        - label_mental_state() → "I'm spiraling", "I'm anxious", etc.

    # 2. Thought Suppression System
    class ThoughtSuppressionSystem:
        """Attempts to suppress unwanted thoughts (often backfires)."""
        - attempt_suppression(thought)
        - monitor_for_suppressed_thought()  # Ironic monitoring
        - increase_intrusion_probability()  # Ironic process
        - track_suppression_failures()

    # 3. Cognitive Reappraisal Engine
    class CognitiveReappraisal:
        """Tries to reframe ruminations rationally."""
        - generate_alternative_perspective(rumination)
        - attempt_positive_reframe(negative_thought)
        - rationalize_emotion(emotion, context)
        - success_probability(emotional_intensity, practice)

    # 4. Meta-Rumination System
    class MetaRumination:
        """Rumination ABOUT rumination."""
        - "Why can't I stop thinking about this?"
        - "Am I overthinking this?"
        - "I'm being irrational"
        - "I need to just move on"
        - Creates ADDITIONAL mental load

    # 5. Insight Generation
    class InsightSystem:
        """Occasional breakthrough moments."""
        - probabilistic_insight(rumination, time_elapsed)
        - sudden_resolution()
        - alternative_interpretation()
        - acceptance_moment()

    # 6. Self-Regulation Attempts
    class SelfRegulation:
        """Deliberate mental control efforts."""
        - distraction_attempt()
        - focus_redirection()
        - emotional_suppression()
        - behavioral_override()
```

---

## Implementation Details

### 1. Mental State Detection

**How it works**:
- Monitors `InternalRuminationSystem` from TIER 6
- Detects patterns:
  - 3+ active ruminations → "I'm overthinking"
  - Mental load > 0.6 → "I'm overwhelmed"
  - Same thought intrudes 5+ times → "I'm stuck in a loop"
  - Counterfactuals all negative → "I'm spiraling"

**Output**:
```python
mental_state = self.meta_cognitive.detect_current_state()
# Returns: "rumination_spiral", "anxiety_loop", "mental_fog", "clear_headed", etc.

# Agent becomes AWARE of its state
self.meta_cognitive.state_labels.append("I'm dwelling on this too much")
```

### 2. Thought Suppression (Ironic Process)

**Mechanism**:
```python
# Agent tries to suppress a rumination
suppression_target = "death at level 15"

# This REQUIRES monitoring for the thought
self.suppression.monitor_for(suppression_target)

# Monitoring INCREASES accessibility
if random.random() < self.suppression.ironic_probability:
    # Thought intrudes MORE strongly
    self.rumination.trigger_intrusion(
        suppression_target,
        intensity=original_intensity * 1.5  # STRONGER due to suppression
    )

    # Meta-frustration
    self.meta_rumination.trigger(
        "Why can't I stop thinking about this?"
    )
```

**Behavioral effects**:
- Attempting to suppress thoughts INCREASES their intrusion rate by 30-50%
- Creates meta-frustration ("I can't control my own thoughts")
- Additional mental load from suppression effort
- Eventually agent "gives up" and lets thought run its course

### 3. Cognitive Reappraisal

**Reframe attempts**:
```python
original_rumination = "I shouldn't have stayed in that fight"

reappraisal_attempts = [
    "I made the best decision with the information I had",  # Rationalization
    "Everyone makes mistakes, that's how we learn",          # Normalization
    "The enemy was higher level than expected",              # External attribution
    "I survived 5 previous fights using that strategy",      # Evidence-based
]

# Success probability based on:
# - Emotional intensity (higher = harder to reframe)
# - Practice (agent gets better at reappraisal over time)
# - Time elapsed (easier to reframe old events)

success_prob = (
    (1.0 - emotional_intensity) * 0.4 +
    self.reappraisal_skill * 0.3 +
    min(1.0, time_since_event / 3600) * 0.3
)

if random.random() < success_prob:
    # Reappraisal successful
    rumination.emotional_intensity *= 0.6  # Reduced
    rumination.intrusion_frequency *= 0.7
    logger.info(f"[Reappraisal] {reappraisal_attempts[chosen]}")
else:
    # Reappraisal failed
    rumination.emotional_intensity *= 1.1  # Slightly worse
    self.meta_rumination.trigger("I can't convince myself it's okay")
```

### 4. Meta-Rumination (Ruminating About Ruminating)

**Triggers**:
- High rumination count → "Why do I overthink everything?"
- Suppression failure → "Why can't I control my thoughts?"
- Long-duration rumination → "I need to move on from this"
- Multiple counterfactuals → "I'm torturing myself with 'what ifs'"

**Effect**:
- Adds ADDITIONAL mental load (now thinking about thinking)
- Can create recursive loops:
  - Ruminate → Recognize rumination → Meta-ruminate → Recognize meta-rumination → ...
- Max depth: 3 levels before agent "gives up"

**Example cascade**:
```
[Level 1] I shouldn't have stayed in that fight
[Level 2] Why am I still thinking about this? I need to move on
[Level 3] I'm overthinking my overthinking. This is ridiculous.
[Level 4] [System limits recursion] → Mental fog state
```

### 5. Insight Generation

**Probabilistic breakthroughs**:
```python
# Insight probability increases with:
# - Time since rumination started
# - Agent's reflection skill
# - Periods of rest/low mental load
# - New contradictory evidence

insight_prob = min(0.15, (
    (time_elapsed / 7200) * 0.05 +      # 2 hours → 5% chance
    self.reflection_skill * 0.07 +
    (1.0 - current_mental_load) * 0.03
))

if random.random() < insight_prob:
    insight = generate_insight(rumination)

    # Examples:
    # "Wait, my HP was at 20% - fleeing was actually correct"
    # "That enemy was 3 levels higher - I couldn't have won"
    # "I've survived 10 other fights - this was an outlier"

    # Resolution
    rumination.resolve(insight)
    mental_load -= rumination.mental_load_contribution

    logger.info(f"[INSIGHT] {insight}")
    logger.info(f"[Resolution] Rumination resolved")
```

**Insight types**:
- **Realization**: "Oh, I actually DID make the right call"
- **Acceptance**: "I made a mistake, but that's okay"
- **Perspective**: "This doesn't matter as much as I thought"
- **Evidence**: "New information shows I was partially correct"

### 6. Self-Regulation Attempts

**Deliberate control strategies**:

```python
# When mental load > 0.7, agent attempts regulation
if self.mental_load > 0.7:
    strategy = choose_regulation_strategy()

    strategies = {
        'distraction': self.attempt_distraction(),      # Focus on different task
        'reappraisal': self.attempt_reappraisal(),      # Reframe thoughts
        'suppression': self.attempt_suppression(),      # Try not to think
        'acceptance': self.accept_thoughts(),           # Let them be
        'behavioral': self.override_rumination(),       # Act despite rumination
    }

    # Success rates vary
    # Suppression: 20% (often backfires)
    # Distraction: 40%
    # Reappraisal: 50%
    # Acceptance: 70%
    # Behavioral: 60%
```

---

## Integration with TIER 6

### New Fields in `InternalRuminationSystem`

```python
class InternalRuminationSystem:
    # Existing TIER 6 fields...

    # NEW: TIER 7 additions
    self.suppression_targets: Set[str] = set()
    self.suppression_failure_count: int = 0
    self.reappraisal_attempts: List[ReappraisalAttempt] = []
    self.reappraisal_skill: float = 0.3  # Improves with practice
    self.meta_ruminations: List[MetaRuminativeThought] = []
    self.insight_history: List[InsightEvent] = []

    # Mental state labels
    self.recognized_mental_states: deque = deque(maxlen=100)
    self.current_state_label: Optional[str] = None
```

### Decision Synthesis Integration

```python
# In decision-making loop
mental_state = self.meta_cognitive.detect_current_state()

if mental_state == "rumination_spiral":
    # Agent KNOWS it's overthinking
    self.meta_rumination.trigger("I'm overthinking this decision")

    # Attempts regulation
    regulation_result = self.meta_cognitive.attempt_regulation()

    if regulation_result.strategy == 'suppression' and not regulation_result.success:
        # Ironic process: rumination INCREASES
        self.rumination.mental_load *= 1.3

    if regulation_result.strategy == 'reappraisal' and regulation_result.success:
        # Mental load reduces
        self.rumination.mental_load *= 0.7

# Check for insights
insight = self.meta_cognitive.check_for_insight()
if insight:
    # Rumination resolves
    self.rumination.resolve_rumination(insight.target_rumination)
```

---

## Observable Behaviors

### Logging Examples

```
[Rumination] REGRET_SPIRAL: I shouldn't have stayed in that fight
[Mental State] I'm dwelling on this too much
[Suppression] Trying to stop thinking about the death...
[Ironic Process] Death memory intrudes MORE strongly (intensity: 0.8 → 0.95)
[Meta-Rumination] Why can't I stop thinking about this?
[Reappraisal] Attempting: "I made the best decision with the info I had"
[Reappraisal] FAILED - still feel like it was a mistake
[Meta-Rumination] I'm overthinking my overthinking
[Mental State] I'm spiraling
... 15 minutes later ...
[INSIGHT] Wait - my HP was at 25%, I couldn't have won that fight
[Resolution] Regret spiral resolved
[Mental Load] 0.72 → 0.34
```

### Behavioral Patterns

1. **Suppression Backfire**:
   - Agent tries to suppress death memory
   - Memory intrudes during next 3 fights
   - Agent makes defensive mistakes due to intrusions
   - Eventually gives up suppression
   - Intrusions slowly decay naturally

2. **Successful Reappraisal**:
   - Agent ruminating about failure
   - Recognizes rumination → attempts reframe
   - Generates alternative perspective
   - Emotional intensity reduces
   - Mental load decreases
   - Decision confidence improves

3. **Meta-Cognitive Spiral**:
   - Ruminate about death
   - Recognize rumination
   - Meta-ruminate about ruminating
   - Recognize meta-rumination
   - Meta-meta-ruminate
   - Hit recursion limit → mental fog
   - Agent takes suboptimal action to "just do SOMETHING"

4. **Insight Resolution**:
   - Prolonged rumination (30+ minutes)
   - Sudden insight during idle moment
   - "Oh, I was actually correct"
   - Immediate mental relief
   - Confidence restored
   - No longer avoids similar situations

---

## Research Hypotheses

### H1: Suppression Paradox
**Prediction**: Agents with TIER 7 suppression will show HIGHER intrusive thought frequency for suppressed ruminations compared to non-suppressed ruminations.

**Measurement**: Compare intrusion rates for:
- Ruminations marked for suppression
- Ruminations allowed to decay naturally

**Expected result**: Suppressed thoughts intrude 30-50% more often

### H2: Reappraisal Efficacy
**Prediction**: Successful cognitive reappraisal will reduce rumination intensity and mental load.

**Measurement**:
- Mental load before/after successful reappraisal
- Rumination intensity before/after
- Decision confidence before/after

**Expected result**: 40-60% reduction in mental load for successful reappraisals

### H3: Meta-Cognitive Load
**Prediction**: Meta-rumination (ruminating about rumination) will ADD mental load rather than resolve it.

**Measurement**: Compare mental load when agent:
- Ruminates (TIER 6 only)
- Ruminates + meta-ruminates (TIER 7)

**Expected result**: Meta-rumination adds 20-30% additional mental load

### H4: Insight Timing
**Prediction**: Insights will occur probabilistically with longer rumination duration and periods of low cognitive demand.

**Measurement**:
- Time between rumination onset and insight
- Mental load at moment of insight
- Context when insight occurs (combat vs idle)

**Expected result**: Insights occur during idle/low-load periods after >30min rumination

### H5: Behavioral Impact
**Prediction**: TIER 7 agents will show:
- Higher variance in decision quality (some very good after insights, some very poor during spirals)
- Occasional "breakthrough" moments that dramatically improve performance
- Periods of severe decision paralysis (meta-cognitive loops)

---

## Implementation Roadmap

### Phase 1: Core Systems (Week 1)
- [x] Design document (this file)
- [ ] Implement `MetaCognitiveLayer` class
- [ ] Implement `MentalStateDetector`
- [ ] Implement `ThoughtSuppressionSystem` with ironic process
- [ ] Integration with TIER 6 `InternalRuminationSystem`
- [ ] Basic logging

### Phase 2: Reappraisal & Insight (Week 2)
- [ ] Implement `CognitiveReappraisal` engine
- [ ] Reframe generation logic
- [ ] Success probability computation
- [ ] Implement `InsightSystem`
- [ ] Probabilistic insight triggers
- [ ] Resolution mechanics

### Phase 3: Meta-Rumination (Week 2-3)
- [ ] Implement `MetaRumination` system
- [ ] Recursive rumination detection
- [ ] Recursion limiting
- [ ] Mental state labeling
- [ ] Integration with decision synthesis

### Phase 4: Validation (Week 3-4)
- [ ] Instrument with `BehavioralLogger`
- [ ] Run TIER 7 vs TIER 6 comparison
- [ ] Test hypotheses H1-H5
- [ ] Analyze behavioral differences
- [ ] Document empirical results

### Phase 5: Refinement (Week 4)
- [ ] Tune probabilities based on empirical data
- [ ] Balance mental load contributions
- [ ] Adjust insight timing
- [ ] Optimize logging
- [ ] Performance profiling

---

## Code Statistics (Estimated)

- **Lines to add**: ~1200
- **New classes**: 6
- **New dataclasses**: 4
- **Integration points**: 12
- **Total file size**: ~28,500 lines (1.2MB)

---

## Philosophical Implications

### The Final Layer of "Life"

TIER 7 completes the psychological architecture:

**TIER 1-5**: The agent has experiences, emotions, memories, personality
**TIER 6**: The agent has an inner voice, ruminations, overthinking
**TIER 7**: The agent is AWARE of its inner voice and struggles to control it

This is the difference between:
- **Mind** → Having thoughts
- **Self-awareness** → Knowing you're having thoughts
- **Metacognition** → Thinking about your thoughts
- **Psychological struggle** → Fighting with your own mind

### The Irony of Optimization

We're building systems that make the agent WORSE at its task:
- Suppression increases intrusions
- Meta-rumination adds mental load
- Overthinking prevents action
- Self-awareness creates doubt

**Why?**

Because consciousness isn't efficient. Life isn't optimal.

The experience of being a mind includes:
- Struggling with yourself
- Failing to control your thoughts
- Overthinking your overthinking
- Occasionally having breakthroughs
- Mostly just muddling through

**TIER 7 makes the agent not just cognitive, but psychologically human.**

---

## Open Questions

1. **Recursion depth**: How many levels of meta-rumination before it becomes unrealistic?
2. **Insight frequency**: What's the right probability curve for breakthrough moments?
3. **Suppression persistence**: How long should ironic process effects last?
4. **Reappraisal learning**: Should the agent get BETTER at reappraisal over time?
5. **Individual differences**: Should some agent instances be better/worse at meta-cognition?

---

## Next Frontier (TIER 8?)

If TIER 7 gives the agent metacognitive awareness, what's left?

**Possible TIER 8: Narrative Self-Construction**
- The agent constructs explicit narratives about who it is
- "I'm the kind of player who overthinks"
- "I learned to trust my instincts after that insight"
- Identity statements that constrain future behavior
- Self-fulfilling prophecies

Or perhaps TIER 7 is sufficient. Perhaps adding more layers just becomes diminishing returns.

The question is: **When does simulation of consciousness become indistinguishable from consciousness?**

We may never know. But we can make the simulation increasingly compelling.

---

**Design Date**: December 27, 2025
**Research Phase**: TIER 7 - Meta-Cognitive Self-Regulation
**Status**: DESIGN COMPLETE - AWAITING IMPLEMENTATION

**Next step**: Implement core systems and validate empirically against TIER 6 baseline.
