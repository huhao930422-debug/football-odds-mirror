#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Football Data Fetcher
Downloads complete CSV data from football-data.co.uk
"""

import requests
import time
from pathlib import Path
import sys


# European leagues: code -> directory name
# URL format: mmz4281/{season}/{code}.csv
EUROPEAN_LEAGUES = {
    'E0': 'premier-league',
    'SP1': 'la-liga',
    'I1': 'serie-a',
    'D1': 'bundesliga',
    'F1': 'ligue-1',
    'E1': 'championship',
    'E2': 'league-one',
    'D2': 'bundesliga-2',
    'I2': 'serie-b',
    'SP2': 'la-liga-2',
    'F2': 'ligue-2',
    'SC0': 'scottish-premiership',
    'SC1': 'scottish-championship',
    'N1': 'eredivisie',
    'B1': 'jupiler-league',
    'P1': 'primeira-liga',
    'T1': 'super-lig',
}

# Extra leagues (non-European): code -> directory name
# URL format: new/{code}.csv (all seasons in one file)
EXTRA_LEAGUES = {
    'BRA': 'brazil',
    'DNK': 'denmark',
    'FIN': 'finland',
    'JPN': 'japan',
    'NOR': 'norway',
    'SWE': 'sweden',
    'USA': 'usa',
}

# Base URLs
BASE_URL_EUROPEAN = 'https://www.football-data.co.uk/mmz4281'
BASE_URL_EXTRA = 'https://www.football-data.co.uk/new'

# User-Agent header to mimic browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}


def generate_seasons():
    """Generate season codes from 9394 to 2526."""
    seasons = []

    # 1993/94 to 1999/00
    for year in range(93, 100):
        next_year = (year + 1) % 100
        seasons.append(f'{year:02d}{next_year:02d}')

    # 2000/01 to 2025/26
    for year in range(0, 26):
        next_year = year + 1
        seasons.append(f'{year:02d}{next_year:02d}')

    return seasons


def download_csv(league_code, season, output_path):
    """
    Download a single CSV file for European leagues.

    Returns:
        'success': downloaded and saved
        'unchanged': downloaded but identical to existing file
        'error': failed to download
    """
    url = f'{BASE_URL_EUROPEAN}/{season}/{league_code}.csv'

    try:
        response = requests.get(url, headers=HEADERS, timeout=30)

        if response.status_code == 404:
            print(f'  [404] {url}')
            return 'error'

        response.raise_for_status()
        content = response.content

        # Check if file exists and is identical
        if output_path.exists():
            existing_content = output_path.read_bytes()
            if existing_content == content:
                print(f'  [SKIP] {output_path.name} (unchanged)')
                return 'unchanged'

        # Save the file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(content)
        print(f'  [OK] {output_path.name} ({len(content)} bytes)')
        return 'success'

    except requests.RequestException as e:
        print(f'  [ERROR] {url}: {e}')
        return 'error'


def download_extra_league(league_code, league_dir):
    """
    Download all-seasons CSV file for extra (non-European) leagues.

    Returns:
        'success': downloaded and saved
        'unchanged': downloaded but identical to existing file
        'error': failed to download
    """
    url = f'{BASE_URL_EXTRA}/{league_code}.csv'
    output_path = Path('data') / league_dir / 'all-seasons.csv'

    # Sleep before request to be polite
    time.sleep(3)

    try:
        response = requests.get(url, headers=HEADERS, timeout=30)

        if response.status_code == 404:
            print(f'  [404] {url}')
            return 'error'

        response.raise_for_status()
        content = response.content

        # Check if file exists and is identical
        if output_path.exists():
            existing_content = output_path.read_bytes()
            if existing_content == content:
                print(f'  [SKIP] all-seasons.csv (unchanged)')
                return 'unchanged'

        # Save the file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(content)
        print(f'  [OK] all-seasons.csv ({len(content)} bytes)')
        return 'success'

    except requests.RequestException as e:
        print(f'  [ERROR] {url}: {e}')
        return 'error'


def main():
    """Main function to download all data."""
    print('Football Data Fetcher')
    print('=' * 60)

    seasons = generate_seasons()
    print(f'Seasons to fetch: {len(seasons)} (from 9394 to 2526)')
    print(f'European leagues: {len(EUROPEAN_LEAGUES)}')
    print(f'Extra leagues: {len(EXTRA_LEAGUES)}')
    print(f'Total European files to check: {len(seasons) * len(EUROPEAN_LEAGUES)}')

    # Determine active seasons (most recent 2 seasons)
    active_seasons = seasons[-2:]
    print(f'Active seasons (will be downloaded): {active_seasons}')
    print('=' * 60)

    stats = {
        'success': 0,
        'unchanged': 0,
        'error': 0,
        'kept': 0,
        'extra_updated': 0,
        'extra_unchanged': 0
    }

    # Process European leagues
    print('\n### EUROPEAN LEAGUES ###')
    for league_code, league_dir in EUROPEAN_LEAGUES.items():
        print(f'\n[{league_code}] {league_dir}')

        for season in seasons:
            output_path = Path('data') / league_dir / f'season-{season}.csv'

            # Skip historical files that already exist locally
            if season not in active_seasons and output_path.exists():
                print(f'  [KEEP] {output_path.name} (historical, unchanged)')
                stats['kept'] += 1
                continue

            result = download_csv(league_code, season, output_path)
            stats[result] += 1

            # Be polite: wait 3 seconds between requests
            time.sleep(3)

    # Process extra leagues
    print('\n### EXTRA LEAGUES (NON-EUROPEAN) ###')
    for league_code, league_dir in EXTRA_LEAGUES.items():
        print(f'\n[{league_code}] {league_dir}')

        result = download_extra_league(league_code, league_dir)
        if result == 'success':
            stats['extra_updated'] += 1
        elif result == 'unchanged':
            stats['extra_unchanged'] += 1
        else:
            stats['error'] += 1

    print('\n' + '=' * 60)
    print('Summary:')
    print(f'  European leagues:')
    print(f'    - Successfully downloaded: {stats["success"]} files')
    print(f'    - Skipped (unchanged): {stats["unchanged"]} files')
    print(f'    - Kept (historical): {stats["kept"]} files')
    print(f'  Extra leagues:')
    print(f'    - Updated: {stats["extra_updated"]} files')
    print(f'    - Unchanged: {stats["extra_unchanged"]} files')
    print(f'  Total errors: {stats["error"]} files')
    print('=' * 60)

    # Exit with error code if all downloads failed
    if stats['success'] == 0 and stats['unchanged'] == 0 and stats['extra_updated'] == 0 and stats['extra_unchanged'] == 0:
        print('ERROR: No files were downloaded successfully!')
        sys.exit(1)


if __name__ == '__main__':
    main()
