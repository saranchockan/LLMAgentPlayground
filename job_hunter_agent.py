"""

The core idea of agents is to use a language model to choose a sequence of actions to take. In chains, a sequence of actions is hardcoded (in code). In agents, a language model is used as a reasoning engine to determine which actions to take and in which order.

Reasoning -> Actions

Fact: I am currently on the company's career page. 


Reason: Is there a search input that can let me search for 
open software engineering roles?
Action: Search for "Software" in the search input. 


Regardless of whether you have searched for software roles 
or not...

Reason: I am on the careers page. Are there clickable elements (links, buttons) I can click that are related to software?
NOTE: There is more clickable elements than just links and buttons. 
Anthropic jobs page shows us that there can be <div> and <span>
that can be clickable


These reasoning and actions should end 
when you land a job application page. 

How do you determine that you are on a job listing/application
page? // https://chatgpt.com/c/0e4f0c4d-7bd8-4b7a-ae5a-6e21bcdd43f3 :) 



Store the job application/listing page in DB and then Job Applier Agent
will take care of the rest. 



"""
