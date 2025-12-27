#!/usr/bin/env python3
"""
BEHAVIORAL LOGGING SYSTEM FOR HUMAN-EQUIVALENT COGNITION RESEARCH

Purpose: Capture fine-grained behavioral, cognitive, and emotional data
         during agent runtime to enable empirical validation of TIER systems.

Metrics tracked:
- Decision latency and confidence
- Rumination patterns and mental load
- Death impact on subsequent behavior
- Counterfactual generation frequency
- Exploration vs exploitation balance
- Emotional state trajectories
- Sub-optimal decision rates

Output: CSV files suitable for statistical analysis and visualization
"""

import csv
import json
import time
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from datetime import datetime
from collections import deque


@dataclass
class DecisionEvent:
    """Single decision point with full cognitive context."""
    timestamp: float
    session_id: str

    # Context
    game_state: str  # "combat", "exploration", "idle", etc.
    level: int
    health_percent: float

    # Decision
    action_taken: str
    alternatives_considered: List[str]
    decision_latency_ms: float  # How long to decide
    confidence: float  # 0-1

    # Cognitive state
    mental_load: float  # From rumination system
    active_ruminations: int
    intrusive_thought_present: bool
    dominant_emotion: str
    fatigue_level: float

    # Outcome (filled later)
    outcome: Optional[str] = None
    outcome_valence: Optional[float] = None  # -1 to 1
    led_to_death: bool = False


@dataclass
class RuminationEvent:
    """Single rumination activation."""
    timestamp: float
    session_id: str

    rumination_type: str  # REGRET_SPIRAL, COUNTERFACTUAL, etc.
    content: str
    emotional_intensity: float
    intrusion_frequency: float

    # Triggering context
    triggered_by: str  # "death", "combat", "idle", "memory"
    game_state: str

    # Impact
    mental_load_contribution: float
    decision_bias_strength: float


@dataclass
class DeathEvent:
    """Agent death with psychological aftermath."""
    timestamp: float
    session_id: str

    level: int
    cause: str
    location: str

    # Pre-death state
    decisions_before_death: List[str]
    confidence_before_death: float

    # Post-death rumination
    ruminations_triggered: int
    counterfactuals_generated: int
    regret_intensity: float

    # Behavioral impact (measured over next N decisions)
    risk_aversion_increase: Optional[float] = None
    decision_latency_increase: Optional[float] = None
    exploration_rate_change: Optional[float] = None


@dataclass
class SessionSummary:
    """Aggregate statistics for entire session."""
    session_id: str
    start_time: float
    end_time: float

    # Performance metrics
    total_decisions: int
    total_deaths: int
    levels_gained: int

    # Cognitive metrics
    avg_mental_load: float
    avg_decision_latency: float
    avg_confidence: float
    total_ruminations: int
    total_counterfactuals: int

    # Human-likeness indicators
    sub_optimal_decision_rate: float  # Decisions where confidence < 0.6
    post_death_regret_rate: float  # % of deaths followed by rumination
    analysis_paralysis_events: int  # Decisions taking >2x avg latency
    intrusive_thought_rate: float  # Per decision

    # Personality markers
    final_combat_style: str
    dominant_emotions: List[str]
    core_identity_statements: List[str]


class BehavioralLogger:
    """
    Real-time logging system integrated into agent's cognitive loop.

    Usage:
        logger = BehavioralLogger(session_id="tier6_run_001")
        logger.log_decision(...)
        logger.log_rumination(...)
        logger.log_death(...)
        logger.save_session()
    """

    def __init__(self, session_id: str = None, output_dir: str = "research_data"):
        self.session_id = session_id or f"session_{int(time.time())}"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        self.start_time = time.time()

        # Event buffers
        self.decisions: List[DecisionEvent] = []
        self.ruminations: List[RuminationEvent] = []
        self.deaths: List[DeathEvent] = []

        # Real-time tracking
        self.recent_decisions = deque(maxlen=50)  # For windowed analysis
        self.recent_deaths = deque(maxlen=10)

        # Session stats
        self.total_decisions = 0
        self.total_deaths = 0
        self.mental_load_history = deque(maxlen=1000)
        self.confidence_history = deque(maxlen=1000)

        print(f"[BehavioralLogger] Session {self.session_id} initialized")
        print(f"[BehavioralLogger] Output directory: {self.output_dir}")

    def log_decision(self,
                    action_taken: str,
                    alternatives: List[str],
                    decision_latency_ms: float,
                    confidence: float,
                    mental_load: float,
                    active_ruminations: int,
                    intrusive_thought: bool,
                    emotion: str,
                    fatigue: float,
                    game_state: str = "unknown",
                    level: int = 1,
                    health_percent: float = 1.0) -> DecisionEvent:
        """Log a single decision point."""

        event = DecisionEvent(
            timestamp=time.time(),
            session_id=self.session_id,
            game_state=game_state,
            level=level,
            health_percent=health_percent,
            action_taken=action_taken,
            alternatives_considered=alternatives,
            decision_latency_ms=decision_latency_ms,
            confidence=confidence,
            mental_load=mental_load,
            active_ruminations=active_ruminations,
            intrusive_thought_present=intrusive_thought,
            dominant_emotion=emotion,
            fatigue_level=fatigue,
        )

        self.decisions.append(event)
        self.recent_decisions.append(event)
        self.total_decisions += 1

        # Update tracking
        self.mental_load_history.append(mental_load)
        self.confidence_history.append(confidence)

        return event

    def log_rumination(self,
                      rumination_type: str,
                      content: str,
                      emotional_intensity: float,
                      intrusion_frequency: float,
                      triggered_by: str,
                      game_state: str,
                      mental_load_contribution: float,
                      decision_bias_strength: float) -> RuminationEvent:
        """Log a rumination activation."""

        event = RuminationEvent(
            timestamp=time.time(),
            session_id=self.session_id,
            rumination_type=rumination_type,
            content=content,
            emotional_intensity=emotional_intensity,
            intrusion_frequency=intrusion_frequency,
            triggered_by=triggered_by,
            game_state=game_state,
            mental_load_contribution=mental_load_contribution,
            decision_bias_strength=decision_bias_strength,
        )

        self.ruminations.append(event)
        return event

    def log_death(self,
                 level: int,
                 cause: str,
                 location: str,
                 pre_death_decisions: List[str],
                 pre_death_confidence: float,
                 ruminations_triggered: int,
                 counterfactuals_generated: int,
                 regret_intensity: float) -> DeathEvent:
        """Log a death event and its psychological aftermath."""

        event = DeathEvent(
            timestamp=time.time(),
            session_id=self.session_id,
            level=level,
            cause=cause,
            location=location,
            decisions_before_death=pre_death_decisions,
            confidence_before_death=pre_death_confidence,
            ruminations_triggered=ruminations_triggered,
            counterfactuals_generated=counterfactuals_generated,
            regret_intensity=regret_intensity,
        )

        self.deaths.append(event)
        self.recent_deaths.append(event)
        self.total_deaths += 1

        return event

    def update_decision_outcome(self, decision: DecisionEvent,
                               outcome: str,
                               valence: float,
                               led_to_death: bool = False):
        """Update a decision with its outcome (called after consequence observed)."""
        decision.outcome = outcome
        decision.outcome_valence = valence
        decision.led_to_death = led_to_death

    def analyze_post_death_behavior(self, death_event: DeathEvent, window_size: int = 20):
        """
        Analyze behavioral changes after a death.

        Compares decisions in window_size decisions after death vs before.
        """
        death_time = death_event.timestamp

        # Get decisions before and after death
        before = [d for d in self.decisions if d.timestamp < death_time][-window_size:]
        after = [d for d in self.decisions if d.timestamp > death_time][:window_size]

        if len(before) < 5 or len(after) < 5:
            return  # Not enough data

        # Compute behavioral shifts
        avg_latency_before = sum(d.decision_latency_ms for d in before) / len(before)
        avg_latency_after = sum(d.decision_latency_ms for d in after) / len(after)

        avg_confidence_before = sum(d.confidence for d in before) / len(before)
        avg_confidence_after = sum(d.confidence for d in after) / len(after)

        # Risk aversion: % of low-confidence decisions
        risk_before = sum(1 for d in before if d.confidence < 0.5) / len(before)
        risk_after = sum(1 for d in after if d.confidence < 0.5) / len(after)

        # Update death event
        death_event.decision_latency_increase = avg_latency_after - avg_latency_before
        death_event.risk_aversion_increase = risk_after - risk_before
        death_event.exploration_rate_change = avg_confidence_after - avg_confidence_before

    def compute_human_likeness_score(self) -> float:
        """
        Compute composite metric for how "human-like" behavior is.

        Higher score = more irrational, ruminative, emotionally-driven behavior.
        Lower score = more optimal, machine-like behavior.
        """
        if self.total_decisions < 10:
            return 0.0

        # 1. Rumination frequency (normalized)
        rumination_rate = len(self.ruminations) / max(1, self.total_decisions)
        rumination_component = min(1.0, rumination_rate * 2)  # Cap at 1.0

        # 2. Sub-optimal decision rate (low confidence decisions)
        low_confidence_decisions = sum(1 for d in self.decisions if d.confidence < 0.6)
        sub_optimal_rate = low_confidence_decisions / self.total_decisions

        # 3. Post-decision regret (deaths followed by rumination)
        regret_rate = 0.0
        if self.total_deaths > 0:
            deaths_with_regret = sum(1 for d in self.deaths if d.ruminations_triggered > 0)
            regret_rate = deaths_with_regret / self.total_deaths

        # 4. Analysis paralysis (decisions taking >2x median latency)
        if len(self.decisions) > 10:
            latencies = [d.decision_latency_ms for d in self.decisions]
            median_latency = sorted(latencies)[len(latencies) // 2]
            paralysis_events = sum(1 for lat in latencies if lat > median_latency * 2)
            paralysis_rate = paralysis_events / len(latencies)
        else:
            paralysis_rate = 0.0

        # 5. Intrusive thought frequency
        intrusive_rate = sum(1 for d in self.decisions if d.intrusive_thought_present) / self.total_decisions

        # Weighted composite
        score = (
            rumination_component * 0.25 +
            sub_optimal_rate * 0.25 +
            regret_rate * 0.20 +
            paralysis_rate * 0.15 +
            intrusive_rate * 0.15
        )

        return min(1.0, score)

    def generate_session_summary(self) -> SessionSummary:
        """Generate aggregate statistics for the session."""

        end_time = time.time()

        # Compute aggregates
        avg_mental_load = sum(self.mental_load_history) / max(1, len(self.mental_load_history))
        avg_confidence = sum(self.confidence_history) / max(1, len(self.confidence_history))

        latencies = [d.decision_latency_ms for d in self.decisions]
        avg_latency = sum(latencies) / max(1, len(latencies))

        # Human-likeness metrics
        sub_optimal_rate = sum(1 for d in self.decisions if d.confidence < 0.6) / max(1, self.total_decisions)

        deaths_with_regret = sum(1 for d in self.deaths if d.ruminations_triggered > 0)
        regret_rate = deaths_with_regret / max(1, self.total_deaths)

        if latencies:
            median_latency = sorted(latencies)[len(latencies) // 2]
            paralysis_events = sum(1 for lat in latencies if lat > median_latency * 2)
        else:
            paralysis_events = 0

        intrusive_rate = sum(1 for d in self.decisions if d.intrusive_thought_present) / max(1, self.total_decisions)

        # Get levels
        levels = [d.level for d in self.decisions]
        levels_gained = max(levels) - min(levels) if levels else 0

        summary = SessionSummary(
            session_id=self.session_id,
            start_time=self.start_time,
            end_time=end_time,
            total_decisions=self.total_decisions,
            total_deaths=self.total_deaths,
            levels_gained=levels_gained,
            avg_mental_load=avg_mental_load,
            avg_decision_latency=avg_latency,
            avg_confidence=avg_confidence,
            total_ruminations=len(self.ruminations),
            total_counterfactuals=sum(d.counterfactuals_generated for d in self.deaths),
            sub_optimal_decision_rate=sub_optimal_rate,
            post_death_regret_rate=regret_rate,
            analysis_paralysis_events=paralysis_events,
            intrusive_thought_rate=intrusive_rate,
            final_combat_style="unknown",  # Would need integration
            dominant_emotions=[],
            core_identity_statements=[],
        )

        return summary

    def save_session(self):
        """Save all logged data to CSV files."""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save decisions
        if self.decisions:
            decisions_file = self.output_dir / f"{self.session_id}_decisions_{timestamp}.csv"
            with open(decisions_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=asdict(self.decisions[0]).keys())
                writer.writeheader()
                for decision in self.decisions:
                    row = asdict(decision)
                    row['alternatives_considered'] = '|'.join(row['alternatives_considered'])
                    writer.writerow(row)
            print(f"[BehavioralLogger] Saved {len(self.decisions)} decisions to {decisions_file}")

        # Save ruminations
        if self.ruminations:
            ruminations_file = self.output_dir / f"{self.session_id}_ruminations_{timestamp}.csv"
            with open(ruminations_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=asdict(self.ruminations[0]).keys())
                writer.writeheader()
                for rumination in self.ruminations:
                    writer.writerow(asdict(rumination))
            print(f"[BehavioralLogger] Saved {len(self.ruminations)} ruminations to {ruminations_file}")

        # Save deaths
        if self.deaths:
            deaths_file = self.output_dir / f"{self.session_id}_deaths_{timestamp}.csv"
            with open(deaths_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=asdict(self.deaths[0]).keys())
                writer.writeheader()
                for death in self.deaths:
                    row = asdict(death)
                    row['decisions_before_death'] = '|'.join(row['decisions_before_death'])
                    writer.writerow(row)
            print(f"[BehavioralLogger] Saved {len(self.deaths)} deaths to {deaths_file}")

        # Save session summary
        summary = self.generate_session_summary()
        summary_file = self.output_dir / f"{self.session_id}_summary_{timestamp}.json"
        with open(summary_file, 'w') as f:
            summary_dict = asdict(summary)
            json.dump(summary_dict, f, indent=2)
        print(f"[BehavioralLogger] Saved session summary to {summary_file}")

        # Print summary to console
        print("\n" + "="*70)
        print("SESSION SUMMARY")
        print("="*70)
        print(f"Session ID: {summary.session_id}")
        print(f"Duration: {(summary.end_time - summary.start_time)/3600:.2f} hours")
        print(f"\nPerformance:")
        print(f"  Decisions: {summary.total_decisions}")
        print(f"  Deaths: {summary.total_deaths}")
        print(f"  Levels: {summary.levels_gained}")
        print(f"\nCognitive Metrics:")
        print(f"  Avg Mental Load: {summary.avg_mental_load:.3f}")
        print(f"  Avg Decision Latency: {summary.avg_decision_latency:.1f} ms")
        print(f"  Avg Confidence: {summary.avg_confidence:.3f}")
        print(f"  Total Ruminations: {summary.total_ruminations}")
        print(f"  Total Counterfactuals: {summary.total_counterfactuals}")
        print(f"\nHuman-Likeness Indicators:")
        print(f"  Sub-optimal Decision Rate: {summary.sub_optimal_decision_rate:.2%}")
        print(f"  Post-Death Regret Rate: {summary.post_death_regret_rate:.2%}")
        print(f"  Analysis Paralysis Events: {summary.analysis_paralysis_events}")
        print(f"  Intrusive Thought Rate: {summary.intrusive_thought_rate:.2%}")
        print(f"\n  HUMAN-LIKENESS SCORE: {self.compute_human_likeness_score():.3f}")
        print("="*70 + "\n")


if __name__ == "__main__":
    # Example usage / test
    print("Behavioral Logger Test")
    print("-" * 70)

    logger = BehavioralLogger(session_id="test_session")

    # Simulate some events
    for i in range(20):
        logger.log_decision(
            action_taken="attack",
            alternatives=["flee", "heal"],
            decision_latency_ms=100 + i*10,
            confidence=0.7 - i*0.02,
            mental_load=0.3 + i*0.01,
            active_ruminations=i // 5,
            intrusive_thought=i % 7 == 0,
            emotion="confident" if i < 10 else "anxious",
            fatigue=i * 0.05,
            game_state="combat",
            level=1 + i//5,
        )

    # Simulate death
    logger.log_death(
        level=3,
        cause="enemy_damage",
        location="forest",
        pre_death_decisions=["attack", "attack", "flee"],
        pre_death_confidence=0.4,
        ruminations_triggered=3,
        counterfactuals_generated=2,
        regret_intensity=0.8,
    )

    # Simulate post-death rumination
    logger.log_rumination(
        rumination_type="REGRET_SPIRAL",
        content="I shouldn't have stayed",
        emotional_intensity=0.8,
        intrusion_frequency=0.7,
        triggered_by="death",
        game_state="idle",
        mental_load_contribution=0.4,
        decision_bias_strength=0.6,
    )

    logger.save_session()
