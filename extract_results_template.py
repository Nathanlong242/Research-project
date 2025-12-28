#!/usr/bin/env python3
"""
Results Extraction Template
Run this after experiments complete to extract statistics for paper Section 5.

Usage:
  python extract_results_template.py --data research_data/ --output paper_results.md
"""

import argparse
import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats
import json

def load_all_sessions(data_dir, pattern='*_decisions_*.csv'):
    """Load all decision CSVs matching pattern"""
    dfs = []
    for csv in Path(data_dir).glob(pattern):
        df = pd.read_csv(csv)
        # Extract condition from filename
        if 'T7' in csv.name:
            df['condition'] = 'TIER7'
        elif 'T6' in csv.name:
            df['condition'] = 'TIER6'
        elif 'T5' in csv.name:
            df['condition'] = 'TIER5'
        dfs.append(df)

    if not dfs:
        raise ValueError(f"No CSV files found matching {pattern} in {data_dir}")

    return pd.concat(dfs, ignore_index=True)

def test_h6_1_post_death_latency(data_dir):
    """H6.1: Post-death decision latency increase"""

    # Load deaths
    deaths = load_all_sessions(data_dir, '*_deaths_*.csv')
    decisions = load_all_sessions(data_dir, '*_decisions_*.csv')

    # For each death, get next 20 decisions
    post_death_latencies = {'TIER6': [], 'TIER5': []}
    pre_death_latencies = {'TIER6': [], 'TIER5': []}

    # This is simplified - actual implementation needs to match deaths to decision timestamps
    # and extract windows before/after each death

    # Placeholder logic:
    tier6_post = decisions[(decisions['condition'] == 'TIER6') & (decisions['post_death_window'] == True)]['decision_latency']
    tier6_pre = decisions[(decisions['condition'] == 'TIER6') & (decisions['post_death_window'] == False)]['decision_latency']

    tier5_post = decisions[(decisions['condition'] == 'TIER5') & (decisions['post_death_window'] == True)]['decision_latency']
    tier5_pre = decisions[(decisions['condition'] == 'TIER5') & (decisions['post_death_window'] == False)]['decision_latency']

    # T-test
    t_stat, p_value = stats.ttest_ind(tier6_post, tier5_post)
    cohens_d = (tier6_post.mean() - tier5_post.mean()) / np.sqrt((tier6_post.std()**2 + tier5_post.std()**2) / 2)

    return {
        'hypothesis': 'H6.1',
        'tier6_post_mean': tier6_post.mean(),
        'tier6_post_std': tier6_post.std(),
        'tier6_pre_mean': tier6_pre.mean(),
        'tier5_post_mean': tier5_post.mean(),
        't_statistic': t_stat,
        'p_value': p_value,
        'cohens_d': cohens_d,
        'supported': p_value < 0.005  # Bonferroni corrected alpha
    }

def test_h7_1_suppression_paradox(data_dir):
    """H7.1: Thought suppression increases intrusion frequency"""

    ruminations = load_all_sessions(data_dir, '*_ruminations_*.csv')

    # Filter to TIER7 only (only tier with suppression)
    tier7 = ruminations[ruminations['condition'] == 'TIER7']

    # Compare intrusion rates for suppressed vs non-suppressed ruminations
    suppressed = tier7[tier7['suppressed'] == True]['intrusion_frequency']
    not_suppressed = tier7[tier7['suppressed'] == False]['intrusion_frequency']

    # T-test
    t_stat, p_value = stats.ttest_ind(suppressed, not_suppressed)
    cohens_d = (suppressed.mean() - not_suppressed.mean()) / np.sqrt((suppressed.std()**2 + not_suppressed.std()**2) / 2)

    # Percent increase
    pct_increase = (suppressed.mean() - not_suppressed.mean()) / not_suppressed.mean() * 100

    return {
        'hypothesis': 'H7.1',
        'suppressed_mean': suppressed.mean(),
        'suppressed_std': suppressed.std(),
        'not_suppressed_mean': not_suppressed.mean(),
        'percent_increase': pct_increase,
        't_statistic': t_stat,
        'p_value': p_value,
        'cohens_d': cohens_d,
        'supported': p_value < 0.005 and pct_increase > 30
    }

def generate_paper_text(results):
    """Generate markdown text for paper Section 5"""

    md = []
    md.append("# Section 5: Results (Generated from Actual Data)\n")
    md.append("## 5.2 TIER 6 Results: Rumination Effects\n")

    # H6.1
    h6_1 = results['H6.1']
    md.append("### H6.1: Post-Death Decision Latency\n")
    md.append(f"**Hypothesis**: Agents with rumination (TIER 6) exhibit increased decision latency in the 20 decisions following death.\n")
    md.append(f"\n**Results**:\n")
    md.append(f"```")
    md.append(f"Condition        Mean Latency (ms)    SD")
    md.append(f"-------------------------------------------------")
    md.append(f"TIER 6 (post)    {h6_1['tier6_post_mean']:.1f}               {h6_1['tier6_post_std']:.1f}")
    md.append(f"TIER 6 (pre)     {h6_1['tier6_pre_mean']:.1f}               ")
    md.append(f"TIER 5 (post)    {h6_1['tier5_post_mean']:.1f}               ")
    md.append(f"")
    md.append(f"t-test: t = {h6_1['t_statistic']:.2f}, p = {h6_1['p_value']:.4f}, d = {h6_1['cohens_d']:.2f}")
    md.append(f"```\n")

    if h6_1['supported']:
        pct = (h6_1['tier6_post_mean'] - h6_1['tier5_post_mean']) / h6_1['tier5_post_mean'] * 100
        md.append(f"**Interpretation**: ✓ SUPPORTED - TIER 6 agents show {pct:.0f}% increase in decision latency after death.\n")
    else:
        md.append(f"**Interpretation**: ✗ NOT SUPPORTED - Effect size smaller than predicted.\n")

    # H7.1
    md.append("\n## 5.3 TIER 7 Results: Meta-Cognitive Self-Regulation\n")
    h7_1 = results['H7.1']
    md.append("### H7.1: Suppression Paradox\n")
    md.append(f"**Hypothesis**: Thought suppression increases intrusion frequency by 30-50%.\n")
    md.append(f"\n**Results**:\n")
    md.append(f"```")
    md.append(f"Suppressed:     {h7_1['suppressed_mean']:.2f} intrusions/hour (SD={h7_1['suppressed_std']:.2f})")
    md.append(f"Not Suppressed: {h7_1['not_suppressed_mean']:.2f} intrusions/hour")
    md.append(f"Increase:       {h7_1['percent_increase']:.1f}%")
    md.append(f"")
    md.append(f"t-test: t = {h7_1['t_statistic']:.2f}, p = {h7_1['p_value']:.4f}, d = {h7_1['cohens_d']:.2f}")
    md.append(f"```\n")

    if h7_1['supported']:
        md.append(f"**Interpretation**: ✓ SUPPORTED - Suppressed thoughts intrude {h7_1['percent_increase']:.0f}% more frequently, demonstrating ironic process effect.\n")
    else:
        md.append(f"**Interpretation**: ✗ NOT SUPPORTED - Effect not significant or magnitude below threshold.\n")

    return '\n'.join(md)

def main():
    parser = argparse.ArgumentParser(description='Extract results for paper Section 5')
    parser.add_argument('--data', default='research_data/', help='Data directory')
    parser.add_argument('--output', default='paper_results.md', help='Output markdown file')
    args = parser.parse_args()

    print(f"Loading data from {args.data}...")

    # Test all hypotheses
    results = {}

    print("Testing H6.1: Post-death decision latency...")
    try:
        results['H6.1'] = test_h6_1_post_death_latency(args.data)
        print(f"  ✓ H6.1: {'SUPPORTED' if results['H6.1']['supported'] else 'NOT SUPPORTED'}")
    except Exception as e:
        print(f"  ✗ H6.1: Failed - {e}")
        results['H6.1'] = {'error': str(e)}

    print("Testing H7.1: Suppression paradox...")
    try:
        results['H7.1'] = test_h7_1_suppression_paradox(args.data)
        print(f"  ✓ H7.1: {'SUPPORTED' if results['H7.1']['supported'] else 'NOT SUPPORTED'}")
    except Exception as e:
        print(f"  ✗ H7.1: Failed - {e}")
        results['H7.1'] = {'error': str(e)}

    # TODO: Add tests for H6.2, H6.3, H6.4, H7.2, H7.3, H7.4, H7.5

    # Generate paper text
    print(f"\nGenerating paper text...")
    paper_text = generate_paper_text(results)

    # Save
    with open(args.output, 'w') as f:
        f.write(paper_text)

    print(f"✓ Results saved to {args.output}")

    # Save raw statistics
    stats_file = args.output.replace('.md', '_stats.json')
    with open(stats_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"✓ Raw statistics saved to {stats_file}")

    # Summary
    supported = sum(1 for r in results.values() if isinstance(r, dict) and r.get('supported', False))
    total = len([r for r in results.values() if isinstance(r, dict) and 'supported' in r])

    print(f"\n{'='*60}")
    print(f"HYPOTHESIS TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Supported: {supported}/{total} hypotheses")
    print(f"Minimum for publication: 5/10")
    print(f"Strong publication: 8/10")
    print(f"\nNext steps:")
    if supported >= 5:
        print("  ✓ Sufficient evidence for publication")
        print("  → Update RESEARCH_PAPER.md Section 5 with actual results")
        print("  → Revise Discussion based on findings")
    else:
        print("  ⚠ Below publication threshold")
        print("  → Review failed hypotheses")
        print("  → Consider parameter adjustments or exploratory analysis")

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
