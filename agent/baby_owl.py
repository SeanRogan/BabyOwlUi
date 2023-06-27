import json
import logging

import openai
from serpapi import GoogleSearch

from agent.tools.web_scrape_tool import web_search_tool


class BabyOwlAgent:
    OBJECTIVE = ''
    openai_api_key = ''
    serp_api_key = ''
    websearch_var = ''
    task_list = []
    if serp_api_key:
        serpapi_client = GoogleSearch({"api_key": serp_api_key})
        websearch_var = "[web-search]"
    else:
        websearch_var = ''

    def __init__(self, openai_key: str, serp_key: str, obj: str):
        self.openai_api_key = openai_key
        openai.api_key = openai_key
        self.serp_api_key = serp_key
        self.OBJECTIVE = obj
        self.task_list = []

    def create_task_list(self, objective: str) -> list[dict]:
        OBJECTIVE = objective
        task_list = []
        # set prompt
        prompt = (
            f"You are a task creation AI tasked with creating a list of tasks as a JSON array, considering the ultimate objective of your team: {OBJECTIVE}. "
            f"Create new tasks based on the objective. Limit tasks types to those that can be completed with the available tools listed below. Task description should be detailed."
            f"Current tool option is [text-completion] and {self.websearch_var} only."  # web-search is added automatically if SERPAPI exists
            f"For tasks using [web-search], provide the search query, and only the search query to use (eg. not 'research waterproof shoes, but 'waterproof shoes')"
            f"dependent_task_ids should always be an empty array, or an array of numbers representing the task ID it should pull results from."
            f"Make sure all task IDs are in chronological order.\n"
            f"The last step is always to provide a final summary report including tasks executed and summary of knowledge acquired.\n"
            f"Do not create any summarizing steps outside of the last step..\n"
            f"An example of the desired output format is: "
            "[{\"id\": 1,"
            " \"task\": \"https://untapped.vc\","
            " \"tool\": \"web-scrape\","
            " \"dependent_task_ids\": [],"
            " \"status\": \"incomplete\","
            " \"result\": null,"
            " \"result_summary\": null},"
            " {\"id\": 2,"
            " \"task\": \"Consider additional insights that can be reasoned from the results and of output of the dependent tasks.\","
            " \"tool\": \"text-completion\","
            " \"dependent_task_ids\": [1],"
            " \"status\": \"incomplete\","
            " \"result\": null,"
            " \"result_summary\": null},"
            " {\"id\": 3,"
            " \"task\": \"Untapped Capital\","
            " \"tool\": \"web-search\","
            " \"dependent_task_ids\": [],"
            " \"status\": \"incomplete\","
            " \"result\": null,"
            " \"result_summary\": null}].\n"
            f"JSON TASK LIST="
        )

        # log statements
        print("\033[90m\033[3m" + "\nInitializing...\n" + "\033[0m")
        print("\033[90m\033[3m" + "Analyzing objective...\n" + "\033[0m")
        print("\033[90m\033[3m" + "Running task creation agent...\n" + "\033[0m")

        # todo replace with better api call
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a project manager. Your job is to break down a given objective into a list of tasks to be completed."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=2000,
            n=1,
            stop="###",
            temperature=0.5,
        )
        result = response["choices"][0]["message"]["content"]
        try:
            task_list = json.loads(result)
        except Exception as err:
            logging.error(str(err))

        return task_list

    def convert_task_to_search_query(self, task):
        # todo llm call to convert task to search query
        system_content_prompt = "You are an expert at SEO and the use of internet search engines. Your job is to review a task and form the ideal google search query in order to complete the task. EXAMPLE: {\'example task\': \'Search for recently published papers related to the study of nuclear physics.\', \'example output\' : \'nuclear physics AND recently published AND peer reviewed OR scientific papers\'"
        user_content_prompt = f'{task}'

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": system_content_prompt
                },
                {
                    "role": "user",
                    "content": user_content_prompt
                }
            ],
            max_tokens=600,
            n=1,
            stop="###",
            temperature=0.5,
        )
        result = response["choices"][0]["message"]["content"]
        return result

    def execute_task(self, task: dict, task_list: list, obj: str):
        OBJECTIVE = obj
        task_output = None
        task_index = None
        # Check if dependent_task_ids is not empty
        # todo this loops over the whole task list to check for incomplete tasks with every iteration, need a more performant way to check that tasks are done
        if task["dependent_task_ids"]:  # if there are any dependencies...
            for dependent_task_id in task["dependent_task_ids"]:  # loop through dependency tasks
                dependent_task = self.get_task_by_id(dependent_task_id)
                if not dependent_task or dependent_task["status"] != "complete":  # if the task is NOT complete
                    break

        # Execute task
        print("\033[92m\033[1m" + "\n*****NEXT TASK*****\n" + "\033[0m\033[0m")
        print(str(task['id']) + ": " + str(task['task']) + " [" + str(task['tool'] + "]"))
        task_prompt = f"Complete your assigned task based on the objective " \
                      f"and based on information " \
                      f"provided in the dependent task output, if dependent task output is provided." \
                      f" Your objective: {OBJECTIVE}. Your task: {task['task']}"
        if task["dependent_task_ids"]:  # if the task has dependent tasks
            dependent_tasks_output = ""
            # todo this is broke, self.get_task_by_id returns none for some reason.
            for dependent_task_id in task["dependent_task_ids"]:  # loop through their ids
                dependent_task_output = self.get_task_by_id(dependent_task_id)["output"]
                # dependent_task_output = dependent_task_output["choices"][0]["message"]["content"]
                print(dependent_task_output)  # find the tasks output and save it
                dependent_task_output = dependent_task_output[0:2000]  # clip it to size
                dependent_tasks_output += f" {dependent_task_output}"  # append the dependency task outputs together
            task_prompt += f" Your dependent tasks output: {dependent_tasks_output}\n OUTPUT:"  # append the outputs to the prompt context

        # Use tool to complete the task
        # todo this is rudimentary we can use a routing chain for this
        if task["tool"] == "text-completion":
            task_output = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {  # todo this prompt should be rewritten and benchmarked against the original.
                        "role": "system",
                        "content": "You are a task creation AI."
                    },
                    {
                        "role": "user",
                        "content": task_prompt
                    }
                ],
                max_tokens=2000,
                n=1,
                stop="###",
                temperature=0.5,
            )
            task_output = task_output["choices"][0]["message"]["content"]
        elif task["tool"] == "web-search":
            task_query = self.convert_task_to_search_query(str(task['task']))
            task_output = web_search_tool(task_query, self)
        # Find task index in the task_list
        for i, t in enumerate(task_list):
            if t["id"] == task["id"]:
                task_index = i
                break
        # Mark task as complete and save output
        task_list[task_index]["status"] = "complete"
        task_list[task_index]["output"] = task_output
        # todo save prompt and output to chroma db
        # Print task output
        print("\033[93m\033[1m" + "\nTask Output:" + "\033[0m\033[0m")
        print(task_output)

        # # Add task output to session_summary
        # global session_summary
        # session_summary += f"\n\nTask {task['id']} - {task['task']}:\n{task_output}"

    def get_objective(self) -> str:
        return self.OBJECTIVE

    def get_completed_tasks(self):
        return [task for task in self.task_list if task["status"] == "complete"]

    def get_task_by_id(self, id: int) -> dict:
        for task in self.task_list:
            if task["id"] == id:
                return task

    def add_task(self, task: dict):
        self.task_list.append(task)

    # Print task list and session summary
    def print_task_list(self):
        print("\033[95m\033[1m" + "\n*****TASK LIST*****\n" + "\033[0m")
        for t in self.task_list:
            dependent_task = ""
            if t['dependent_task_ids']:
                dependent_task = f"\033[31m<dependencies: {', '.join([f'#{dep_id}' for dep_id in t['dependent_task_ids']])}>\033[0m"
            status_color = "\033[32m" if t['status'] == "complete" else "\033[31m"
            print(
                f"\033[1m{t['id']}\033[0m: {t['task']} {status_color}[{t['status']}]\033[0m \033[93m[{t['tool']}] {dependent_task}\033[0m")

    def fly(self):
        # start = time.time()
        print("\033[96m\033[1m" + "\n*****HOO HOO... How may I help you?*****\n" + "\033[0m\033[0m")
        # OBJECTIVE = "Find me three recent peer reviewed research papers on the subject of artificial intelligence, describe the findings in the papers, and include a direct quote with a properly formatted citation from each paper"
        OBJECTIVE = self.OBJECTIVE
        task_list = self.create_task_list(OBJECTIVE)
        # print_task_list()
        # todo here is a good place to have a human intervention step to reorder or edit the tasklist
        tasks_completed = []

        while len(tasks_completed) < len(task_list):
            for task in task_list:
                if task["status"] != "complete":
                    self.execute_task(task, task_list, OBJECTIVE)
                    # print_task_list()
                    tasks_completed.append(task)
                    break
        # end = time.time()
        # print(end - start)
