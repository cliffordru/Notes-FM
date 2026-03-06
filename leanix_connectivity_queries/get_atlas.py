#!/usr/bin/env python3
"""
Minimal script to retrieve the Atlas application factsheet from LeanIX.
"""

import os
import json
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
    
    print("✓ Successfully authenticated")
    return 'Bearer ' + token_data['access_token']


def get_atlas_factsheet(token):
    """Query LeanIX for the Atlas application factsheet."""
    print("\nQuerying for Atlas application...")
    
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    # GraphQL query to search for Atlas application
    query = """
    query getAtlasApp($filter: FilterInput!) {
      allFactSheets(filter: $filter) {
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
              businessCriticality
              functionalSuitability
              technicalSuitability
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
    
    # Filter to search for application named "Atlas"
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
                ],
                "fullTextSearch": "Atlas"
            }
        }
    }
    
    response = requests.post(LEANIX_GRAPHQL_URL, headers=headers, json=payload)
    response.raise_for_status()
    
    data = response.json()
    return data


def main():
    """Main execution function."""
    try:
        # Authenticate
        token = get_leanix_token()
        
        # Get Atlas factsheet
        atlas_data = get_atlas_factsheet(token)
        
        # Check for errors in response
        if 'errors' in atlas_data:
            print(f"\n✗ GraphQL Error: {atlas_data['errors']}")
            return 1
        
        if 'data' not in atlas_data:
            print(f"\n✗ Unexpected response format: {json.dumps(atlas_data, indent=2)}")
            return 1
        
        # Display results
        total_count = atlas_data['data']['allFactSheets']['totalCount']
        print(f"✓ Found {total_count} matching application(s)")
        
        if total_count > 0:
            print("\n" + "=" * 70)
            print("ATLAS APPLICATION FACTSHEET")
            print("=" * 70)
            
            for edge in atlas_data['data']['allFactSheets']['edges']:
                app = edge['node']
                print(f"\nID: {app['id']}")
                print(f"Name: {app['name']}")
                print(f"Alias: {app.get('alias', 'N/A')}")
                print(f"Display Name: {app.get('displayName', 'N/A')}")
                print(f"Status: {app.get('status', 'N/A')}")
                print(f"Description: {app.get('description', 'N/A')[:200]}...")
                
                # Save full JSON
                output_file = 'atlas_factsheet.json'
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(app, f, indent=2, ensure_ascii=False)
                print(f"\n✓ Full factsheet saved to: {output_file}")
        else:
            print("\n⚠ No application named 'Atlas' found")
    
    except requests.exceptions.RequestException as e:
        print(f"\n✗ Error: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
