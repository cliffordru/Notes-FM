#!/usr/bin/env python3
"""
Script to retrieve detailed information for specific applications from LeanIX.
Includes tags, documents, IT components, and other fields that might contain logging information.
"""

import os
import json
import requests
from typing import List, Dict, Any

# LeanIX API Configuration
LEANIX_TOKEN_URL = 'https://fmglobal.leanix.net/services/mtm/v1/oauth2/token'
LEANIX_GRAPHQL_URL = 'https://fmglobal.leanix.net/services/pathfinder/v1/graphql'
LEANIX_USERNAME = 'apitoken'
LEANIX_PASSWORD = os.getenv('LEANIX_API_TOKEN', 'cnskscsY3QzDuLfPMCtYYm2kwxLkTQtu8wGPKRKa')

# Applications to query
TARGET_APPLICATIONS = [
    "ARGUS Enterprise",
    "Bloomberg Anywhere",
    "Clearwater Analytics",
    "NetDocuments",
    "PeopleSoft - Investment Accounting",
    "Treasura",
    "Yardi Real Estate Suite",
    "Atlas"
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


def get_application_details(token: str, app_name: str) -> Dict[str, Any]:
    """Query LeanIX for detailed application information."""
    print(f"\nQuerying for: {app_name}...")
    
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    # GraphQL query with comprehensive fields
    query = """
    query getApplicationDetails($filter: FilterInput!) {
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
              
              # Criticality and suitability
              businessCriticality
              businessCriticalityDescription
              functionalSuitability
              functionalSuitabilityDescription
              technicalSuitability
              technicalSuitabilityDescription
              
              # Lifecycle
              lifecycle {
                asString
                phases {
                  phase
                  startDate
                }
              }
              
              # Ownership/Subscriptions
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
              
              # Documents (may contain logging docs)
              documents {
                edges {
                  node {
                    name
                    url
                    documentType
                    description
                  }
                }
              }
              
              # Tags (may include logging-related tags)
              tags {
                id
                name
                tagGroup {
                  id
                  name
                  shortName
                }
              }
              
              # Related IT Components (may include logging tools)
              relApplicationToITComponent {
                edges {
                  node {
                    factSheet {
                      id
                      name
                      displayName
                      ... on ITComponent {
                        category
                        description
                      }
                    }
                  }
                }
              }
              
              # User Groups
              relApplicationToUserGroup {
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
              
              # Business Capabilities
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
          }
        }
      }
    }
    """
    
    # Filter to search for the specific application
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
                "fullTextSearch": app_name
            }
        }
    }
    
    response = requests.post(LEANIX_GRAPHQL_URL, headers=headers, json=payload)
    response.raise_for_status()
    
    data = response.json()
    
    # Check for errors
    if 'errors' in data:
        print(f"  ✗ GraphQL Error: {data['errors']}")
        return None
    
    # Find exact match (case-insensitive)
    if data.get('data', {}).get('allFactSheets', {}).get('edges'):
        for edge in data['data']['allFactSheets']['edges']:
            node = edge['node']
            if node['name'].lower() == app_name.lower() or \
               node.get('displayName', '').lower() == app_name.lower():
                print(f"  ✓ Found exact match")
                return node
        
        # If no exact match, return first result
        if len(data['data']['allFactSheets']['edges']) > 0:
            print(f"  ⚠ No exact match, using closest result")
            return data['data']['allFactSheets']['edges'][0]['node']
    
    print(f"  ✗ Not found")
    return None


def format_application_details(app: Dict[str, Any]) -> str:
    """Format application details for display."""
    if not app:
        return "Not found"
    
    output = []
    output.append(f"\n{'=' * 80}")
    output.append(f"Application: {app.get('displayName', app.get('name'))}")
    output.append(f"{'=' * 80}")
    
    # Basic Info
    output.append(f"\n[BASIC INFORMATION]")
    output.append(f"  ID: {app.get('id')}")
    output.append(f"  Name: {app.get('name')}")
    output.append(f"  Alias: {app.get('alias', 'N/A')}")
    output.append(f"  Status: {app.get('status', 'N/A')}")
    
    lifecycle = app.get('lifecycle')
    if lifecycle and isinstance(lifecycle, dict):
        output.append(f"  Lifecycle: {lifecycle.get('asString', 'N/A')}")
    else:
        output.append(f"  Lifecycle: N/A")
    
    # Description
    if app.get('description'):
        desc = app['description'][:300] + "..." if len(app.get('description', '')) > 300 else app.get('description', 'N/A')
        output.append(f"  Description: {desc}")
    
    # Criticality
    output.append(f"\n[CRITICALITY & SUITABILITY]")
    output.append(f"  Business Criticality: {app.get('businessCriticality', 'N/A')}")
    output.append(f"  Functional Suitability: {app.get('functionalSuitability', 'N/A')}")
    output.append(f"  Technical Suitability: {app.get('technicalSuitability', 'N/A')}")
    
    # Subscriptions (Owners)
    output.append(f"\n[OWNERSHIP]")
    if app.get('subscriptions', {}).get('edges'):
        for sub_edge in app['subscriptions']['edges']:
            sub = sub_edge['node']
            output.append(f"  {sub['type']}: {sub['user']['displayName']} ({sub['user']['email']})")
    else:
        output.append("  No subscriptions found")
    
    # Tags
    output.append(f"\n[TAGS]")
    if app.get('tags'):
        for tag in app['tags']:
            tag_group = tag.get('tagGroup', {}).get('name', 'Unassigned') if tag.get('tagGroup') else 'Unassigned'
            output.append(f"  [{tag_group}] {tag['name']}")
    else:
        output.append("  No tags found")
    
    # Documents
    output.append(f"\n[DOCUMENTS]")
    if app.get('documents', {}).get('edges'):
        for doc_edge in app['documents']['edges']:
            doc = doc_edge['node']
            output.append(f"  • {doc['name']}")
            output.append(f"    Type: {doc.get('documentType', 'N/A')}")
            output.append(f"    URL: {doc.get('url', 'N/A')}")
            if doc.get('description'):
                output.append(f"    Description: {doc['description']}")
    else:
        output.append("  No documents found")
    
    # IT Components
    output.append(f"\n[IT COMPONENTS]")
    if app.get('relApplicationToITComponent', {}).get('edges'):
        for comp_edge in app['relApplicationToITComponent']['edges']:
            comp = comp_edge['node']['factSheet']
            output.append(f"  • {comp.get('displayName', comp.get('name'))}")
            if comp.get('category'):
                output.append(f"    Category: {comp['category']}")
            if comp.get('description'):
                desc = comp['description'][:150] + "..." if len(comp.get('description', '')) > 150 else comp.get('description', '')
                output.append(f"    Description: {desc}")
    else:
        output.append("  No IT components found")
    
    # Business Capabilities
    output.append(f"\n[BUSINESS CAPABILITIES]")
    if app.get('relApplicationToBusinessCapability', {}).get('edges'):
        for cap_edge in app['relApplicationToBusinessCapability']['edges']:
            cap = cap_edge['node']['factSheet']
            output.append(f"  • {cap.get('displayName', cap.get('name'))}")
    else:
        output.append("  No business capabilities found")
    
    return "\n".join(output)


def main():
    """Main execution function."""
    try:
        # Authenticate
        token = get_leanix_token()
        
        all_results = {}
        found_count = 0
        not_found = []
        
        # Query each application
        for app_name in TARGET_APPLICATIONS:
            app_details = get_application_details(token, app_name)
            if app_details:
                all_results[app_name] = app_details
                found_count += 1
            else:
                not_found.append(app_name)
        
        # Display summary
        print(f"\n{'=' * 80}")
        print(f"QUERY SUMMARY")
        print(f"{'=' * 80}")
        print(f"Total applications queried: {len(TARGET_APPLICATIONS)}")
        print(f"Found: {found_count}")
        print(f"Not found: {len(not_found)}")
        
        if not_found:
            print(f"\nApplications not found:")
            for app in not_found:
                print(f"  • {app}")
        
        # Display detailed results
        print(f"\n{'=' * 80}")
        print(f"DETAILED RESULTS")
        print(f"{'=' * 80}")
        
        for app_name in TARGET_APPLICATIONS:
            if app_name in all_results:
                print(format_application_details(all_results[app_name]))
        
        # Save to JSON file
        output_file = 'results/application_details.json'
        os.makedirs('results', exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'=' * 80}")
        print(f"✓ Results saved to: {output_file}")
        print(f"{'=' * 80}")
        
        return 0
        
    except requests.exceptions.RequestException as e:
        print(f"\n✗ HTTP Error: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
