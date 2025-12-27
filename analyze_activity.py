#!/usr/bin/env python3
"""
analyze_activity.py
A simple script to summarize beaver activity observations recorded in a CSV file.

The CSV should have the following columns (see beaver_activity_template.csv):
    Date, Observer, Location, Activity Type, Impact Notes

Usage:
    python analyze_activity.py <input_csv>
Example:
    python analyze_activity.py beaver_activity_template.csv
"""

import sys
import csv
from collections import Counter
from datetime import datetime

def load_observations(filename):
    """Load observations from CSV, return list of dicts."""
    observations = []
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            # Ensure required columns exist
            required = {'Date', 'Observer', 'Location (GPS or description)', 'Activity Type', 'Impact Notes'}
            if not required.issubset(reader.fieldnames):
                print(f"Error: CSV must contain columns {required}")
                sys.exit(1)
            for row in reader:
                observations.append(row)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        sys.exit(1)
    return observations

def summarize(observations):
    """Generate summary statistics."""
    total = len(observations)
    if total == 0:
        print("No observations found.")
        return
    
    # Count activities
    activity_counts = Counter(obs['Activity Type'] for obs in observations)
    
    # Count observers
    observer_counts = Counter(obs['Observer'] for obs in observations)
    
    # Extract months for temporal trend
    months = []
    for obs in observations:
        try:
            dt = datetime.strptime(obs['Date'], '%Y-%m-%d')
            months.append(dt.strftime('%Y-%m'))
        except ValueError:
            pass
    month_counts = Counter(months)
    
    # Print report
    print("=" * 60)
    print("BEAVER ACTIVITY ANALYSIS REPORT")
    print("=" * 60)
    print(f"Total observations: {total}")
    print()
    
    print("Activity Type Frequency:")
    for activity, count in activity_counts.most_common():
        print(f"  {activity}: {count} ({count/total*100:.1f}%)")
    print()
    
    print("Observer Contributions:")
    for observer, count in observer_counts.most_common():
        print(f"  {observer}: {count} observations")
    print()
    
    print("Observations per Month:")
    for month, count in sorted(month_counts.items()):
        print(f"  {month}: {count}")
    print()
    
    # Show a few sample impacts
    print("Sample Impact Notes (first 5):")
    for i, obs in enumerate(observations[:5]):
        print(f"  {obs['Date']} – {obs['Activity Type']}: {obs['Impact Notes']}")
    print("=" * 60)

def main():
    if len(sys.argv) != 2:
        print(__doc__)
        print("\nPlease provide the CSV file path.")
        sys.exit(1)
    
    filename = sys.argv[1]
    observations = load_observations(filename)
    summarize(observations)

if __name__ == '__main__':
    main()