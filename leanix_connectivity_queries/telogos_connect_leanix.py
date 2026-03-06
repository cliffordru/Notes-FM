#!/usr/bin/env python3
"""
Telogos Connect - LeanIX Data Pipeline
This script connects to LeanIX GraphQL API and retrieves application factsheet data.
"""

import os
import sys
import json
import argparse
import requests
import pandas as pd
from pathlib import Path
from datetime import datetime

# LeanIX API Configuration
LEANIX_TOKEN_URL = 'https://fmglobal.leanix.net/services/mtm/v1/oauth2/token'
LEANIX_GRAPHQL_URL = 'https://fmglobal.leanix.net/services/pathfinder/v1/graphql'
LEANIX_USERNAME = 'apitoken'
# Note: In production, retrieve password from secure storage
LEANIX_PASSWORD = os.getenv('LEANIX_API_TOKEN', 'cnskscsY3QzDuLfPMCtYYm2kwxLkTQtu8wGPKRKa')

# Directory structure
DATA_DIR = Path(__file__).parent / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
QUERIES_DIR = Path(__file__).parent / "queries"

def load_graphql_query(query_name):
    """
    Load a GraphQL query from the queries directory.
    
    Args:
        query_name: Name of the query file (without .graphql extension)
    
    Returns:
        The query string
    """
    query_file = QUERIES_DIR / f"{query_name}.graphql"
    
    if not query_file.exists():
        raise FileNotFoundError(f"Query file not found: {query_file}")
    
    with open(query_file, 'r', encoding='utf-8') as f:
        return f.read()

def get_leanix_token():
    """
    Authenticate with LeanIX and retrieve an access token.
    Returns the Bearer token string for API requests.
    """
    print("Authenticating with LeanIX...")
    
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = 'grant_type=client_credentials'
    
    try:
        response = requests.post(
            LEANIX_TOKEN_URL,
            headers=headers,
            data=data,
            auth=(LEANIX_USERNAME, LEANIX_PASSWORD)
        )
        response.raise_for_status()
        token_data = response.json()
        
        print("✓ Successfully authenticated with LeanIX")
        return 'Bearer ' + token_data['access_token']
    
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed to authenticate with LeanIX: {str(e)}")
        return None

def get_application_factsheets(token, enriched=False):
    """
    Query LeanIX GraphQL API for application factsheets with relationships.
    
    Args:
        token: Bearer token for authentication
        enriched: If True, use enriched query with all relationships
    
    Returns the JSON response containing all application data.
    """
    query_name = "leanix_applications_enriched" if enriched else "leanix_applications_basic"
    print(f"\nQuerying LeanIX for application factsheets (query: {query_name})...")
    
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    # Load GraphQL query from file
    query_string = load_graphql_query(query_name)
    
    # Build request payload
    graphql_query = {
        "query": query_string,
        "operationName": "application_enriched" if enriched else "factSheetDetailsQuery"
    }
    
    # Add variables for basic query (enriched query has them inline)
    if not enriched:
        graphql_query["variables"] = {
            "filter": {
                "responseOptions": {"maxFacetDepth": 10},
                "facetFilters": [{"facetKey": "FactSheetTypes", "operator": "OR", "keys": ["Application"]}]
            },
            "sortings": [{"key": "updatedAt", "order": "desc"}]
        }
    
    try:
        response = requests.post(LEANIX_GRAPHQL_URL, headers=headers, json=graphql_query)
        response.raise_for_status()
        
        data = response.json()
        total_count = data['data']['allFactSheets']['totalCount']
        
        print(f"✓ Retrieved {total_count} applications from LeanIX")
        return data
    
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed to query LeanIX: {str(e)}")
        return None

def parse_factsheets_to_dataframe(factsheet_data, enriched=False):
    """
    Parse LeanIX factsheet JSON data into a pandas DataFrame.
    Flattens the nested structure for easier analysis.
    """
    print("\nParsing factsheet data...")
    
    applications = []
    
    for edge in factsheet_data['data']['allFactSheets']['edges']:
        app = edge['node']
        
        # Base fields (always present)
        app_data = {
            'leanix_id': app['id'],
            'name': app['name'],
            'alias': app.get('alias', ''),
            'display_name': app.get('displayName', ''),
            'description': app.get('description', ''),
            'type': app.get('type', ''),
            'status': app.get('status', ''),
            'created_at': app.get('createdAt', ''),
            'updated_at': app.get('updatedAt', '')
        }
        
        # Enriched fields (only if using enriched query)
        if enriched:
            app_data.update({
                'business_criticality': app.get('businessCriticality', ''),
                'business_criticality_description': app.get('businessCriticalityDescription', ''),
                'functional_suitability': app.get('functionalSuitability', ''),
                'functional_suitability_description': app.get('functionalSuitabilityDescription', ''),
                'technical_suitability': app.get('technicalSuitability', ''),
                'technical_suitability_description': app.get('technicalSuitabilityDescription', ''),
                'aggregated_obsolescence_risk': app.get('aggregatedObsolescenceRisk', ''),
                'mitigated_obsolescence_risk_percentage': app.get('mitigatedObsolescenceRiskPercentage', ''),
                'unaddressed_obsolescence_risk_percentage': app.get('unaddressedObsolescenceRiskPercentage', '')
            })
            
            # Lifecycle information
            lifecycle = app.get('lifecycle', {})
            if lifecycle:
                app_data['lifecycle_status'] = lifecycle.get('asString', '')
                phases = lifecycle.get('phases', [])
                if phases:
                    app_data['lifecycle_current_phase'] = phases[0].get('phase', '') if len(phases) > 0 else ''
            else:
                app_data['lifecycle_status'] = ''
                app_data['lifecycle_current_phase'] = ''
            
            # Subscriptions (owners, accountable, etc.)
            subscriptions = app.get('subscriptions', {}).get('edges', [])
            responsible_users = [s['node']['user']['displayName'] for s in subscriptions if s['node'].get('type') == 'RESPONSIBLE' and s['node'].get('user')]
            accountable_users = [s['node']['user']['displayName'] for s in subscriptions if s['node'].get('type') == 'ACCOUNTABLE' and s['node'].get('user')]
            app_data['responsible_users'] = ', '.join(responsible_users)
            app_data['accountable_users'] = ', '.join(accountable_users)
            app_data['subscription_count'] = len(subscriptions)
            
            # Relationship counts
            app_data['business_capability_count'] = len(app.get('relApplicationToBusinessCapability', {}).get('edges', []))
            app_data['it_component_count'] = len(app.get('relApplicationToITComponent', {}).get('edges', []))
            app_data['consumer_interface_count'] = len(app.get('relConsumerApplicationToInterface', {}).get('edges', []))
            app_data['provider_interface_count'] = len(app.get('relProviderApplicationToInterface', {}).get('edges', []))
            app_data['tech_owner_user_group_count'] = len(app.get('relTechOwnerApplicationToUserGroup', {}).get('edges', []))
            app_data['user_group_count'] = len(app.get('relApplicationToUserGroup', {}).get('edges', []))
            app_data['document_count'] = len(app.get('documents', {}).get('edges', []))
        
        applications.append(app_data)
    
    df = pd.DataFrame(applications)
    
    # Normalize column names
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    
    print(f"✓ Parsed {len(df)} applications")
    print(f"✓ Extracted {len(df.columns)} columns")
    return df

# ============================================================================
# ACQUISITION PHASE - Download and cache raw JSON data
# ============================================================================

def acquire_leanix_data(enriched=False):
    """
    Acquisition phase: Download data from LeanIX GraphQL API and save raw JSON.
    Returns the raw data and timestamp.
    """
    print("=" * 70)
    print("ACQUISITION PHASE: Downloading data from LeanIX API")
    print("=" * 70)
    
    # Ensure raw directory exists
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    
    # Authenticate
    token = get_leanix_token()
    if not token:
        return None, None
    
    # Query for factsheets
    factsheet_data = get_application_factsheets(token, enriched=enriched)
    if not factsheet_data:
        return None, None
    
    # Save raw JSON with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    query_type = "enriched" if enriched else "basic"
    json_file = RAW_DIR / f"leanix_applications_{query_type}_{timestamp}.json"
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(factsheet_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Acquisition complete: {factsheet_data['data']['allFactSheets']['totalCount']} applications")
    print(f"✓ Raw data saved to: {json_file}")
    
    return factsheet_data, timestamp

# ============================================================================
# PROCESSING PHASE - Parse JSON and create consolidated CSV
# ============================================================================

def process_leanix_data(json_file=None, enriched=False):
    """
    Processing phase: Parse JSON data and create CSV.
    If json_file is None, processes the most recent file.
    """
    print("=" * 70)
    print("PROCESSING PHASE: Parsing JSON and creating CSV")
    print("=" * 70)
    
    # Ensure processed directory exists
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load JSON data
    if json_file is None:
        # Find most recent JSON file
        query_type = "enriched" if enriched else "basic"
        json_files = sorted(RAW_DIR.glob(f"leanix_applications_{query_type}_*.json"))
        if not json_files:
            print(f"⚠ No LeanIX JSON files found in {RAW_DIR}")
            return None
        json_file = json_files[-1]
    
    print(f"\nLoading data from: {json_file.name}")
    
    with open(json_file, 'r', encoding='utf-8') as f:
        factsheet_data = json.load(f)
    
    # Parse to DataFrame
    df = parse_factsheets_to_dataframe(factsheet_data, enriched=enriched)
    
    # Save to CSV
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    query_type = "enriched" if enriched else "basic"
    csv_file = PROCESSED_DIR / f"leanix_applications_{query_type}_{timestamp}.csv"
    
    df.to_csv(csv_file, index=False)
    
    print(f"\n✓ Consolidated dataset created: {len(df)} rows")
    print(f"✓ Output saved to: {csv_file}")
    print(f"✓ Columns: {len(df.columns)} total")
    
    return csv_file

def display_summary(df):
    """Display summary statistics of LeanIX data"""
    print("\n" + "=" * 70)
    print("LEANIX DATA SUMMARY")
    print("=" * 70)
    
    print(f"\nTotal Applications: {len(df)}")
    print(f"Total Columns: {len(df.columns)}")
    
    if 'alias' in df.columns:
        apps_with_alias = df['alias'].notna().sum()
        print(f"Applications with alias: {apps_with_alias}")
    
    print(f"\nSample applications:")
    print(df[['name', 'alias', 'display_name']].head(5).to_string(index=False))

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description='Telogos Connect - LeanIX Data Pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run full pipeline (acquire + process) with enriched data
  python telogos_connect_leanix.py --enriched
  
  # Only download data from API
  python telogos_connect_leanix.py --acquire --enriched
  
  # Only process existing JSON files
  python telogos_connect_leanix.py --process --enriched
  
  # Test connectivity only (no data save)
  python telogos_connect_leanix.py --test-only --enriched
        """
    )
    
    parser.add_argument('--acquire', action='store_true',
                        help='Run acquisition phase only (download JSON from API)')
    parser.add_argument('--process', action='store_true',
                        help='Run processing phase only (parse JSON to CSV)')
    parser.add_argument('--test-only', action='store_true',
                        help='Test connectivity only, do not save data')
    parser.add_argument('--enriched', action='store_true',
                        help='Use enriched query with all relationships and metadata')
    
    args = parser.parse_args()
    
    # Determine what to run
    run_acquire = args.acquire or (not args.acquire and not args.process and not args.test_only)
    run_process = args.process or (not args.acquire and not args.process and not args.test_only)
    
    try:
        # Test-only mode (legacy behavior)
        if args.test_only:
            token = get_leanix_token()
            if not token:
                sys.exit(1)
            
            factsheet_data = get_application_factsheets(token, enriched=args.enriched)
            if not factsheet_data:
                sys.exit(1)
            
            df = parse_factsheets_to_dataframe(factsheet_data, enriched=args.enriched)
            display_summary(df)
            
            print("\n" + "=" * 70)
            print("CONNECTIVITY TEST COMPLETE")
            print("=" * 70)
            return
        
        # Run acquisition if requested
        if run_acquire:
            factsheet_data, timestamp = acquire_leanix_data(enriched=args.enriched)
            if not factsheet_data:
                print("\n✗ Acquisition failed")
                sys.exit(1)
        
        # Run processing if requested
        if run_process:
            output_file = process_leanix_data(enriched=args.enriched)
            if output_file:
                print("\n" + "=" * 70)
                print("PIPELINE COMPLETE")
                print("=" * 70)
                print(f"LeanIX data available at: {output_file}")
    
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
