from flask import Flask, jsonify, request
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool, WebsiteSearchTool
import os
from flask_cors import CORS

# Configurando a chave da API do Serper
os.environ["SERPER_API_KEY"] = "0de6e185f983b1d170902c2030540ff023d3904a"
os.environ["OPENAI_API_KEY"] = "sk-proj-Jx4cJCCUfnxdNm32jx3fT3BlbkFJjsv8CiBVIuXLa5RmxSO1"
os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"

# Inicializando o Flask app
app = Flask(__name__)
CORS(app)

# Rota para a API de pesquisa
@app.route('/search', methods=['POST'])
def search():
    data = request.json

    # Extraindo dados do corpo da requisição
    search_query = data.get('query', '')
    role = data.get('role')
    goal = data.get('goal')
    backstory = data.get('backstory')
    description = data.get('description')
    expected_output = data.get('expected_output')

    # Verificando se todos os dados necessários foram fornecidos
    if not search_query:
        return jsonify({'error': 'No search query provided'}), 400
    if not role or not goal or not backstory:
        return jsonify({'error': 'Missing role, goal, or backstory'}), 400
    if not description or not expected_output:
        return jsonify({'error': 'Missing description or expected_output'}), 400

    # Criando o agente do Serper com os dados recebidos
    search_tool = SerperDevTool()
    web_rag_tool = WebsiteSearchTool()

    search_agent = Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        tools=[search_tool, web_rag_tool],
        verbose=True
    )

    # Criando uma nova tarefa de pesquisa com os dados recebidos
    search_task = Task(
        description=description,
        expected_output=expected_output,
        agent=search_agent
    )

    # Criando uma nova equipe com a nova tarefa de pesquisa
    crew = Crew(
        agents=[search_agent],
        tasks=[search_task],
        verbose=2
    )

    # Executando a tarefa de pesquisa
    results = crew.kickoff()

    # Retornando os resultados completos em formato JSON
    return jsonify({'results': results})

# Rodando a aplicação Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8083, debug=True)
