# LeanIX GraphQL Queries

This directory contains GraphQL queries for the LeanIX API.

## Available Queries

### leanix_applications_basic.graphql
**Purpose**: Basic application factsheet data  
**Use**: Quick retrieval of core application information  
**Fields**:
- id, name, alias, displayName
- description
- createdAt, updatedAt

**Usage**:
```bash
python telogos_connect_leanix.py
```

### leanix_applications_enriched.graphql
**Purpose**: Complete application data with all relationships  
**Use**: Full data enrichment for integration and analysis  
**Fields**:
- All basic fields
- Business criticality and suitability metrics
- Obsolescence risk metrics
- Subscriptions (ownership, accountability)
- User group relationships
- Lifecycle information
- Business capability relationships
- IT component relationships
- Interface relationships (consumer/provider)
- Documents

**Usage**:
```bash
python telogos_connect_leanix.py --enriched
```

### leanix_application_documents.graphql
**Purpose**: Query existing documents attached to an application  
**Use**: Check for duplicate documents before creating new ones  
**Fields**:
- id, name, description
- documentType, url

**Important**: LeanIX Document schema does NOT include `updatedAt` or `createdAt` fields. These fields were removed after causing GraphQL validation errors.

**Usage**:
```python
# Used internally by telogos_connect_update_leanix.py
# Queries documents for a specific factsheet to check for duplicates
```

## Mutations

### leanix_document_create.graphql
**Purpose**: Create a new document attachment for an application  
**Use**: Add repository or pipeline links to LeanIX applications  
**Parameters**:
- `factSheetId`: Application UUID
- `name`: Document name (e.g., "veracode_repo|ProjectName/repo-name")
- `description`: Import details (e.g., "Repository imported from Veracode on 2026-01-26")
- `documentType`: Must be "Documentation" (LeanIX pre-configured type)
- `url`: Full URL to repository or pipeline

**Usage**:
```bash
python telogos_connect_update_leanix.py --dry-run  # Preview changes
python telogos_connect_update_leanix.py            # Execute mutations
```

## Query Development

### Testing Queries
Test queries without saving data:
```bash
python telogos_connect_leanix.py --test-only
python telogos_connect_leanix.py --test-only --enriched
```

### Adding New Queries
1. Create a new `.graphql` file in this directory
2. Use descriptive naming: `leanix_{entity}_{purpose}.graphql`
3. Update the Python script to reference the new query
4. Document it in this README

### Query Naming Convention
- `leanix_applications_basic.graphql` - Core fields only
- `leanix_applications_enriched.graphql` - Full relationships
- `leanix_interfaces_*.graphql` - Interface-specific queries
- `leanix_capabilities_*.graphql` - Business capability queries

## Benefits of External Queries

✅ **Maintainability** - Easier to modify without touching code  
✅ **Version Control** - Query changes visible in diffs  
✅ **IDE Support** - Syntax highlighting for GraphQL  
✅ **Reusability** - Same queries across multiple scripts  
✅ **Testability** - Test queries independently  
✅ **Collaboration** - Non-developers can work on queries
