#!/usr/bin/env python3
"""
Script to analyze relationships between specific applications.
Focus on organizational and business unit connections.
"""

import os
import json
import requests

# LeanIX API Configuration
LEANIX_TOKEN_URL = 'https://fmglobal.leanix.net/services/mtm/v1/oauth2/token'
LEANIX_GRAPHQL_URL = 'https://fmglobal.leanix.net/services/pathfinder/v1/graphql'
LEANIX_USERNAME = 'apitoken'
LEANIX_PASSWORD = os.getenv('LEANIX_API_TOKEN', 'cnskscsY3QzDuLfPMCtYYm2kwxLkTQtu8wGPKRKa')

# Applications to analyze
TARGET_APPS = [
    "7Shifts",
    "ARGUS Enterprise",
    "Bellwether",
    "Bloomberg Anywhere",
    "Building Engines",
    "ChathamDirect",
    "Cove",
    "Dynamo",
    "Highwire",
    "Jones COI",
    "Lease Pilot",
    "Lightspeed Hotel Management System",
    "NetDocuments",
    "OfficeSpace",
    "OpenTable",
    "Parsley",
    "Placer.ai",
    "Treasura",
    "Yardi Real Estate Suite"
]


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


def get_applications_with_relationships(token):
    """Query LeanIX for applications with organizational relationships."""
    print(f"\nQuerying for applications with relationships...")
    
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    # GraphQL query to get applications with relationships
    query = """
    query getApplications {
      allFactSheets(first: 2000, filter: {facetFilters: [{facetKey: "FactSheetTypes", operator: OR, keys: ["Application"]}]}) {
        totalCount
        edges {
          node {
            ... on Application {
              id
              name
              alias
              displayName
              description
              status
              completion {
                percentage
              }
              qualitySeal
              lifecycle {
                asString
              }
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
              relApplicationToUserGroup {
                edges {
                  node {
                    factSheet {
                      id
                      name
                      displayName
                      type
                    }
                  }
                }
              }
              relTechOwnerApplicationToUserGroup {
                edges {
                  node {
                    factSheet {
                      id
                      name
                      displayName
                      type
                    }
                  }
                }
              }
              relApplicationToBusinessCapability {
                edges {
                  node {
                    factSheet {
                      id
                      name
                      displayName
                      type
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


def filter_target_applications(all_apps_data, target_names):
    """Filter for specific target applications."""
    filtered = []
    
    if 'data' not in all_apps_data or 'allFactSheets' not in all_apps_data['data']:
        return filtered
    
    # Create lowercase map for case-insensitive matching
    target_names_lower = [name.lower() for name in target_names]
    
    for edge in all_apps_data['data']['allFactSheets']['edges']:
        app = edge['node']
        app_name_lower = app['name'].lower()
        
        if app_name_lower in target_names_lower:
            # Add LeanIX URL
            app['leanixUrl'] = f"https://fmglobal.leanix.net/fmglobalproduction/factsheet/Application/{app['id']}"
            filtered.append(app)
    
    return filtered


def analyze_relationships(apps):
    """Analyze common relationships between applications."""
    print(f"\n{'='*70}")
    print("RELATIONSHIP ANALYSIS")
    print(f"{'='*70}")
    
    # Collect all user groups
    all_user_groups = {}
    app_to_user_groups = {}
    
    for app in apps:
        app_name = app['name']
        app_to_user_groups[app_name] = set()
        
        # Application to UserGroup relationships
        for rel in app.get('relApplicationToUserGroup', {}).get('edges', []):
            ug = rel['node']['factSheet']
            ug_name = ug['name']
            app_to_user_groups[app_name].add(ug_name)
            
            if ug_name not in all_user_groups:
                all_user_groups[ug_name] = {
                    'id': ug['id'],
                    'displayName': ug.get('displayName', ug_name),
                    'apps': []
                }
            all_user_groups[ug_name]['apps'].append(app_name)
        
        # Tech Owner UserGroup relationships
        for rel in app.get('relTechOwnerApplicationToUserGroup', {}).get('edges', []):
            ug = rel['node']['factSheet']
            ug_name = ug['name']
            app_to_user_groups[app_name].add(ug_name)
            
            if ug_name not in all_user_groups:
                all_user_groups[ug_name] = {
                    'id': ug['id'],
                    'displayName': ug.get('displayName', ug_name),
                    'apps': []
                }
            if app_name not in all_user_groups[ug_name]['apps']:
                all_user_groups[ug_name]['apps'].append(app_name)
    
    # Find shared user groups (organizations/business units)
    print("\nSHARED USER GROUPS / ORGANIZATIONS:")
    print("-" * 70)
    
    shared_groups = {name: data for name, data in all_user_groups.items() if len(data['apps']) > 1}
    
    if shared_groups:
        for ug_name, ug_data in sorted(shared_groups.items(), key=lambda x: len(x[1]['apps']), reverse=True):
            print(f"\n{ug_data['displayName']}")
            print(f"  ID: {ug_data['id']}")
            print(f"  Connected Applications ({len(ug_data['apps'])}):")
            for app_name in sorted(ug_data['apps']):
                print(f"    - {app_name}")
    else:
        print("\n  No shared user groups found among these applications.")
    
    # Collect all business capabilities
    all_capabilities = {}
    app_to_capabilities = {}
    
    for app in apps:
        app_name = app['name']
        app_to_capabilities[app_name] = set()
        
        for rel in app.get('relApplicationToBusinessCapability', {}).get('edges', []):
            bc = rel['node']['factSheet']
            bc_name = bc['name']
            app_to_capabilities[app_name].add(bc_name)
            
            if bc_name not in all_capabilities:
                all_capabilities[bc_name] = {
                    'id': bc['id'],
                    'displayName': bc.get('displayName', bc_name),
                    'apps': []
                }
            all_capabilities[bc_name]['apps'].append(app_name)
    
    # Find shared business capabilities
    print(f"\n\nSHARED BUSINESS CAPABILITIES:")
    print("-" * 70)
    
    shared_capabilities = {name: data for name, data in all_capabilities.items() if len(data['apps']) > 1}
    
    if shared_capabilities:
        for bc_name, bc_data in sorted(shared_capabilities.items(), key=lambda x: len(x[1]['apps']), reverse=True):
            print(f"\n{bc_data['displayName']}")
            print(f"  ID: {bc_data['id']}")
            print(f"  Connected Applications ({len(bc_data['apps'])}):")
            for app_name in sorted(bc_data['apps']):
                print(f"    - {app_name}")
    else:
        print("\n  No shared business capabilities found among these applications.")
    
    return {
        'userGroups': all_user_groups,
        'capabilities': all_capabilities,
        'appToUserGroups': {k: list(v) for k, v in app_to_user_groups.items()},
        'appToCapabilities': {k: list(v) for k, v in app_to_capabilities.items()}
    }


def main():
    """Main execution function."""
    try:
        # Authenticate
        token = get_leanix_token()
        
        # Get all applications with relationships
        all_apps_data = get_applications_with_relationships(token)
        
        # Check for errors
        if 'errors' in all_apps_data:
            print(f"\n✗ GraphQL Error: {all_apps_data['errors']}")
            return 1
        
        if 'data' not in all_apps_data:
            print(f"\n✗ Unexpected response format")
            return 1
        
        total_count = all_apps_data['data']['allFactSheets']['totalCount']
        print(f"✓ Retrieved {total_count} total applications")
        
        # Filter for target applications
        target_apps = filter_target_applications(all_apps_data, TARGET_APPS)
        
        print(f"\n{'='*70}")
        print(f"TARGET APPLICATIONS FOUND")
        print(f"{'='*70}")
        print(f"\nSearched for: {len(TARGET_APPS)} applications")
        print(f"Found: {len(target_apps)} applications\n")
        
        if len(target_apps) < len(TARGET_APPS):
            found_names = {app['name'] for app in target_apps}
            missing = [name for name in TARGET_APPS if name not in found_names]
            print(f"⚠️  Missing applications ({len(missing)}):")
            for name in missing:
                print(f"  - {name}")
            print()
        
        # Display basic info
        for i, app in enumerate(target_apps, 1):
            print(f"{i}. {app['name']}")
            print(f"   Status: {app.get('status', 'N/A')}")
            
            completion = app.get('completion', {})
            if completion:
                percentage = completion.get('percentage')
                if percentage is not None:
                    print(f"   Completion: {percentage}%")
            
            quality_seal = app.get('qualitySeal')
            if quality_seal:
                print(f"   Quality Seal: {quality_seal}")
            
            # Show responsible users
            responsible = []
            for sub in app.get('subscriptions', {}).get('edges', []):
                if sub['node'].get('type') == 'RESPONSIBLE':
                    user = sub['node'].get('user', {})
                    responsible.append(user.get('displayName', 'Unknown'))
            if responsible:
                print(f"   Responsible: {', '.join(responsible)}")
            
            print(f"   URL: {app['leanixUrl']}")
            print()
        
        # Analyze relationships
        if target_apps:
            relationship_data = analyze_relationships(target_apps)
            
            # Save detailed data
            output_data = {
                'applications': target_apps,
                'relationships': relationship_data
            }
            
            output_file = 'app_relationship_analysis.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            print(f"\n{'='*70}")
            print(f"✓ Full data saved to: {output_file}")
            print(f"{'='*70}")
        else:
            print("\n⚠️  No target applications found to analyze")
    
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
