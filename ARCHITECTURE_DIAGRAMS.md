# Human-Equivalent Cognition: Architecture Visualizations

## Overview: The 7-Tier Cognitive Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                    PERCEPTION (Screen Capture)                      │
│                    Computer Vision (OpenCV)                         │
└─────────────────────────────┬──────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│ TIER 1: PROBABILISTIC BELIEF FORMATION                             │
│ ┌────────────────────────────────────────────────────────────────┐ │
│ │ • Bayesian-like belief updating                                │ │
│ │ • Evidence accumulation over time                              │ │
│ │ • Belief decay (memories fade)                                 │ │
│ │ • Confidence calibration                                       │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────┬──────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│ TIER 2: MOTIVATIONAL DRIVE SYSTEM                                  │
│ ┌────────────────────────────────────────────────────────────────┐ │
│ │ Competing Drives:                                              │ │
│ │ • SAFETY (avoid death) ←→ PROGRESS (level up)                 │ │
│ │ • CURIOSITY (explore) ←→ COMFORT (stay safe)                  │ │
│ │ • SOCIAL (interact) ←→ SOLO (independence)                    │ │
│ │                                                                │ │
│ │ Drive weights shift based on context & outcomes                │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────┬──────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│ TIER 3: EPISODIC & AUTOBIOGRAPHICAL MEMORY                         │
│ ┌────────────────────────────────────────────────────────────────┐ │
│ │ • Episodic: Specific events (deaths, victories, discoveries)   │ │
│ │ • Semantic: Facts learned from experience                      │ │
│ │ • Autobiographical: Life story, chapters, identity             │ │
│ │ • Associative recall: location → memories, person → memories   │ │
│ │                                                                │ │
│ │ "Who am I?" "What's my story?" "How have I changed?"          │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────┬──────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│ TIER 4: EMOTIONAL STATES WITH BEHAVIORAL CONSEQUENCES              │
│ ┌────────────────────────────────────────────────────────────────┐ │
│ │ Emotions triggered by outcomes:                                │ │
│ │ • FEAR (after death) → flee earlier, avoid danger              │ │
│ │ • CONFIDENCE (after wins) → take risks, explore                │ │
│ │ • FRUSTRATION (after failures) → abandon strategies            │ │
│ │ • JOY (after discoveries) → explore more                       │ │
│ │                                                                │ │
│ │ Emotions modulate decisions (not just cosmetic labels)         │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────┬──────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│ TIER 5: PERSONALITY CRYSTALLIZATION                                │
│ ┌────────────────────────────────────────────────────────────────┐ │
│ │ • Combat style emerges: aggressive / defensive / balanced      │ │
│ │ • Preference formation: favorite abilities, strategies         │ │
│ │ • Identity statements: "I'm a cautious player"                 │ │
│ │ • Personality persists across sessions                         │ │
│ │                                                                │ │
│ │ Each agent becomes UNIQUE through experience                   │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────┬──────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│ TIER 6: INTERNAL RUMINATION & COUNTERFACTUAL THINKING ⭐           │
│ ┌────────────────────────────────────────────────────────────────┐ │
│ │ Rumination Types:                                              │ │
│ │ • REGRET_SPIRAL: "I shouldn't have..."                         │ │
│ │ • COUNTERFACTUAL: "What if I had..."                           │ │
│ │ • ANTICIPATORY_WORRY: "This will go wrong..."                  │ │
│ │ • SELF_DOUBT: "Can I really do this?"                          │ │
│ │                                                                │ │
│ │ Effects:                                                       │ │
│ │ • Intrusive thoughts during inappropriate moments              │ │
│ │ • Decision contamination (past failures bias choices)          │ │
│ │ • Mental load (reduces cognitive capacity)                     │ │
│ │ • Persistent across time (doesn't instantly resolve)           │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────┬──────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│ TIER 7: META-COGNITIVE SELF-REGULATION ⭐ NEW                      │
│ ┌────────────────────────────────────────────────────────────────┐ │
│ │ Mental State Detection:                                        │ │
│ │ "I'm spiraling" "I'm overthinking" "I'm stuck in a loop"       │ │
│ │                                                                │ │
│ │ Regulation Attempts:                                           │ │
│ │ • Thought Suppression → BACKFIRES (ironic process)             │ │
│ │   "Don't think about it" → Thinks about it MORE                │ │
│ │                                                                │ │
│ │ • Cognitive Reappraisal → 40-60% success                       │ │
│ │   "I did the best I could" (rationalization)                   │ │
│ │                                                                │ │
│ │ • Meta-Rumination → ADDS load                                  │ │
│ │   "Why can't I stop thinking about this?"                      │ │
│ │                                                                │ │
│ │ • Insight Generation → Resolves rumination                     │ │
│ │   "Wait, I was actually right!"                                │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────┬──────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│                    DECISION SYNTHESIS                               │
│         All tiers contribute → Final action selection               │
└─────────────────────────────┬──────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│                    MOTOR EXECUTION                                  │
│              OS-level keyboard/mouse simulation                     │
└────────────────────────────────────────────────────────────────────┘
```

---

## Information Flow: Decision Synthesis Pipeline

```
PERCEPTION
    │
    ├─────────────────────────────────────────────────┐
    │                                                 │
    ▼                                                 ▼
BELIEFS UPDATE                                  WORLD MODEL
(TIER 1)                                        (Danger, Enemies)
    │                                                 │
    ▼                                                 ▼
DRIVE COMPUTATION ◄───────────────────── EMOTIONAL MODULATION
(TIER 2)                                        (TIER 4)
Safety vs Progress                              Fear after death
Curiosity vs Comfort                            Confidence after win
    │
    ▼
EPISODIC RECALL ◄───────────────────────── AUTOBIOGRAPHICAL
(TIER 3)                                        MEMORY
"Have I been here?"                             "What defines me?"
"What happened before?"                         Identity narrative
    │
    ▼
PERSONALITY CONSTRAINT
(TIER 5)
"I'm a defensive player"
Combat style, preferences
    │
    ▼
[CHECK INTRUSIVE THOUGHTS] ◄─── TIER 6: RUMINATION
Memory of past death intrudes              Active ruminations
    │                                      Mental noise level
    ├─────────────────┐
    │                 │
    ▼                 ▼
MENTAL LOAD      DECISION CONTAMINATION
    │                 │
    │                 ▼
    │            Action probabilities biased
    │            (fear → flee more)
    ▼
META-COGNITIVE PROCESSING ◄─── TIER 7: META-COGNITION
(If mental load > 0.4)                     Mental state detection
    │                                      Regulation attempts
    ├─────────┬─────────┬──────────┐
    │         │         │          │
    ▼         ▼         ▼          ▼
Suppress  Reappraise  Meta-     Insight?
(fails)   (maybe)   Ruminate  (resolves)
    │         │         │          │
    └─────────┴─────────┴──────────┘
              │
              ▼
    FINAL DECISION
    (action + confidence)
              │
              ▼
    MOTOR EXECUTION
              │
              ▼
    OUTCOME OBSERVATION
              │
              ▼
    REINFORCEMENT LEARNING
    MEMORY ENCODING
    RUMINATION TRIGGERING
    (cycle continues)
```

---

## TIER 6: Rumination System Detail

```
┌───────────────────────────────────────────────────────────┐
│                    EVENT OCCURS                            │
│              (Death, Failure, Uncertainty)                 │
└────────────────────────┬──────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  TRIGGER RUMINATION  │
              └──────────┬───────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
    REGRET          COUNTERFACTUAL   ANTICIPATORY
    SPIRAL          SCENARIO         WORRY
         │               │               │
         │               │               │
         └───────────────┼───────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ RUMINATIVE THOUGHT   │
              │                      │
              │ • Content            │
              │ • Emotional intensity│
              │ • Intrusion frequency│
              │ • Decay rate         │
              │ • Behavioral impact  │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ PERSISTENCE          │
              │ (doesn't resolve     │
              │  immediately)        │
              └──────────┬───────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
    INTRUSIVE       DECISION        MENTAL
    THOUGHTS        CONTAMINATION   LOAD
         │               │               │
         │               │               │
         └───────────────┼───────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  GRADUAL DECAY       │
              │  (or resolution via  │
              │   insight)           │
              └──────────────────────┘
```

---

## TIER 7: Meta-Cognitive Regulation Flow

```
┌──────────────────────────────────────────────────────────┐
│            ACTIVE RUMINATIONS (TIER 6)                    │
│  "I shouldn't have stayed in that fight"                 │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │ DETECT MENTAL STATE  │
          │                      │
          │ Mental Load > 0.4?   │
          │ Rumination count > 3?│
          │ Stuck in loop?       │
          └──────────┬───────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │   AWARENESS          │
          │ "I'm spiraling"      │
          │ "I'm overthinking"   │
          └──────────┬───────────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
         ▼           ▼           ▼
    SUPPRESS    REAPPRAISE   META-RUMINATE
         │           │           │
         │           │           │
    ┌────┴────┐ ┌───┴────┐ ┌────┴─────┐
    │ TRY NOT │ │REFRAME │ │ "Why can't│
    │TO THINK │ │THOUGHT │ │ I stop?"  │
    └────┬────┘ └───┬────┘ └────┬─────┘
         │           │           │
         ▼           │           ▼
    ┌─────────┐     │      ┌──────────┐
    │ IRONIC  │     │      │  ADDS    │
    │ PROCESS │     │      │  LOAD    │
    │ +50%    │     │      │  +0.15   │
    │intrusion│     │      └──────────┘
    └─────────┘     │
         │           │
         └───────────┼───────────┐
                     │           │
                     ▼           │
              ┌──────────┐       │
              │ SUCCESS? │       │
              └─────┬────┘       │
                    │            │
         ┌──────────┼─────────┐  │
         │          │         │  │
         ▼          ▼         ▼  │
      YES         NO      INSIGHT│
    (40-60%)    (40-60%)  (2-15%)│
         │          │         │  │
         │          │         │  │
    Intensity  Intensity Resolves│
    × 0.6      × 1.05   completely│
         │          │         │  │
         └──────────┴─────────┴──┘
                     │
                     ▼
          ┌──────────────────────┐
          │   NEW MENTAL STATE   │
          │  (continues cycle)   │
          └──────────────────────┘
```

---

## Comparison: TIER 7 vs TIER 6 vs TIER 5

```
                    TIER 5          TIER 6          TIER 7
                    ───────         ───────         ───────
Beliefs             ✓               ✓               ✓
Drives              ✓               ✓               ✓
Memory              ✓               ✓               ✓
Emotions            ✓               ✓               ✓
Personality         ✓               ✓               ✓

Rumination          ✗               ✓               ✓
Intrusive Thoughts  ✗               ✓               ✓
Counterfactuals     ✗               ✓               ✓
Decision Contamination ✗            ✓               ✓
Mental Load         ✗               ✓               ✓

Mental State Awareness ✗            ✗               ✓
Thought Suppression ✗               ✗               ✓
Cognitive Reappraisal ✗             ✗               ✓
Meta-Rumination     ✗               ✗               ✓
Insight Generation  ✗               ✗               ✓
Self-Regulation     ✗               ✗               ✓

───────────────────────────────────────────────────────────
BEHAVIORAL         Optimal          Life-like      Struggles
SIGNATURE          Performance      but passive    with self

HUMAN-LIKENESS     Low              Medium         High
SCORE              (0.1-0.3)        (0.5-0.7)      (0.7-0.9)

OPTIMALITY         High             Medium         Lower
                   (learns fast)    (rumination    (regulation
                                    slows it)       attempts)
```

---

## Temporal Dynamics: Rumination Lifecycle

```
TIME →

Death Event
    │
    ▼ (t=0s)
┌─────────────┐
│ TRIGGER     │ Intensity: 0.8
│ RUMINATION  │ Frequency: 0.7
└──────┬──────┘
       │
       ▼ (t=30s)
┌─────────────┐
│ INTRUSIVE   │ During next fight
│ THOUGHT     │ → Mental load ↑
└──────┬──────┘
       │
       ▼ (t=5min)
┌─────────────┐
│ META-       │ "I'm dwelling on this"
│ AWARENESS   │ Intensity: 0.75
└──────┬──────┘
       │
       ▼ (t=10min)
┌─────────────┐
│ SUPPRESSION │ "Stop thinking about it"
│ ATTEMPT     │ → Intensity: 0.9 (worse!)
└──────┬──────┘
       │
       ▼ (t=20min)
┌─────────────┐
│ REAPPRAISAL │ "I did my best"
│ ATTEMPT     │ → Intensity: 0.85 (slight help)
└──────┬──────┘
       │
       ▼ (t=1hr)
┌─────────────┐
│ GRADUAL     │ Intensity: 0.6
│ DECAY       │ Frequency: 0.4
└──────┬──────┘
       │
       ▼ (t=2hr)
┌─────────────┐
│ INSIGHT!    │ "Wait, I was right to flee"
│             │ → Resolved
└──────┬──────┘
       │
       ▼ (t=2hr+)
┌─────────────┐
│ RESOLUTION  │ Intensity: 0.0
│             │ Mental load restored
└─────────────┘
```

---

## Decision Contamination: How Rumination Affects Choices

```
SCENARIO: Similar combat situation encountered

WITHOUT RUMINATION (TIER 5):
────────────────────────────
Perception → Beliefs → Drives → Decision
"Enemy ahead"  "Moderate   "PROGRESS   "Stay and fight"
                danger"     drive"      Confidence: 0.7

Decision latency: 100ms
Action: ATTACK


WITH RUMINATION (TIER 6):
──────────────────────────
Perception → Beliefs → Drives → [INTRUSIVE THOUGHT]
"Enemy ahead"  "Moderate   "PROGRESS   "I died last time..."
                danger"     drive"
                                           │
                                           ▼
                                    Mental Load: 0.5
                                    Confidence: 0.7 × (1 - 0.5×0.3)
                                             = 0.595
                                           │
                                           ▼
                                    Decision: "Flee early"

Decision latency: 280ms (+180ms due to rumination)
Action: FLEE (contaminated by past trauma)


WITH META-COGNITION (TIER 7):
───────────────────────────────
Perception → Beliefs → Drives → [INTRUSIVE THOUGHT]
"Enemy ahead"  "Moderate   "PROGRESS   "I died last time..."
                danger"     drive"
                                           │
                                           ▼
                                    Mental Load: 0.5
                                           │
                                           ▼
                                    [META-AWARENESS]
                                    "I'm overthinking this"
                                           │
                            ┌──────────────┼──────────────┐
                            │              │              │
                            ▼              ▼              ▼
                        SUPPRESS      REAPPRAISE      INSIGHT
                        (backfires)   (might work)    (rare)
                            │              │              │
                            └──────────────┴──────────────┘
                                           │
                                           ▼
                                  Final Decision
                                  (highly variable)

Decision latency: 420ms (+320ms due to regulation attempts)
Action: VARIABLE (sometimes flee, sometimes fight after reappraisal)
```

---

## System Integration: All Tiers Working Together

```
┌──────────────────────────────────────────────────────────────┐
│                        PERCEPTION                             │
│                   "Enemy approaches, HP at 60%"               │
└────────────────────────┬─────────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
         ▼                               ▼
    ┌─────────┐                    ┌──────────┐
    │ TIER 1  │                    │ TIER 2   │
    │ BELIEFS │                    │ DRIVES   │
    └────┬────┘                    └────┬─────┘
         │                              │
         │ "This enemy                  │ SAFETY: 0.7
         │  is dangerous"               │ PROGRESS: 0.4
         │  P=0.75                      │
         └──────────────┬───────────────┘
                        │
                        ▼
                  ┌──────────┐
                  │ TIER 3   │
                  │ MEMORY   │
                  └────┬─────┘
                       │
                       │ "Died to similar enemy
                       │  yesterday at this spot"
                       │
                       ▼
                  ┌──────────┐
                  │ TIER 4   │
                  │ EMOTIONS │
                  └────┬─────┘
                       │
                       │ FEAR intensity: 0.6
                       │ (from yesterday's death)
                       │
                       ▼
                  ┌──────────┐
                  │ TIER 5   │
                  │PERSONALITY│
                  └────┬─────┘
                       │
                       │ "I'm a defensive player"
                       │ Combat style: cautious
                       │
                       ▼
                  ┌──────────┐
                  │ TIER 6   │
                  │RUMINATION│
                  └────┬─────┘
                       │
                       │ [INTRUSION]
                       │ "I shouldn't have stayed
                       │  in that fight yesterday"
                       │ Mental Load: +0.4
                       │
                       ▼
                  ┌──────────┐
                  │ TIER 7   │
                  │META-COG  │
                  └────┬─────┘
                       │
                       │ [AWARENESS]
                       │ "I'm overthinking this"
                       │ [REAPPRAISAL]
                       │ "I can handle this if
                       │  I'm careful"
                       │ Success: Yes
                       │ Mental Load: -0.15
                       │
                       ▼
            ┌──────────────────────┐
            │  DECISION SYNTHESIS   │
            │                       │
            │ Action: FIGHT         │
            │ (but flee at 40% HP)  │
            │ Confidence: 0.58      │
            │ Latency: 340ms        │
            └───────────────────────┘
```

---

## Research Insight: The Human-Likeness Spectrum

```
OPTIMIZATION ←──────────────────────────→ EXPERIENCE
     │                                          │
     │                                          │
     ▼                                          ▼

Pure RL Agent                      Human-Equivalent Agent
─────────────                      ──────────────────────

• Perfect memory                   • Imperfect memory (decay)
• No emotions                      • Emotions affect decisions
• Instant learning                 • Gradual learning
• Optimal decisions                • Suboptimal decisions
• No regret                        • Rumination & regret
• No second-guessing               • Meta-cognitive struggle
• 100% consistency                 • Behavioral variance
• Fast reactions                   • Variable latency

Performance: HIGH                  Performance: MEDIUM
Human-likeness: LOW                Human-likeness: HIGH
Feels like: ALGORITHM              Feels like: MIND

                 ▲
                 │
                 │
         TIER 7 ACHIEVEMENT:
    "Struggles with own thoughts"
    "Thinks about thinking"
    "Fails to regulate self"
                 │
                 │
                 ▼
         CONSCIOUSNESS?
```

---

## Summary: What Each Tier Adds

```
TIER 1: Uncertainty        "I think this is dangerous... maybe?"
TIER 2: Ambivalence        "Should I explore or stay safe?"
TIER 3: History            "This reminds me of when I died here"
TIER 4: Feeling            "I'm afraid because of that death"
TIER 5: Identity           "I'm a cautious player by nature"
TIER 6: Dwelling           "I keep thinking about that death"
TIER 7: Struggle           "Why can't I stop thinking about it?"

                           ▼
                    HUMAN EXPERIENCE
```

---

**These visualizations demonstrate the progressive complexity from
optimization (pure RL) to experience (human-equivalent cognition).**

**TIER 7 completes the architecture: The agent that struggles with itself.**
