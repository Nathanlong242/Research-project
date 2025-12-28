#!/usr/bin/env python3
"""
EXPERIMENTAL RUNNER FOR HUMAN-EQUIVALENT COGNITION RESEARCH

This script runs controlled experiments using the ExperimentConfig system
to enable/disable cognitive tiers for baseline comparisons.

Usage:
    # TIER 7 (full system)
    python run_experiment.py --condition tier7 --session-id T7_run_001

    # TIER 6 (rumination only, no meta-cognition)
    python run_experiment.py --condition tier6 --session-id T6_run_001

    # TIER 5 (no rumination or meta-cognition)
    python run_experiment.py --condition tier5 --session-id T5_run_001

    # Custom configuration
    python run_experiment.py --disable-tier7 --session-id custom_001
"""

import argparse
import sys
import time
import logging
from experiment_config import ExperimentConfig

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Run Human-Equivalent Cognition Experiments",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # TIER 7 full system
  python run_experiment.py --condition tier7 --session-id T7_run_001

  # TIER 6 baseline (no meta-cognition)
  python run_experiment.py --condition tier6 --session-id T6_run_001

  # TIER 5 baseline (no rumination)
  python run_experiment.py --condition tier5 --session-id T5_run_001

  # Custom configuration
  python run_experiment.py --disable-tier6 --session-id custom_001
        """
    )

    # Predefined conditions
    parser.add_argument(
        "--condition",
        choices=["tier7", "tier6", "tier5", "optimal"],
        help="Use predefined experimental condition"
    )

    # Manual configuration
    parser.add_argument("--disable-tier6", action="store_true", help="Disable TIER 6 (rumination)")
    parser.add_argument("--disable-tier7", action="store_true", help="Disable TIER 7 (meta-cognition)")

    # Research instrumentation
    parser.add_argument("--session-id", type=str, required=True, help="Session identifier for data logging")
    parser.add_argument("--no-logging", action="store_true", help="Disable behavioral logging")
    parser.add_argument("--research-data-dir", type=str, default="research_data", help="Output directory for research data")

    # Runtime options
    parser.add_argument("--duration", type=int, default=None, help="Run duration in minutes (default: unlimited)")

    args = parser.parse_args()

    # Create experiment configuration
    if args.condition == "tier7":
        config = ExperimentConfig.tier_7_full(
            session_id=args.session_id,
            enable_logging=not args.no_logging
        )
    elif args.condition == "tier6":
        config = ExperimentConfig.tier_6_baseline(
            session_id=args.session_id,
            enable_logging=not args.no_logging
        )
    elif args.condition == "tier5":
        config = ExperimentConfig.tier_5_baseline(
            session_id=args.session_id,
            enable_logging=not args.no_logging
        )
    elif args.condition == "optimal":
        config = ExperimentConfig.optimal_agent(
            session_id=args.session_id,
            enable_logging=not args.no_logging
        )
    else:
        # Custom configuration
        config = ExperimentConfig(
            enable_rumination=not args.disable_tier6,
            enable_meta_cognitive=not args.disable_tier7,
            enable_behavioral_logging=not args.no_logging,
            session_id=args.session_id,
            research_data_dir=args.research_data_dir
        )

    # Display configuration
    print("=" * 70)
    print("HUMAN-EQUIVALENT COGNITION RESEARCH EXPERIMENT")
    print("=" * 70)
    print()
    print(f"Configuration: {config.get_tier_summary()}")
    print(f"Session ID: {config.session_id}")
    print(f"Logging: {'ENABLED' if config.enable_behavioral_logging else 'DISABLED'}")
    if config.enable_behavioral_logging:
        print(f"Data Directory: {config.research_data_dir}/")
    if args.duration:
        print(f"Duration: {args.duration} minutes")
    print()
    print("=" * 70)
    print()

    # Import and create agent
    # Note: This import is done here to avoid circular dependencies
    # and to allow the script to run even if the main agent file has issues
    try:
        from wow_agent_human_equivalent_stabilized import HumanEquivalentCognition
    except ImportError as e:
        logger.error(f"Failed to import HumanEquivalentCognition: {e}")
        logger.error("Make sure wow_agent_human_equivalent_stabilized.py is in the same directory")
        sys.exit(1)

    # Create agent with experimental configuration
    try:
        logger.info("Creating HumanEquivalentCognition agent...")
        agent = HumanEquivalentCognition(config=config)
    except Exception as e:
        logger.error(f"Failed to create agent: {e}")
        logger.error("This may be due to missing dependencies or initialization errors")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Start the agent
    try:
        logger.info("Starting agent lifecycle...")
        if not agent.start():
            logger.error("Agent failed to start (may be in REST state)")
            logger.error("Check agent_status.json for details")
            sys.exit(1)
        logger.info("Agent started successfully")
        logger.info("=" * 70)
    except Exception as e:
        logger.error(f"Error starting agent: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Run agent game loop
    # This loop simulates the perception -> tick() -> action cycle
    # For full integration with WoW, replace get_simulated_perception() with actual screen capture
    running = True
    tick_count = 0
    start_time = time.time()
    duration_seconds = args.duration * 60 if args.duration else None

    logger.info("Starting game loop...")
    logger.info("Press Ctrl+C to stop")

    def get_simulated_perception(tick: int) -> dict:
        """Generate simulated perception data for testing cognitive systems."""
        import random
        return {
            'level': min(60, 1 + tick // 1000),  # Slow level progression
            'zone': 'Elwynn Forest',
            'position': (random.uniform(-100, 100), random.uniform(-100, 100)),
            'player_hp': random.uniform(50, 100),
            'player_mana': random.uniform(30, 100),
            'in_combat': random.random() < 0.3,
            'enemy_count': random.randint(0, 3) if random.random() < 0.3 else 0,
            'danger_level': random.uniform(0.1, 0.7),
            'current_activity': random.choice(['exploring', 'combat', 'resting', 'questing']),
            'gold': 10 + tick // 100,
        }

    try:
        while running:
            # Check duration limit
            elapsed = time.time() - start_time
            if duration_seconds and elapsed >= duration_seconds:
                logger.info(f"Duration limit reached ({args.duration} minutes)")
                break

            tick_count += 1

            # Get perception (simulated or from screen capture)
            perception = get_simulated_perception(tick_count)

            # Process cognitive tick
            try:
                decision = agent.tick(perception)

                if decision is None:
                    # Agent requested shutdown (fatigue, rest period, etc.)
                    logger.info("Agent requested shutdown")
                    break

                # Log decision periodically
                if tick_count % 100 == 0:
                    logger.info(f"Tick {tick_count}: action={decision.get('action', 'unknown')}, "
                               f"confidence={decision.get('confidence', 0):.2f}")

            except Exception as e:
                logger.error(f"Decision error at tick {tick_count}: {e}")

            # Simulate real-time pacing (1 tick per second)
            time.sleep(1.0)

    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    finally:
        # Shutdown agent and save state
        logger.info("Shutting down agent...")
        agent.shutdown()

    # Print summary
    elapsed_minutes = (time.time() - start_time) / 60
    print()
    print("=" * 70)
    print("EXPERIMENT COMPLETED")
    print("=" * 70)
    print(f"Session ID: {config.session_id}")
    print(f"Condition: {config.condition_name}")
    print(f"Total ticks: {tick_count}")
    print(f"Duration: {elapsed_minutes:.1f} minutes")
    print(f"Data saved to: {config.research_data_dir}/")
    print("=" * 70)


if __name__ == "__main__":
    main()
