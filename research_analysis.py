#!/usr/bin/env python3
"""
RESEARCH ANALYSIS PIPELINE

Purpose: Analyze behavioral data logged from human-equivalent agents
         to validate hypotheses about rumination effects.

Capabilities:
- Load and process CSV data from behavioral_logger.py
- Statistical analysis (t-tests, ANOVA, effect sizes)
- Hypothesis testing (H1.1 - H1.5)
- Visualization (plots, trajectories, distributions)
- Cross-condition comparison (TIER 6 vs TIER 5 vs Baseline)

Usage:
    python research_analysis.py --data research_data/ --output analysis_results/
"""

import argparse
import json
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict

# Visualization
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    PLOTTING_AVAILABLE = True
    sns.set_style("whitegrid")
except ImportError:
    PLOTTING_AVAILABLE = False
    print("Warning: matplotlib/seaborn not available. Plotting disabled.")

# Statistics
try:
    from scipy import stats
    STATS_AVAILABLE = True
except ImportError:
    STATS_AVAILABLE = False
    print("Warning: scipy not available. Statistical tests disabled.")


@dataclass
class SessionData:
    """Container for all data from a single session."""
    session_id: str
    condition: str  # "tier6", "tier5", or "baseline"

    decisions: pd.DataFrame
    ruminations: pd.DataFrame
    deaths: pd.DataFrame
    summary: Dict

    def __repr__(self):
        return (f"SessionData(id={self.session_id}, condition={self.condition}, "
                f"decisions={len(self.decisions)}, deaths={len(self.deaths)}, "
                f"ruminations={len(self.ruminations)})")


class ResearchAnalyzer:
    """Main analysis class for behavioral data."""

    def __init__(self, data_dir: str, output_dir: str = "analysis_results"):
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        self.sessions: List[SessionData] = []
        self.sessions_by_condition: Dict[str, List[SessionData]] = defaultdict(list)

        print(f"ResearchAnalyzer initialized")
        print(f"  Data directory: {self.data_dir}")
        print(f"  Output directory: {self.output_dir}")

    def load_sessions(self, pattern: str = "*"):
        """Load all sessions matching pattern from data directory."""
        print(f"\nLoading sessions from {self.data_dir}...")

        # Find all summary files
        summary_files = list(self.data_dir.glob(f"{pattern}_summary_*.json"))

        if not summary_files:
            print(f"No session summary files found matching pattern: {pattern}")
            return

        for summary_file in summary_files:
            try:
                session = self._load_session(summary_file)
                if session:
                    self.sessions.append(session)
                    self.sessions_by_condition[session.condition].append(session)
            except Exception as e:
                print(f"Error loading {summary_file}: {e}")

        print(f"Loaded {len(self.sessions)} sessions:")
        for condition, sessions in self.sessions_by_condition.items():
            print(f"  {condition}: {len(sessions)} sessions")

    def _load_session(self, summary_file: Path) -> Optional[SessionData]:
        """Load a single session from summary file."""
        # Extract session ID and timestamp from filename
        # Format: {session_id}_summary_{timestamp}.json
        parts = summary_file.stem.split('_summary_')
        if len(parts) != 2:
            print(f"Warning: Unexpected filename format: {summary_file}")
            return None

        session_id = parts[0]
        timestamp = parts[1]

        # Infer condition from session ID (or could be in summary)
        if 'tier6' in session_id.lower():
            condition = 'tier6'
        elif 'tier5' in session_id.lower():
            condition = 'tier5'
        elif 'baseline' in session_id.lower():
            condition = 'baseline'
        else:
            condition = 'unknown'

        # Load summary
        with open(summary_file, 'r') as f:
            summary = json.load(f)

        # Find corresponding data files
        decisions_file = self.data_dir / f"{session_id}_decisions_{timestamp}.csv"
        ruminations_file = self.data_dir / f"{session_id}_ruminations_{timestamp}.csv"
        deaths_file = self.data_dir / f"{session_id}_deaths_{timestamp}.csv"

        # Load DataFrames
        decisions = pd.read_csv(decisions_file) if decisions_file.exists() else pd.DataFrame()
        ruminations = pd.read_csv(ruminations_file) if ruminations_file.exists() else pd.DataFrame()
        deaths = pd.read_csv(deaths_file) if deaths_file.exists() else pd.DataFrame()

        return SessionData(
            session_id=session_id,
            condition=condition,
            decisions=decisions,
            ruminations=ruminations,
            deaths=deaths,
            summary=summary
        )

    def test_h1_1_post_death_latency(self, window_size: int = 20):
        """
        H1.1: TIER 6 agent shows increased decision latency following deaths.

        Compares decision latency in window_size decisions before vs after deaths.
        """
        print("\n" + "="*70)
        print("H1.1: POST-DEATH DECISION LATENCY")
        print("="*70)

        results = {}

        for condition in ['tier6', 'tier5', 'baseline']:
            if condition not in self.sessions_by_condition:
                continue

            latency_increases = []

            for session in self.sessions_by_condition[condition]:
                for _, death in session.deaths.iterrows():
                    death_time = death['timestamp']

                    # Get decisions before and after
                    before = session.decisions[session.decisions['timestamp'] < death_time].tail(window_size)
                    after = session.decisions[session.decisions['timestamp'] > death_time].head(window_size)

                    if len(before) >= 5 and len(after) >= 5:
                        latency_before = before['decision_latency_ms'].mean()
                        latency_after = after['decision_latency_ms'].mean()

                        increase = latency_after - latency_before
                        percent_increase = (increase / latency_before) * 100 if latency_before > 0 else 0

                        latency_increases.append(percent_increase)

            if latency_increases:
                results[condition] = {
                    'mean_increase': np.mean(latency_increases),
                    'std': np.std(latency_increases),
                    'n': len(latency_increases),
                    'data': latency_increases
                }

        # Print results
        for condition, result in results.items():
            print(f"\n{condition.upper()}:")
            print(f"  Mean latency increase: {result['mean_increase']:.1f}%")
            print(f"  Std: {result['std']:.1f}%")
            print(f"  N deaths: {result['n']}")

        # Statistical test
        if STATS_AVAILABLE and 'tier6' in results and 'tier5' in results:
            t_stat, p_value = stats.ttest_ind(results['tier6']['data'], results['tier5']['data'])
            print(f"\nTIER 6 vs TIER 5:")
            print(f"  t-statistic: {t_stat:.3f}")
            print(f"  p-value: {p_value:.4f}")
            print(f"  Significant: {'YES' if p_value < 0.05 else 'NO'}")

            # Effect size (Cohen's d)
            pooled_std = np.sqrt((results['tier6']['std']**2 + results['tier5']['std']**2) / 2)
            cohens_d = (results['tier6']['mean_increase'] - results['tier5']['mean_increase']) / pooled_std
            print(f"  Cohen's d: {cohens_d:.3f}")

        return results

    def test_h1_2_risk_aversion(self, window_size: int = 20):
        """
        H1.2: TIER 6 agent exhibits increased risk aversion following deaths.

        Measures: flee decisions, low-confidence decisions before/after death.
        """
        print("\n" + "="*70)
        print("H1.2: POST-DEATH RISK AVERSION")
        print("="*70)

        results = {}

        for condition in ['tier6', 'tier5', 'baseline']:
            if condition not in self.sessions_by_condition:
                continue

            risk_changes = []

            for session in self.sessions_by_condition[condition]:
                for _, death in session.deaths.iterrows():
                    death_time = death['timestamp']

                    before = session.decisions[session.decisions['timestamp'] < death_time].tail(window_size)
                    after = session.decisions[session.decisions['timestamp'] > death_time].head(window_size)

                    if len(before) >= 5 and len(after) >= 5:
                        # Risk metric: % of low-confidence decisions
                        risk_before = (before['confidence'] < 0.5).mean()
                        risk_after = (after['confidence'] < 0.5).mean()

                        risk_increase = risk_after - risk_before
                        risk_changes.append(risk_increase * 100)  # Convert to percentage points

            if risk_changes:
                results[condition] = {
                    'mean_increase': np.mean(risk_changes),
                    'std': np.std(risk_changes),
                    'n': len(risk_changes),
                    'data': risk_changes
                }

        # Print results
        for condition, result in results.items():
            print(f"\n{condition.upper()}:")
            print(f"  Mean risk aversion increase: {result['mean_increase']:.1f} percentage points")
            print(f"  Std: {result['std']:.1f}")
            print(f"  N deaths: {result['n']}")

        # Statistical test
        if STATS_AVAILABLE and 'tier6' in results and 'tier5' in results:
            t_stat, p_value = stats.ttest_ind(results['tier6']['data'], results['tier5']['data'])
            print(f"\nTIER 6 vs TIER 5:")
            print(f"  t-statistic: {t_stat:.3f}")
            print(f"  p-value: {p_value:.4f}")
            print(f"  Significant: {'YES' if p_value < 0.05 else 'NO'}")

        return results

    def test_h1_4_mental_load(self):
        """
        H1.4: High mental load reduces decision confidence.

        Correlation analysis: mental_load vs confidence.
        """
        print("\n" + "="*70)
        print("H1.4: MENTAL LOAD EFFECTS")
        print("="*70)

        results = {}

        for condition in ['tier6', 'tier5', 'baseline']:
            if condition not in self.sessions_by_condition:
                continue

            all_mental_loads = []
            all_confidences = []

            for session in self.sessions_by_condition[condition]:
                all_mental_loads.extend(session.decisions['mental_load'].values)
                all_confidences.extend(session.decisions['confidence'].values)

            if all_mental_loads:
                # Correlation
                correlation = np.corrcoef(all_mental_loads, all_confidences)[0, 1]

                # Group by mental load bins
                bins = [0, 0.3, 0.6, 1.0]
                labels = ['Low', 'Medium', 'High']
                df = pd.DataFrame({'mental_load': all_mental_loads, 'confidence': all_confidences})
                df['load_category'] = pd.cut(df['mental_load'], bins=bins, labels=labels)

                results[condition] = {
                    'correlation': correlation,
                    'n': len(all_mental_loads),
                    'avg_confidence_by_load': df.groupby('load_category')['confidence'].mean().to_dict()
                }

        # Print results
        for condition, result in results.items():
            print(f"\n{condition.upper()}:")
            print(f"  Correlation (load vs confidence): {result['correlation']:.3f}")
            print(f"  N decisions: {result['n']}")
            print(f"  Avg confidence by mental load:")
            for load_cat, conf in result['avg_confidence_by_load'].items():
                print(f"    {load_cat}: {conf:.3f}")

        return results

    def compute_human_likeness_scores(self):
        """Compute composite human-likeness scores for all sessions."""
        print("\n" + "="*70)
        print("HUMAN-LIKENESS SCORES")
        print("="*70)

        results = defaultdict(list)

        for session in self.sessions:
            score = session.summary.get('sub_optimal_decision_rate', 0) * 0.25 + \
                    session.summary.get('post_death_regret_rate', 0) * 0.20 + \
                    (session.summary.get('analysis_paralysis_events', 0) / max(1, session.summary.get('total_decisions', 1))) * 0.15 + \
                    session.summary.get('intrusive_thought_rate', 0) * 0.15 + \
                    (session.summary.get('total_ruminations', 0) / max(1, session.summary.get('total_decisions', 1))) * 0.25

            results[session.condition].append(score)

        # Print results
        for condition in ['tier6', 'tier5', 'baseline']:
            if condition in results:
                scores = results[condition]
                print(f"\n{condition.upper()}:")
                print(f"  Mean score: {np.mean(scores):.3f}")
                print(f"  Std: {np.std(scores):.3f}")
                print(f"  Min: {np.min(scores):.3f}")
                print(f"  Max: {np.max(scores):.3f}")
                print(f"  N: {len(scores)}")

        # Statistical comparison
        if STATS_AVAILABLE and len(results) >= 2:
            conditions = list(results.keys())
            if len(conditions) == 3:
                # ANOVA
                f_stat, p_value = stats.f_oneway(*[results[c] for c in conditions])
                print(f"\nANOVA across conditions:")
                print(f"  F-statistic: {f_stat:.3f}")
                print(f"  p-value: {p_value:.4f}")
                print(f"  Significant: {'YES' if p_value < 0.05 else 'NO'}")

        return results

    def plot_decision_latency_distributions(self):
        """Plot decision latency distributions by condition."""
        if not PLOTTING_AVAILABLE:
            print("Plotting not available (matplotlib/seaborn not installed)")
            return

        print("\nGenerating decision latency distribution plot...")

        fig, ax = plt.subplots(figsize=(10, 6))

        for condition in ['tier6', 'tier5', 'baseline']:
            if condition not in self.sessions_by_condition:
                continue

            latencies = []
            for session in self.sessions_by_condition[condition]:
                latencies.extend(session.decisions['decision_latency_ms'].values)

            if latencies:
                ax.hist(latencies, bins=50, alpha=0.5, label=condition.upper(), density=True)

        ax.set_xlabel('Decision Latency (ms)')
        ax.set_ylabel('Density')
        ax.set_title('Decision Latency Distributions by Condition')
        ax.legend()
        ax.set_xlim(0, 500)

        output_file = self.output_dir / 'decision_latency_distributions.png'
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"Saved to {output_file}")
        plt.close()

    def plot_mental_load_over_time(self):
        """Plot mental load trajectories over time."""
        if not PLOTTING_AVAILABLE:
            print("Plotting not available")
            return

        print("\nGenerating mental load trajectory plot...")

        fig, axes = plt.subplots(len(self.sessions_by_condition), 1,
                                 figsize=(12, 4 * len(self.sessions_by_condition)),
                                 squeeze=False)

        for i, (condition, sessions) in enumerate(self.sessions_by_condition.items()):
            ax = axes[i, 0]

            for session in sessions[:3]:  # Plot first 3 sessions per condition
                df = session.decisions.copy()
                df['time_hours'] = (df['timestamp'] - df['timestamp'].min()) / 3600

                ax.plot(df['time_hours'], df['mental_load'], alpha=0.6, linewidth=0.8)

            ax.set_xlabel('Time (hours)')
            ax.set_ylabel('Mental Load')
            ax.set_title(f'{condition.upper()} - Mental Load Over Time')
            ax.set_ylim(0, 1)
            ax.grid(True, alpha=0.3)

        plt.tight_layout()
        output_file = self.output_dir / 'mental_load_trajectories.png'
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"Saved to {output_file}")
        plt.close()

    def plot_post_death_behavior(self, window_size: int = 30):
        """Plot behavioral changes around death events."""
        if not PLOTTING_AVAILABLE:
            print("Plotting not available")
            return

        print("\nGenerating post-death behavior plot...")

        fig, axes = plt.subplots(2, 1, figsize=(12, 10))

        for condition in ['tier6', 'tier5', 'baseline']:
            if condition not in self.sessions_by_condition:
                continue

            latencies_timeline = defaultdict(list)
            confidence_timeline = defaultdict(list)

            for session in self.sessions_by_condition[condition]:
                for _, death in session.deaths.iterrows():
                    death_time = death['timestamp']

                    # Get decisions around death
                    window = session.decisions[
                        (session.decisions['timestamp'] >= death_time - window_size * 5) &
                        (session.decisions['timestamp'] <= death_time + window_size * 5)
                    ].copy()

                    window['relative_index'] = range(-len(window[window['timestamp'] < death_time]),
                                                     len(window[window['timestamp'] >= death_time]))

                    for idx, row in window.iterrows():
                        rel_idx = (window.loc[idx, 'relative_index'] // 5) * 5  # Bin into 5-decision chunks
                        latencies_timeline[rel_idx].append(row['decision_latency_ms'])
                        confidence_timeline[rel_idx].append(row['confidence'])

            # Compute means
            indices = sorted(latencies_timeline.keys())
            latency_means = [np.mean(latencies_timeline[i]) for i in indices]
            confidence_means = [np.mean(confidence_timeline[i]) for i in indices]

            axes[0].plot(indices, latency_means, marker='o', label=condition.upper(), linewidth=2)
            axes[1].plot(indices, confidence_means, marker='o', label=condition.upper(), linewidth=2)

        axes[0].axvline(x=0, color='red', linestyle='--', linewidth=2, label='Death')
        axes[0].set_xlabel('Decisions Relative to Death')
        axes[0].set_ylabel('Decision Latency (ms)')
        axes[0].set_title('Decision Latency Around Death Events')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)

        axes[1].axvline(x=0, color='red', linestyle='--', linewidth=2, label='Death')
        axes[1].set_xlabel('Decisions Relative to Death')
        axes[1].set_ylabel('Confidence')
        axes[1].set_title('Decision Confidence Around Death Events')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)

        plt.tight_layout()
        output_file = self.output_dir / 'post_death_behavior.png'
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"Saved to {output_file}")
        plt.close()

    def generate_full_report(self):
        """Generate comprehensive analysis report."""
        print("\n" + "="*70)
        print("GENERATING FULL ANALYSIS REPORT")
        print("="*70)

        report = []
        report.append("# Human-Equivalent Cognition Research - Analysis Report\n")
        report.append(f"Generated: {pd.Timestamp.now()}\n")
        report.append(f"\n## Sessions Loaded\n")

        for condition, sessions in self.sessions_by_condition.items():
            report.append(f"- {condition.upper()}: {len(sessions)} sessions\n")

        # Run all analyses
        report.append("\n## Hypothesis Tests\n")

        h1_1 = self.test_h1_1_post_death_latency()
        h1_2 = self.test_h1_2_risk_aversion()
        h1_4 = self.test_h1_4_mental_load()
        human_likeness = self.compute_human_likeness_scores()

        # Generate plots
        if PLOTTING_AVAILABLE:
            report.append("\n## Visualizations\n")
            self.plot_decision_latency_distributions()
            self.plot_mental_load_over_time()
            self.plot_post_death_behavior()
            report.append("- decision_latency_distributions.png\n")
            report.append("- mental_load_trajectories.png\n")
            report.append("- post_death_behavior.png\n")

        # Save report
        report_file = self.output_dir / 'analysis_report.md'
        with open(report_file, 'w') as f:
            f.writelines(report)

        print(f"\nReport saved to {report_file}")
        print("\nAnalysis complete!")


def main():
    parser = argparse.ArgumentParser(description='Analyze behavioral data from human-equivalent agents')
    parser.add_argument('--data', type=str, default='research_data',
                       help='Directory containing behavioral logs')
    parser.add_argument('--output', type=str, default='analysis_results',
                       help='Output directory for analysis results')
    parser.add_argument('--pattern', type=str, default='*',
                       help='Session ID pattern to match (default: all)')

    args = parser.parse_args()

    analyzer = ResearchAnalyzer(args.data, args.output)
    analyzer.load_sessions(pattern=args.pattern)

    if not analyzer.sessions:
        print("No sessions loaded. Exiting.")
        return

    analyzer.generate_full_report()


if __name__ == "__main__":
    main()
