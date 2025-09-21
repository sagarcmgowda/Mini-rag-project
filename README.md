# Mini RAG Project: Industrial Safety Document Q&A System

This project implements a Retrieval-Augmented Generation (RAG) system to answer questions about industrial safety. It uses a vector database (FAISS) for semantic search and a hybrid reranker to improve the relevance of results. The system is exposed via a simple Flask API.

## Project Deliverables

-   **Code:** `ingest.py`, `reranker.py`, and `app.py`
-   **Data:** `sources.json` and a file containing 8 questions.
-   **Documentation:** This `README.md` file, which explains the setup, how to run the project, and a detailed analysis of the results.

---

## Setup and Installation

Follow these steps to set up the project on your local machine.

1.  **Clone the repository:**
    ```bash
    git clone [your-repo-url]
    cd mini-rag-project
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Add data files:**
    Ensure you have `industrial-safety-pdfs.zip` and `sources.json` in the project's root directory.

---

## How to Run

1.  **Run the data ingestion script:** This will unzip the PDFs, chunk the text, create embeddings, and build the FAISS index and SQLite database.
    ```bash
    python ingest.py
    ```
2.  **Start the Flask API:** Open a new terminal window and start the Flask development server. This terminal must remain open and running.
    ```bash
    python app.py
    ```
3.  **Send requests:** Use `curl` from a separate terminal to interact with the API.

---

## Example:

Here are two example requests to test the API for both search modes.

### Baseline Search Example

This command uses cosine similarity to find the most relevant chunks.

```bash
curl -X POST [http://127.0.0.1:5000/ask](http://127.0.0.1:5000/ask) -H "Content-Type: application/json" -d "{\"q\": \"What is the Machinery Regulation?\", \"k\": 3, \"mode\": \"baseline\"}"
```

### Reranker Search Example

This command uses a hybrid approach (cosine similarity + BM25 keyword search) to rerank the results for better accuracy.

```bash
curl -X POST [http://127.0.0.1:5000/ask](http://127.0.0.1:5000/ask) -H "Content-Type: application/json" -d "{\"q\": \"How to protect workers from amputations?\", \"k\": 5, \"mode\": \"reranker\"}"
```

### Results and Findings
The following table summarizes the results for the 8 questions, comparing the performance of the baseline and reranker modes.
| Question | Baseline Result | Reranker Result | Better Performer |
|----------|----------------|----------------|----------------|
| Q1: What is risk assessment? | "I am sorry, but the most relevant information found has a low confidence score." | <details><summary>View Answer</summary>"5 Safety functions and their contribution to risk reduction The hazards are then identified; all phases of the The objective of the further procedure is to reduce the risk machine\u2018s lifetime must be considered in this process. In to an acceptable level. For this purpose, Figure 5.3 shows addition to automatic mode, particular attention is paid to the proportions of risk reduction with and without safety- operating modes requiring manual intervention, e.g. for: related parts of a control system. Further information on the subject of risk can be found in the IFA Manual [19]. \u2022 Setting \u2022 Testing 5.2.2 Risk evaluation \u2022 Teaching/programming \u2022 Commissioning Following the risk estimation, a risk evaluation is per- \u2022 Material charging formed in order to determine whether a risk reduction is \u2022 Retrieval of the product necessary. The criteria for adequate risk reduction are \u2022 Troubleshooting and fault clearance specified in EN 12100 [3]: \u2022 Cleaning \u2022 Maintenance \u2022 Have all operating conditions and all intervention pro- cedures been considered? Further details of this process step can be found in EN ISO 12100 [3]. A range of methods exist for systematic \u2022 Have hazards been eliminated by suitable protective identification of the hazards; examples can be found measures or the risks reduced to the lowest practicable in ISO/DTR 14121-2 [4]. Possible hazards are also listed level? extensively in EN ISO 12100 [3]. Figure 5.2 shows an excerpt. \u2022 Has it been ensured that the measures taken do not give rise to new hazards? 5.2.1 Risk estimation \u2022 Have the users been sufficiently informed and warned Once all potential hazards which may be presented by the concerning the residual risks? machine have been identified, the risk must be estima- ted for each hazard. The risk associated with a particular \u2022 Has it been ensured that the protective measures taken hazardous situation can be determined from the following do not adversely affect the operators\u2018 working condi- risk elements: tions or the usability of the machine? a) Severity of harm \u2022 Are the protective measures taken compatible with one another? b) Probability of this harm occurring as a function of: \u2013 Exposure of a person/of persons to the hazard \u2022 Has sufficient consideration been given to the conse- \u2013 A hazardous event occurring quences that can arise from the use in a non-profes- \u2013 The technical and human possibilities for avoidance sional/non-industrial context of a machine designed for or limitation of the harm professional/industrial use? Electric shock Obstacles Counter-rotating rollers Automatic machinery: Crushing hazard may start without warning Figure 5.2: Examples of hazards (source: German Hand injuries Social Accident Insurance Institution for the food stuffs and catering industry) 27"</details> | Reranker |
| Q2: How to protect workers from amputations? | "Safeguarding Equipment and Protecting Employees from Amputations Occupational Safety and Health Administration U.S. Department of Labor OSHA3170-02R 2007" | <details><summary>View Answer</summary>"Hazardous Activities Controlling Amputation Employees operating and caring for machinery Hazards perform various activities that present potential amputation hazards. Safeguarding is essential for protecting employees from needless and preventable injury. A good rule Machine set-up/threading/preparation,* to remember is: Machine inspection,* Any machine part, function, or process that may Normal production operations, cause injury must be safeguarded. Clearing jams,* Machine adjustments,* In this booklet, the term primary safeguarding Cleaning of machine,* methods refers to machine guarding techniques Lubricating of machine parts,* and that are intended to prevent or greatly reduce the Scheduled and unscheduled maintenance.* chance that an employee will have an amputation injury. Refer to the OSHA general industry (e.g., * These activities are servicing and/or mainte- Subpart O) and construction (e.g., Subparts I and nance activities. N) standards for specific guarding requirements. Many of these standards address preventive meth- Hazard Analysis ods (such as using barrier guards or two-hand trip- You can help prevent workplace amputations by ping devices) as primary control measures; while looking at your workplace operations and identify- other OSHA standards allow guarding techniques ing the hazards associated with the use and care of (such as a self-adjustable table saw guard) that the machine. A hazard analysis is a technique that reduce the likelihood of injury. Other less protective focuses on the relationship between the employee, safeguarding methods (such as safe work methods) the task, the tools, and the environment. When that do not satisfactorily protect employees from evaluating work activities for potential amputation the machine hazard areas are considered second- hazards, you need to consider the entire machine ary control methods. operation production process, the machine modes Machine safeguarding must be supplemented of operation, individual activities associated with by an effective energy control (lockout/tagout) the operation, servicing and maintenance of the program that ensures that employees are protected machine, and the potential for injury to employees. from hazardous energy sources during machine The results from the analysis may then be used servicing and maintenance work activities. as a basis to design machine safeguarding and an Lockout/tagout plays an essential role in the pre- overall energy control (lockout/tagout) program. vention and control of workplace amputations. In This is likely to result in fewer employee amputa- terms of controlling amputation hazards, employ- tions; safer, more effective work methods; reduced ees are protected from hazardous machine work workers\u2019 compensation costs; and increased em- activities either by: 1) effective machine safeguard- ployee productivity and morale. ing, or 2) lockout/tagout where safeguards are ren- dered ineffective or do not protect employees from hazardous energy during servicing and mainte- nance operations. Additionally, there are some servicing activities, such as lubricating, cleaning, releasing jams and making machine adjustments that are minor in nature and are performed during normal produc- tion operations. It is not necessary to lockout/ tagout a machine if the activity is routine, repetitive and integral to the production operation provided that you use an alternative control method that affords effective protection from the machine\u2019s hazardous energy sources. Safeguarding Machinery The employer is responsible for safeguarding machines and should consider this need when pur- chasing machinery. Almost all new machinery is SAFEGUARDING EQUIPMENT AND PROTECTING EMPLOYEES FROM AMPUTATIONS 9"</details> | Reranker |
| Q3: What is a safeguarding device? | "I am sorry, but the most relevant information found has a low confidence score." | <details><summary>View Answer</summary>"3A – DEFINING THE SAFETY FUNCTIONS Temporarily preventing access ..." </details> | Reranker |
| Q4: What are the requirements for safety-related parts of control systems? | "I am sorry, but the most relevant information found has a low confidence score." | <details><summary>View Answer</summary>"12/22 PU05907001Z-EN 9 noitcudortnI Risk reduction through the use of safety-related parts ..." </details> | Reranker |
| Q5: What is the Machinery Regulation? | "I am sorry, but the most relevant information found has a low confidence score." | <details><summary>View Answer</summary>"§ – LAWS, DIRECTIVES, STANDARDS NOTE The directives are freely available ... " </details> | Reranker |
| Q6: What is SISTEMA? | "I am sorry, but the most relevant information found has a low confidence score." | <details><summary>View Answer</summary>"Annex H: SISTEMA: the software utility for evaluation of SRP/CS ..." </details> | Reranker |
| Q7: What is the purpose of a safety circuit? | "I am sorry, but the most relevant information found has a low confidence score." | <details><summary>View Answer</summary>"Inherent stability functions are performed: Property of a switching device ..." </details> | Reranker |
| Q8: How to calculate Performance Level (PL)? | "I am sorry, but the most relevant information found has a low confidence score." | <details><summary>View Answer</summary>"Example: Determining the PL of the “power control elements” subsystem ..." </details> | Reranker |



