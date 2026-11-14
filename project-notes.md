### Research Agent

---
#### Set up the project

##### Initialized the environment
``` bash
$ python -m venv .venv
```

##### Initialized via uv
``` bash
$ uv init
```

This created a "main.py" among other things.

##### Install what we need for the project
``` bash
$ uv add langchain langgraph langchain-deepseek python-dotenv
```

##### Create the .env file in the root dir
``` bash
$ touch .env
```

##### Add the BRIGHTDATA and DEEPSEEK keys envirionment variable
```
DEEPSEEK_API_KEY=[deepseek key here]
BRIGHTDATA_API_KEY=[brightdata key here]
```
---
#### Import the dependencies

In the ```main.py``` we're going to add some dependencies needed for the application to work. We need [load_env](https://github.com/theskumar/python-dotenv/blob/main/src/dotenv/main.py#L388) from [dotenv](https://pypi.org/project/python-dotenv/) to protect our environment variables. As well as the [langchain]() and [langgraph]() imports for the llm tools

<i>/main.py</i>
``` {.python .numberLines .lineAnchors}

# Import dependencies
from typing import Annotated, List
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict

# Import invironment variables
from dotenv import load_dotenv
load_dotenv()
```

#### Create the state and define the functions.

Next, we're going to define the llm and assign it. We're also going to write up the state that we're going to use in the graph. ```add_messages``` will modify the string for us.

<i>main.py</i>
```python {startFrom="10" .numberLines .lineAnchors}
...
load_dotenv()

# Defining the llm we're going to use here.
llm = init_chat_model("deepseek") 

# State for the data that the graph is going to use.
class State(TypedDict):
  messages: Annotated[list, add_messages]
  user_question: str | None
  google_results: str | None
  bing_results: str | None
  reddit_results: str | None
  selected_reddit_urls: list[str] | None
  reddit_post_data: list | None
  google_analysis: str | None
  bing_analysis: str | None
  reddit_analysis: str | None
  final_answer: str | None
```

Now we define the functions. They're going to be empty for now we're going to add the logic after we design the graph.

```python {startFrom="28" .numberLines .lineAnchors}
...
  final_answer: str | None

def google_search(state: State):
  return

def bing_search(state: State):
  return

def reddit_search(state: State):
  return

def analyze_reddit_posts(state: State):
  return

def retrieve_reddit_posts(state: State):
  return

def analyze_google_results(state: State):
  return

def analyze_bing_results(state: State):
  return

def analyze_reddit_results(state: State):
  return

def synthesize_analyses(state: State):
  return
```

#### Create the graph

This graph is going to compile into the workflow for the research agent. We use ```graph_builder``` and it's built in mehtods like so:

```python {startFrom="50" .numberLines .lineAnchors}
...
def synthesize_analyses(state: State):
  return

# Define the state graph with the State TypedDict
graph_builder = StateGraph(State) 

# Nodes for defining the steps in the graph
graph_builder.add_node("google_search", google_search)
graph_builder.add_node("bing_search", bing_search)
graph_builder.add_node("reddit_search", reddit_search)
graph_builder.add_node("analyze_reddit_posts", analyze_reddit_posts)
graph_builder.add_node("retrieve_reddit_posts", retrieve_reddit_posts)
graph_builder.add_node("analyze_google_results", analyze_google_results)
graph_builder.add_node("analyze_bing_results", analyze_bing_results)
graph_builder.add_node("analyze_reddit_results", analyze_reddit_results)
graph_builder.add_node("synthesize_analyses", synthesize_analyses)

# Edges for connecting the nodes
graph_builder.add_edge(START, "google_search")
graph_builder.add_edge(START, "bing_search")
graph_builder.add_edge(START, "reddit_search")

# Edges for connecting the search nodes to the analysis node
graph_builder.add_edge("google_search", "analyze_reddit_posts")
graph_builder.add_edge("bing_search", "analyze_reddit_posts")
graph_builder.add_edge("reddit_search", "analyze_reddit_posts")
graph_builder.add_edge("analyze_reddit_posts", "retrieve_reddit_posts")

# Edges for connecting the retrieval node to the analysis nodes
graph_builder.add_edge("retrieve_reddit_posts", "analyze_google_results")
graph_builder.add_edge("retrieve_reddit_posts", "analyze_bing_results")
graph_builder.add_edge("retrieve_reddit_posts", "analyze_reddit_results")

# Edges for connecting the analysis nodes to the synthesis node
graph_builder.add_edge("analyze_google_results", "synthesize_analyses")
graph_builder.add_edge("analyze_bing_results", "synthesize_analyses")
graph_builder.add_edge("analyze_reddit_results", "synthesize_analyses")

graph_builder.add_edge("synthesize_analyses", END)

# Compile the graph
graph = graph_builder.compile()

```
#### Execute agent for the graph

```python {startFrom="90" .numberLines .lineAnchors}
...
graph = graph_builder.compile()

# This chatbot will run the application
def run_chatbot():
	print("Multi-Source Research Agent")
	print("Type 'exit' to quit \n")

	while True:
		user_input = input("Ask me anything: ")
		if user_input.lower() == "exit":
			print("Bye")
			break

		state = {
			"messages": [{"role": "user", "content": user_input}],
      "user_question": user_input,
      "google_results": None,
			"bing_results": None,
      "reddit_results": None,
			"selected_reddit_urls": None,
      "reddit_post_data": None,
			"google_analysis": None,
			"bing_analysis": None,
			"reddit_analysis": None,
			"final_answer": None
		}

		print("\n Starting parallel research process...\n")
		print("This may take a few seconds depending on the complexity of your question.\n")

		final_state = graph.invoke(state)

		if final_state["final_answer"]:
			print(f"Final Answer: {final_state['final_answer']}\n")
		print("-" * 80)

if __name__ == "__main__":
  run_chatbot()

```

---
#### Add logic to the nodes

Here, we're going to scaffold the logic for the nodes and set up their retrun values before we test the application.

```python {startFrom="28" .numberLines .lineAnchors}
...
  final_answer: str | None

def google_search(state: State):
  user_question = state.get("user_question", "")
  print(f"Searching Google for: {user_question}")

  google_results = []
  return {"google_results": google_results}

def bing_search(state: State):
  user_question = state.get("user_question", "")
  print(f"Searching Bing for: {user_question}")

  bing_results = []
  return {"bing_results": bing_results}

def reddit_search(state: State):
  user_question = state.get("user_question", "")
  print(f"Searching Reddit for: {user_question}")

  reddit_results = []
  return {"reddit_results": reddit_results}

def analyze_reddit_posts(state: State):
  return {"selected_reddit_urls": []}

def retrieve_reddit_posts(state: State):
  return {"reddit_post_data": []}

def analyze_google_results(state: State):
  return {"google_analysis": ""}

def analyze_bing_results(state: State):
  return {"bing_analysis": ""}

def analysze_reddit_results(state: State):
  return {"reddit_analysis": ""}

def synthesize-analyses(state: State):
  return {"final_answer": ""}

# Define the state graph with the State TypedDict
graph_builder = StateGraph(State) 
...
```
Now we can test the application to make sure that there are no errors yet. We are ready to run the following script in the console:
``` bash
$ python main.py 
```
---

#### Setting up Brightdata
##### We're going to do the setup online first

At the [BrightData](https://brightdata.com/) website we can set up a free account. You can create an account with Google or Github.

Once your account is created you can select the SERP API service in the "API Web Access" section of the site. You can also copy your API key into your .env file. We're going to import it later.

![alt text](<Screenshot from 2026-08-29 18-41-57.png>)

Click the dropdown to find SERP API and click it
![alt text](<Screenshot from 2026-08-30 13-47-33.png>)

Choose the Google scraper and name it. 
![alt text](<Screenshot from 2026-08-30 13-50-18.png>)

Choose RAW HTML and click "Add API"
![alt text](<Screenshot from 2026-08-30 13-49-39.png>)

#### Back in the application we're going to add the functionality

##### Create a new file called "web_operations.py"

``` bash
$ touch web_operations.py
```

##### We configure web_operations to start testing the request

We add the imports for these operations and create the request.

<i>web_operations.py</i>
```python {startFrom="90" .numberLines .lineAnchors}
from dotenv import load_dotenv 
import os
from urllib.parse import quote_plus

def _make_api_request(url, **kwargs):
  api_key = os.getenv("BRIGHTDATA_API_KEY")

	headers = {
		"Authorization": f"Bearer {api_key}",
		"Content-Type": "application/json",
	}

	try:
		response = requests.post(url, headers=headers, ##kwargs)
		response.raise_for_status()
		return response.json()
	except reqeustion.exceptions.REquestException as e: # checks for issues related to the network request
		print(f"API request failed: {e}")

		return None
	except Exception as e:	# checks for issue not related to the network request
		print(f"Unkown error: {e}")
		return None

```

##### Next we're going to create the actual SERP function

We're going to use [DRY principles](https://www.geeksforgeeks.org/software-engineering/dont-repeat-yourselfdry-in-software-development/) to create the SERP function so that it can be used for the different sources Brightdata will be pulling from.

<i>web_operations.py</i>
```python {startFrom="90" .numberLines .lineAnchors}
...
  except Exception as e:	# checks for issue not related to the network request
    print(f"Unkown error: {e}")
    return None

# We're going to set the engine to google 
def serp_search(query, engine="google"): by default
  if engine == "google":
    base_url = "https://google.com/search"
  elif engine == "bing":
    base_url = "https://ww.bing.com/search"
  else:
    raise ValueError(f"Uknown engine {engine}")
  
	url = "https://api.brightdata.com/request"
	payload = {
		"zone": "ai_agent",
		"url": f"{base_url}?q={quote_plus(query)}&brd_json=1",
		"format": "raw"
	}

	full_response = _make_api_request(url, json=payload)
	if not full_response:
		return None

	return full_response

	extracted_data = {
		"knowledge": full_response.get("knowledge", {}),
		"organic": full_response.get("organic", []),
	}
	
	return extracted_data
```

##### Add it to main.py

We're going to import what we just did in "web_operations.py" like so:

<i>main.py</i>
```python {startFrom="90" .numberLines .lineAnchors}
...
from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict

+ from web_operations import search_serp

# Load environment variables
from dotenv import load_dotenv
load_dotenv()
...
```

```python {startFrom="90" .numberLines .lineAnchors}
...
	final_answer: str | None

def google_search(state: State):
	user_question = state.get("user_question", "")
	print(f"Searching Google for: {user_question}")

	- google_results = []
	+ google_results = serp_search(user_question, engine="google)
	+ print(google_results) # To see if the data is coming in or not.

	return {"google_results": google_results}


def bing_search(state: State):
	user_question = state.get("user_question", "")
	print(f"Searching Bing for: {user_question}")

	- bing_results = []
	+ bing_results = serp_search(user_question, engine="bing")
	+ print(bing_results)

	return {"bing_results": bing_results}
...
```

##### Time to test!
Great! Now we can run the application again to see whether or not we get a response!

``` bash
$ python main.py 
```

This will prompt you to input a query. When this happens you should input something like "invest in Microsoft" or something along those lines. 

You'll get a response like this (but less pretty)

``` json
{
  "knowledge": {},
  "organic": [
    {
      "link": "https://www.microsoft.com/en-us/investor/investor-information",
      "source": "Microsoft",
      "display_link": "https://www.microsoft.com › en-us › investor › investor-...",
      "title": "Information for Investors",
      "description": "Microsoft's transfer agent, administers a direct stock purchase plan and a dividend reinvestment plan for the company. at (800) 285-7772,",
      "snippet_highlighted_words": [
        "Microsoft's"
      ],
      "icon": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAAABnRSTlMAAAAAAABupgeRAAAAWklEQVR4AWP4FKBEJPrip8wABrV7GOp3EYtGhgWjFoxaMGrBqAXf/OSIRD995CEWVO9hqN1FLBoOYNlnotF3iI7/O4lHQOVL3hONPo9agB2NWjBqwagFoxYAAB2zMZ7bQW2tAAAAAElFTkSuQmCC",
      "rank": 1,
      "global_rank": 1
    },
    {
      "link": "https://www.trading212.com/trading-instruments/invest/MSFT.US",
      "source": "Trading 212",
      "display_link": "https://www.trading212.com › trading-instruments › M...",
      "title": "MSFT Stock - Invest in Microsoft, NASDAQ",
      "description": "View real-time MSFT price charts. .96 Day's range $ 517 . Commission-free investing for everyone",
      "snippet_highlighted_words": [
        "MSFT price charts"
      ],
      "icon": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAMAAABF0y+mAAAAKlBMVEVHcEwAAAAAAAAAAAAAp+EAAAAArusAq+YAHykAbJEAhrUAn9YAU3AAOU2n486VAAAABHRSTlMA9uCR26w5xgAAAKdJREFUKJF9k9kSgCAIRckNt/7/dwspxfU+NAMnsIsEAFpddtKlNLxakI+/dTtmrQa1h2rflfqKwBeJhIDeFfkljGhIcQmZGVzB8MOwgKZqhhl/5vIEE+UTP0eYXTmuHIx5gMUH8idj7OHtPovlJXd3kHOexiRKGYoU9/cChtbsdm0Q0CaXhCdskAtzZ6pCQ1dVrSeKTIXDJdfwvCbHBTuu5nGpT7/DA7U+D7aZJj+1AAAAAElFTkSuQmCC",
      "rank": 2,
      "global_rank": 6
    }
    ...
  ]
}
```

You can delete those print statements now that we know it's working
``` python
def google_search(state: State):
	user_question = state.get("user_question", "")
	print(f"Searching Google for: {user_question}")

	google_results = serp_search(user_question, engine="google)
	- print(google_results) # To see if the data is coming in or not.

	return {"google_results": google_results}


def bing_search(state: State):
	user_question = state.get("user_question", "")
	print(f"Searching Bing for: {user_question}")

	bing_results = serp_search(user_question, engine="bing")
	- print(bing_results)

	return {"bing_results": bing_results}
```

##### Now it's time to implement the Reddit Search

We're going to go to the Scraper secion of Brightdata and click "New" then click "Brows scrapers marketplace". 

![alt text](<Screenshot from 2026-08-31 12-40-46.png>)

Next we're going to search for reddit using the searchbar and click on the "reddit.com" domain card.

![alt text](<Screenshot from 2026-08-31 12-52-18.png>)

And we're going to select the "Discover by keyword" option. And we'er going to click "Run Manually" so we can retrieve a dataset_id that we're going to use for development.

<i>Bright Data likes to change things around for no reason I had to get my dataset_id from downloading a snapshot. Good luck everybody else!</i>

![alt text](<Screenshot from 2026-08-31 12-53-40.png>)

##### Now for the reddit part

We're going to start by scaffolding the reddit_search function. We're also going to build a function that allows us to retrieve the reddit info from Bright Data.

<i>web_operations.py</i>
```python {startFrom="90" .numberLines .lineAnchors}

...
	return extracted_data

def reddit_search_API(keyword, date="All time", sort_by="Hot", num_of_posts=75):
	trigger_url = "https://api.brightdata.com/datasets/v3/trigger"

	params = {
		"dataset_id": """[dataset_id that we retrieved from Bright Data here]""",
		"include_errors": "true",
		"type": "discover_new",
		"discover_by": "keyword"
	}

	data = [
		{
			"keyword": keyword,
			"date": date,
			"sort_by": sort_by,
			"num_of_posts": num_of_post
		}
	]
	
	raw_data = None

	if not raw_data:
		return None
```

We're going to create the snapshot fetcher for the reddit search_function

```python {startFrom="90" .numberLines .lineAnchors}
...
	return extracted_data

def _trigger_and_download_snapshot(trigger_url, params, data, operation_name="operation"):
	trigger_result = _make_api_request(trigger_url, params=params, json=data)
	if not trigger_result:
		return None
	
	snapshot_id = trigger_result.get("snapshot_id")
	if not snapshot_id:
		return None

def reddit_search_API(keyword, date="All time", sort_by="Hot", num_of_posts=75):
...
```
Because this file would get too bloated if we were to do everything here we're going to create a new file just for the snapshot operations:
```bash
$ touch snapshot_operations.py
```
We're going to past all of this into 
<i>snapshot_operations.py</i>
```python {startFrom="1" .numberLines .lineAnchors}
import os
import time
import requests
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional

load_dotenv()


def poll_snapshot_status(
    snapshot_id: str, max_attempts: int = 60, delay: int = 5
) -> bool:
    api_key = os.getenv("BRIGHTDATA_API_KEY")
    progress_url = f"https://api.brightdata.com/datasets/v3/progress/{snapshot_id}"
    headers = {"Authorization": f"Bearer {api_key}"}

    for attempt in range(max_attempts):
        try:
            print(
                f"⏳ Checking snapshot progress... (attempt {attempt + 1}/{max_attempts})"
            )

            response = requests.get(progress_url, headers=headers)
            response.raise_for_status()

            progress_data = response.json()
            status = progress_data.get("status")

            if status == "ready":
                print("✅ Snapshot completed!")
                return True
            elif status == "failed":
                print("❌ Snapshot failed")
                return False
            elif status == "running":
                print("🔄 Still processing...")
                time.sleep(delay)
            else:
                print(f"❓ Unknown status: {status}")
                time.sleep(delay)

        except Exception as e:
            print(f"⚠️ Error checking progress: {e}")
            time.sleep(delay)

    print("⏰ Timeout waiting for snapshot completion")
    return False


def download_snapshot(
    snapshot_id: str, format: str = "json"
) -> Optional[List[Dict[Any, Any]]]:
    api_key = os.getenv("BRIGHTDATA_API_KEY")
    download_url = (
        f"https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}?format={format}"
    )
    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        print("📥 Downloading snapshot data...")

        response = requests.get(download_url, headers=headers)
        response.raise_for_status()

        data = response.json()
        print(
            f"🎉 Successfully downloaded {len(data) if isinstance(data, list) else 1} items"
        )

        return data

    except Exception as e:
        print(f"❌ Error downloading snapshot: {e}")
        return None
```

We're going to import all of that into "web_operations.py" to be used by the snapshot downloader function.

<i>web_operations.py</i>
```python
...
load_dotenv()

+ from snapshot_opersations import download_snapshot, poll_snapshot_status

import requests
...

...
	return None

# Poll the snapshot status until it's ready or failed
+ if not poll_snapshot_status(snapshot_id):
+	  return None

+ raw_data = download_snapshot(snapshot_id):

return raw_data
...

...
			"num_of_posts": num_of_posts
		}
	]
	
	# We're getting the raw data now so we can assign it
	- raw_data = None
	+ raw_data = _trigger_and_download_snapshot(
	+	trigger_url, params, data, operation_name="reddit"
	+ )


	if not raw_data:
		return None

	# We're going to parse the data
	+ parsed_data = []

	+ for post in _data:
	+	parsed_post = {
	+		"title": post.get("title),
	+		"url": post.get("url"),
	+	}
	+	parsed_data.append(parsed_post)

	+ return parsed_data

```

That was was a lot. However, now if we try to trigger reddit_search it will collect a lot of reddit posts. Time to test

<i>main.py</i>
``` 	return {"bing_results": bing_results}


def reddit_search(state: State):
	user_question = state.get("user_question", "")
	print(f"Searching Reddit for: {user_question}")

	- reddit_results = []
	+ reddit_results = reddit_search_API()
	+ print(reddit_results)
	
	return {"reddit_results": reddit_results}


def analyze_reddit_posts(state: State):

``` 
Let's run it:
``` bash
$ python main.py
```
It will ask a for a question. Give it a prompt:
``` bash
Ask me anything: + Should I buy Intel stock?
```

You should start getting reddit results. Keep in mind when you run these prompts they have to have some relevance to the subject matter defined in the scraper on Bright Data's platform otherwise you will get "None" as a result and <b>it won't be your code causing the problem</b>.

We're about to start needing the data to be more organized a so we're going to rewrite the way we are returning ```parsed_data```

<i>web_operations.py</i>
``` python
...
		parsed_data.append(parsed_post)

	- return parsed_data
	+ return {"parsed_posts": parsed_data, "total_found": len(parsed_data)"}
```
---
##### Now to get the comments

We need to generate them using the scraper using the "Reddit - Comments -> Collect by URL" feature on Bright Data. When the scraper is done we can get a dataset_id. I had to get mine by clicking "Download logs" at the top of the table and extracting it from a JSON.

![alt text](<Screenshot from 2026-09-03 12-20-51.png>)

While that's running we're going to start with a new function called ```reddit_post_retrieval```

<i>web_operations.py</i>
``` python
...
	return {"parsed_data": parsed_data, "total_found": len(parsed_data)}

def reddit_post_retrieval(urls, days_back=10, load_all_replies=False, comment_limit=100):
	dataset_id = 'gd_lvzdpsdlw09j6t702'
	if not urls:
		return None

		trigger_url = "https://api.brightdata.com/datasets/v3/trigger"

	params = {
		"dataset_id": dataset_id,
		"include_errors": "true",
	}

	data = [
		{
			"url": url,
			"days_back": days_back,
			"load_all_replies": load_all_replies,
			"comment_limit": comment_limit
		}
		for url in urls
	]
			
	raw_data = _trigger_and_download_snapshot(
		trigger_url, params, data, operation_name="reddit comments"
	)
	if not raw_data:
		return None

	parsed_comments = []

	for comment in raw_data:
		parsed_comment = {
			"comment_id": comment.get("comment_id"),
			"content": comment.get("comment"),
			"date": comment.get("date_posted")
		}
		parsed_comments.append(parsed_comment)

	return {"comments": parsed_comments, "total_retrieved": len(parsed_comments)}
```

We've scaffolded the reddit_post_retrieval function but before we continue we're going to create a prompts file in the root dir that we are going to need soon.

```bash
$ touch prompts.py
```

In side we're just going to paste all of this. It's a bunch of pre-tested prompts and with static methods built in too. It contains the ```reddit_url_analysis_system``` that we are about to use. 

<i>prompts.py</i>
```python
from typing import Dict, Any


class PromptTemplates:
    """Container for all prompt templates used in the research assistant."""

    @staticmethod
    def reddit_url_analysis_system() -> str:
        """System prompt for analyzing Reddit URLs."""
        return """You are an expert at analyzing social media content. Your task is to examine Reddit search results and identify the most relevant posts that would provide valuable additional information for answering the user's question.

Analyze the provided Reddit results and identify URLs of posts that contain valuable information worth investigating further. Focus on posts that:
- Directly relate to the user's question
- Contain detailed discussions or expert opinions
- Have high engagement (upvotes/comments)
- Provide unique perspectives or insights

Return a structured response with the selected URLs."""

    @staticmethod
    def reddit_url_analysis_user(user_question: str, reddit_results: str) -> str:
        """User prompt for analyzing Reddit URLs."""
        return f"""User Question: {user_question}

Reddit Results: {reddit_results}

Please analyze these Reddit results and identify the most valuable posts for answering the user's question."""

    @staticmethod
    def google_analysis_system() -> str:
        """System prompt for analyzing Google search results."""
        return """You are an expert research analyst. Analyze the provided Google search results to extract key insights that answer the user's question.

Focus on:
- Main factual information and authoritative sources
- Official websites, documentation, and reliable sources
- Key statistics, dates, and verified information
- Any conflicting information from different sources

Provide a concise analysis highlighting the most relevant findings."""

    @staticmethod
    def google_analysis_user(user_question: str, google_results: str) -> str:
        """User prompt for analyzing Google search results."""
        return f"""Question: {user_question}

Google Search Results: {google_results}

Please analyze these Google results and extract the key insights that help answer the question."""

    @staticmethod
    def bing_analysis_system() -> str:
        """System prompt for analyzing Bing search results."""
        return """You are an expert research analyst. Analyze the provided Bing search results to extract complementary insights that answer the user's question.

Focus on:
- Additional perspectives not covered in other sources
- Technical details and documentation
- News articles and recent developments
- Microsoft ecosystem and enterprise perspectives

Provide a concise analysis highlighting unique findings and perspectives."""

    @staticmethod
    def bing_analysis_user(user_question: str, bing_results: str) -> str:
        """User prompt for analyzing Bing search results."""
        return f"""Question: {user_question}

Bing Search Results: {bing_results}

Please analyze these Bing results and extract insights that complement other search sources."""

    @staticmethod
    def reddit_analysis_system() -> str:
        """System prompt for analyzing Reddit discussions."""
        return """You are an expert at analyzing social media discussions. Analyze the provided Reddit content to extract community insights and user experiences.

Focus on:
- Real user experiences and testimonials
- Community consensus and popular opinions
- Practical tips and advice from users
- Different perspectives and debates
- Specific quotes from posts and comments (use quotation marks)

IMPORTANT: When referencing specific content, directly quote it and mention the subreddit or context.
Highlight both positive and negative experiences, controversies, and varying opinions."""

    @staticmethod
    def reddit_analysis_user(
        user_question: str, reddit_results: str, reddit_post_data: list
    ) -> str:
        """User prompt for analyzing Reddit discussions."""
        return f"""Question: {user_question}

Reddit Search Results: {reddit_results}

Detailed Reddit Post Data: {reddit_post_data}

Please analyze this Reddit content and extract community insights, user experiences, and relevant discussions."""

    @staticmethod
    def synthesis_system() -> str:
        """System prompt for synthesizing all analyses."""
        return """You are an expert research synthesizer. Combine the provided analyses from different sources to create a comprehensive, well-structured answer.

Your task:
- Synthesize insights from Google, Bing, and Reddit analyses
- Identify common themes and conflicting information
- Present a balanced view incorporating different perspectives
- Structure the response logically with clear sections
- Cite the source type (Google, Bing, Reddit) for key claims
- Highlight any contradictions or uncertainties

Create a comprehensive answer that addresses the user's question from multiple angles."""

    @staticmethod
    def synthesis_user(
        user_question: str,
        google_analysis: str,
        bing_analysis: str,
        reddit_analysis: str,
    ) -> str:
        """User prompt for synthesizing all analyses."""
        return f"""Question: {user_question}

Google Analysis: {google_analysis}

Bing Analysis: {bing_analysis}

Reddit Community Analysis: {reddit_analysis}

Please synthesize these analyses into a comprehensive answer that addresses the question from multiple perspectives."""


def create_message_pair(system_prompt: str, user_prompt: str) -> list[Dict[str, Any]]:
    """
    Create a standardized message pair for LLM interactions.

    Args:
        system_prompt: The system message content
        user_prompt: The user message content

    Returns:
        List containing system and user message dictionaries
    """
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


# Convenience functions for creating complete message arrays
def get_reddit_url_analysis_messages(
    user_question: str, reddit_results: str
) -> list[Dict[str, Any]]:
    """Get messages for Reddit URL analysis."""
    return create_message_pair(
        PromptTemplates.reddit_url_analysis_system(),
        PromptTemplates.reddit_url_analysis_user(user_question, reddit_results),
    )


def get_google_analysis_messages(
    user_question: str, google_results: str
) -> list[Dict[str, Any]]:
    """Get messages for Google results analysis."""
    return create_message_pair(
        PromptTemplates.google_analysis_system(),
        PromptTemplates.google_analysis_user(user_question, google_results),
    )


def get_bing_analysis_messages(
    user_question: str, bing_results: str
) -> list[Dict[str, Any]]:
    """Get messages for Bing results analysis."""
    return create_message_pair(
        PromptTemplates.bing_analysis_system(),
        PromptTemplates.bing_analysis_user(user_question, bing_results),
    )


def get_reddit_analysis_messages(
    user_question: str, reddit_results: str, reddit_post_data: list
) -> list[Dict[str, Any]]:
    """Get messages for Reddit discussions analysis."""
    return create_message_pair(
        PromptTemplates.reddit_analysis_system(),
        PromptTemplates.reddit_analysis_user(
            user_question, reddit_results, reddit_post_data
        ),
    )


def get_synthesis_messages(
    user_question: str, google_analysis: str, bing_analysis: str, reddit_analysis: str
) -> list[Dict[str, Any]]:
    """Get messages for final synthesis."""
    return create_message_pair(
        PromptTemplates.synthesis_system(),
        PromptTemplates.synthesis_user(
            user_question, google_analysis, bing_analysis, reddit_analysis
        ),
    )
```

Let's go ahead and import these into main.py

<i>main.py</i>
```python
...
from typing_extensions import TypedDict

+ from prompts import (
+	get_reddit_url_analysis_messages,
+	get_google_analysis_messages,
+	get_bing_analysis_messages,
+	get_reddit_analysis_messages,
+	get_synthesis_messages
+ )

# Load environment variables
from dotenv import load_dotenv
...

...

# Useful formatter for the reddit posts
	final_answer: str | None

+ class RedditURLAnalysis(BaseModel):
+		selected_urls: List[str] = Field(description="List of RedditURLs that contain valuable information for answering the user's question ")

def google_search(state: State):
...
... 
	return {"reddit_results": reddit_results}


def analyze_reddit_posts(state: State):
+ 	user_question = state.get("user_question", "")
+ 	reddit_results = state.get("reddit_results", "")

+ 	if not reddit_results:
+		return {"reddit_results": reddit_results} 

+		structured_llm = llm(with_structured_output())
+		messages = get_reddit_analysis_messages(user_question, reddit_results)
+	try:
+ 		analysis = structure_llm.invoke(messages)
+ 		selected_urls = analysis.selected_urls

+			print("Selected URLs:")
+			for i, url in enumarate(selected_urls, 1):
+				print(f" {i}. {url}")

+ 	except Exception as e:
+			print(e)
+			selected_urls = []
return {"selected_reddit_urls": []}

def retrieve_reddit_posts(state: State):

```

Let's test this
``` bash
$ python main.py
```

Run a query (with subject matter relevant to the scraper) to see some results and you'll see an ouptut that looks something like this:

``` bash
Selected URLs:
1. https://www.reddit.com/r/datascience/comments/1w4c38i/at_senior_levels_where_do_you_draw_the_line/
2. https://www.reddit.com/r/datascience/comments/1w3klb5/anyone_whos_never_worked_at_faang_or_big_tech_do/
3. https://www.reddit.com/r/datascience/comments/1w67e3p/how_are_llms_used_in_predictive_modeling_and/
4. https://www.reddit.com/r/datascience/comments/1w7c6t7/costoptimal_design_under_heterogeneous_treatment/
5. https://www.reddit.com/r/datascience/comments/1w3n6p7/thoughts_on_ds_at_mckinseybainbcg/
6. https://www.reddit.com/r/datascience/comments/1vx8ltd/feeling_frustrated_as_a_junior_who_has_never/
7. https://www.reddit.com/r/datascience/comments/1vtnzfr/help_point_me_in_the_right_direction_how_to/
8. https://www.reddit.com/r/datascience/comments/1vnh7w2/how_widely_is_r_still_used_in_industry_today/
9. https://www.reddit.com/r/datascience/comments/1vlzpvt/laid_off_after_45_yrs_at_the_company_as_sr_data/
10. https://www.reddit.com/r/datascience/comments/1vobzd9/what_hugging_face_learned_from_reproducing_2200/
11. https://www.reddit.com/r/datascience/comments/1vmbfw4/data_science_in_manufacturing_vs_itconsulting/
12. https://www.reddit.com/r/datascience/comments/1vhci9u/how_do_you_design_a_forecasting_system/
13. https://www.reddit.com/r/datascience/comments/1ve1ddf/reflections_on_airbnb/
14. https://www.reddit.com/r/datascience/comments/1vfshsd/stakeholders_want_high_level_then_ask_detailed/
15. https://www.reddit.com/r/datascience/comments/1vehgl9/should_you_worry_about_staying_at_one_job_for/
--------------------------------------------------------------------------------
```

Now lets write the function that retrieves the comments and passes them to the LLM. We've got the function for it but now we're going to add it to main.py

<i>main.py</i>
```python
...
from dotenv import load_dotenv

- from web_operations import serp_search, reddit_search_API
+ from web_operations import serp_search, reddit_search_API, reddit_post_retrieval
load_dotenv()

...
...
		selcected_urls = []

def retrieve_reddit_posts(state: State):
+ 	print("Getting redditpost comments")
+ 	selected_urls = state.get("selected_reddit_urls", [])

+ 	if not selected_urls:
+		return {"reddit_post_data": []}
+ 	print(f"Processing {len(selected_urls)} Reddit URLs)
+ 	reddit_post_data = reddit_post_retrieval(selected_urls)
+ 	if reddit_post_data:
+		print(f"Successfully got {len(reddit_post_data)} posts")
+	else:
+		print("Failed to get post data")
+		reddit_post_data = []
-	return {"reddit_post_data": []}
+ 	return {"reddit_post_data": reddit_post_data}
+	print(reddit_post_data)

def analyze_google_results(state: State):
```

Great let's test what we did
``` bash
$ python main.py
```

Feed it a topic related to what the scraper would have looked for:
``` bash
$ Ask me anything: datascience
```

It will output data after checking for the reddit posts

##### Next let's write the functions for the other methods (google and bing analytics)

For the most part we are going to import the methods from ```prompts.py``` so that these functions will work. For ```analyze_google_results```, ```analyze_bing_results``` we're pretty much going to get prompt-based responses.

After that we're going to combine everything in ```synthesize_analyses```

<i>main.py</i>
``` python
...
	return {"reddit_post_data": reddit_post_data}

def analyze_google_results(state: State):
+	print("Analyzing google results")

+	user_question = state.get("user_question", "")
+	google_results = state.get("google_results", "")

+	messages = get_google_analysis_messages(user_question, google_results)
+	resply = llm.invoke(messages)

-	return {"google_analysis": ""}
+	return {"google_analysis": reply.content}

def analyze_bing_results(state: State):
+	print("Analyzing bing results")

+	user_question = state.get("user_question", "")
+	google_results = state.get("bing_results", "")

+	messages = get_bing_analysis_messages(user_question, bing_results)
+	resply = llm.invoke(messages)

-	return {"bing_analysis": ""}
+	return {"bing_analysis": reply.content}

def analyze_reddit_results(state: State):
+	print("Analyzing reddit search results")

+	user_question = state.get("user_question", "")
+	reddit_results = state.get("reddit_results", "")
+	reddit_post_data = state.get("reddit_post_data", "")

+	messages = get_reddit_analysis_messages(user_question, reddit_results, reddit_post_data)
+	resply = llm.invoke(messages)

-	return {"reddit_analysis": ""}
+	return {"reddit_analysis": reply.content}

def synthesize_analyses(state: State):
+	print("Combine all results together")

+	user_question = state.get("user_question")
+	google_analysis = state.get("google_analysis, "")
+	bing_analysis = state.get("bing_analysis", "")
+	reddit_analysis = state.get("reddit_analysis", "")

+	messages = get_syhtesis_messages(
+		user_question, google_analysis, bing_analysis, reddit_analysis
+	)

+	reply = llm.invokoe(messages)	# pass all of this to the llm
+	final_answer = reply.content

-	return {"final_answer": ""}

	#The langflow "messagees" format is needed because it is opinionated and needs it to operate properly
+	return {"final_answer": final_answer, "messages": [{"role": "assistant", "content": final_answer}]}

graph_builder = StateGraph(State) 
...
```

##### Final Result

When we log everything to the console and run a test again you'll get a result that looks something like this.

``` bash
Final Answer:
# Latest on Data Science: A Synthesis

## Overview

The search evidence is uneven. **Google returned no usable results**, **Reddit was largely off-topic**, and **Bing provided two substantive sources**—Springer (academic) and Towards Data Science (practitioner). As a result, “the latest” cannot be reduced to a single breaking event. However, several useful signals emerge when the sources are read together.

---

## 1. Academic / Research Pulse (Bing: Springer)

Springer’s data science hub was refreshed within the **past 2 days**, indicating that peer-reviewed data science research remains highly active. Key takeaways:

- **Data science is treated as a formal academic subject**, not just a job title—this has implications for curricula, funding, and credentialing.
- The hub features **stories and opinions from top researchers**, giving a window into who is shaping the field academically.
- This is the **slow, validated layer** of knowledge: peer-reviewed discoveries, reproducible methods, and citable findings.

> *Source type: Bing search result (Springer, academic publisher)*

## 2. Practitioner / Industry Pulse (Bing: Towards Data Science)

Towards Data Science (TDS) explicitly covers **four adjacent domains**: data science, data analytics, data engineering, and machine learning. This signals that the field’s boundaries have blurred—**data science is now an umbrella term** for a broader technical stack.

- TDS provides **applied, tutorial-driven content**, covering new tools and techniques (e.g., LLM frameworks, vector databases, AI agents) before formal literature exists.
- Its content reflects what practitioners **actually care about**, filtered by readership engagement rather than peer review.
- This is the **fast layer**: tool adoption, practical techniques, and career-relevant skills.

> *Source type: Bing search result (Towards Data Science, practitioner publication)*

## 3. Community / Job Market Signals (Reddit)

Reddit results were mostly irrelevant, but two marginally relevant items appeared:

- A **Daily AI & Data News Summary** on `r/DecodingDataSciAI`—unfortunately, only the title was retrieved, with no post body or comments.
- A **Data Scientist II – Decision Science – PlayStation** job listing in `r/sports_jobs`, suggesting ongoing demand for decision science roles in the gaming industry.

No meaningful community discussion, debates, or sentiment about data science could be extracted. The only comment across all results was a single word (“Fabulous”) with no context.

> *Source type: Reddit search results*

---

## Key Themes Across Sources

| Theme | Evidence |
|-------|----------|
| **Two speeds of knowledge** | Fast practitioner layer (TDS) vs. slow academic layer (Springer). Organizations should monitor both—fast tells you what’s being *tried*; slow tells you what’s been *proven*. |
| **Blurred boundaries** | TDS now covers analytics, engineering, and ML alongside data science—the field is becoming an integrated technical stack. |
| **Formalization as a discipline** | Springer treats data science as a formal academic subject, indicating institutional recognition and growth. |
| **Continued hiring demand** | The PlayStation job listing hints at industry demand, especially in decision science. |

---

## Gaps, Contradictions, and Uncertainties

- **No Google results**: This is a major gap. No official documentation, news, or additional authoritative sources could be triangulated.
- **No enterprise or industry-analyst perspective**: Sources like Microsoft Research, Gartner, Forrester, or Azure ML were absent, so enterprise adoption and vendor-specific developments are not covered.
- **No breaking news**: Neither Springer nor TDS is a traditional news outlet, so funding rounds, product launches, or regulatory actions were not captured.
- **No real community voice**: Reddit search did not reach core communities like `r/datascience`, `r/MachineLearning`, or `r/dataengineering`, so no practitioner debates or career insights were available.
- **No direct contradictions** between Springer and TDS—they are complementary rather than conflicting. The main uncertainty is what was missed due to search gaps.

---

## Recommendations for a Fuller Picture

To get a more complete view of the latest in data science:

- **Academic/validated advances**: Springer, arXiv.org, peer-reviewed journals.
- **Applied/fast-moving techniques**: Towards Data Science, KDnuggets, Google AI Blog, OpenAI Blog.
- **Community and career discussions**: `r/datascience`, `r/MachineLearning`, `r/dataengineering`, `r/artificial`.
- **Enterprise and vendor news**: Microsoft Research, Azure ML blog, Gartner/Forrester reports.
- **Better search terms**: Use quotes (“data science”), year-specific queries (“data science news 2026”), or filter by specific subreddits.

---

## Bottom Line

The latest on data science is best characterized by **ongoing activity rather than one headline event**: active academic publishing, blurred boundaries across analytics/engineering/ML, fast-moving practitioner tooling, and continued industry hiring. However, because Google returned no results and Reddit was largely off-topic, this synthesis is **partial** and should be supplemented with targeted searches before drawing firm conclusions about any single “latest” development.
Final Answer: # Latest on Data Science: A Synthesis

## Overview

The search evidence is uneven. **Google returned no usable results**, **Reddit was largely off-topic**, and **Bing provided two substantive sources**—Springer (academic) and Towards Data Science (practitioner). As a result, “the latest” cannot be reduced to a single breaking event. However, several useful signals emerge when the sources are read together.

---

## 1. Academic / Research Pulse (Bing: Springer)

Springer’s data science hub was refreshed within the **past 2 days**, indicating that peer-reviewed data science research remains highly active. Key takeaways:

- **Data science is treated as a formal academic subject**, not just a job title—this has implications for curricula, funding, and credentialing.
- The hub features **stories and opinions from top researchers**, giving a window into who is shaping the field academically.
- This is the **slow, validated layer** of knowledge: peer-reviewed discoveries, reproducible methods, and citable findings.

> *Source type: Bing search result (Springer, academic publisher)*

## 2. Practitioner / Industry Pulse (Bing: Towards Data Science)

Towards Data Science (TDS) explicitly covers **four adjacent domains**: data science, data analytics, data engineering, and machine learning. This signals that the field’s boundaries have blurred—**data science is now an umbrella term** for a broader technical stack.

- TDS provides **applied, tutorial-driven content**, covering new tools and techniques (e.g., LLM frameworks, vector databases, AI agents) before formal literature exists.
- Its content reflects what practitioners **actually care about**, filtered by readership engagement rather than peer review.
- This is the **fast layer**: tool adoption, practical techniques, and career-relevant skills.

> *Source type: Bing search result (Towards Data Science, practitioner publication)*

## 3. Community / Job Market Signals (Reddit)

Reddit results were mostly irrelevant, but two marginally relevant items appeared:

- A **Daily AI & Data News Summary** on `r/DecodingDataSciAI`—unfortunately, only the title was retrieved, with no post body or comments.
- A **Data Scientist II – Decision Science – PlayStation** job listing in `r/sports_jobs`, suggesting ongoing demand for decision science roles in the gaming industry.

No meaningful community discussion, debates, or sentiment about data science could be extracted. The only comment across all results was a single word (“Fabulous”) with no context.

> *Source type: Reddit search results*

---

## Key Themes Across Sources

| Theme | Evidence |
|-------|----------|
| **Two speeds of knowledge** | Fast practitioner layer (TDS) vs. slow academic layer (Springer). Organizations should monitor both—fast tells you what’s being *tried*; slow tells you what’s been *proven*. |
| **Blurred boundaries** | TDS now covers analytics, engineering, and ML alongside data science—the field is becoming an integrated technical stack. |
| **Formalization as a discipline** | Springer treats data science as a formal academic subject, indicating institutional recognition and growth. |
| **Continued hiring demand** | The PlayStation job listing hints at industry demand, especially in decision science. |

---

## Gaps, Contradictions, and Uncertainties

- **No Google results**: This is a major gap. No official documentation, news, or additional authoritative sources could be triangulated.
- **No enterprise or industry-analyst perspective**: Sources like Microsoft Research, Gartner, Forrester, or Azure ML were absent, so enterprise adoption and vendor-specific developments are not covered.
- **No breaking news**: Neither Springer nor TDS is a traditional news outlet, so funding rounds, product launches, or regulatory actions were not captured.
- **No real community voice**: Reddit search did not reach core communities like `r/datascience`, `r/MachineLearning`, or `r/dataengineering`, so no practitioner debates or career insights were available.
- **No direct contradictions** between Springer and TDS—they are complementary rather than conflicting. The main uncertainty is what was missed due to search gaps.

---

## Recommendations for a Fuller Picture

To get a more complete view of the latest in data science:

- **Academic/validated advances**: Springer, arXiv.org, peer-reviewed journals.
- **Applied/fast-moving techniques**: Towards Data Science, KDnuggets, Google AI Blog, OpenAI Blog.
- **Community and career discussions**: `r/datascience`, `r/MachineLearning`, `r/dataengineering`, `r/artificial`.
- **Enterprise and vendor news**: Microsoft Research, Azure ML blog, Gartner/Forrester reports.
- **Better search terms**: Use quotes (“data science”), year-specific queries (“data science news 2026”), or filter by specific subreddits.

---

## Bottom Line

The latest on data science is best characterized by **ongoing activity rather than one headline event**: active academic publishing, blurred boundaries across analytics/engineering/ML, fast-moving practitioner tooling, and continued industry hiring. However, because Google returned no results and Reddit was largely off-topic, this synthesis is **partial** and should be supplemented with targeted searches before drawing firm conclusions about any single “latest” development.

--------------------------------------------------------------------------------
```