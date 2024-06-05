from flask import Flask, jsonify, request
from flask_cors import CORS
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool
import os

# Configurando as chaves da API
os.environ["SERPER_API_KEY"] = "0de6e185f983b1d170902c2030540ff023d3904a"  # serper.dev API key
os.environ["OPENAI_API_KEY"] = "sk-proj-la3OYkko7KtgExM9XtfUT3BlbkFJUI7chpIYpJgYwfasHZ4c"

# Instanciando o SerperDevTool
search_tool = SerperDevTool()

app = Flask(__name__)
CORS(app)

@app.route('/api/execute', methods=['POST'])
def execute_crew():
    data = request.get_json()

    # Parse dos dados recebidos para criar os agentes e as tarefas
    researcher_data = data.get('researcher')
    writer_data = data.get('writer')
    task1_data = data.get('task1')
    task2_data = data.get('task2')

    researcher = Agent(**researcher_data)
    writer = Agent(**writer_data)
    task1 = Task(**task1_data, agent=researcher)
    task2 = Task(**task2_data, agent=writer)

    # Adicionando o SerperDevTool aos agentes
    researcher.tools.append(search_tool)
    writer.tools.append(search_tool)

    # Criando a equipe
    crew = Crew(
        agents=[researcher, writer],
        tasks=[task1, task2],
        verbose=2
    )

    # Executando a equipe
    result = crew.kickoff()
    print('JSON retornado:')
    print(result)
    return result

if __name__ == '__main__':
    app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # Definindo o limite para 32MB (ou ajuste conforme necessário)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8083)))
