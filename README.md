# Análise de Dados das Interrupções no Sistema Elétrico de Distribuição no Nordeste em 2023

![image](https://github.com/victorcbarros/eda-rede-eletrica-nordeste/blob/main/reports/figures/Banner%20Portfolio.png)

## 📌 Introdução

Este projeto tem como objetivo analisar as interrupções de energia elétrica na rede de distribuição do Nordeste do Brasil ao longo de 2023. O objetivo principal é analisar a frequência, a duração, a quantidade de consumidores afetados dessas interrupções, identificar os fatores que contribuíram para essas ocorrências e explorar possíveis correlações com fatores externos, como os dados mensais de chuva na região. Utilizando bases de dados públicas disponibilizadas pela ANEEL (Agência Nacional de Energia Elétrica) e pelo INMET (Instituto Nacional de Meteorologia), foi realizado uma análise exploratória abrangente dos dados utilizando a linguagem de programação Python para a extração,tratamento e análise.

## 📌 Visão Geral

Atualmente o acesso à energia elétrica está relacionada diretamente com qualidade de vida e desenvolvimento da sociedade. Para isso, garantir que o fornecimento de serviço seja confiável, de qualidade e disponível 100% do tempo é o principal objetivo de uma concessionária de distribuição de energia elétrica. Porém, por se tratar de um serviço essencial e que exige uma estrutura complexa e com muitas etapas, entender e evitar qualquer tipo de interrupção no fornecimento é algo extremamente importante para um serviço de qualidade.

Neste sentido, o órgão regulador do sistema elétrico, ANEEL, impõe às concessionárias de energia elétrica regras e procedimentos para que o fornecimento de energia seja confiável, seguro e de qualidade. Por sua vez, as distribuidoras de energia elétrica tentam a todo custo evitar que haja uma interrupção no fornecimento de energia para não serem penalizadas pela regulação.

Garantir um fornecimento confiável e contínuo é o principal objetivo das concessionárias de energia. Para evitar penalidades da ANEEL, é crucial entender e prevenir interrupções no serviço. Analisar as principais causas dessas interrupções ajuda a melhorar os indicadores de qualidade de energia e protege a rede elétrica, beneficiando tanto os consumidores quanto as distribuidoras.

## 💼 Entendimento do Negócio

O sistema de distribuição de energia elétrica é responsável por captar a energia elétrica do setor de transmissão e transferi-la com a tensão regulada para os consumidores finais, sejam eles empresas ou residências. Este segmento é crucial para a entrega de energia e a cobrança proporcional ao consumo mensal dos usuários (KAGAN, 2005). A estrutura de distribuição inclui fios condutores, equipamentos de proteção, medição e controle, e transformadores, formando uma rede ramificada com equipamentos de menor escala comparados ao sistema de transmissão.

**Estrutura e Configuração da Rede de Distribuição**

As redes de distribuição são subdivididas em três tipos, dependendo da tensão elétrica:

- Redes de Alta Tensão (Subtransmissão): Transportam tensões de 138kV, reduzindo para até 34,5kV.

- Redes de Média Tensão (Distribuição Primária): Interligam a subtransmissão e a baixa tensão.

- Redes de Baixa Tensão (Distribuição Secundária): Operam entre 127V e 380V, conectando-se diretamente às residências (KAGAN, 2005).

As redes de distribuição primária podem ser aéreas ou subterrâneas. As redes aéreas são mais comuns devido ao custo mais baixo, enquanto as redes subterrâneas são usadas em áreas de alta densidade de carga ou com restrições estéticas.

**Regulação e Qualidade do Serviço**

Para assegurar a qualidade do fornecimento de energia elétrica, a ANEEL (Agência Nacional de Energia Elétrica) estabeleceu os Procedimentos de Distribuição de Energia Elétrica (PRODIST), que padronizam as atividades de distribuição. O módulo 8 do PRODIST é especialmente relevante, pois aborda a qualidade do serviço e da energia elétrica (ANEEL, 2022). A ANEEL utiliza diversos indicadores para monitorar a qualidade do serviço, incluindo a continuidade do fornecimento. Esses indicadores são públicos e permitem a avaliação do desempenho das distribuidoras em diferentes regiões.

**Indicadores de Continuidade**

Os indicadores de continuidade são fundamentais para medir a qualidade do serviço de distribuição. Eles avaliam a duração e a frequência das interrupções, tanto em nível individual quanto coletivo. Interrupções com duração superior a três minutos são consideradas significativas e impactam negativamente os indicadores. A ANEEL estabelece que o Consumidor Hora interrompido  (CHI) é calculado com base na Duração de Interrupção Individual por Unidade Consumidora (DIC), expresso em horas (ANEEL, 2021) ou de maneira mais clara multiplicando a quantidade de clientes(consumidores) interrompidos pela duração da interrupção.

**Importância da Minimização de Interrupções**

Minimizar as interrupções é crucial para garantir a qualidade do serviço de distribuição. Menor duração, menor frequência de interrupções e um número reduzido de clientes afetados resultam em melhores classificações nos indicadores de continuidade. Essa prática não só garante a satisfação dos consumidores, mas também evita penalidades regulatórias, como multas e compensações financeiras aos consumidores afetados. Ao longo do projeto vamos nos referir as interupções tambem chamando-a de ocorrências.


**Tipos de Análise Realizados:**
- Análise exploratoria dos dados
- Análise das sazonalidade
- Analise da relação entre variavies quantitavias e categoricas

**Principais Indicadores Chave de Desempenho:**
- Número de Ocorrencias ou Interrupções
- Duração das Interrupções
- Quantidade de Consumidores Atingidos
- Valor do CHI (Consumidor Hora Interrompido)

## 📜 Estrutura do Projeto

A estrutura de diretórios do projeto foi organizada da seguinte forma:
```
├── README.md 
├── notebooks
├── reports
│ └── figures
```

## 🛠 Tratamento e Limpeza dos Dados

A análise de dados de vinhos exige um processo meticuloso de tratamento e limpeza para garantir a confiabilidade e a qualidade das informações. Este estudo detalha as etapas realizadas para preparar os dados para análise subsequente, utilizando a biblioteca Pandas do Python.

_Considerações Importantes:_
1. Foram utilizados conjuntos de dados reais e de plataformas de dados abertos, com referências disponíveis no final do codigo presente na pasta "notebooks".
2. Os dados brutos foram filtrados para incluir apenas informações sobre o nordeste, excluindo dados irrelevantes ou inconsistentes.
3. As etapas de tratamento de dados incluíram remoção de valores ausentes; analise dos dados duplicados; Identificação e correção de erros de digitação, formatação,codificação conversão de unidades,e padronização de nomes e categorias.
   
_Etapas do Tratamento e Limpeza dos Dados:_
1. Importação dos dados e biblioteca
2. Filtragem dos dados do Nordeste do Brasil
3. Tratamento e Limpeza dos Dados de Interrupções
4. Tratamento e Limpeza dos Dados de Chuva

Todo processo de tratamento e limpeza de dados esta presente detalhadamente na pasta notebooks deste repositorio no notebook **Análise Exploratoria Interrupções Nordeste 2023.ipynb**.

## 📊 Análise dos Dados

A etapa de análise de dados é o ponto central deste projeto, transformando todo o conhecimento adquirido sobre o setor em insights valiosos para a distribuição de energia elétrica tanto no Nordeste quanto no restante do Brasil. Por meio de técnicas avançadas e análises detalhadas, identificamos as tendências e oportunidades que impulsionam esse setor dinâmico.

_Etapas da Análise dos Dados:_
1. Importação dos dados e biblioteca
2. Análise inicial dos dados e das variáveis quantitativas
3. Análise dos Dados ao Longo dos Meses de 2023
4. Analise das Causas

Todo processo de análise de dados esta presente detalhadamente na pasta notebooks deste repositorio no notebook **Análise Exploratoria Interrupções Nordeste 2023.ipynb**.

## 📈 Insights e Conclusões

A análise das interrupções na rede de distribuição de energia elétrica no Nordeste brasileiro em 2023 revelou insights importantes sobre os principais desafios e áreas de melhoria para garantir um serviço elétrico mais confiável e eficiente na região. Atraves dos dados conseguimos descobrir que :

- **Análise das Variaveis quantitativas**
    - Duração:

        - A média é relativamente alta em comparação com a mediana, sugerindo a presença de eventos de longa duração que influenciam significativamente a média.
        - A dispersão ampla dos dados indica que há uma variedade de eventos, desde curtos até muito longos.

    - Consumidores Atingidos:

        - A média é muito maior que a mediana, indicando que algumas interrupções afetam um número significativo de consumidores.
        - A presença de um valor máximo alto (103.581 consumidores afetados) destaca o impacto considerável de eventos de alta magnitude nesse indicador.

    - CHI (Clientes-Hora Interrompidos):

        - A diferença entre a média e o desvio padrão sugere a presença de outliers que exercem uma influência significativa no CHI.
        - Os outliers podem representar eventos graves ou incomuns que demandam atenção especial durante a análise.
        - O pico observado em agosto foi causado por eventos de alívio de carga em 15 de agosto, impactando significativamente a média de consumidores afetados.


- **Comportamento ao Longo dos Meses**
    - O número de ocorrências ao longo de 2023 não é uniforme, variando significativamente de mês a mês.
    - A análise sazonal mostra que o verão e o outono tendem a ter mais interrupções, enquanto o inverno apresenta o menor número.
    - A correlação entre as interrupções e o volume de chuva mensal é moderada a alta, indicando que períodos chuvosos estão associados a mais interrupções.

- **Análise dos Fatores Geradores da Interrupção**
    - Origem: A maioria das interrupções é de origem interna, destacando a necessidade de melhorias e manutenção dentro do sistema de distribuição.
    - Tipo: A grande maioria das interrupções é não programada, o que implica em eventos inesperados e não planejados.
    - Responsabilidade: As ocorrências próprias do sistema e relacionadas ao meio ambiente são predominantes, exigindo medidas preventivas para minimizar seu impacto.
    - Causa: Uma ampla gama de motivos contribui para as interrupções, cada um exigindo uma estratégia específica para mitigação.


Entre os principais insights obtidos estão:

- **Impacto das Condições Climáticas**: As condições climáticas adversas, como tempestades e ventos fortes, foram responsáveis por uma parte significativa das interrupções. Investimentos em infraestrutura resiliente e sistemas de monitoramento avançados podem ajudar a mitigar esses impactos.

- **Manutenção Preventiva**: A falta de manutenção preventiva em alguns trechos da rede contribuiu para o aumento das interrupções. Estratégias proativas de manutenção, incluindo inspeções regulares e atualizações de equipamentos, são essenciais para reduzir falhas não programadas.

- **Capacidade de Resposta**: A capacidade de resposta rápida das equipes de manutenção foi fundamental para minimizar o tempo de indisponibilidade do serviço. Investimentos em treinamento e tecnologia para melhorar a eficiência das equipes podem resultar em tempos de reparo mais rápidos e menor impacto para os consumidores.

- **Monitoramento e Análise de Dados**: A utilização de sistemas avançados de monitoramento e análise de dados pode proporcionar insights em tempo real sobre o estado da rede, permitindo a identificação precoce de potenciais pontos de falha e a implementação de medidas corretivas proativas.

- **Engajamento com Stakeholders**: O envolvimento contínuo com os stakeholders, incluindo consumidores, órgãos reguladores e comunidades locais, é crucial para entender as necessidades específicas da região e implementar soluções personalizadas que promovam a resiliência do sistema elétrico.
