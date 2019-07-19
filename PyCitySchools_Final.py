#!/usr/bin/env python
# coding: utf-8

# # PyCity Schools Analysis
# 
# * As a whole, schools with higher budgets, did not yield better test results. By contrast, schools with higher spending per student actually (\$645-675) underperformed compared to schools with smaller budgets (<\$585 per student).
# 
# * As a whole, smaller and medium sized schools dramatically out-performed large sized schools on passing math performances (89-91% passing vs 67%).
# 
# * As a whole, charter schools out-performed the public district schools across all metrics. However, more analysis will be required to glean if the effect is due to school practices or the fact that charter schools tend to serve smaller student populations per school. 
# ---

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[1]:


# Dependencies and Setup
import pandas as pd
import numpy as np

# File to Load (Remember to Change These)
school_data_to_load = "Resources/schools_complete.csv"
student_data_to_load = "Resources/students_complete.csv"

# Read School and Student Data File and store into Pandas Data Frames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])
school_data_complete


# ## District Summary
# 
# * Calculate the total number of schools
# 
# * Calculate the total number of students
# 
# * Calculate the total budget
# 
# * Calculate the average math score 
# 
# * Calculate the average reading score
# 
# * Calculate the overall passing rate (overall average score), i.e. (avg. math score + avg. reading score)/2
# 
# * Calculate the percentage of students with a passing math score (70 or greater)
# 
# * Calculate the percentage of students with a passing reading score (70 or greater)
# 
# * Create a dataframe to hold the above results
# 
# * Optional: give the displayed data cleaner formatting

# In[2]:


total_number = len(school_data_complete["School ID"].unique())
total_number


# In[3]:


total_students = len(school_data_complete["Student ID"].unique())
total_students


# In[4]:


total_budget = school_data["budget"].sum()
total_budget


# In[5]:


average_math = student_data["math_score"].mean()
average_math


# In[6]:


average_reading = student_data["reading_score"].mean()
average_reading


# In[8]:


overall_average = (average_math + average_reading)/2
overall_average


# In[9]:


student_data["passing_math"] = student_data["math_score"] >= 70
student_data["passing_reading"] = student_data["reading_score"] >= 70
percent_math = ((student_data["passing_math"]).mean())*100
percent_math


# In[10]:


percent_reading = ((student_data["passing_reading"]).mean())*100
percent_reading


# In[13]:


overall_passing = (percent_math + percent_reading)/2
overall_passing


# In[20]:


district_results = [{"Total Schools": total_number, 
            "Total Students": total_students,"Total Budget": total_budget,"Average Math Score":  round(average_math,2), 
            "Average Reading Score":  round(average_reading,2),"Passing Math": round(percent_math,2),"Passing Reading": round(percent_reading,2),
            "Overall Passing Rate": round(overall_passing,2)}]
district_table = pd.DataFrame(district_results)


# In[21]:


district_table["Passing Math"] = district_table["Passing Math"].map("{:,.2f}".format)
district_table["Passing Reading"] = district_table["Passing Reading"].map("{:,.2f}".format)
district_table["Overall Passing Rate"] = district_table["Overall Passing Rate"].map("{:,.2f}".format)
district_table["Total Budget"] = district_table["Total Budget"].map("{:,.2f}".format)
district_table["Total Students"] = district_table["Total Students"].map("{:,}".format)


# In[23]:


district_table


# ## School Summary

# * Create an overview table that summarizes key metrics about each school, including:
#   * School Name
#   * School Type
#   * Total Students
#   * Total School Budget
#   * Per Student Budget
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * Overall Passing Rate (Average of the above two)
#   
# * Create a dataframe to hold the above results

# In[24]:


school_data_complete["passing_math"] = school_data_complete["math_score"] >= 70
school_data_complete["passing_reading"] = school_data_complete["reading_score"] >= 70

school_data_complete


# In[25]:


school_group = school_data_complete.groupby(["school_name"]).mean()
school_group["Per Student Budget"] = school_group["budget"]/school_group["size"]
school_group["Passing Math"] = round(school_group["passing_math"]*100,2)
school_group["Passing Reading"] = round(school_group["passing_reading"]*100,2)
school_group["Overall Passing Rate"] = round(((school_group["passing_math"] + school_group["passing_reading"])/2)*100,3)


# In[26]:


school_data_summary = pd.merge(school_group, school_data, how="left", on=["school_name", "school_name"])
del school_data_summary['size_y']
del school_data_summary['budget_y']
del school_data_summary['Student ID']
del school_data_summary['School ID_x']


# In[27]:


school_summary_dataframe = pd.DataFrame({"School Name":  school_data_summary["school_name"],
                                "School Type": school_data_summary["type"],"Total Students":school_data_summary["size_x"],
                               "Total School Budget": school_data_summary["budget_x"],"Per Student Budget":school_data_summary["Per Student Budget"], 
                               "Average Math Score":round(school_data_summary["math_score"],2),"Average Reading Score":round(school_data_summary["reading_score"],2), 
                               "Passing Math": school_data_summary["Passing Math"],"Passing Reading": school_data_summary["Passing Reading"],
                               "Overall Passing Rate": school_data_summary["Overall Passing Rate"]})


# In[28]:


school_summary_dataframe["Total Students"] = school_summary_dataframe["Total Students"].map("{:,.0f}".format)
school_summary_dataframe["Total School Budget"] = school_summary_dataframe["Total School Budget"].map("${:,.2f}".format)
school_summary_dataframe["Per Student Budget"] = school_summary_dataframe["Per Student Budget"].map("${:,.2f}".format)
school_summary_dataframe


# ## Top Performing Schools (By Passing Rate)

# * Sort and display the top five schools in overall passing rate

# In[29]:


top_performing = school_summary_dataframe.sort_values('Overall Passing Rate', ascending=False).iloc[0:5,]
top_performing


# ## Bottom Performing Schools (By Passing Rate)

# * Sort and display the five worst-performing schools

# In[30]:


top_performing = school_summary_dataframe.sort_values('Overall Passing Rate', ascending=True).iloc[0:5,]
top_performing


# ## Math Scores by Grade

# * Create a table that lists the average Reading Score for students of each grade level (9th, 10th, 11th, 12th) at each school.
# 
#   * Create a pandas series for each grade. Hint: use a conditional statement.
#   
#   * Group each series by school
#   
#   * Combine the series into a dataframe
#   
#   * Optional: give the displayed data cleaner formatting

# In[31]:


nineth_grade=  school_data_complete[school_data_complete["grade"] == "9th"].groupby("school_name").mean()["math_score"]
tenth_grade =  school_data_complete[school_data_complete["grade"] == "10th"].groupby("school_name").mean()["math_score"]
eleventh_grade =  school_data_complete[school_data_complete["grade"] == "11th"].groupby("school_name").mean()["math_score"]
twelveth_grade=  school_data_complete[school_data_complete["grade"] == "12th"].groupby("school_name").mean()["math_score"]


math_grade_dataframe= pd.DataFrame({"Ninth Grade":nineth_grade, "Tenth Grade":tenth_grade, 
                                     "Eleventh Grade":eleventh_grade, "Twelveth Grade":twelveth_grade})            


math_grade_dataframe[["Ninth Grade","Tenth Grade","Eleventh Grade","Twelveth Grade"]] = math_grade_dataframe[["Ninth Grade","Tenth Grade","Eleventh Grade","Twelveth Grade"]].applymap("{:.2f}".format)


math_grade_dataframe


# ## Reading Score by Grade 

# * Perform the same operations as above for reading scores

# In[32]:


nineth_grade=  school_data_complete[school_data_complete["grade"] == "9th"].groupby("school_name").mean()["reading_score"]
tenth_grade =  school_data_complete[school_data_complete["grade"] == "10th"].groupby("school_name").mean()["reading_score"]
eleventh_grade =  school_data_complete[school_data_complete["grade"] == "11th"].groupby("school_name").mean()["reading_score"]
twelveth_grade=  school_data_complete[school_data_complete["grade"] == "12th"].groupby("school_name").mean()["reading_score"]

reading_grade_dataframe = pd.DataFrame({"Ninth Grade":nineth_grade, "Tenth Grade":tenth_grade, 
                                     "Eleventh Grade":eleventh_grade, "Twelveth Grade":twelveth_grade})

reading_grade_dataframe[["Ninth Grade","Tenth Grade","Eleventh Grade","Twelveth Grade"]] = reading_grade_dataframe[["Ninth Grade","Tenth Grade","Eleventh Grade","Twelveth Grade"]].applymap("{:.2f}".format)

reading_grade_dataframe


# ## Scores by School Spending

# * Create a table that breaks down school performances based on average Spending Ranges (Per Student). Use 4 reasonable bins to group school spending. Include in the table each of the following:
#   * Average Math Score
#   * Average Reading Score
#   * % Passing Math
#   * % Passing Reading
#   * Overall Passing Rate (Average of the above two)

# In[33]:


# Sample bins. Feel free to create your own bins.
spending_bins = [0, 585, 615, 645, 675]
group_names = ["<$585", "$585-615", "$615-645", "$645-675"]


# In[34]:


school_data_summary["Spending Ranges (Per Student)"] = pd.cut(school_data_summary["Per Student Budget"], spending_bins, labels=group_names)

school_spending_grouped = school_data_summary.groupby("Spending Ranges (Per Student)").mean() 

del school_spending_grouped['size_x']
del school_spending_grouped['budget_x']
del school_spending_grouped['Per Student Budget']
del school_spending_grouped['School ID_y']
del school_spending_grouped['passing_math']
del school_spending_grouped['passing_reading']

school_spending_grouped


# ## Scores by School Size

# * Perform the same operations as above, based on school size.

# In[35]:


# Sample bins. Feel free to create your own bins.
size_bins = [0, 1000, 2000, 5000]
group_names = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]


# In[36]:


school_data_summary["School Size"] = pd.cut(school_data_summary["size_x"], size_bins, labels=group_names)
school_data_summary

school_size = school_data_summary.groupby("School Size").mean() 
school_size

del school_size['budget_x']
del school_size['Per Student Budget']
del school_size['School ID_y']
del school_size['passing_math']
del school_size['passing_reading']

school_size


# ## Scores by School Type

# * Perform the same operations as above, based on school type.

# In[37]:


school_type = school_data_summary.groupby("type").mean()

del school_type['size_x']
del school_type['budget_x']
del school_type['Per Student Budget']
del school_type['School ID_y']
del school_type['passing_math']
del school_type['passing_reading']

school_type


# In[38]:


#The first observation I can make are that charter shools preformed better than distric schools in all categorys.


# In[39]:


#The second observation I can make schools sizes (2000 - 5000) preform worse than the smaller school sizes.


# In[ ]:





# In[ ]:




