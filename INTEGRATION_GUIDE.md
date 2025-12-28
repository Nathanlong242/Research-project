# Behavioral Logger Integration Guide

## Overview

This guide shows how to integrate the `BehavioralLogger` into `wow_agent_human_equivalent_stabilized.py` to enable empirical validation of TIER 6 (rumination) and TIER 7 (meta-cognition) systems.

**Updated**: December 28, 2025 - Now includes TIER 7 meta-cognitive logging.

---

## Quick Start

### 1. Import the Logger

Add to imports section (around line 170):

```python
from behavioral_logger import BehavioralLogger, DecisionEvent, RuminationEvent, DeathEvent
```

### 2. Initialize Logger in HumanEquivalentCognition

In `HumanEquivalentCognition.__init__` (around line 2033), add:

```python
def __init__(self):
    # ... existing initialization ...

    # Behavioral logging for research
    self.behavioral_logger = BehavioralLogger(
        session_id=f"tier6_run_{int(time.time())}",
        output_dir="research_data"
    )

    logger.info("Behavioral logging enabled for research")
```

### 3. Log Decision Events

In the decision synthesis method (find where action selection happens), add:

```python
def decide_action(self, context, available_actions):
    decision_start_time = time.time()

    # ... existing decision logic ...
    # chosen_action, confidence, alternatives = ...

    decision_latency_ms = (time.time() - decision_start_time) * 1000

    # Get current cognitive state
    mental_load = self.rumination.get_mental_load() if hasattr(self, 'rumination') else 0.0
    active_ruminations = len(self.rumination.active_ruminations) if hasattr(self, 'rumination') else 0
    intrusive_thought = self.rumination.check_for_intrusive_thoughts(context) if hasattr(self, 'rumination') else None

    # Log decision
    decision_event = self.behavioral_logger.log_decision(
        action_taken=chosen_action,
        alternatives=alternatives,
        decision_latency_ms=decision_latency_ms,
        confidence=confidence,
        mental_load=mental_load,
        active_ruminations=active_ruminations,
        intrusive_thought=intrusive_thought is not None,
        emotion=self.current_emotion if hasattr(self, 'current_emotion') else 'neutral',
        fatigue=self.fatigue_level if hasattr(self, 'fatigue_level') else 0.0,
        game_state=context.get('state', 'unknown'),
        level=context.get('level', 1),
        health_percent=context.get('hp', 1.0)
    )

    # Store for outcome logging
    self.last_decision_event = decision_event

    return chosen_action
```

### 4. Log Rumination Events

In `InternalRuminationSystem.trigger_rumination_from_event` (around line 6700), add:

```python
def trigger_rumination_from_event(self, event_type: str, description: str,
                                  emotional_intensity: float, context: str = "unknown"):
    # ... existing rumination creation ...

    rumination = RuminativeThought(...)
    self.active_ruminations.append(rumination)

    # Log for research
    if hasattr(self, 'behavioral_logger') and self.behavioral_logger:
        self.behavioral_logger.log_rumination(
            rumination_type=rumination_type.name,
            content=rumination.content,
            emotional_intensity=rumination.emotional_intensity,
            intrusion_frequency=rumination.intrusion_frequency,
            triggered_by=event_type,
            game_state=context,
            mental_load_contribution=self.get_mental_load(),
            decision_bias_strength=rumination.behavioral_impact.get('bias_strength', 0.0)
        )
```

### 5. Log Death Events

In the death handling code (search for "def handle_death" or similar), add:

```python
def handle_death(self, level: int, cause: str, location: str):
    # Capture pre-death state
    pre_death_decisions = [d.action_taken for d in self.recent_decisions[-5:]]
    pre_death_confidence = sum(d.confidence for d in self.recent_decisions[-5:]) / 5 if self.recent_decisions else 0.5

    # ... existing death handling ...

    # Trigger rumination (existing code)
    self.rumination.trigger_rumination_from_event('death', f"died at level {level}", 0.8)
    counterfactuals = self.rumination.generate_counterfactual(...)

    # Log death event
    death_event = self.behavioral_logger.log_death(
        level=level,
        cause=cause,
        location=location,
        pre_death_decisions=pre_death_decisions,
        pre_death_confidence=pre_death_confidence,
        ruminations_triggered=len([r for r in self.rumination.active_ruminations if r.triggered_recently]),
        counterfactuals_generated=len(counterfactuals),
        regret_intensity=self.rumination.get_regret_intensity()
    )

    # Schedule post-death analysis
    self.deaths_to_analyze.append(death_event)
```

### 6. Update Outcomes

After executing an action and observing outcome:

```python
def process_outcome(self, outcome, valence):
    # ... existing outcome processing ...

    # Update last decision with outcome
    if hasattr(self, 'last_decision_event') and self.last_decision_event:
        self.behavioral_logger.update_decision_outcome(
            decision=self.last_decision_event,
            outcome=outcome,
            valence=valence,
            led_to_death=(outcome == 'death')
        )
```

### 7. Save Session Data

In shutdown/cleanup (search for "def cleanup" or `atexit` registration):

```python
def cleanup(self):
    # ... existing cleanup ...

    # Analyze post-death behavior
    for death_event in self.deaths_to_analyze:
        self.behavioral_logger.analyze_post_death_behavior(death_event, window_size=20)

    # Save all logged data
    logger.info("Saving behavioral data...")
    self.behavioral_logger.save_session()
    logger.info("Behavioral data saved")
```

---

## Complete Integration Example

Here's a minimal complete example showing the key integration points:

```python
class HumanEquivalentCognition:
    def __init__(self):
        # ... existing init ...

        # Add behavioral logger
        self.behavioral_logger = BehavioralLogger(
            session_id=f"tier6_{int(time.time())}",
            output_dir="research_data"
        )
        self.last_decision_event = None
        self.deaths_to_analyze = []

        # Register cleanup
        atexit.register(self.save_behavioral_data)

    def decide_action(self, context, actions):
        start = time.time()

        # Decision logic here
        action, confidence, alternatives = self._synthesize_decision(context, actions)

        # Log decision
        decision_event = self.behavioral_logger.log_decision(
            action_taken=action,
            alternatives=alternatives,
            decision_latency_ms=(time.time() - start) * 1000,
            confidence=confidence,
            mental_load=self.rumination.get_mental_load(),
            active_ruminations=len(self.rumination.active_ruminations),
            intrusive_thought=self._check_intrusive_thought(),
            emotion=self.emotion_state,
            fatigue=self.fatigue,
            game_state=context['state'],
            level=context['level'],
            health_percent=context['hp']
        )

        self.last_decision_event = decision_event
        return action

    def handle_death(self, level, cause, location):
        # Capture state
        pre_decisions = [d.action_taken for d in self.recent_decisions[-5:]]
        pre_confidence = np.mean([d.confidence for d in self.recent_decisions[-5:]])

        # Trigger rumination (existing)
        self.rumination.trigger_rumination_from_event('death', f"died at {level}", 0.8)

        # Log death
        death_event = self.behavioral_logger.log_death(
            level=level,
            cause=cause,
            location=location,
            pre_death_decisions=pre_decisions,
            pre_death_confidence=pre_confidence,
            ruminations_triggered=3,  # Or count actual ruminations
            counterfactuals_generated=2,
            regret_intensity=0.7
        )

        self.deaths_to_analyze.append(death_event)

    def save_behavioral_data(self):
        # Analyze all deaths
        for death in self.deaths_to_analyze:
            self.behavioral_logger.analyze_post_death_behavior(death)

        # Save session
        self.behavioral_logger.save_session()
```

---

## Testing the Integration

### Minimal Test

Add this to test logging without running full agent:

```python
# At bottom of wow_agent_human_equivalent_stabilized.py
if __name__ == "__main__":
    if "--test-logging" in sys.argv:
        print("Testing behavioral logging integration...")

        from behavioral_logger import BehavioralLogger

        logger = BehavioralLogger(session_id="integration_test")

        # Simulate some events
        for i in range(10):
            logger.log_decision(
                action_taken="attack",
                alternatives=["flee", "heal"],
                decision_latency_ms=100 + i * 10,
                confidence=0.7 - i * 0.05,
                mental_load=i * 0.1,
                active_ruminations=i // 3,
                intrusive_thought=i % 4 == 0,
                emotion="anxious",
                fatigue=i * 0.05,
                game_state="combat",
                level=1,
                health_percent=0.8
            )

        logger.log_death(
            level=1,
            cause="enemy",
            location="test_zone",
            pre_death_decisions=["attack", "attack"],
            pre_death_confidence=0.6,
            ruminations_triggered=2,
            counterfactuals_generated=1,
            regret_intensity=0.7
        )

        logger.save_session()
        print("Test complete - check research_data/ directory")
        sys.exit(0)
```

Run with:
```bash
python wow_agent_human_equivalent_stabilized.py --test-logging
```

---

## Configuration Flags

Add command-line flag to enable/disable logging:

```python
parser.add_argument('--enable-logging', action='store_true',
                   help='Enable behavioral logging for research')
parser.add_argument('--session-id', type=str, default=None,
                   help='Session ID for behavioral logs')
```

Then in init:

```python
if args.enable_logging:
    self.behavioral_logger = BehavioralLogger(
        session_id=args.session_id or f"session_{int(time.time())}"
    )
else:
    self.behavioral_logger = None
```

And check before logging:

```python
if self.behavioral_logger:
    self.behavioral_logger.log_decision(...)
```

---

## Baseline Comparison Setup

The experiment configuration system (`experiment_config.py`) provides predefined configurations for controlled comparisons:

```python
from experiment_config import ExperimentConfig

# TIER 7: Full system (rumination + meta-cognition)
config = ExperimentConfig.tier_7_full(session_id="T7_run_001")

# TIER 6: Rumination without meta-cognition
config = ExperimentConfig.tier_6_baseline(session_id="T6_run_001")

# TIER 5: Baseline (no rumination or meta-cognition)
config = ExperimentConfig.tier_5_baseline(session_id="T5_run_001")
```

**Run experiments using the CLI runner**:

```bash
# TIER 7 (full system with meta-cognition)
python run_experiment.py --condition tier7 --session-id T7_run_001

# TIER 6 (rumination only, no meta-cognition)
python run_experiment.py --condition tier6 --session-id T6_run_001

# TIER 5 (baseline without rumination)
python run_experiment.py --condition tier5 --session-id T5_run_001
```

### TIER 7 Meta-Cognitive Logging

When TIER 7 is enabled, additional events are logged:

- **Suppression attempts** and ironic process effects
- **Reappraisal attempts** with success/failure outcomes
- **Meta-rumination** triggers
- **Insight events** and resolutions
- **Mental state transitions** (clear-headed → rumination spiral, etc.)

These events are captured automatically through the `MetaCognitiveLayer` integration.

---

## Troubleshooting

### Logger not saving data

- Check that `cleanup()` is being called
- Check that `atexit` is registered
- Manually call `behavioral_logger.save_session()` before exit

### Missing rumination logs

- Ensure rumination system has reference to logger
- Pass logger in init: `self.rumination = InternalRuminationSystem(logger=self.behavioral_logger)`
- Or set after init: `self.rumination.behavioral_logger = self.behavioral_logger`

### CSV files empty

- Check that events are being logged (print statements)
- Verify data directory exists and is writable
- Check for exceptions during logging (try/except around log calls)

---

## Next Steps After Integration

1. **Run pilot session**: 1-hour session to validate logging works
2. **Check data quality**: Open CSVs, verify fields are populated
3. **Run analysis**: `python research_analysis.py --data research_data/`
4. **Run baseline comparison**: TIER 6 vs TIER 5 for 10 hours each
5. **Statistical validation**: Confirm hypotheses with t-tests

---

## Performance Considerations

Logging overhead is minimal (~1-2% CPU), but for very high-frequency decisions:

- Batch logging (buffer events, write every N seconds)
- Use background thread for file I/O
- Compress CSVs with gzip

Example batched logging:

```python
class BehavioralLogger:
    def __init__(self, ...):
        self.decision_buffer = []
        self.buffer_size = 100

    def log_decision(self, ...):
        event = DecisionEvent(...)
        self.decision_buffer.append(event)

        if len(self.decision_buffer) >= self.buffer_size:
            self._flush_buffer()

    def _flush_buffer(self):
        self.decisions.extend(self.decision_buffer)
        self.decision_buffer.clear()
```

---

## Summary

**Required changes**:
1. Import `BehavioralLogger`
2. Initialize in `__init__`
3. Add logging calls at decision points, rumination triggers, deaths
4. Save on cleanup

**Total lines of code to add**: ~50-100 (depending on existing structure)

**Impact on runtime**: Minimal (<2% overhead)

**Data output**: CSV files suitable for pandas/R analysis

**Next**: Run experiments and validate hypotheses!
