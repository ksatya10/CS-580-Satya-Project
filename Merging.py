import pandas as pd

main_df = pd.read_excel("all_repos_pull_request_contributions_Final1.xlsx")

mapping_df = pd.read_excel("GitHubID_StudentID.xlsx")

merged_df = main_df.merge(mapping_df, left_on="Author", right_on="GitHubID", how="left")

merged_df["Author"] = merged_df["StudentID"]

merged_df.drop(columns=["GitHubID", "StudentID"], inplace=True)

merged_df.to_excel("main_file_with_student_ids.xlsx", index=False)

print("Merged successfully. New file saved as 'main_file_with_student_ids.xlsx'")
