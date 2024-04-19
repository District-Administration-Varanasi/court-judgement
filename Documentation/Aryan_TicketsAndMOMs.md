# Automated Document Drafting System

## Flow 1: Document Analysis and Section Building

### 1. Document Collection
- Gather 20 representative documents.
- Ensure that the documents cover diverse cases and styles for better generalization

### 2. Semantic Structure Extraction
- Develop an NLP system to parse documents and extract sections, headings, and contents.
- For structured data, this step could be done heuristacally. For unstructured data like images and pdf, document segmentation modelling. BeamSeg: A Joint Model for Multi-Document Segmentation and Topic Identification (Pedro Mota et el 2019) https://aclanthology.org/K19-1054/ is a good reference.

### 3. Template and Rule Creation
- Utilize extracted semantic structures to define section formats.
- Identify typical content organization.
- Convert structures to drafting rules or templates.

### 4. Model Training
- Use semantic structures as training data for drafting algorithms.

### 5. Section Builder Implementation
- Implement a system to construct document sections from new data using trained models.

## Flow 3: Closeness Evaluation Process
This step would ensure that the QnA pairs generated via the few shot approach and the semantics captured in flow 1 are good enough to reproduce the original document. Otherwise flow 1 and flow 2 have to be reiterated for better performance in metrics of flow 3.

### Step 1: Metric Definition
- Determine metrics to measure the closeness between original and reproduced documents, focusing on semantic accuracy, structural fidelity, completeness, and consistency.
- Structural fidelity: How closely does the format and organization of the reproduced document match the original?
- Completeness: Does the reproduced document contain all the essential information from the original?
- Consistency: Are the terms, definitions, and language used in the reproduced document consistent with the original?
- Semantic Accuracy: How well does the content of the reproduced document capture the meaning and intent of the original?

### Step 2: Comparison Framework
- Create a framework to deconstruct and compare the original and reproduced documents.
- It should breakdown the original and generated document to sections and map these sections for each document so that a check could be conducted.
- Initially, for the baseline version, the comparison could be performed manually because lot of experimentation is expected in the initial phase.

### Step 3: Automated Evaluation
- Apply text similarity analysis and information extraction for evaluation. eg. BERT, cosine similarity etc
- Use Named Entity Recognition to check for the consistency of key information between original and regenerated document.

### Step 4: Manual Review
- This is a manual check layer in the development process when the amount of data is low and experimentation and reiteration of system is rapid.
- On a longer timescale, user could be allowed for pointing out flaws in the document in any specific part (via selecting that part) and the system should revisit it for a improved response.

### Step 5: Iterative Improvement
- Retrain models with evaluation feedback.
- Refine QnA pairs for better semantic capture.

### Step 6: Quality Thresholds
- Define clear acceptance criteria for the reproduced document to be considered "close enough".
- Redraft sections that don't meet criteria.


# Meeting minutes
## April 16
- This was a all team meet and an orientation to the project.
- The flow for the project was introduced and explained.
- It was planned to develop a baseline version in a week's time. Post this, further development and refineing would be done.


## April 17
- Discussions on the flow were undertaken.
- The complications of imperfect answer by the user were disucussed.
- Flow of investigating the sufficiency of information provided by the user and mapping them with the required QnA was discussed.
- Aryan asked about the possibility of utlizing GPT-3.5,4 like models for the task because it has an edge in handling imperfect cases in human answers.
- Role of document segmentation modelling in flow 1 was discussed. For structured data it is not required but in a longer run, it will make us dataset agnostic thus improving model's performance.
