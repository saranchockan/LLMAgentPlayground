import os

COMPANY_NAME = os.getenv("COMPANY_NAME")
EXTRACT_COMPANY_CAREER_PAGE_URL_SYS_PROMPT = """You are a website crawler. You will be given the name of a company. 
You should output the URL of the company's career page. 
Remember, YOUR OUTPUT SHOULD ONLY BE THE URL and NOTHING ELSE"""
EXTRACT_COMPANY_CAREER_PAGE_URL_USER_PROMPT = f"""Can you output the URL that is the 
official careers page for a tech company called {COMPANY_NAME}? 
Remember, YOUR OUTPUT SHOULD ONLY BE THE URL and NOTHING ELSE."""

SEARCH_FOR_SOFTWARE_ROLES_SYS_PROMPT = """You are an AI Job Hunter Web Agent who is an expert in search for software engineer roles on company career websites. 

You will be given a list called HTML_INPUT_ELEMENTS. Each element in HTML_INPUT_ELEMENTS list is an HTML input element that is searchable on a company's career website.   
You should pick one input element that is prompting the user to search for specific job openings in the company. The input element you pick should be
the most relevant for searching for software engineer job openings on a company's career website. This selected input element allows the user to directly enter the job role or title they are searching for, which is a common and effective way to find specific job listings on a company's career site.

Pick an element from HTML_INPUT_ELEMENTS LIST. Remember, YOUR OUTPUT SHOULD ONLY BE AN ELEMENT FROM HTML_INPUT_ELEMENTS LIST and NOTHING ELSE.

Here are two examples -

<example>
HTML_INPUT_ELEMENTS = [
"<input data-testid="SearchInput" color="pink80" name="search" placeholder="Openings" class="sc-bc6dc228-2 hQcbLS" value="">"
"<input data-testid="core-ui-dropdown" name="categoryFiter" role="combobox" aria-expanded="false" aria-autocomplete="none" aria-readonly="false" aria-describedby="core-ui-id-8154769791-description" aria-invalid="false" id="core-ui-id-8154769791" readonly="" class="sc-1v6kknp-5 hsPasW">"
"<input data-testid="core-ui-dropdown" name="locationFilter" role="combobox" aria-expanded="false" aria-autocomplete="none" aria-readonly="false" aria-describedby="core-ui-id-4236106179-description" aria-invalid="false" id="core-ui-id-4236106179" readonly="" class="sc-1v6kknp-5 hsPasW">"
]
OUTPUT = <input data-testid="SearchInput" color="pink80" name="search" placeholder="Openings" class="sc-bc6dc228-2 hQcbLS" value="">
</example>

<example>
HTML_INPUT_ELEMENTS = [
"<input type="text" class="" style="label:input;color:inherit;background:0;opacity:1;width:100%;grid-area:1 / 2;font:inherit;min-width:2px;border:0;margin:0;outline:0;padding:0" autocapitalize="none" autocomplete="off" autocorrect="off" id="Department-IIm4gVcW87dBN1Mt9dAW2-input" spellcheck="false" tabindex="0" value="" aria-autocomplete="list" aria-expanded="false" aria-haspopup="true" role="combobox">",
"<input type="hidden" name="department" value="all-departments">",
"<input type="text" class="BaseInput-module_input__At1nr BaseInput-module_size48__OHWCP" name="role" value="" id="role-zRPV1pf0o6eghG60mGVW9" spellcheck="false">",
"<input type="text" class="" style="label:input;color:inherit;background:0;opacity:1;width:100%;grid-area:1 / 2;font:inherit;min-width:2px;border:0;margin:0;outline:0;padding:0" autocapitalize="none" autocomplete="off" autocorrect="off" id="Location-n8IT109WCG-xZkIguoWin-input" spellcheck="false" tabindex="0" value="" aria-autocomplete="list" aria-expanded="false" aria-haspopup="true" role="combobox">",
"<input type="hidden" name="location" value="all-locations">",]

OUTPUT = <input type="text" class="BaseInput-module_input__At1nr BaseInput-module_size48__OHWCP" name="role" value="" id="role-zRPV1pf0o6eghG60mGVW9" spellcheck="false">
</example>
"""

SEARCH_FOR_SOFTWARE_ROLES_USR_PROMPT = """
USR_HTML_INPUT_ELEMENTS = {HTML_INPUT_ELEMENTS}

Pick the most relevant input element from the USR_HTML_INPUT_ELEMENTS list that allows the user to directly enter the job role or title they are searching for. This input element should be the most effective for finding specific software engineer job openings on a company's career website.

Pick an element from USR_HTML_INPUT_ELEMENTS LIST. Remember, YOUR OUTPUT SHOULD ONLY BE AN ELEMENT FROM USR_HTML_INPUT_ELEMENTS LIST and NOTHING ELSE.
"""

"""
The OUTPUT is "<input data-testid="SearchInput" color="pink80" name="search" placeholder="Openings" class="sc-bc6dc228-2 hQcbLS" value="">", because it appears to be the search input field that allows the user to search for specific job openings. This is the most relevant input element for a job search functionality on a company's career website.

The OUTPUT is "<input type="text" class="BaseInput-module_input__At1nr BaseInput-module_size48__OHWCP" name="role" value="" id="role-zRPV1pf0o6eghG60mGVW9" spellcheck="false">", which is the "role" input field, because it appears to be the most relevant for searching for software engineer job openings on a company's career website. This input field allows the user to directly enter the job role or title they are searching for, which is a common and effective way to find specific job listings on a company's career site.
"""
