# Import necessary modules
from typing import Annotated, List
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict

from prompts import (
	get_reddit_url_analysis_messages,
	get_google_analysis_messages,
	get_bing_analysis_messages,
	get_reddit_analysis_messages,
	get_synthesis_messages,
)

# Load environment variables
from dotenv import load_dotenv

from web_operations import serp_search, reddit_search_API, reddit_post_retrieval
load_dotenv()

llm = init_chat_model("deepseek:deepseek-v4-pro")

# Thinking mode rejects the pinned tool_choice that with_structured_output sends,
# and it is on by default, so structured extraction runs with thinking disabled.
structured_llm_model = init_chat_model(
	"deepseek:deepseek-v4-flash",
	extra_body={"thinking": {"type": "disabled"}},
)

class State(TypedDict):
	"""State of the agent."""
	messages: Annotated[list, add_messages]
	user_question: str | None
	google_results: list | None
	bing_results: list | None
	reddit_results: list | None
	selected_reddit_urls: list | None
	reddit_post_data: list | None
	google_analysis: str | None
	bing_analysis: str | None
	reddit_analysis: str | None
	final_answer: str | None

class RedditURLAnalysis(BaseModel):
	selected_urls: List[str] = Field(..., description="List of selected Reddit URLs for analysis.")

def google_search(state: State):
	user_question = state.get("user_question", "")
	print(f"Searching Google for: {user_question}")

	google_results = serp_search(user_question, engine="google")

	return {"google_results": google_results}


def bing_search(state: State):
	user_question = state.get("user_question", "")
	print(f"Searching Bing for: {user_question}")

	bing_results = serp_search(user_question, engine="bing")

	return {"bing_results": bing_results}


def reddit_search(state: State):
	user_question = state.get("user_question", "")
	print(f"Searching Reddit for: {user_question}")

	reddit_results = reddit_search_API(user_question)
	
	return {"reddit_results": reddit_results}


def analyze_reddit_posts(state: State):
	user_question = state.get("user_question", "")
	reddit_results = state.get("reddit_results", "")

	if not reddit_results:
		return {"selected_reddit_urls": []}

	structured_llm = structured_llm_model.with_structured_output(RedditURLAnalysis)
	messages = get_reddit_url_analysis_messages(user_question, reddit_results)

	try:
		analysis = structured_llm.invoke(messages)
		selected_urls = analysis.selected_urls

		print("Selected URLs:")
		for i, url in enumerate(selected_urls, 1):
			print(f"{i}. {url}")

	except Exception as e:
		print(e)
		selected_urls = []

	return {"selected_reddit_urls": selected_urls}

def retrieve_reddit_posts(state: State):
	print("Getting redditpost comments")
	selected_urls = state.get("selected_reddit_urls", [])

	if not selected_urls:
		return {"reddit_post_data": []}

	print(f"Processing {len(selected_urls)} Reddit URLs")

	reddit_post_data = reddit_post_retrieval(selected_urls)

	if reddit_post_data:
		print(f"Successfully got {len(reddit_post_data)} posts")

	else:
		print("Failed to get post data")
		reddit_post_data = []

	print(reddit_post_data)
	return {"reddit_post_data": reddit_post_data}

def analyze_google_results(state: State):
	print("Analyzing Google results")

	user_question = state.get("user_question", "")
	google_results = state.get("google_results", "")
	messages = get_google_analysis_messages(user_question, google_results)

	reply = llm.invoke(messages)
	return {"google_analysis": reply.content}

def analyze_bing_results(state: State):
	print("Analyzing Bing results")

	user_question = state.get("user_question", "")
	bing_results = state.get("bing_results", "")

	messages = get_bing_analysis_messages(user_question, bing_results)
	reply = llm.invoke(messages)
	return {"bing_analysis": reply.content}

def analyze_reddit_results(state: State):
	print("Analyzing reddit search results")

	user_question = state.get("user_question", "")
	reddit_results = state.get("reddit_results", "")
	reddit_post_data = state.get("reddit_post_data", "")

	messages = get_reddit_analysis_messages(user_question
																				 , reddit_results
																				 , reddit_post_data)
	reply = llm.invoke(messages)

	return {"reddit_analysis": reply.content}

def synthesize_analyses(state: State):
	print("Combine all results together")

	user_question = state.get("user_question", "")
	google_analysis = state.get("google_analysis", "")
	bing_analysis = state.get("bing_analysis", "")
	reddit_analysis = state.get("reddit_analysis", "")

	messages = get_synthesis_messages(
		user_question
		, google_analysis
		, bing_analysis
		, reddit_analysis
	)

	reply = llm.invoke(messages)	# pass all of this to the llm
	final_answer = reply.content

	print("Final Answer:")
	print(final_answer)
	return {"final_answer": final_answer, "messages": [{"role": "assistant", "content": final_answer}]}

graph_builder = StateGraph(State) # Define the state graph with the State TypedDict

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

		if final_state.get("final_answer"):
			print(f"Final Answer: {final_state.get("final_answer")}\n")
		print("-" * 80)

if __name__ == "__main__":
	run_chatbot()


	