from flask import Flask, jsonify, request
from flask_cors import CORS
# Importe todo o código necessário aqui, incluindo os e os imports do CrewAI

from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
import os
from openai import OpenAI
import json
os.environ['OPENAI_MODEL_NAME'] = 'gpt-3.5-turbo'
os.environ["OPENAI_API_KEY"] = "sk-proj-la3OYkko7KtgExM9XtfUT3BlbkFJUI7chpIYpJgYwfasHZ4c"
os.environ["SERPER_API_KEY"] = "0de6e185f983b1d170902c2030540ff023d3904a" # serper.dev API key

search_tool = SerperDevTool()

app = Flask(__name__)
CORS(app)

@app.route('/api/execute', methods=['POST'])
def execute_crew():
    data = request.get_json()

    # Parse os dados recebidos para criar os agentes e as tarefas
    researcher_data = data.get('researcher')
    writer_data = data.get('writer')
    task1_data = data.get('task1')
    task2_data = data.get('task2')

    # Remove 'verbose' if it exists to avoid conflict
    researcher_data.pop('verbose', None)
    writer_data.pop('verbose', None)

    # Create Agents with verbose=True
    researcher = Agent(**researcher_data, verbose=True)
    writer = Agent(**writer_data, verbose=True)

    task1 = Task(**task1_data, agent=researcher)
    task2 = Task(**task2_data, agent=writer)

    crew = Crew(
        agents=[researcher, writer],
        tasks=[task1, task2],
        verbose=2
    )
    result = crew.kickoff()

 

    
    return jsonify(result)

if __name__ == '__main__':
    app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # Set limit to 32MB (or adjust as needed)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8083)))
