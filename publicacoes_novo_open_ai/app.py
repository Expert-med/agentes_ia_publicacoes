from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from crewai import Agent, Task, Crew

app = Flask(__name__)
CORS(app)

# Set up API keys
os.environ["SERPER_API_KEY"] = "0de6e185f983b1d170902c2030540ff023d3904a"  # serper.dev API key
os.environ["OPENAI_API_KEY"] = "sk-proj-Jx4cJCCUfnxdNm32jx3fT3BlbkFJjsv8CiBVIuXLa5RmxSO1"
os.environ["OPENAI_MODEL_NAME"]="gpt-3.5-turbo"

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()

    # Create agents
    researcher_agent = Agent(
        role=data['researcher']['role'],
        goal=data['researcher']['goal'],
        backstory=data['researcher']['backstory'],
        tools=[],  # Utiliza a ferramenta de busca na web para obter informações atualizadas
        verbose=True,
        model='gpt-3.5-turbo',
    )

    writer_agent = Agent(
        role=data['writer']['role'],
        goal=data['writer']['goal'],
        backstory=data['writer']['backstory'],
        tools=[],  # Utiliza a ferramenta de leitura de arquivo para revisar publicações
        verbose=True,
        model='gpt-3.5-turbo',
    )

    # Define tasks
    generate_publication_task = Task(
        description=data['task1']['description'],
        expected_output=data['task1']['expected_output'],
        agent=researcher_agent,
        model='gpt-3.5-turbo',    )

    review_publications_task = Task(
        description=data['task2']['description'],
        expected_output=data['task2']['expected_output'],
        agent=writer_agent,
        output_file='blog-posts/new_post.md',
        model='gpt-3.5-turbo'
        
    )

    # Assemble a crew
    crew = Crew(
        agents=[researcher_agent, writer_agent],
        tasks=[generate_publication_task, review_publications_task],
        verbose=2
    )

    # Execute tasks
    result = crew.kickoff()

    print('JSON retornado:')
    print(result)
    return result

if __name__ == '__main__':
    app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # Definindo o limite para 32MB (ou ajuste conforme necessário)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8083)))
