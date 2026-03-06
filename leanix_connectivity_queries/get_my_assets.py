#!/usr/bin/env python3
"""
Script to retrieve all LeanIX assets (Applications, IT Components, etc.) 
where clifford.gray@fm.com is RESPONSIBLE.
"""

import os
import json
import requests

# LeanIX API Configuration
LEANIX_TOKEN_URL = 'https://fmglobal.leanix.net/services/mtm/v1/oauth2/token'
LEANIX_GRAPHQL_URL = 'https://fmglobal.leanix.net/services/pathfinder/v1/graphql'
LEANIX_USERNAME = 'apitoken'
LEANIX_PASSWORD = os.getenv('LEANIX_API_TOKEN', 'cnskscsY3QzDuLfPMCtYYm2kwxLkTQtu8wGPKRKa')

# Email to filter by
TARGET_EMAIL = 'clifford.gray@fm.com'


def get_leanix_token():
    """Authenticate with LeanIX and retrieve an access token."""
    print("Authenticating with LeanIX...")
    
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = 'grant_type=client_credentials'
    
    response = requests.post(
        LEANIX_TOKEN_URL,
        headers=headers,
        data=data,
        auth=(LEANIX_USERNAME, LEANIX_PASSWORD)
    )
    response.raise_for_status()
    token_data = response.json()
    
    print("✓ Successfully authenticated")
    return 'Bearer ' + token_data['access_token']


def get_all_factsheets(token):
    """Query LeanIX for all factsheets with subscriptions."""
    print(f"\nQuerying for all factsheets...")
    
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    # GraphQL query to get all factsheets (all types) with subscription details
    query = """
    query getAllFactSheets {
      allFactSheets(first: 2000) {
        totalCount
        edges {
          node {
            id
            name
            displayName
            description
            type
            status
            createdAt
            updatedAt
            completion {
              completion
              percentage
            }
            qualitySeal
            subscriptions {
              edges {
                node {
                  type
                  user {
                    displayName
                    email
                  }
                }
              }
            }
            ... on Application {
              alias
              businessCriticality
              functionalSuitability
              technicalSuitability
              lifecycle {
                asString
              }
            }
            ... on ITComponent {
              alias
              category
              lifecycle {
                asString
              }
            }
            ... on BusinessCapability {
              alias
            }
            ... on UserGroup {
              alias
            }
            ... on Process {
              alias
            }
            ... on DataObject {
              alias
            }
            ... on Provider {
              alias
            }
            ... on Project {
              alias
            }
          }
        }
      }
    }
    """
    
    payload = {
        "query": query
    }
    
    response = requests.post(LEANIX_GRAPHQL_URL, headers=headers, json=payload)
    response.raise_for_status()
    
    data = response.json()
    return data


def filter_factsheets_by_responsible(factsheets_data, target_email):
    """Filter factsheets where target_email is RESPONSIBLE and add URL."""
    filtered_items = []
    
    if 'data' not in factsheets_data or 'allFactSheets' not in factsheets_data['data']:
        return filtered_items
    
    for edge in factsheets_data['data']['allFactSheets']['edges']:
        item = edge['node']
        
        # Check if target email is in RESPONSIBLE subscriptions
        subscriptions = item.get('subscriptions', {}).get('edges', [])
        for sub in subscriptions:
            sub_node = sub.get('node', {})
            if (sub_node.get('type') == 'RESPONSIBLE' and 
                sub_node.get('user', {}).get('email') == target_email):
                # Add LeanIX URL to the item
                item['leanixUrl'] = f"https://fmglobal.leanix.net/fmglobalproduction/factsheet/{item['type']}/{item['id']}"
                filtered_items.append(item)
                break  # Found a match, no need to check other subscriptions
    
    return filtered_items


def main():
    """Main execution function."""
    try:
        # Authenticate
        token = get_leanix_token()
        
        # Get all factsheets
        all_factsheets_data = get_all_factsheets(token)
        
        # Check for errors in response
        if 'errors' in all_factsheets_data:
            print(f"\n✗ GraphQL Error: {all_factsheets_data['errors']}")
            return 1
        
        if 'data' not in all_factsheets_data:
            print(f"\n✗ Unexpected response format: {json.dumps(all_factsheets_data, indent=2)}")
            return 1
        
        total_count = all_factsheets_data['data']['allFactSheets']['totalCount']
        print(f"✓ Retrieved {total_count} total factsheets")
        
        # Filter for factsheets where target email is RESPONSIBLE
        my_assets = filter_factsheets_by_responsible(all_factsheets_data, TARGET_EMAIL)
        
        print(f"\n{'='*70}")
        print(f"ALL ASSETS WHERE {TARGET_EMAIL} IS RESPONSIBLE")
        print(f"{'='*70}")
        print(f"\nFound {len(my_assets)} asset(s)\n")
        
        if my_assets:
            # Group by type
            assets_by_type = {}
            for asset in my_assets:
                asset_type = asset.get('type', 'Unknown')
                if asset_type not in assets_by_type:
                    assets_by_type[asset_type] = []
                assets_by_type[asset_type].append(asset)
            
            # Display summary grouped by type
            for asset_type, assets in sorted(assets_by_type.items()):
                print(f"\n{asset_type} ({len(assets)}):")
                print("-" * 70)
                
                for i, asset in enumerate(assets, 1):
                    print(f"\n  {i}. {asset['name']}")
                    print(f"     ID: {asset['id']}")
                    if asset.get('alias'):
                        print(f"     Alias: {asset['alias']}")
                    print(f"     Status: {asset.get('status', 'N/A')}")
                    
                    # Show completion/score
                    completion = asset.get('completion', {})
                    if completion:
                        percentage = completion.get('percentage')
                        if percentage is not None:
                            print(f"     Completion: {percentage}%")
                    
                    # Show quality seal
                    quality_seal = asset.get('qualitySeal')
                    if quality_seal:
                        print(f"     Quality Seal: {quality_seal}")
                    
                    lifecycle = asset.get('lifecycle', {})
                    if lifecycle and lifecycle.get('asString'):
                        print(f"     Lifecycle: {lifecycle.get('asString')}")
                    
                    # Show category for IT Components
                    if asset_type == 'ITComponent' and asset.get('category'):
                        print(f"     Category: {asset['category']}")
                    
                    # Show all RESPONSIBLE users
                    responsible_users = []
                    subscriptions = asset.get('subscriptions', {}).get('edges', [])
                    for sub in subscriptions:
                        sub_node = sub.get('node', {})
                        if sub_node.get('type') == 'RESPONSIBLE':
                            user = sub_node.get('user', {})
                            responsible_users.append(user.get('displayName', 'Unknown'))
                    
                    if responsible_users:
                        print(f"     Responsible: {', '.join(responsible_users)}")
                    
                    # Generate LeanIX URL
                    leanix_url = f"https://fmglobal.leanix.net/fmglobalproduction/factsheet/{asset_type}/{asset['id']}"
                    print(f"     URL: {leanix_url}")
            
            # Summary by type
            print(f"\n{'='*70}")
            print("SUMMARY BY TYPE")
            print(f"{'='*70}")
            for asset_type, assets in sorted(assets_by_type.items()):
                print(f"  {asset_type}: {len(assets)}")
            print(f"\n  TOTAL: {len(my_assets)}")
            
            # Save full data to JSON
            output_file = 'my_assets.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(my_assets, f, indent=2, ensure_ascii=False)
            print(f"\n✓ Full data saved to: {output_file}")
        else:
            print(f"⚠ No assets found where {TARGET_EMAIL} is RESPONSIBLE")
    
    except requests.exceptions.RequestException as e:
        print(f"\n✗ Error: {str(e)}")
        if hasattr(e, 'response') and hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
