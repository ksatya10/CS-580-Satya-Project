# A Data-Driven Framework for Identifying Student Behaviors in Collaborative Software Projects

This project aims to analyze student behavior in collaborative software engineering projects by using GitHub contribution data.

Our goal is to provide instructors with a data-driven framework to automatically detect participation patterns like Good Teammate, Lone Wolf, Hitchhiker, and Couch Potato, enabling early intervention and improved fairness.

<h3>Project Files:</h3>

Final_File_StudentID1.csv – GitHub-derived contribution data per student.

all_teammate_types_final1.csv – Ground truth behavior labels from peer evaluations.

repomining3.py – Script to extract github contribution data from GitHub using API.

Merging.py – Script to map GitHub usernames to anonymized student IDs.

Project.ipynb – Jupyter notebook performing clustering, GPT labeling, and behavior analysis.

<h3>Setup:</h3>

Clone the repository or unzip the file.

<ol>
<li><div>

If you want to re-mine data from Github:

Step1: Open repomining3.py

Step2: Paste your github token in the code.

Step3: Run the script to generate a new PR data.

</div></li>

<li><div>

To Merge the student's GitHub ID's with their assigned student ID's:

Step1: run repomining3.py

</div></li>

<li><div>

Run the Project.ipynb file to see the student contributions:

Step1: Open Project.ipynb

Step2: Paste the OpenAI token to access the GPT classification

Step3: Run the notebook using "jupyter notebook Project.ipynb"

</div></li>
</ol>

<h4>Note:</h4>

Haven't uploaded the Student ID with their GitHub ID's mapping due to IRB compliance and privacy concerns.
