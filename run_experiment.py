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

    # Run agent
    # TODO: Add proper game loop here
    # For now, this is a placeholder that shows the configuration is working
    logger.warning("NOTE: Full game loop not yet implemented in this script")
    logger.warning("HumanEquivalentCognition requires integration with screen capture and input systems")
    logger.warning("Use this script to verify configuration, then integrate with full agent architecture")

    print()
    print("=" * 70)
    print("EXPERIMENT CONFIGURATION VERIFIED")
    print("=" * 70)
    print()
    print("Next steps:")
    print("1. Integrate HumanEquivalentCognition with WoW screen capture")
    print("2. Add game loop with perception -> tick() -> action cycle")
    print("3. Run full experiments for data collection")
    print()
    print("For now, the experimental configuration is ready and tested.")
    print(f"Session ID: {config.session_id}")
    print(f"Condition: {config.condition_name}")
    print("=" * 70)


if __name__ == "__main__":
    main()
