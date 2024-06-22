import os

COMPANY_NAME = os.getenv("COMPANY_NAME")
EXTRACT_COMPANY_CAREER_PAGE_URL_SYS_PROMPT = """You are a website crawler. You will be given the name of a company. 
You should output the URL of the company's career page. 
Remember, YOUR OUTPUT SHOULD ONLY BE THE URL and NOTHING ELSE"""
EXTRACT_COMPANY_CAREER_PAGE_URL_USER_PROMPT = f"""Can you output the URL that is the 
official careers page for a tech company called {COMPANY_NAME}? 
Remember, YOUR OUTPUT SHOULD ONLY BE THE URL and NOTHING ELSE."""


SEARCH_FOR_SOFTWARE_ROLES_USR_PROMPT = """ You are an AI Job Hunter Web Agent who is an expert in searching for software engineer roles on company career websites. 

You will be given a list called HTML_INPUT_ELEMENTS. Each element in HTML_INPUT_ELEMENTS list is an HTML input element that is searchable on a company's career website.   
You should pick one input element that is prompting the user to search for specific job openings in the company. The input element you pick should be
the most relevant for searching for software engineer job openings on a company's career website. This selected input element allows the user to directly enter the type of job they are searching for, which is a common and effective way to find specific job listings on a company's career site.

Pick an element from HTML_INPUT_ELEMENTS LIST. Remember, YOUR OUTPUT SHOULD ONLY BE AN ELEMENT FROM HTML_INPUT_ELEMENTS LIST and NOTHING ELSE.

Here are two examples -

<example>

HTML_INPUT_ELEMENTS = ['input datatestidSearchInput colorpink80 namesearch placeholderOpenings classscbc6dc2282 hQcbLS value', 'input datatestidcoreuidropdown namecategoryFiter rolecombobox ariaexpandedfalse ariaautocompletenone ariareadonlyfalse 
ariadescribedbycoreuiid8154769791description ariainvalidfalse idcoreuiid8154769791 readonly classsc1v6kknp5 hsPasW', 'input datatestidcoreuidropdown namelocationFilter rolecombobox ariaexpandedfalse ariaautocompletenone ariareadonlyfalse ariadescribedbycoreuiid4236106179description ariainvalidfalse idcoreuiid4236106179 readonly classsc1v6kknp5 hsPasW']

OUTPUT = input datatestidSearchInput colorpink80 namesearch placeholderOpenings classscbc6dc2282 hQcbLS value

</example>

<example>

HTML_INPUT_ELEMENTS = ['input typetext class stylelabelinputcolorinheritbackground0opacity1width100gridarea1  2fontinheritminwidth2pxborder0margin0outline0padding0 autocapitalizenone autocompleteoff autocorrectoff idDepartmentIIm4gVcW87dBN1Mt9dAW2input spellcheckfalse tabindex0 value ariaautocompletelist ariaexpandedfalse ariahaspopuptrue rolecombobox', 'input typehidden namedepartment valuealldepartments
', 'input typetext classBaseInputmoduleinputAt1nr BaseInputmodulesize48OHWCP namerole value idrolezRPV1pf0o6eghG60mGVW9 spellcheckfalse', 'input typetext class stylelabelinputcolorinheritbackground0opacity1width100gridarea1  2fontinheritminwidth2pxborder0margin0outline0padding0 autocapitalizenone autocompleteoff autocorrectoff idLocationn8IT109WCGxZkIguoWininput spellcheckfalse tabindex0 value ariaautocompletelist ariaexpandedfalse ariahaspopuptrue rolecombobox', 'input typehidden namelocation valuealllocations',]

OUTPUT = input typetext classBaseInputmoduleinputAt1nr BaseInputmodulesize48OHWCP namerole value idrolezRPV1pf0o6eghG60mGVW9 spellcheckfalse

</example>

USR_HTML_INPUT_ELEMENTS = {HTML_INPUT_ELEMENTS}

Pick the most relevant input element from the USR_HTML_INPUT_ELEMENTS list that allows the user to directly enter the type of job they are searching for. This input element should be the most effective for finding specific software engineer job openings on a company's career website.

Pick an element from USR_HTML_INPUT_ELEMENTS LIST. Remember, YOUR OUTPUT SHOULD ONLY BE AN ELEMENT FROM USR_HTML_INPUT_ELEMENTS LIST and NOTHING ELSE.
"""

"""
The OUTPUT is "<input data-testid="SearchInput" color="pink80" name="search" placeholder="Openings" class="sc-bc6dc228-2 hQcbLS" value="">", because it appears to be the search input field that allows the user to search for specific job openings. This is the most relevant input element for a job search functionality on a company's career website.

The OUTPUT is "<input type="text" class="BaseInput-module_input__At1nr BaseInput-module_size48__OHWCP" name="role" value="" id="role-zRPV1pf0o6eghG60mGVW9" spellcheck="false">", which is the "role" input field, because it appears to be the most relevant for searching for software engineer job openings on a company's career website. This input field allows the user to directly enter the job role or title they are searching for, which is a common and effective way to find specific job listings on a company's career site.
"""

IS_WEB_ELEMENT_RELATED_TO_CAREER_EXPLORATION_PROMPT = """You are an AI Job Hunter Web Agent who is an expert in search for software engineer roles on company career websites.

You will be given metadata of a web element. 

WEB_ELEMENT_METADATA = {WEB_ELEMENT_METADATA}

Evaluate the WEB_ELEMENT_METADATA based on its label, url, and description on
the following criteria

1. WEB_ELEMENT_METADATA is relevant for the user to explore career
opportunities or job openings. 

Your output should be "True" if the web element metadata meets these criteria and "False" if it does not.

Output Format:
Your output should be a single word: "True" or "False."

REMEMBER, YOUR OUTPUT SHOULD ONLY EITHER "True" OR "False" AND NOTHING ELSE.
"""


DETERMINE_WEB_PAGE_IS_SOFTWARE_APPLICATION_PROMPT = """
You are an AI trained to analyze images of a web page. The images stitched together is the entire web page. Determine if the web page is for a software engineering role job listing where the user can fill out their information and submit the job application. Evaluate the web page based on the following criteria:

1. Job Title and Description: Look for terms related to software engineering such as "Software Engineer," "Developer," "Programmer," or similar titles. Read the description to ensure it aligns with typical software engineering duties.

2. Application Form: Check for fields where applicants can enter their personal information, such as name, email, phone number, resume/CV, and cover letter. These fields must be present on the web page. 

3. Submission Mechanism: Identify if there is a visible button or link that allows users to submit their application, often labeled as "Apply," "Submit," or similar.

If the web page contains all of these elements, then it is a job listing for a software engineering role. Your output should be "True" if the web page meets these criteria and "False" if it does not.

Output Format:
Your output should be a single word: "True" or "False."

REMEMBER, YOUR OUTPUT SHOULD ONLY EITHER "True" OR "False" AND NOTHING ELSE.
"""
