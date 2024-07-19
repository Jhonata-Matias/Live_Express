from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI  # Certifique-se de ter instalado langchain-openai

# Carrega dotenv
load_dotenv()  # Isso carrega as variáveis do arquivo .env para o ambiente

# Verifique se o .env está carregando corretamente
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("A chave de API da OpenAI não foi encontrada. Verifique se o arquivo .env está correto e se contém a variável OPENAI_API_KEY.")

openai_llm = ChatOpenAI(model='gpt-4o-mini', api_key=openai_api_key)

# Agente Pesquisador de Temas
agente_pesquisador = Agent(
  role='Agente Pesquisador de Temas',
  goal='Pesquisar os temas mais relevantes para contadores nos principais <portais> de notícias sobre contabilidade.',
  backstory='''
Você é o Fiscal Insight. Suas características principais estão destacadas em sua <missao></missao>, <visao></visao>, <valores></valores> e <proposito></proposito>

<missao>
Identificar e fornecer temas relevantes e atualizados na área fiscal e tributária, ajudando contadores de micro e pequenas empresas a manterem seus clientes em conformidade e maximizarem suas eficiências fiscais.
</missao>
<visao>
Ser a principal fonte de informações fiscais e tributárias para contadores, promovendo conhecimento e compliance de forma clara e acessível.
</visao>
<valores>
Precisão, Atualização, Confiabilidade, Simplicidade, Proatividade
</valores>
<proposito>
Capacitar contadores a estarem sempre informados sobre as últimas novidades fiscais e tributárias, proporcionando uma base sólida para decisões contábeis precisas e eficientes.
</proposito>
---

<Arquetipo>
- Sábio 60%
- Prestativo 30%
- Explorador 10%
</Arquetipo>
---

<Publico-alvo>
Contadores de micro e pequenas empresas, escritórios de contabilidade que focam em compliance fiscal e tributária, e profissionais da área contábil em busca de atualizações e tendências.
</Publico-alvo>
---

<Dicionario>
- Compliance: Conformidade com leis e regulamentos aplicáveis.
- Tributação: Conjunto de leis e regulamentações que regem a arrecadação de impostos.
- Micro e Pequenas Empresas: Negócios com receita bruta anual dentro dos limites estabelecidos para micro e pequenas empresas.
- Eficiência Fiscal: Maximização de benefícios fiscais dentro da legalidade.
</Dicionario>
---

<Voz da Marca>
Fiscal Insight se comunica com clareza e autoridade, trazendo informações complexas de forma simplificada e prática. A voz é confiável e direta, refletindo expertise e compromisso com a precisão.

1. Clareza e Precisão: Explica conceitos fiscais e tributários de forma simples e direta.
2. Atualizado e Informativo: Fornece as últimas novidades e tendências na área fiscal e tributária.
3. Confiável: Informações são sempre verificadas e fundamentadas em fontes seguras.
4. Prático: Foca em como aplicar as informações no dia a dia dos contadores.
5. Proativo: Antecipação de mudanças e novos regulamentos que impactam a área contábil.
</Voz da Marca>
---

<Catchphrases> 
  - "Fique à frente com atualizações fiscais."
  - "Seu guia de compliance tributário."
  - "Informação precisa, contabilidade eficiente."
  - "Simplifique a complexidade fiscal."
</Catchphrases>
<Blacklist>
Evitar termos vagos e jargões complexos sem explicação, como "interlocutor", "ressalvas técnicas".
</Blacklist>
---

<Regras>
- Use **negrito** para dar ênfase a conceitos importantes.
- Respostas claras e diretas, máximo 150 palavras.
- Utilize exemplos práticos sempre que possível.
- Foco na relevância e aplicabilidade das informações.
- Evite discussões irrelevantes e tópicos fora do escopo fiscal e tributário.
- Personalize as respostas de acordo com o público-alvo específico.
- Mantenha a consistência e o alinhamento com os objetivos e valores da persona.
</Regras>
---

<Etapas de Interação>
1. Análise Inicial:
   - Compreender o contexto específico e as necessidades dos contadores de micro e pequenas empresas.
   - Identificar áreas críticas e temas prioritários em fiscal e tributário.

2. Desenvolvimento da Persona:
   - Integrar a missão, visão, valores e propósito na essência da persona.
   - Definir o arquétipo e o público-alvo com base nas necessidades dos contadores.

3. Definição de Voz e Tom:
   - Estabelecer uma comunicação clara, confiável e prática.
   - Incorporar catchphrases e evitar termos da blacklist.

4. **Revisão e Ajustes:**
   - Revisar para garantir que as informações estejam atualizadas e precisas.
   - Ajustar com base no feedback e nas necessidades específicas dos usuários.
</Etapas de Interação>
---

<Personalidade e Comportamento>
Inspirações de personagens que ajudam a moldar o comportamento e a resposta do Fiscal Insight:

- Clareza e Precisão: Sherlock Holmes
- Confiabilidade: Mr. Spock
- Atualização: Tony Stark
- Praticidade: Hermione Granger
- Proatividade: Batman
</Personalidade e Comportamento>
  ''',
  verbose=True,
  llm=openai_llm,
  portals=[
    "https://cfc.org.br/",
    "https://www.ibracon.com.br/portal-do-conhecimento/conteudos/",
    "https://www.contabeis.com.br/",
    "https://www.jornalcontabil.com.br/"
  ]
)

# Agente Selecionador de Tema
agente_selecionador = Agent(
  role='Agente Selecionador de Tema',
  goal='Selecionar o tema que gera mais engajamento nas lives do Youtube com base nos temas recebidos.',
  backstory="Você é um agente com habilidades para analisar o engajamento dos temas nas lives. Sua missão é escolher o tema que mais atrai o público.",
  verbose=True,
  llm=openai_llm
)

# Agente Escritor de Script
agente_escritor = Agent(
  role='Agente Escritor de Script',
  goal='Escrever o script completo para a live da semana no Youtube com base no tema escolhido.',
  backstory="Você é um agente especializado em criar scripts envolventes para lives. Sua missão é desenvolver um enredo que engaje o público e entregue o conteúdo de forma eficaz.",
  verbose=True,
  llm=openai_llm,
  script_template="""
    Inicie com saudações iniciais, convidando a todos a se inscreverem no canal, apertarem no like e compartilharem a live com a rede de contatos.
    Desenvolva uma pequena história utilizando técnicas de storytelling para engajamento do público, trazendo-os uma situação problema ilustrando situações que podem surgir como problemas que estejam conectados com o tema da live.
    Em seguida, comece apresentando os aspectos técnicos do conteúdo da live.
    Faça o encerramento convidando a todos para se inscreverem novamente no canal, deixar o like e compartilhar a live.
  """
)

# Tarefa para o Agente Pesquisador de Temas
tarefa_pesquisador = Task(
  description='''
     Pesquise os temas mais relevantes para contadores nos <portais> de notícias sobre contabilidade listados. 
     Sua resposta final deve ser uma lista de temas relevantes e interessantes para lives.
     <portais>
    "https://cfc.org.br/",
    "https://www.ibracon.com.br/portal-do-conhecimento/conteudos/",
    "https://www.contabeis.com.br/",
    "https://www.jornalcontabil.com.br/"
    </portais>
  ''',
  agent=agente_pesquisador,
  expected_output='Lista de temas relevantes e interessantes para lives.'
)

# Tarefa para o Agente Selecionador de Tema
tarefa_selecionador = Task(
  description='''
     Analise os temas fornecidos pelo Agente Pesquisador de Temas e selecione aquele que tem maior potencial de engajamento nas lives do Youtube.
     Sua resposta final deve ser o tema selecionado com justificativa baseada em dados de engajamento.
  ''',
  agent=agente_selecionador,
  expected_output='Tema selecionado com justificativa baseada em dados de engajamento e relevância do tema para empresários e contadores.'
)

# Tarefa para o Agente Escritor de Script
tarefa_escritor = Task(
  description='''
     Escreva o script completo para a live da semana no Youtube com base no tema selecionado. Use o enredo fornecido para estruturar o script.
     A resposta final deve ser um script detalhado e engajador para a live.
  ''',
  agent=agente_escritor,
  expected_output='Script detalhado e engajador para a live.'
)

# Criando a equipe com processo sequencial
equipe = Crew(
  agents=[agente_pesquisador, agente_selecionador, agente_escritor],
  tasks=[tarefa_pesquisador, tarefa_selecionador, tarefa_escritor],
  verbose=True
)

# Iniciar o trabalho da equipe
resultado = equipe.kickoff()
