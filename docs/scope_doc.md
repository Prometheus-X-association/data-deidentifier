# Data DeIdentifier (DDI)
## Overview

The issue of having non-anonymized or non-pseudonymized data presents several challenges, especially concerning GDPR compliance, data sharing, and AI training. Under GDPR, there are strict regulations on how personal data must be handled and protected. Non-compliance can result in severe penalties for organizations. Non-anonymized data can lead to privacy violations, as individuals' personal information might be exposed without their explicit consent, thereby breaching GDPR guidelines. When it comes to data sharing, transferring non-anonymized data between organizations, even those that are trusted, increases the risk of unauthorized access and data breaches.
For AI training, using non-anonymized data can introduce ethical concerns and privacy risks. AI models trained on such data might inadvertently learn and perpetuate biases, or worse, recreate personal information that should remain private. This can lead to biased or unfair AI systems and raise legal questions about data usage and model compliance with existing privacy laws.

Therefore, the lack of anonymization or pseudonymization can hinder the ability to safely and legally process, share, and utilize data, ultimately stagnating innovation and collaboration in data-driven fields. Implementing robust anonymization or pseudonymization processes is crucial to overcoming these challenges and ensuring ethical, legal, and secure data management.

As a result, Inokufu was tasked, within the Prometheus-X ecosystem, to develop a Data De-Identifier (DDI) which anonymizes and pseudonymizes json and text traces.

Data De-Identifier (DDI) aims to anonymize or pseudonymize a text or JSON. Subsequently, the organization that requested this feature will be able to transfer these anonymized/pseudonymized data between trusted organizations.


## Objectives and Expected Outcomes
The objective of this building block is to specify and develop APIs type "parser" to anonymize or pseudonymize JSON data or text. This feature is designed to enhance data privacy and security. Once the data has been anonymized or pseudonymized, the requesting organization can share it with other trusted entities without compromising privacy. This secure sharing capability is essential for collaborative projects, research, and data analysis across different organizations that require the use of sensitive information.

Since anonymized data cannot be traced back to individuals, obtaining consent from data subjects is not required, allowing for an expansive dataset. This will enable, among other benefits, the merging of datasets to achieve a larger data volume. Such combined datasets facilitate the training of Machine Learning models on an unprecedented scale.

This tool also helps organizations more easily comply with GDPR requirements. Compliance is mandatory for all organizations and can be adapted between general terms and conditions of use and user consent. Therefore, the DDI allows for the anonymization or pseudonymization of data traces in accordance with specified requirements.

## Approach
The Data De-Identifier (DDI) is a robust and flexible application designed to anonymize or pseudonymize JSON data and text. Tailored to adhere to the CNIL and edpb specifications, DDI facilitates a streamlined conversion process by choosing whether the trace sent should be anonymized or pseudonymized.

As explained, in this API we will be concentrating on JSON and text traces. Although the xAPI format is JSON, a separate [project has been developed to anonymize an xAPI trace](https://github.com/Prometheus-X-association/trace-deidentifier). Throughout the DDI BB process, we will be relying on the work of Presidio. [Presidio](https://microsoft.github.io/presidio/) is an open source tool that identifies the elements to be anonymized/pseudonimized and performs the conversion. Our complementary developments will enable Prometheus-X to correspond more closely to education issues.

The **Data De-Identifier (DDI)** will have 2 separate endpoints to make an anonymization or pseudonymization call.
<img width="787" alt="Capture d’écran 2025-06-19 à 10 26 40" src="https://github.com/user-attachments/assets/0bf39c6f-dd83-427f-8105-2ca776010902" />


### Anonymization
We are going to undertake the anonymization of either text or JSON data. The primary goal of anonymization is to remove any information that could identify the user originating the data trace. In this process, primary and sensitive information will be modified by the chosen method:
- modification by selected text (e.g. ANONYMOUS)
- modification by data type (e.g. PERSON)
- modification by selected character (e.g. ___)
The advantage of this anonymization process is that it allows for data sharing without needing to obtain user consent. While this enables AI training and statistical analysis to be conducted, it is done at a reduced level of granularity.

Anonymization involves stripping the data of any personally identifiable information (PII), making it impossible to trace back to an individual. This process is crucial for organizations that handle sensitive data and need to comply with data protection regulations such as the GDPR or CCPA.

Data that will be anonymized :
- EMAIL_ADDRESS
- IP_ADDRESS
- LOCATION
- PERSON
- PHONE_NUMBER
- MEDICAL_LICENSE

Data exchange :
- Input : text or json
- Output : anonymized text or anonymized json
<img width="863" alt="Anonymiz" src="https://github.com/user-attachments/assets/2adf4113-01de-4a49-ba8a-302a39207808" />

**Example**

Input
```
Martin is a student from Paris living in Tour. His telephone number is +33123456789. He achieved a mark of 15/20 in maths, giving him the opportunity to continue his semester.
His classmate, Louise, also from Paris, only scored 3/20. We advise Louise to ask Martin for advice on the use of differential equations.
```
Output with a text replacement of your choice, here ANONYMOUS
```
ANONYMOUS is a student from ANONYMOUS living in ANONYMOUS. His telephone number is ANONYMOUS. He achieved a mark of 15/20 in maths, giving him the opportunity to continue his semester.
His classmate, ANONYMOUS, also from ANONYMOUS, only scored 3/20. We advise ANONYMOUS to ask ANONYMOUS for advice on the use of differential equations.
```
Or output with replacement by data type
```
<PERSON> is a student from <LOCATION> living in <LOCATION>. His telephone number is <PHONE_NUMBER>. He achieved a mark of 15/20 in maths, giving him the opportunity to continue his semester. His classmate, <PERSON>, also from <LOCATION>, only scored 3/20. We advise <PERSON> to ask <PERSON> for advice on the use of differential equations.
```
Or output with character replacement
```
______ is a student from _____ living in ____. His telephone number is ____________. He achieved a mark of 15/20 in maths, giving him the opportunity to continue his semester. His classmate, ______, also from _____, only scored 3/20. We advise ______ to ask ______ for advice on the use of differential equations.
```

### Pseudonymization
The second aspect of DDI is the ability to pseudonymize text or JSON data. Pseudonymization involves replacing private identifiers with pseudonyms, allowing data processing and analysis while minimizing the risk of unauthorized disclosure. 
In the context of data management and privacy, it is essential to pseudonymize data traces to protect individual identities. Pseudonymization serves as a valuable technique that allows organizations to process data without revealing personal identities, thereby enhancing privacy and security. However, despite its benefits, there are challenges when it comes to obtaining consent from individuals. Many stakeholders remain hesitant to provide consent, even for pseudonymization.

To address these concerns, a system can be implemented whereby data traces originating from the same person are pseudonymized in a consistent manner within a single dataset. This ensures that the data remains useful for analysis while maintaining privacy. It is important to note that once the processing task has been completed, the table linking the pseudonym to the person's real identity is destroyed. This means that if the data is accessed or processed again in the future, the same individual's data from the first dataset will not be assigned the same pseudonym in a new dataset.

Consequently, this approach does not require the user's consent, as re-identification of the person is not possible.

The DDI employs random number or counter methods as a strategy for pseudonymizing data. Each has its own approach to generating pseudonyms:
- Random Number Method:
  -   Description: This method involves replacing identifiable information with randomly generated numbers. The random numbers act as pseudonyms to represent individuals' data without directly revealing their identities.
  -   Process: Instead of using sequential or predictably structured identifiers, a random number (often generated using a secure random number generator) is assigned to each piece of personal data. The randomness ensures that the pseudonym cannot be easily traced back to the original data.
  -   Advantage: The randomness provides strong privacy protection because it is difficult for unauthorized parties to reverse-engineer the pseudonyms to identify individuals.

- Counter Method:
  -   Description: This method uses a sequential counter to assign pseudonyms to identifiable data.
  -   Process: A counter starts at a specific value (often 1 or 0), and each item of data is assigned the next available number as its pseudonym. This creates a straightforward one-to-one mapping.
  -   Advantage: The counter method is simple to implement and ensures that each pseudonym is unique, as long as the counter does not repeat.

Data that will be pseudonymized :
- EMAIL_ADDRESS (example : <EMAIL_ADRESS_001>)
- IP_ADDRESS (example : <IP_ADDRESS_001>)
- LOCATION, for this data, we also indicate the country to give a better context without being able to re-identify the person (example : <LOCATION_001>(FRANCE))
- PERSON (example : <PERSON_001>)
- PHONE_NUMBER (example : <PHONE_NUMBER_001>)
- MEDICAL_LICENSE (example : <MEDICAL_LICENSE_001>)

Data exchange :
- Input : text or json
- Output : pseudonymized text or pseudonymized json
<img width="921" alt="pseudonimiz" src="https://github.com/user-attachments/assets/f8f7e2b2-7eae-4441-979b-9a2672473389" />



**Example with counter method**

Input
```
Martin is a student from Paris living in Tour. His telephone number is +33123456789. He achieved a mark of 15/20 in maths, giving him the opportunity to continue his semester.
His classmate, Louise, also from Paris, only scored 3/20. We advise Louise to ask Martin for advice on the use of differential equations.
```

Output
```
<PERSON_001> is a student from <LOCATION_001>(FRANCE) living in <LOCATION_002>(FRANCE). His telephone number is <PHONE_NUMBER_001>. He achieved a mark of 15/20 in maths, giving him the opportunity to continue his semester.
His classmate, <PERSON_002>, also from <LOCATION_001>(FRANCE), only scored 3/20. We advise <PERSON_002> to ask <PERSON_001> for advice on the use of differential equations.
```

## Use case examples
In the context of the education sector, data that might be anonymized or pseudonymized can be varied and include multiple types of information. Here are some examples:

**Report Cards and Grades:**
Detailed performance metrics and evaluations for students, including grades in subjects, comments from teachers, and overall GPA.

**Attendance Records:**
Data on student attendance, absences, tardiness, and participation, which can be used to analyze patterns and understand potential issues affecting academic performance.

**Behavioral Reports:**
Records concerning incidents, disciplinary actions, or behavioral notes that may be used for understanding student behavior trends without implicating individuals.

**Course Enrollment and Completion:**
Data regarding the courses students have enrolled in, completed, or dropped, which helps in understanding trends in course popularity and completion rates.

**Health Records:**
Information related to student health, such as immunization records or visits to school health services, while ensuring compliance with health privacy regulations.

**Extracurricular Activities:**
Participation data in clubs, sports, and other school-sponsored activities, helping to assess student engagement outside of academics.

**Alumni Tracking:**
Data on graduates, such as employment status, higher education enrollment, and career progression, used to assess long-term educational outcomes.

**Teacher and Staff Evaluations:**
Performance reviews and evaluations, anonymous feedback from students, or peer reviews, ensuring that staff development remains non-biased.

**Letter of motivation:**
A source of motivation before starting training.

These text or json, when anonymized or pseudonymized, enable educational institutions to share and analyze information without compromising the privacy of individuals involved. This facilitates research, policy-making, and operational improvements while adhering to necessary ethical and legal standards.

## Project status
Please note this project is work in progress.
- [x] Definition of the architecture of the API endpoints
- [ ] Development of the endpoints necessary for anonymization and pseudonymization
- [ ] API testing with model datasets provided by Prometheus volunteer partners
- [ ] Deployment of the service in a managed version in one of the partner cloud providers
- [ ] Drafting of the public documentation, hosting and putting it online

## Roadmap
Here are the key milestones of the project:
- 2025 Q2: Start of development of the data de-identifier
- 2025 Q3: Launch V0 of data de-identifier
- 2025 Q4: test avec des partenaires, Launch V1 of data de-identifier

## Setup and installation
ToDo: this part will be completed when the first stable version of the code will be released.

## Contribution guidelines
We welcome and appreciate contributions from the community! There are two ways to contribute to this project:
- If you have a question or if you have spotted an issue or a bug, please start a new issue in this repository.
- If you have a suggestion to improve the code or fix an issue, please follow these guidelines:
  -   a. **Fork the Repository**: Fork the Data De-Identifier repository to your own GitHub account.
  -   b. **Create a Branch**: Make a new branch for each feature or bug you are working on.
  -   c. **Make your Changes**: Implement your feature or bug fix on your branch.
  -   d. **Submit a Pull Request**: Once you've tested your changes, submit a pull request against the Data De-Identifier's master branch.
Before submitting your pull request, please ensure that your code follows our coding and documentation standards. Don't forget to include tests for your changes!

## References
- https://gaia-x.eu/gaia-x-framework/
- https://prometheus-x.org/
- https://www.edpb.europa.eu/our-work-tools/documents/public-consultations/2025/guidelines-012025-pseudonymisation_fr
- https://www.cnil.fr/fr/professionnel
- https://www.enisa.europa.eu/sites/default/files/all_files/Pseudonymisation%20Techniques%20and%20best%20practices_FR.pdf
