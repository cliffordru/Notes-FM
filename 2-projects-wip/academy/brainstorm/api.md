API documentation
https://help.brainstorminc.com/platform-connections/api-references-and-use-cases

POST Acquire Token

POST /connect/token HTTP/1.1
Host: api.brainstorminc.com
Ocp-Apim-Subscription-Key: YOUR_API_KEY
Content-Type: application/x-www-form-urlencoded
Accept: */*
Content-Length: 97

"'client_id=client1&client_secret=secret&grant_type=client_impersonation&scope=gateway.fullAccess'"

GET Content

/api/content

GET /api/content HTTP/1.1
Host: api.brainstorminc.com
Ocp-Apim-Subscription-Key: YOUR_API_KEY
Authorization: text


Here’s the content converted into **clean, well-structured Markdown**, with duplication removed and formatting normalized for readability:

***

# BrainStorm API Authentication Overview

To authenticate with the **BrainStorm API** (specifically for their learning platform and QuickHelp services), you typically use **OAuth 2.0** or a combination of **API Keys and Subscription Keys**, depending on the endpoint or integration type.

Based on documentation for their modern platform (often used by partners like Moveworks), the process aligns with the flows described below.

***

## 1. OAuth 2.0 Authentication (Client ID & Secret)

For most modern search and content indexing integrations, BrainStorm uses **OAuth 2.0 credentials**.

### Setup Steps

*   **Generation**  
    Log in to the **BrainStorm Admin Portal**.

*   **Navigation**  
    Click the **Settings** icon (or your organization logo) at the bottom of the left sidebar and select **API**.

*   **Credentials**  
    Toggle **Read Only Access** to generate a **Client ID** and **Client Secret**.

*   **Flow**
    1.  Send the Client ID and Client Secret to BrainStorm’s identity provider.
    2.  Receive an **access token**.
    3.  Include the token in the `Authorization` header as a **Bearer token** for subsequent API requests (e.g., fetching content lists or search results).

*   **Note**  
    Client secrets typically expire after **12 months** and must be rotated.

***

## 2. QuickHelp Legacy API (API Key & Subscription Key)

If you are using older **QuickHelp-specific APIs**, authentication differs and requires **two headers**.

### Required Keys

*   **API Key**  
    Generated in the **QuickHelp Admin Portal**:  
    `Settings > Configure > Regenerate Key`

*   **Subscription Key**  
    Not self-service.  
    Email **<support@quickhelp.com>** with an administrator’s details to receive a unique subscription key.

### Usage

Both keys must be included in the headers of every request, for example:

*   `Ocp-Apim-Subscription-Key`
*   A custom API key header

***

## 3. User & Management Integrations

For managing users and group content, BrainStorm commonly integrates with:

*   **Microsoft Graph**
*   **Google Workspace**

### Authentication Model

*   In this scenario, you do **not** authenticate *to* BrainStorm using a client secret.
*   Instead, BrainStorm is granted permission to access your tenant via an **Authorization Token** during the SSO or integration setup in the Azure or Google Admin portal.

***

## Summary: Content List Retrieval Flow

If your goal is to retrieve a list of content:

1.  **Obtain Credentials**  
    Generate a **Client ID** and **Client Secret** from the Admin Portal.

2.  **Request Token**  
    Send a `POST` request to the BrainStorm token endpoint.

3.  **Fetch Content**  
    Use the resulting **Bearer token** to call content endpoints (e.g., `GET /content` or search-related endpoints).

> **Note:**  
> Specific endpoint URLs are typically available in the **Developer / API** section of the Admin Portal once API access is enabled for your organization.

***


