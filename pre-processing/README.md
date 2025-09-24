# Codebook: Data Analysis File

This Codebook describes the meaning of the column names in the file "data_for_moderation_analyses.csv" used for the meta-analysis of the Relative Prevalences of PTSD Symptom Trajectories (Pre-print: https://doi.org/10.31219/osf.io/fkjb2_v1).

| Column Title(s) | Meaning |
|---|---|
| Study | Name of the author and year, e.g., Lowe et al., 2020 or Allison & Berle, 2023. In case the study had more than one sample / cohort, we added it with a “_” here to indicate the appropriate data, such as “_CSR” and “_NonCSR”. |
| Sample_name | Indicates which cohort/sample from the respective paper it is if there were more than one. |
| MID | Paper ID in the Mother file. |
| Grolts | Final quality score for each paper. |
| Sample_Size | Sample size of the analytic sample of the paper (per cohort/sample if applicable). |
| Mean_age | Mean age of the analytic sample of the paper. |
| Developmental_age | Whether the sample was adult or youth (age <18). Mixed samples are indicated as NA. |
| Percentage_women | Percentage of women / female gender in the sample. |
| Percentage_minority | Percentage of minorities in the sample according to the country (e.g., African Americans and Asians in the US). |
| Percentage_partner | Percentage of individuals in the samples who are married / have a partner. |
| High_education | Percentage of individuals with some college or a completed college degree. |
| Location | Country where the sample is from. |
| Location_US | Whether the sample is from the US vs other countries. |
| Assessed_trauma_type | Our evaluation of the type(s) of trauma experienced by the individuals in the studies. |
| Discrete | Whether the sample was affected by a discrete trauma (i.e., a traumatic event identifiable in time, such as a terrorist attack or an earthquake) or not. If mixed, indicated by NA. |
| Health_First | Whether the sample included health workers and first responders or not. |
| Trauma_type | Whether the sample in the study was exposed to a natural disaster (Natural), injury or combat. If the trauma experienced was different, it is indicated by NA. |
| Military | Whether the sample included military personnel (Yes) or not (No). If mixed, indicated by NA. |
| Occupational_trauma | Whether the sample experienced occupational trauma (e.g., military, first responders, health workers) or not. If mixed, indicated by NA. |
| Trauma_exposure | Whether the sample experienced non-interpersonal (Non) or interpersonal (Inter) trauma. Mixed samples were indicated by NA. |
| Scale_moderator | Whether the PTSD assessment was self-measured (Self) or an interview (Interview). |
| Diagnostic_DSM | Whether the sample as assessed using DSM-III (3), DSM-IV (4), DSM-5 (5), ICD or mixed (Mix). |
| Trajectory_analysis | Whether the final model selected in the study was latent growth mixture model (LGMM) or latent growth mixture analysis (LCGA). |
| TP_assessments | Number of time-point assessments in the study. |
| N_trajectories | Number of trajectories reported in the paper. |
| Trauma_TP1 | Number of months between traumatic event and the first timepoint assessment. |
| TP1_TPX | Number of months between the first timepoint assessment and the last timepoint assessment. |
| Trauma_TPX | Number of months between the traumatic event and the last timepoint assessment. |
| Entropy | Value for the entropy of the chosen model. |
| Low, Decreasing, Increasing, High, Moderate, Relapsing, Worsened_improving | Whether the trajectory is present (1) or absent (0) based on our interpretation and discussion. |
| Low_rate, Low_percentage, Decreasing_rate, Decreasing_percentage, Increasing_rate, Increasing_percentage, High_rate, High_percentage, Moderate_rate, Moderate_percentage, Relapsing_rate | Rate (decimal) and percentage of individuals in each trajectory based on our interpretation and discussion. This data reflects our interpretation and may involve the merging of trajectories. |
| Merging | For each study, we reported 0 if no trajectories were merged and 1 if trajectories were merged. |
| Relabeling | For each study, we reported 0 if no trajectory was relabeled and 1 if any trajectory was relabeled. |

---
