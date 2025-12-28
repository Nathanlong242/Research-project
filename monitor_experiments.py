#!/usr/bin/env python3
"""
Real-time Experiment Monitoring Dashboard
Run this in a separate terminal while experiments are running.
"""

import os
import sys
import time
import glob
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name != 'nt' else 'cls')

def get_session_files():
    """Find all active session files"""
    data_dir = Path('research_data')
    if not data_dir.exists():
        return {}

    sessions = {}
    for csv in data_dir.glob('*_decisions_*.csv'):
        # Extract session ID from filename
        parts = csv.name.split('_')
        if len(parts) >= 2:
            session_id = '_'.join(parts[:2])  # e.g., "T7_RUN"
            if session_id not in sessions:
                sessions[session_id] = {}
            sessions[session_id]['decisions'] = csv

    for csv in data_dir.glob('*_ruminations_*.csv'):
        parts = csv.name.split('_')
        if len(parts) >= 2:
            session_id = '_'.join(parts[:2])
            if session_id not in sessions:
                sessions[session_id] = {}
            sessions[session_id]['ruminations'] = csv

    for csv in data_dir.glob('*_deaths_*.csv'):
        parts = csv.name.split('_')
        if len(parts) >= 2:
            session_id = '_'.join(parts[:2])
            if session_id not in sessions:
                sessions[session_id] = {}
            sessions[session_id]['deaths'] = csv

    return sessions

def analyze_session(session_files):
    """Compute real-time statistics for a session"""
    stats = {
        'decisions': 0,
        'ruminations': 0,
        'deaths': 0,
        'mean_latency': 0,
        'mean_mental_load': 0,
        'last_update': 'N/A',
        'errors': []
    }

    try:
        # Decisions
        if 'decisions' in session_files:
            df = pd.read_csv(session_files['decisions'])
            stats['decisions'] = len(df)
            if len(df) > 0:
                stats['mean_latency'] = df['decision_latency'].mean() if 'decision_latency' in df else 0
                stats['mean_mental_load'] = df['mental_load'].mean() if 'mental_load' in df else 0

                # Get last timestamp
                if 'timestamp' in df.columns:
                    last_time = df['timestamp'].iloc[-1]
                    stats['last_update'] = str(last_time)[:19]  # Truncate

        # Ruminations
        if 'ruminations' in session_files:
            df = pd.read_csv(session_files['ruminations'])
            stats['ruminations'] = len(df)

        # Deaths
        if 'deaths' in session_files:
            df = pd.read_csv(session_files['deaths'])
            stats['deaths'] = len(df)

    except Exception as e:
        stats['errors'].append(str(e)[:50])

    return stats

def format_duration(seconds):
    """Format seconds as HH:MM:SS"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def display_dashboard(sessions_stats, start_time):
    """Display formatted dashboard"""
    clear_screen()

    elapsed = time.time() - start_time

    print("=" * 80)
    print(f"EXPERIMENT MONITORING DASHBOARD - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Elapsed: {format_duration(elapsed)}")
    print("=" * 80)
    print()

    if not sessions_stats:
        print("No active sessions detected. Waiting for data files...")
        print()
        print("Expected files in research_data/:")
        print("  - *_decisions_*.csv")
        print("  - *_ruminations_*.csv")
        print("  - *_deaths_*.csv")
        print()
        return

    # Header
    header = f"{'Session':<20} {'Decisions':>10} {'Deaths':>8} {'Ruminations':>12} {'Latency':>10} {'MentalLoad':>12} {'LastUpdate':<20}"
    print(header)
    print("-" * 80)

    # Session rows
    for session_id, stats in sorted(sessions_stats.items()):
        row = (
            f"{session_id:<20} "
            f"{stats['decisions']:>10,} "
            f"{stats['deaths']:>8} "
            f"{stats['ruminations']:>12} "
            f"{stats['mean_latency']:>10.1f} "
            f"{stats['mean_mental_load']:>12.3f} "
            f"{stats['last_update']:<20}"
        )
        print(row)

        # Show errors if any
        if stats['errors']:
            for err in stats['errors']:
                print(f"  ⚠ {err}")

    print()
    print("=" * 80)

    # Summary stats
    total_decisions = sum(s['decisions'] for s in sessions_stats.values())
    total_deaths = sum(s['deaths'] for s in sessions_stats.values())
    total_ruminations = sum(s['ruminations'] for s in sessions_stats.values())

    print(f"TOTALS: {total_decisions:,} decisions | {total_deaths} deaths | {total_ruminations} ruminations")

    # Health checks
    print()
    print("HEALTH CHECKS:")

    for session_id, stats in sessions_stats.items():
        issues = []

        # Check if data is flowing
        if stats['decisions'] == 0:
            issues.append("No decisions logged yet")

        # Check if rumination system is working (for TIER 6/7)
        if 'T6' in session_id or 'T7' in session_id:
            if stats['decisions'] > 100 and stats['ruminations'] == 0:
                issues.append("No ruminations despite >100 decisions (check TIER 6 triggering)")

        # Check if deaths are happening
        if stats['decisions'] > 500 and stats['deaths'] == 0:
            issues.append("No deaths logged (unusually safe gameplay)")

        # Check decision rate
        if elapsed > 600 and stats['decisions'] < 50:  # After 10 min, should have 50+ decisions
            decisions_per_min = stats['decisions'] / (elapsed / 60)
            issues.append(f"Low decision rate: {decisions_per_min:.1f}/min (expected ~5-10/min)")

        if issues:
            print(f"  ⚠ {session_id}: {', '.join(issues)}")
        else:
            print(f"  ✓ {session_id}: Healthy")

    print()
    print("Press Ctrl+C to stop monitoring")
    print()

def main():
    """Main monitoring loop"""
    print("Starting experiment monitor...")
    print("Monitoring research_data/ for active sessions...")
    print()

    start_time = time.time()

    try:
        while True:
            sessions = get_session_files()
            sessions_stats = {sid: analyze_session(files) for sid, files in sessions.items()}
            display_dashboard(sessions_stats, start_time)
            time.sleep(5)  # Update every 5 seconds

    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")
        print("Session data preserved in research_data/")
        return 0

if __name__ == '__main__':
    sys.exit(main())
