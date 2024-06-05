from flask import Flask, jsonify, request
import os
from crewai import Agent, Task, Crew
from crewai_tools import FileReadTool, WebsiteSearchTool

app = Flask(__name__)

# Set up API keys
os.environ["SERPER_API_KEY"] = "0de6e185f983b1d170902c2030540ff023d3904a"  # serper.dev API key
os.environ["OPENAI_API_KEY"] = "sk-proj-la3OYkko7KtgExM9XtfUT3BlbkFJUI7chpIYpJgYwfasHZ4c"

file_tool = FileReadTool()
web_rag_tool = WebsiteSearchTool()

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()

    # Create agents
    researcher_agent = Agent(
        role=data['researcher']['role'],
        goal=data['researcher']['goal'],
        backstory=data['researcher']['backstory'],
        tools=[web_rag_tool],  # Utiliza a ferramenta de busca na web para obter informações atualizadas
        verbose=True
    )

    writer_agent = Agent(
        role=data['writer']['role'],
        goal=data['writer']['goal'],
        backstory=data['writer']['backstory'],
        tools=[file_tool],  # Utiliza a ferramenta de leitura de arquivo para revisar publicações
        verbose=True
    )

    # Define tasks
    generate_publication_task = Task(
        description=data['task1']['description'],
        expected_output=data['task1']['expected_output'],
        agent=researcher_agent
    )

    review_publications_task = Task(
        description=data['task2']['description'],
        expected_output=data['task2']['expected_output'],
        agent=writer_agent,
        output_file='blog-posts/new_post.md'
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
    app.run(debug=True)
