import requests
from bs4 import BeautifulSoup, Tag

def scrape_p_tags_between_anchor_instances(url):
    """
    Fetches static HTML, finds the first instance of a specific <p> tag by text,
    and extracts all information from the element FOLLOWING the first instance
    up to the element PRECEDING the second instance.
    
    WARNING: This method uses requests/BeautifulSoup (static content only).
    It will only return results if the ANCHOR_TEXT appears twice in the static HTML.
    """
    
    # 1. Configuration
    ANCHOR_TEXT = '*Note: FedRAMP Moderate and FedRAMP High platforms implement controls restricting TLS 1.1/1.0 connections at the domain level.'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    p_tag_data = []
    
    try:
        print(f"Fetching static HTML content from: {url}")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.content, 'html.parser')

        # 2. Find ALL <p> tags with the anchor text
        anchor_p_tags = soup.find_all('p', string=lambda t: t and t.strip() == ANCHOR_TEXT)
        
        if len(anchor_p_tags) < 2:
            return (f"Error: Only {len(anchor_p_tags)} instance(s) of the anchor <p> tag were found. "
                    "Cannot define a start and end boundary using the same tag text.")
        
        anchor_start = anchor_p_tags[0]
        anchor_end = anchor_p_tags[1]
        
        print(f"Two anchor <p> tags found. Defining collection window between them.")

        # 3. Define the start point: The element immediately following the first anchor
        current_element = anchor_start.next_sibling
        
        # 4. Traverse all elements between the two anchors
        while current_element and current_element is not anchor_end:
            
            # Check if we've somehow passed the end anchor's position (sanity check)
            if current_element is None or anchor_end.sourceline is None or current_element.sourceline is not None and current_element.sourceline > anchor_end.sourceline:
                break
                
            # We only care about HTMl elements (tags)
            if isinstance(current_element, Tag):
                
                # Helper function to extract info
                def extract_p_tag_info(tag):
                    return {
                        'text_content': tag.get_text(strip=True),
                        'attributes': tag.attrs
                    }

                # Check if the current element is a <p> tag
                if current_element.name == 'p':
                    p_tag_data.append(extract_p_tag_info(current_element))
                
                # Check if the current element is a container and search for nested <p> tags
                elif current_element.name in ['div', 'section', 'article']:
                    nested_p_tags = current_element.find_all('p')
                    for nested_tag in nested_p_tags:
                        p_tag_data.append(extract_p_tag_info(nested_tag))

            # Move to the next element in the document structure
            current_element = current_element.next_sibling
        
        # NOTE: The loop naturally stops before processing the anchor_end tag itself.
        
        return p_tag_data

    except requests.exceptions.RequestException as e:
        return f"An error occurred while fetching the page: {e}"
    except Exception as e:
        return f"An unexpected error occurred during parsing: {e}"

# =========================================================================
# --- Configuration ---
# =========================================================================
TARGET_URL = "https://cloud.google.com/security/compliance/fedramp?e=48754805#services-in-scope"

# =========================================================================
# --- Execution ---
# =========================================================================
if __name__ == '__main__':
    
    results = scrape_p_tags_between_anchor_instances(TARGET_URL)
    
    if isinstance(results, str):
        print("\n--- ERROR/STATUS ---")
        print(results)
        print("--------------------")
    else:
        print("\n" + "=" * 80)
        print("STATIC SCRAPE RESULTS (Content between first and second anchor tag)")
        print(f"Successfully extracted data from {len(results)} <p> tags.")
        print("=" * 80)
        TEXT_CONTENTS = []
        if results:
            # Print a structured summary of the first few results
            for i, item in enumerate(results):                    
                # Print text content
                text_content = item['text_content']
                if text_content and text_content not in TEXT_CONTENTS:
                    # print("TEXT CONTENT:")
                    TEXT_CONTENTS.append(text_content)
                    # print(text_content[:150] + '...' if len(text_content) > 150 else text_content)
                else:
                    print("TEXT CONTENT: (Empty)")        
        else:
            print("No <p> tags were found between the first and second anchor tag instances in the static HTML source.")
        
        print(TEXT_CONTENTS)    

'''

OUTPUT:

Fetching static HTML content from: https://cloud.google.com/security/compliance/fedramp?e=48754805#services-in-scope
Two anchor <p> tags found. Defining collection window between them.

================================================================================
STATIC SCRAPE RESULTS (Content between first and second anchor tag)
Successfully extracted data from 157 <p> tags.
================================================================================
['Access Approval', 'Access Context Manager', 'Access Transparency', 'Admin Console (including Admin SDK, Directory Sync)',
 'Agent Assist', 'Agentspace (as part of Vertex AI Search)', 'AI Platform Data Labeling', 
 'AI Platform Neural Architecture Search (NAS)', 'AI Platform Training and Prediction (formerly Cloud Machine Learning Engine)', 
 'AlloyDB', 'Anthos Config Management (ACM) (feature of GKE Enterprise)', 'API Keys', 'Apigee', 
 'App Engine standard environment without bundled services', 'Application Integration', 'Artifact Analysis', 
 'Artifact Registry', 'Assured Open Source Software (AOSS)', 'Assured Workloads', 'AutoML Natural Language',
  'AutoML Tables', 'AutoML Translation', 'AutoML Video', 'AutoML Vision', 'Backup for GKE', 'Batch', 
  'BeyondCorp Enterprise', 'BigQuery', 'BigQuery Data Transfer Service', 'Bigtable', 'Binary Authorization', 
  'Care Studio', 'Certificate Authority Service', 'Certificate Manager', 'Cloud Armor (base)', 
  'Cloud Asset Inventory', 'Cloud Billing', 'Cloud Build', 'Cloud CDN', 'Cloud Composer', 'Cloud Console',
   'Cloud Console App', 'Cloud Data Fusion', 'Cloud Deploy', 'Cloud Deployment Manager', 'Cloud DNS', 
   'Cloud Endpoints', 'Cloud Error Reporting', 'Cloud External Key Manager (EKM)', 
   'Cloud Functions for Firebase', 'Cloud Healthcare API', 'Cloud HSM', 'Cloud Identity', 
   'Cloud IDS', 'Cloud Interconnect', 'Cloud Key Management Service', 
   'Cloud Life Sciences (formerly Google Genomics)', 'Cloud Load Balancing (L4 ILB)', 
   'Cloud Load Balancing (L7 ILB / Regional XLB)', 'Cloud Load Balancing (Network Load Balancing)',
    'Cloud Logging (includes Error Reporting)', 'Cloud Monitoring', 'Cloud Network Address Translation (NAT)',
     'Cloud Natural Language API', 'Cloud NGFW (Cloud Firewall) (Standard & Essential)', 
     'Cloud Profiler (Stackdriver Profiler)', 'Cloud Resource Manager', 'Cloud Router',
      'Cloud Run', 'Cloud Run Functions', 'Cloud Scheduler', 'Cloud SDK', 'Cloud Service Mesh', 
      'Cloud Shell', 'Cloud Source Repositories', 'Cloud SQL', 'Cloud Storage', 
      'Cloud Storage for Firebase', 'Cloud Tasks', 'Cloud Trace (formerly Stackdriver Trace)', 
      'Cloud Translation', 'Cloud Vision API', 'Cloud VPN', 'Cloud Workstations', 'Compute Engine', 
      'Connect', 'Container Registry', 'Conversational Agents (Dialogflow CX)', 
      'Conversational Insights (CCAI Insights)', 'Data Catalog', 'Database Migration Service', 
      'Dataform', 'Dataflow', 'Dataproc', 'Datastore', 'DataStream', 'Document AI', 
      'Earth Engine', 'Eventarc (Standard)', 'Filestore (Basic HDD and Basic SSD tiers)',
       'Firebase Authentication', 'Firestore', 'Generative AI on Vertex AI (Gemini)', 
       'GKE Hub', 'GKE Identity Service (Anthos Identity Service)', 'Google Cloud Identity-Aware Proxy',
        'Google Cloud Marketplace', 'Google Kubernetes Engine', 'Google SecOps (Chronicle SIEM)', 
        'Google SecOps SOAR', 'Identity & Access Management (IAM)', 'Identity Platform',
         'Identity-Aware Proxy (IAP)', 'Infrastructure Manager', 'Integration Connectors', 
         'Key Access Justifications (KAJ)', 'Knative Serving (Cloud Run for Anthos)', 
         'Looker (Google Cloud Core)', 'Looker Studio (including Pro, formerly Google Data Studio)', 
         'Memorystore for Memcache', 'Memorystore for Redis', 'Network Connectivity Center', 
         'Network Intelligence Center', 'Network Service Tiers', 'Persistent Disk', 'Pub/Sub', 
         'reCAPTCHA Enterprise', 'Secret Manager', 'Secure Source Manager', 'Secure Web Proxy',
          'Security Command Center (Standard/Premium)', 
          'Sensitive Data Protection (including Cloud Data Loss Prevention)', 'Serverless VPC Access', 
          'Service Infrastructure (formerly Service Control; includes Service Management API and Service Consumer Management API)', 
          'Spanner', 'Speech-to-Text', 'Storage Transfer Service', 'Talent Solution', 'Text-to-Speech', 
          'Traffic Director (part of Cloud Service Mesh)', 'Vertex AI Forecast', 'Vertex AI Model Registry', 
          'Vertex AI Search', 'Vertex AI Vector Search', 'Vertex AI Workbench Instances', 'Vertex Batch Predictions',
           'Vertex ML Metadata', 'Vertex Model Monitoring', 'Vertex Online Predictions', 'Vertex Pipelines',
            'Vertex Training', 'Video Intelligence API', 'Virtual Private Cloud', 'VPC Service Controls', 
            'Web Risk API', 'Workflows', 'Workforce Identity Federation (BYOID)']



'''        