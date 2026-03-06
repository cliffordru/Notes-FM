#!/usr/bin/env python3
"""
Script to retrieve all applications where clifford.gray@fm.com is RESPONSIBLE.
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


def get_all_applications(token):
    """Query LeanIX for all application factsheets with subscriptions."""
    print(f"\nQuerying for all applications...")
    
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    # GraphQL query to get all applications with subscription details
    query = """
    query getAllApps($filter: FilterInput!) {
      allFactSheets(first: 1500, filter: $filter) {
        totalCount
        edges {
          node {
            ... on Application {
              id
              name
              alias
              displayName
              description
              type
              status
              createdAt
              updatedAt
              lifecycle {
                asString
                phases {
                  phase
                  startDate
                }
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
            }
          }
        }
      }
    }
    """
    
    # Filter for Application type
    payload = {
        "query": query,
        "variables": {
            "filter": {
                "facetFilters": [
                    {
                        "facetKey": "FactSheetTypes",
                        "operator": "OR",
                        "keys": ["Application"]
                    }
                ]
            }
        }
    }
    
    response = requests.post(LEANIX_GRAPHQL_URL, headers=headers, json=payload)
    response.raise_for_status()
    
    data = response.json()
    return data


def filter_applications_by_responsible(applications_data, target_email):
    """Filter applications where target_email is RESPONSIBLE."""
    filtered_apps = []
    
    if 'data' not in applications_data or 'allFactSheets' not in applications_data['data']:
        return filtered_apps
    
    for edge in applications_data['data']['allFactSheets']['edges']:
        app = edge['node']
        
        # Check if target email is in RESPONSIBLE subscriptions
        subscriptions = app.get('subscriptions', {}).get('edges', [])
        for sub in subscriptions:
            sub_node = sub.get('node', {})
            if (sub_node.get('type') == 'RESPONSIBLE' and 
                sub_node.get('user', {}).get('email') == target_email):
                filtered_apps.append(app)
                break  # Found a match, no need to check other subscriptions
    
    return filtered_apps


def main():
    """Main execution function."""
    try:
        # Authenticate
        token = get_leanix_token()
        
        # Get all applications
        all_apps_data = get_all_applications(token)
        
        # Check for errors in response
        if 'errors' in all_apps_data:
            print(f"\n✗ GraphQL Error: {all_apps_data['errors']}")
            return 1
        
        if 'data' not in all_apps_data:
            print(f"\n✗ Unexpected response format: {json.dumps(all_apps_data, indent=2)}")
            return 1
        
        total_count = all_apps_data['data']['allFactSheets']['totalCount']
        print(f"✓ Retrieved {total_count} total applications")
        
        # Filter for applications where target email is RESPONSIBLE
        my_apps = filter_applications_by_responsible(all_apps_data, TARGET_EMAIL)
        
        print(f"\n{'='*70}")
        print(f"APPLICATIONS WHERE {TARGET_EMAIL} IS RESPONSIBLE")
        print(f"{'='*70}")
        print(f"\nFound {len(my_apps)} application(s)\n")
        
        if my_apps:
            # Display summary
            for i, app in enumerate(my_apps, 1):
                print(f"{i}. {app['name']}")
                print(f"   ID: {app['id']}")
                print(f"   Alias: {app.get('alias', 'N/A')}")
                print(f"   Status: {app.get('status', 'N/A')}")
                lifecycle = app.get('lifecycle', {})
                if lifecycle:
                    print(f"   Lifecycle: {lifecycle.get('asString', 'N/A')}")
                
                # Show all RESPONSIBLE users
                responsible_users = []
                subscriptions = app.get('subscriptions', {}).get('edges', [])
                for sub in subscriptions:
                    sub_node = sub.get('node', {})
                    if sub_node.get('type') == 'RESPONSIBLE':
                        user = sub_node.get('user', {})
                        responsible_users.append(user.get('displayName', 'Unknown'))
                
                if responsible_users:
                    print(f"   Responsible: {', '.join(responsible_users)}")
                print()
            
            # Save full data to JSON
            output_file = 'my_applications.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(my_apps, f, indent=2, ensure_ascii=False)
            print(f"✓ Full data saved to: {output_file}")
        else:
            print(f"⚠ No applications found where {TARGET_EMAIL} is RESPONSIBLE")
    
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
