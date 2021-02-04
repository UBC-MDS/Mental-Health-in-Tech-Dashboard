# What We Have Implemented

As we mentioned in our proposal document, we wanted to make the “Mental Health in Tech Workers” app in such a way that it could provide an overview of the survey data used for the app but also include additional information relevant to our target audience. So far we have included these two sections in our app. Right now, the overview section consists of a visualization that allows the user to select a question from the survey and quickly visualize the responses and the HR questions section includes plots that each answer a specific question HR domain experts may have about the ways mental health issues affect work productivity as well as the factors which affect the rate at which productivity issues are experienced. In addition to these plots we have also implemented filters that allow users to filter the data included in the visualizations according to factors like the age and sex of survey respondents so that they can make the visualizations more closely align with the factors that exist in their workplaces (for example, with the current filters an HR domain expert could tune the visualizations to be more relevant to their predominantly male and older workforce).

# Future Improvements

For our future improvements, we would still like to include additional visualizations relevant to HR policies and how they affect mental health. For example, in our proposal's usage scenario section we indicated that we would like to be able to visualize the responses to the survey question “Does your employer provide resources to learn more about mental health issues and how to seek help?” as well as to visualize how certain other variables correlate with the occurences of survey responses indicating high levels of impact on worker productivity due to mental health issues. This would allow users to answer questions like "Does the data indicate that my proposed policy of (for example) expanding remote working options is likely to lead to a decrease in the rate of workers experiencing  mental health issues that impact their work productivity?".

Additonally, we would like to continue to add filters based on the survey response data (ex. filters for the benefits that are available at each of the survey respondents' companies) and make sure they apply to a global dataset which all visualizations could use so that HR domain experts can accurately model the conditions that exist in their workplaces as well as gain intuition on the potential effects of proposed policies.

Also, in our proposal we mentioned that we would like our dashboard to be tabbed but right now there is only a single page with sections so another future improvement would be to change over to tabbed sections. A final priority will be to apply some styling to the app since in its current state it is not very visually appealing, which could impact the user experience.  

# Known Issues

- In the overview section the labels of the dropdown options have been reworded from the original survey questions due to size constraints in the dropdown widget
- Visualization functions not currently adhereing to DRY principles so there could be potential for performance improvements by sharing functions and data between visualizations
- Some visualizations have null values showing up since they use data which has not yet been fully cleaned
