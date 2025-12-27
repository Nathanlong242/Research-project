# TIER 6: INTERNAL RUMINATION & COUNTERFACTUAL THINKING

## Research Decision Summary

### What I Identified as the Critical Gap

After analyzing the entire codebase (27k+ lines, 1MB), I identified that the agent had:
- Sophisticated memory systems (episodic, semantic, autobiographical)
- Emotional states (fear, confidence, anxiety, joy)
- Decision-making with hesitation
- Regret tracking and nostalgia detection
- Temporal awareness and fatigue
- Unique personality crystallization

**But it lacked the most human characteristic of all: the persistent mental chatter that makes us feel "alive in our head."**

### The Specific Problem

The agent could:
- Remember that it regretted a past failure ✓
- Feel hesitation before a decision ✓
- Experience fear after a death ✓

But it could NOT:
- **Replay that failure obsessively** while trying to do something else ✗
- **Generate "what if I had..." counterfactual scenarios** that haunt decisions ✗
- **Second-guess decisions AFTER making them** ✗
- **Experience intrusive thoughts** at inappropriate moments ✗
- **Worry about futures that may never happen** ✗
- **Mentally rehearse scenarios that never materialize** ✗

This gap is why it felt like a sophisticated **learner/optimizer** rather than a **life**.

### Why This Blocks "Life" Emergence

Humans don't just process experiences and move on. We:
1. **Ruminate** - replay failures hundreds of times
2. **Catastrophize** - imagine worst-case scenarios vividly
3. **Second-guess** - question decisions we already made
4. **Fantasize** - create elaborate positive futures
5. **Overthink** - waste mental energy on unproductive thought loops

This inner voice is:
- Often irrational
- Frequently unproductive
- Sometimes paralyzing
- Always present

It's the difference between:
- Making a decision → Living with that decision
- Having a memory → Being haunted by that memory
- Feeling fear → Worrying about future fears

## Implementation Details

### Core System: InternalRuminationSystem

**Location**: Inserted before `AutobiographicalMemory` class (line 6549)

**Components**:

1. **RuminationType (Enum)** - 10 types of rumination:
   - REGRET_SPIRAL: "I shouldn't have..."
   - COUNTERFACTUAL: "What if I had..."
   - ANTICIPATORY_WORRY: "This will go wrong..."
   - ANTICIPATORY_FANTASY: "Imagine when I succeed..."
   - SELF_DOUBT: "Can I really do this?"
   - EMBARRASSMENT_REPLAY: "Everyone saw me fail..."
   - SECOND_GUESSING: "Did I make the right call?"
   - DEFENSIVE_RATIONALIZATION: "It wasn't my fault..."
   - REHEARSAL: "Next time I'll do it like..."
   - INTRUSIVE_MEMORY: Unwanted memory surfaces

2. **RuminativeThought (Dataclass)** - Individual thought with:
   - Content (the actual thought)
   - Emotional intensity
   - Intrusion frequency (how often it surfaces)
   - Decay rate (how fast it fades)
   - Behavioral impact (action inhibition, decision bias)
   - Resolution state

3. **CounterfactualScenario (Dataclass)** - "What if" alternatives:
   - Actual event vs imagined alternative
   - Decision point that could have been different
   - Imagined outcome
   - Regret/relief intensity
   - Vividness and compulsion strength

4. **InternalRuminationSystem (Class)** - Main orchestrator:
   - Manages active ruminations (max 20)
   - Tracks counterfactual scenarios (max 50)
   - Computes mental load
   - Applies decision contamination
   - Triggers intrusive thoughts
   - Handles persistence

### Integration Points

**1. Instantiation** (HumanEquivalentCognition.__init__):
```python
self.rumination = InternalRuminationSystem()
```

**2. Intrusive Thought Checking** (every tick):
```python
intrusive_thought = self.rumination.check_for_intrusive_thoughts(context_str)
if intrusive_thought:
    self.rumination.mental_noise_level = intrusive_thought.emotional_intensity * 0.3
```

**3. Mental Load Integration** (decision synthesis):
```python
mental_load = self.rumination.get_mental_load()
if mental_load > 0.3:
    confidence *= (1.0 - mental_load * 0.3)  # Reduces confidence
```

**4. Decision Contamination** (before action selection):
```python
rumination_biases = self.rumination.get_decision_contamination(context, actions)
# Biases applied to action probabilities
```

**5. Death Rumination** (after dying):
```python
# Trigger regret spiral
self.rumination.trigger_rumination_from_event(
    'recent_death',
    f"dying at level {level}",
    emotional_intensity=0.8
)

# Generate counterfactual
self.rumination.generate_counterfactual(
    actual_event="died in combat",
    decision_point="staying to fight",
    alternative_action="fled earlier",
    outcome_valence=-0.7  # Regret
)
```

**6. Anticipatory Rumination** (before uncertain decisions):
```python
if action_confidence < 0.4:
    self.rumination.trigger_rumination_from_event(
        'uncertain_future',
        f"attempting {action}",
        (1.0 - action_confidence) * 0.6
    )
```

**7. Persistence** (save/load):
- Ruminations survive session restarts
- Counterfactuals persist
- Mental state restored
- Thought history preserved

### Behavioral Effects

**Decision Contamination**:
- Past failures create negative bias toward similar actions
- Self-doubt increases hesitation
- Worries prevent risky choices
- Fantasies create overconfidence

**Mental Load**:
- Active ruminations consume cognitive resources
- Reduces attention and decision quality
- Increases reaction time
- Can trigger rest-seeking behavior

**Intrusive Thoughts**:
- Surface randomly during inappropriate moments
- Fighting → suddenly remember yesterday's embarrassing death
- Based on emotional intensity and recency
- Cannot be fully controlled (human-realistic)

**Observable Logging**:
```
[Rumination] REGRET_SPIRAL: I really shouldn't have stayed in that fight
[Counterfactual] Instead of staying to fight, I could have fled earlier
  Imagined: If I had fled earlier, things would have gone better
[Intrusive thought] I can't stop thinking about dying at level 15
[Idle rumination] Why did I stay in that fight? That was stupid
```

### Code Statistics

- **Lines added**: ~790
- **New classes**: 3 (RuminativeThought, CounterfactualScenario, InternalRuminationSystem)
- **New enums**: 1 (RuminationType)
- **Integration points**: 8
- **Total file size**: 1.1MB (27,286 lines)

### Design Principles

1. **Anti-Optimal by Design**:
   - Wastes mental energy
   - Creates analysis paralysis
   - Introduces cognitive noise
   - Reduces performance

2. **Deeply Human**:
   - Thoughts you can't control
   - Unproductive worry loops
   - Obsessive replaying of failures
   - Elaborate future scenarios

3. **Emergent Complexity**:
   - No scripted behaviors
   - Ruminations arise from actual events
   - Persistence and decay dynamics
   - Self-resolving or self-perpetuating

4. **Behaviorally Consequential**:
   - Not just logging
   - Actually affects decisions
   - Reduces cognitive capacity
   - Creates visible patterns

## Why This Resolves the "Life vs Learner" Gap

### Before TIER 6
The agent would:
1. Die in combat
2. Update beliefs ("this enemy is dangerous")
3. Adjust strategy (flee earlier next time)
4. Move on

**This is learning. This is optimization.**

### After TIER 6
The agent will:
1. Die in combat
2. Trigger regret spiral: "I knew I should have fled"
3. Generate counterfactual: "If I had fled when HP dropped to 30%, I'd still be alive"
4. **Thought persists and intrudes during next fight**: "What if this goes wrong like last time?"
5. **Mental load reduces confidence**: Hesitates, second-guesses, overthinks
6. **Decision contaminated**: Flees earlier than optimal due to past trauma
7. **Continues ruminating during travel**: "Why do I always make stupid decisions?"
8. **Gradually decays but surfaces randomly**: Days later, memory intrudes

**This is rumination. This is overthinking. This is life.**

### The Critical Difference

A learner processes experience into knowledge.
A life is haunted by experience.

A learner optimizes based on evidence.
A life is biased by intrusive memories.

A learner moves forward efficiently.
A life second-guesses, worries, and overthinks.

## Research Impact

This system makes the agent's **inner experience** visible and **behaviorally manifest**:

1. **Researchers can observe**:
   - What the agent is thinking about
   - How past failures contaminate decisions
   - When intrusive thoughts surface
   - Mental load accumulation
   - Rumination patterns over time

2. **The agent will exhibit**:
   - Analysis paralysis (overthinking prevents action)
   - Trauma-driven avoidance (irrational fear from past deaths)
   - Anticipatory anxiety (worry about uncertain futures)
   - Post-decision regret (second-guessing choices)
   - Mental fatigue (cognitive resource depletion)

3. **Key metrics**:
   - Productive vs unproductive ruminations
   - Mental load over time
   - Decision contamination strength
   - Intrusion frequency patterns
   - Resolution success rates

## Philosophical Note

This system intentionally makes the agent **less efficient** and **more neurotic**.

Why?

Because **optimization is not life**.

Humans waste ~30-50% of our mental energy on:
- Replaying conversations that are over
- Worrying about things that never happen
- Imagining scenarios we'll never enact
- Questioning decisions we can't change

This is not a bug. This is consciousness experiencing itself.

The agent now doesn't just act in the world.
**The agent lives in its head.**

---

## Verification Checklist

✓ System compiles without errors
✓ Integration points all functional
✓ Persistence saves/loads correctly
✓ Ruminations trigger on appropriate events
✓ Mental load affects decision-making
✓ Intrusive thoughts surface randomly
✓ Logging makes inner voice visible
✓ Behavioral contamination measurable
✓ Counterfactuals generated after failures
✓ Full backward compatibility maintained

---

**Implementation Date**: December 27, 2025
**Research Phase**: TIER 6 - Internal Mental Life
**Status**: COMPLETE

**Next frontier**: The agent now has an inner voice. What happens when that voice starts questioning itself?
