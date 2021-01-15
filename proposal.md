Motivation and Purpose
----------------------

Our role: Data scientist consultancy firm

Target audience: HR professionals in large companies

Mental health issues can be costly to organizations due to lost
productivity, absences and even disability. The World Health
Organization estimates that half of all disability worldwide is due to
mental health and that 200 million workdays are lost annually due to
absenteeism relating to mental health in the United States (Harnois et
al. 2000). Although HR departments implement processes and cultivate
workplace culture so as to encourage good mental health, it is often
unclear whether these policies do in fact make a difference. If these
policy makers could explore which factors are indicators of mental
health and what policies are effective in helping employees seek out
help, such as providing benefits or providing accessible options, the
organization can take a smarter approach to policy implementation. The
benefits of reducing mental health could lead to decreased absenteeism,
improved employee morale as well providing the organization with a
positive reputation for being viewed as a good place to work.

To address these issues, we propose a dashboard which would be used by
HR professionals who are in charge of setting HR policy in organizations
to visually explore a survey data set of mental health attitudes from
tech workers across the globe to identify potential connections that may
help with policy setting. The dashboard will allow filtering between
responses for those who indicate that they do have a mental health issue
versus those that do not and comparing various variables to see how much
they may interfere with their work.

Description of the Data
-----------------------

Our data-set is part of the survey conducted by a non-profit
organization named Open Sourcing Mental Illness intended to measure
attitudes towards mental health and the frequency of mental health
disorders in the tech workplace. We will be visualizing the data based
on the surveys that have been conducted in the year 2014 and from 2016
to 2020 that are available at OSMI (Illness 2014). The data features
collected varies across the years and has columns that contain
information related to the respondents(age, gender, country, states,
treatment, etc), the respondent’s company, and related wellness
information(number of employees, remote work, benefits, wellness
program, leave, etc) and the viewpoint of the respondent on seeking help
and discussing wellness related issues(e.g.: Do you think that
discussing a mental health issue with your employer would have negative
consequences?)

Research Questions and Usage Scenarios
--------------------------------------

### Example Usage Scenario

Mary is a policy maker in HR for a large tech company and she wants to
understand what factors affect the mental health of tech workers so that
she can create policies that will improve productivity by reducing the
likelihood of employees developing mental health conditions that affect
their work.

She wants to be able to \[explore\] a data set in order to \[compare\]
the effect of different variables on the rate at which employees develop
mental health conditions that affect their work (called `work_interfere`
in the data set) and \[identify\] the most relevant variables around
which to frame her new policies.

When Mary logs on to the “Mental Health in Tech Workers” app, she will
see an overview of all the available variables in the data set,
according to how each variable affects the `work_interfere` rate.

She can then use her domain expert knowledge to \[filter\] out variables
which would be difficult to craft HR policies around (eg. in Canada an
employer cannot make policies which discriminate on the basis of family
history of mental illness (Branch 2021), so this variable will probably
not be relevant for her usage). She can then \[rank\] the remaining
variables according to metrics like how correlated they are to the
`work_interfere` rate. When she does this, Mary may notice that the
`seek_help` variable, which corresponds to the survey question “Does
your employer provide resources to learn more about mental health issues
and how to seek help?”, appears to be strongly negatively correlated to
the development of mental health conditions affecting employment. She
notes this correlation and hypothesizes that introducing a policy to
provide resources for employees seeking help with regards to mental
health will reduce the `work_interfere` rate at her company, and decides
she needs to conduct a follow-on study to test this hypothesis.

### Research Questions

From the usage scenario some example research questions we would like
our dashboard to be able to answer were identified, including:

Are there notable relationships between variables in the data set? Do
these relationships inspire ideas for policy changes among HR domain
experts? What variables correlate most closely to the `work_interfere`
variable? Can the `work_interfere` variable be consistently predicted
using a subset of the other variables in the data set? What are the most
important variables for doing this?

References
==========

Branch, Legislative Services. 2021. “Consolidated Federal Laws of
Canada, Canadian Human Rights Act.” *Canadian Human Rights Act*. Justice
Laws Website.
<https://laws-lois.justice.gc.ca/eng/acts/h-6/fulltext.html#:~:text=3%20(1)%20For%20all%20purposes,which%20a%20pardon%20has%20been>.

Harnois, Gaston, Phyllis Gabriel, World Health Organization, and
International Labour Organisation. 2000. “Mental Health and Work :
Impact, Issues and Good Practices.” Nations for Mental Health. World
Health Organization.

Illness, Open Sourcing Mental. 2014. “2014 Mental Health in Tech Survey
\[Data File and Code Book\].” <https://osmihelp.org/research>.
