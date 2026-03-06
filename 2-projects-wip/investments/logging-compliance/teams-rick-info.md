Hi Rick
 
Could you let me know what if any logging capabilities are in place for these applications (if you are familiar)?  Do they have logging in place and if so what technology/system is used (custom, 3rd party, etc.)?
 
ARGUS Enterprise	
Bloomberg Anywhere	
Clearwater Analytics	
NetDocuments	
PeopleSoft - Investment Accounting	
Treasura	
Yardi Real Estate Suite	
 
If any are aligned with ISS 008: Application Security Standards, that would be useful to know too. Thank you.
security-logging-assessment-user-management _ Enterprise Documentation Portal.pdf

These are our three most important platforms for the list you provided; I will have to research others more:
 
Yardi (Cloud)
Reports for:
User logins
Security changes
User permissions
Cloud access - support done on our behalf
 
NetDocs  (Cloud)
AdministrationActivity Logs
Add/remove users
Create/Delete/Rename groups
Add/Remove group members
Group level access changes
Add/Edit/Delete profile attributes
Consolidated activity log
Detailed data regarding actions taken on documents within a given repository over a specified period of time
A record of each action taken on a document
Information about the document that was acted on (including the name and profile of that document)
Information about what action was taken
Clearwater  (Cloud)
User Account Access Audit report
Compliance and audit reports
 
We don't have direct access to the original logs since these are SaaS applications, so we rely on reports present within the systems.
 

I sent:
Thank you for the info.  Nothing actionable right now but Mark is considering if we need to do a logging compliance analysis on the systems I sent you.  It is a multi-step process including determining high risk data activity and if deemed appropriate an assessment to determine what would be needed to send the logs from each system to our SEIM (Splunk).
 
Again, nothing to do now, JFYI and if we need to move forward I can work with you on the process.  If you are interested, here is info on high risk business data activity:
 
High-Risk Business Data Activity
The scope of High-Risk Business Data (HRBD) activity is broad, including: any data/files classified as Restricted (see ISS 006 for the definition), any client data/files, PII, and NPPI. Logging these events is useful to detect theft and assess the impact of a breach. These events must be logged if your application provides includes processing, storing, or exposing any HRBD.
6.1. Read HRBD
6.2. Create/Write/Modify HRBD
6.3. Delete HRBD: including soft delete
The broad definition of HRBD could result a large volume of logs, which poses the risk of over-logging, a poor signal-to-noise ratio, unnecessary expense, and unnecessarily compliance delays. These techniques can be used to achieve the strategic outcomes in a balanced way:
It is acceptable to limit the events that are logged to only those initiated by (or on behalf of) a user. For example, logging when a user clicks a form to submit HRBD-related data is required, but logging when a trusted backend independently actor moves HRBD data from one system to another is optional.
Log HRBD events based on user intent. Not all CRUD transactions need to be logged per se, the focus should be on the intent of the user's gesture/command/query. For example, if a user submits a command to modify a Policy, and the application technically needed to first read the policy data before modifying it, the requirement is only to log that a user modified the Policy.
It is acceptable to triage logging of 6.1 HRBD Read events after consulting with CTDR. The Product Owner and SA must first consult with CTDR before limiting which of these events to log and record the decision in the assessment for future reference.
It is acceptable for a FM-built shared utility (library or service) to not log HRBD activity if that utility does not have knowledge if the data is considered HRBD. For example, a shared service that stores images that can be used in any context by consuming applications that has no way of knowing if each image is HRBD would not be responsible for logging these HRBD events. In that case, the consuming application (which should know if it is HRBD) must log the event before invoking the service.
The granularity of HRBD activity events should be coarse by default. The goal is to monitor activity at the business entity level primarily. For example, log that a user read or modified a Policy, not the user read or modified the Renewal Date field of the Policy. If there are sensitive operations that involve subsets of entities, or composites of multiple entity types, then log those on a discretionary basis.
All Hasura logs are considered HRBD. Hasura cannot classify which type of HRBD event is occurring. However, since Hasura logs are considered HRBD by default, then they can be leveraged to achieve compliance for a consuming application. For example, if your product has a SPA (web frontend) that queries Core Hasura directly, it is not necessary for that SPA to log a HRBD Read before invoking the Hasura Query. In the assessment, this activity would be listed as being covered by Hasura logging.