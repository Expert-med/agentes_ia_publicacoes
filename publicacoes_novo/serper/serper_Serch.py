from flask import Flask, jsonify, request
from crewai import Agent, Task, Crew
from crewai_tools import (
   
    SerperDevTool,
    WebsiteSearchTool
)
import os
from flask_cors import CORS

# Configurando a chave da API do Serper
os.environ["SERPER_API_KEY"] = "0de6e185f983b1d170902c2030540ff023d3904a"
os.environ["OPENAI_API_KEY"] = "sk-proj-la3OYkko7KtgExM9XtfUT3BlbkFJUI7chpIYpJgYwfasHZ4c"

# Inicializando o Flask app
app = Flask(__name__)
CORS(app)

# Rota para a API de pesquisa
@app.route('/api/search', methods=['POST'])
def search():
    if request.method == 'POST':
        data = request.json
        
        search_query = data.get('query', '')
        role = data.get('role', 'Analista Sênior de Marketing')
        goal = data.get('goal', 'Descobrir desenvolvimentos de ponta em IA e ciência de dados')
        backstory = data.get('backstory', 'Você trabalha em um renomado think tank de tecnologia. Sua expertise está em identificar tendências emergentes. Você tem habilidade para dissecar dados complexos e apresentar insights acionáveis.')

        if not search_query:
            return jsonify({'error': 'No search query provided'}), 400

        # Criando o agente do Serper com os dados recebidos
        search_tool = SerperDevTool()
        web_rag_tool = WebsiteSearchTool()

        search_agent = Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            tools=[search_tool,web_rag_tool],
            verbose=True
        )

        # Criando uma nova tarefa de pesquisa com o termo de busca
        search_task = Task(
            description=f'Realizar uma busca no Serper por "{search_query}" e exibir resultados detalhados',
            expected_output='Um texto longo e detalhado baseado nos conteúdos encontrados pela pesquisa',
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

    # Retorna um erro se o método não for POST
    return jsonify({'error': 'Method not allowed'}), 405

# Rodando a aplicação Flask
if __name__ == '__main__':
    app.run(debug=True)
