#!/usr/bin/env python3
"""
EXPERIMENTAL CONFIGURATION SYSTEM

Allows precise control over which cognitive tiers are enabled for
baseline comparison experiments.

Usage:
    # TIER 7 (full system)
    config = ExperimentConfig.tier_7_full()
    agent = HumanEquivalentCognition(config=config)

    # TIER 6 (no meta-cognition)
    config = ExperimentConfig.tier_6_baseline()
    agent = HumanEquivalentCognition(config=config)

    # TIER 5 (no rumination)
    config = ExperimentConfig.tier_5_baseline()
    agent = HumanEquivalentCognition(config=config)

    # Custom
    config = ExperimentConfig(
        enable_rumination=True,
        enable_meta_cognitive=False
    )
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ExperimentConfig:
    """
    Configuration for cognitive tier enable/disable.

    This allows creating baseline conditions for controlled experiments.
    """

    # === TIER CONTROLS ===

    # TIER 1: Probabilistic Belief Formation (always enabled)
    enable_beliefs: bool = True

    # TIER 2: Motivational Drive System (always enabled)
    enable_drives: bool = True

    # TIER 3: Episodic & Autobiographical Memory (always enabled)
    enable_memory: bool = True

    # TIER 4: Emotional States (always enabled)
    enable_emotions: bool = True

    # TIER 5: Personality Crystallization (always enabled)
    enable_personality: bool = True

    # TIER 6: Internal Rumination & Counterfactual Thinking
    enable_rumination: bool = True

    # TIER 7: Meta-Cognitive Self-Regulation
    enable_meta_cognitive: bool = True

    # === RESEARCH INSTRUMENTATION ===

    # Enable behavioral logging for research
    enable_behavioral_logging: bool = False

    # Session identifier for logs
    session_id: Optional[str] = None

    # Output directory for research data
    research_data_dir: str = "research_data"

    # === EXPERIMENTAL CONDITIONS ===

    # Condition name (for organizing results)
    condition_name: str = "default"

    # Random seed (for reproducibility)
    random_seed: Optional[int] = None

    # === HELPER METHODS ===

    @classmethod
    def tier_7_full(cls, session_id: str = None, enable_logging: bool = True) -> 'ExperimentConfig':
        """
        TIER 7: Full system with meta-cognition.

        All tiers enabled, including rumination and meta-cognitive self-regulation.
        This is the complete psychological architecture.
        """
        return cls(
            enable_rumination=True,
            enable_meta_cognitive=True,
            enable_behavioral_logging=enable_logging,
            session_id=session_id or "tier7_full",
            condition_name="TIER_7_FULL"
        )

    @classmethod
    def tier_6_baseline(cls, session_id: str = None, enable_logging: bool = True) -> 'ExperimentConfig':
        """
        TIER 6 Baseline: Rumination without meta-cognition.

        Agent has inner voice and rumination, but no awareness or regulation attempts.
        Control condition for measuring TIER 7 effects.
        """
        return cls(
            enable_rumination=True,
            enable_meta_cognitive=False,  # NO meta-cognition
            enable_behavioral_logging=enable_logging,
            session_id=session_id or "tier6_baseline",
            condition_name="TIER_6_BASELINE"
        )

    @classmethod
    def tier_5_baseline(cls, session_id: str = None, enable_logging: bool = True) -> 'ExperimentConfig':
        """
        TIER 5 Baseline: Personality without rumination.

        Agent has personality, emotions, memory, but NO rumination or meta-cognition.
        Control condition for measuring TIER 6 effects.
        """
        return cls(
            enable_rumination=False,  # NO rumination
            enable_meta_cognitive=False,  # NO meta-cognition
            enable_behavioral_logging=enable_logging,
            session_id=session_id or "tier5_baseline",
            condition_name="TIER_5_BASELINE"
        )

    @classmethod
    def optimal_agent(cls, session_id: str = None, enable_logging: bool = True) -> 'ExperimentConfig':
        """
        Optimal Agent: Pure reinforcement learning.

        Only TIER 1-2 enabled (beliefs + drives).
        No personality, no rumination, no meta-cognition.
        Pure performance optimization.
        """
        return cls(
            enable_personality=False,
            enable_rumination=False,
            enable_meta_cognitive=False,
            enable_behavioral_logging=enable_logging,
            session_id=session_id or "optimal_baseline",
            condition_name="OPTIMAL_BASELINE"
        )

    def get_tier_summary(self) -> str:
        """Get human-readable summary of enabled tiers."""
        tiers = []
        if self.enable_beliefs and self.enable_drives:
            tiers.append("TIER 1-2 (Beliefs + Drives)")
        if self.enable_memory:
            tiers.append("TIER 3 (Memory)")
        if self.enable_emotions:
            tiers.append("TIER 4 (Emotions)")
        if self.enable_personality:
            tiers.append("TIER 5 (Personality)")
        if self.enable_rumination:
            tiers.append("TIER 6 (Rumination)")
        if self.enable_meta_cognitive:
            tiers.append("TIER 7 (Meta-Cognition)")

        return f"{self.condition_name}: {', '.join(tiers)}"

    def should_enable_tier_6(self) -> bool:
        """Check if TIER 6 systems should be initialized."""
        return self.enable_rumination

    def should_enable_tier_7(self) -> bool:
        """Check if TIER 7 systems should be initialized."""
        return self.enable_meta_cognitive and self.enable_rumination  # TIER 7 requires TIER 6


# === EXPERIMENTAL PROTOCOL HELPERS ===

def create_experiment_batch(base_session_id: str, num_runs: int = 10) -> dict:
    """
    Create a batch of experiment configurations for statistical comparison.

    Returns dict of {condition_name: [configs]}
    """
    batch = {
        'TIER_7_FULL': [],
        'TIER_6_BASELINE': [],
        'TIER_5_BASELINE': [],
    }

    for i in range(num_runs):
        # TIER 7
        batch['TIER_7_FULL'].append(
            ExperimentConfig.tier_7_full(
                session_id=f"{base_session_id}_tier7_run{i:02d}",
                enable_logging=True
            )
        )

        # TIER 6
        batch['TIER_6_BASELINE'].append(
            ExperimentConfig.tier_6_baseline(
                session_id=f"{base_session_id}_tier6_run{i:02d}",
                enable_logging=True
            )
        )

        # TIER 5
        batch['TIER_5_BASELINE'].append(
            ExperimentConfig.tier_5_baseline(
                session_id=f"{base_session_id}_tier5_run{i:02d}",
                enable_logging=True
            )
        )

    return batch


def get_hypothesis_testing_configs() -> list:
    """
    Get configurations for hypothesis testing.

    Returns list of (config, hypothesis_code) tuples.
    """
    return [
        (ExperimentConfig.tier_7_full(session_id="h7_1_tier7"), "H7.1: Suppression Paradox (TIER 7)"),
        (ExperimentConfig.tier_6_baseline(session_id="h7_1_tier6"), "H7.1: Suppression Paradox (TIER 6 control)"),

        (ExperimentConfig.tier_6_baseline(session_id="h6_1_tier6"), "H6.1: Post-Death Latency (TIER 6)"),
        (ExperimentConfig.tier_5_baseline(session_id="h6_1_tier5"), "H6.1: Post-Death Latency (TIER 5 control)"),
    ]


if __name__ == "__main__":
    # Example usage
    print("="*70)
    print("EXPERIMENTAL CONFIGURATION SYSTEM")
    print("="*70)

    print("\n1. TIER 7 Full System:")
    config = ExperimentConfig.tier_7_full(session_id="test_tier7")
    print(f"   {config.get_tier_summary()}")
    print(f"   Session ID: {config.session_id}")
    print(f"   Logging: {config.enable_behavioral_logging}")

    print("\n2. TIER 6 Baseline (no meta-cognition):")
    config = ExperimentConfig.tier_6_baseline(session_id="test_tier6")
    print(f"   {config.get_tier_summary()}")
    print(f"   Rumination: {config.enable_rumination}")
    print(f"   Meta-Cognition: {config.enable_meta_cognitive}")

    print("\n3. TIER 5 Baseline (no rumination):")
    config = ExperimentConfig.tier_5_baseline(session_id="test_tier5")
    print(f"   {config.get_tier_summary()}")
    print(f"   Rumination: {config.enable_rumination}")

    print("\n4. Optimal Agent:")
    config = ExperimentConfig.optimal_agent(session_id="test_optimal")
    print(f"   {config.get_tier_summary()}")
    print(f"   Personality: {config.enable_personality}")

    print("\n5. Experiment Batch (10 runs each):")
    batch = create_experiment_batch("exp_2025_12_27", num_runs=3)
    for condition, configs in batch.items():
        print(f"   {condition}: {len(configs)} runs")
        for cfg in configs[:2]:  # Show first 2
            print(f"     - {cfg.session_id}")

    print("\n" + "="*70)
