#!/usr/bin/env python3
"""
Script to retrieve all LeanIX assets (Applications, IT Components, etc.) 
associated with a specific Business Capability.
"""

import os
import sys
import json
import argparse
import requests

# LeanIX API Configuration
LEANIX_TOKEN_URL = 'https://fmglobal.leanix.net/services/mtm/v1/oauth2/token'
LEANIX_GRAPHQL_URL = 'https://fmglobal.leanix.net/services/pathfinder/v1/graphql'
LEANIX_USERNAME = 'apitoken'
LEANIX_PASSWORD = os.getenv('LEANIX_API_TOKEN', 'cnskscsY3QzDuLfPMCtYYm2kwxLkTQtu8wGPKRKa')


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
    
    print("Successfully authenticated")
    return 'Bearer ' + token_data['access_token']


def get_all_factsheets(token):
    """Query LeanIX for all factsheets with business capability relationships."""
    print(f"\nQuerying for all factsheets...")
    
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    # GraphQL query to get all factsheets with business capabilities
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
              relApplicationToBusinessCapability {
                edges {
                  node {
                    factSheet {
                      id
                      name
                      displayName
                    }
                  }
                }
              }
            }
            ... on ITComponent {
              alias
              category
              lifecycle {
                asString
              }
              relITComponentToBusinessCapability {
                edges {
                  node {
                    factSheet {
                      id
                      name
                      displayName
                    }
                  }
                }
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
              relProcessToBusinessCapability {
                edges {
                  node {
                    factSheet {
                      id
                      name
                      displayName
                    }
                  }
                }
              }
            }
            ... on DataObject {
              alias
            }
            ... on Provider {
              alias
            }
            ... on Project {
              alias
              relProjectToBusinessCapability {
                edges {
                  node {
                    factSheet {
                      id
                      name
                      displayName
                    }
                  }
                }
              }
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


def filter_factsheets_by_capability(factsheets_data, capability_name, exact_match=False):
    """Filter factsheets associated with a specific business capability."""
    filtered_items = []
    capability_name_lower = capability_name.lower()
    
    if 'data' not in factsheets_data or 'allFactSheets' not in factsheets_data['data']:
        return filtered_items
    
    for edge in factsheets_data['data']['allFactSheets']['edges']:
        item = edge['node']
        item_type = item.get('type', '')
        
        # Check business capability relationships based on type
        business_capabilities = []
        
        if item_type == 'Application':
            for rel in item.get('relApplicationToBusinessCapability', {}).get('edges', []):
                bc = rel['node']['factSheet']
                business_capabilities.append(bc)
        elif item_type == 'ITComponent':
            for rel in item.get('relITComponentToBusinessCapability', {}).get('edges', []):
                bc = rel['node']['factSheet']
                business_capabilities.append(bc)
        elif item_type == 'Process':
            for rel in item.get('relProcessToBusinessCapability', {}).get('edges', []):
                bc = rel['node']['factSheet']
                business_capabilities.append(bc)
        elif item_type == 'Project':
            for rel in item.get('relProjectToBusinessCapability', {}).get('edges', []):
                bc = rel['node']['factSheet']
                business_capabilities.append(bc)
        
        # Check if any business capability matches
        matched = False
        for bc in business_capabilities:
            bc_name = bc.get('name', '').lower()
            bc_display = bc.get('displayName', '').lower()
            
            if exact_match:
                if bc_name == capability_name_lower or bc_display == capability_name_lower:
                    matched = True
                    break
            else:
                if capability_name_lower in bc_name or capability_name_lower in bc_display:
                    matched = True
                    break
        
        if matched:
            # Add LeanIX URL and business capabilities list
            item['leanixUrl'] = f"https://fmglobal.leanix.net/fmglobalproduction/factsheet/{item_type}/{item['id']}"
            item['businessCapabilities'] = [
                {
                    'id': bc.get('id'),
                    'name': bc.get('name'),
                    'displayName': bc.get('displayName', bc.get('name'))
                }
                for bc in business_capabilities
            ]
            filtered_items.append(item)
    
    return filtered_items


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Get all LeanIX assets for a specific Business Capability',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get all Investments assets (partial match)
  python get_assets_by_capability.py "investments"
  
  # Get exact match only
  python get_assets_by_capability.py "Investment Accounting" --exact
  
  # Specify output file
  python get_assets_by_capability.py "Investments" --output investments_assets.json
        """
    )
    
    parser.add_argument('capability', 
                        help='Business Capability name to filter by')
    parser.add_argument('--exact', action='store_true',
                        help='Require exact match (case-insensitive)')
    parser.add_argument('--output', '-o', 
                        help='Output JSON filename (default: <capability_name>_assets.json)')
    
    args = parser.parse_args()
    
    capability_name = args.capability
    exact_match = args.exact
    
    # Generate output filename from capability name if not specified
    if args.output:
        output_file = args.output
    else:
        safe_name = capability_name.lower().replace(' ', '_').replace('/', '_')
        output_file = f'{safe_name}_assets.json'
    
    try:
        # Authenticate
        token = get_leanix_token()
        
        # Get all factsheets
        all_factsheets_data = get_all_factsheets(token)
        
        # Check for errors in response
        if 'errors' in all_factsheets_data:
            print(f"\nGraphQL Error: {all_factsheets_data['errors']}")
            return 1
        
        if 'data' not in all_factsheets_data:
            print(f"\nUnexpected response format: {json.dumps(all_factsheets_data, indent=2)}")
            return 1
        
        total_count = all_factsheets_data['data']['allFactSheets']['totalCount']
        print(f"Retrieved {total_count} total factsheets")
        
        # Filter for business capability
        capability_assets = filter_factsheets_by_capability(all_factsheets_data, capability_name, exact_match)
        
        match_type = "exact match" if exact_match else "partial match"
        print(f"\n{'='*70}")
        print(f"ASSETS FOR BUSINESS CAPABILITY: {capability_name} ({match_type})")
        print(f"{'='*70}")
        print(f"\nFound {len(capability_assets)} asset(s)\n")
        
        if capability_assets:
            # Group by type
            assets_by_type = {}
            for asset in capability_assets:
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
                    
                    # Show business capabilities
                    bcs = asset.get('businessCapabilities', [])
                    if bcs:
                        bc_names = [bc['displayName'] for bc in bcs]
                        print(f"     Business Capabilities: {', '.join(bc_names)}")
                    
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
                    
                    print(f"     URL: {asset['leanixUrl']}")
            
            # Summary by type
            print(f"\n{'='*70}")
            print("SUMMARY BY TYPE")
            print(f"{'='*70}")
            for asset_type, assets in sorted(assets_by_type.items()):
                print(f"  {asset_type}: {len(assets)}")
            print(f"\n  TOTAL: {len(capability_assets)}")
            
            # Save full data to JSON
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(capability_assets, f, indent=2, ensure_ascii=False)
            print(f"\nFull data saved to: {output_file}")
        else:
            print(f"No assets found for business capability: {capability_name}")
    
    except requests.exceptions.RequestException as e:
        print(f"\nError: {str(e)}")
        if hasattr(e, 'response') and hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        return 1
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
