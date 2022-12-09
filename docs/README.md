# Diretrizes

Este arquivo tem o propósito de explicar a organização do projeto.

## Estrutura de Arquivos

O projeto é dividido em 2 diretórios principais `src`, `docs`. `src` contém os arquivos de código-fonte, em Python, `docs` contém este arquivo de diretrizes e um relatório em LaTeX (com um subdiretório para imagens). Os arquivos do código fonte estão divididos em módulos. Em especial, o módulo `test` contém testes de unidade que podem ser executados usando a biblioteca *pytest*.

A especificação do trabalho se encontra no diretório `spec`.

## Práticas de Código

Na medida do possível, o projeto é fortemente tipado. No mais, valem as seguintes práticas:

- Nomes de módulos devem ser em *snake_case* 
- Nomes de classes devem ser em *PascalCase*
- Nomes de funções devem ser em *snake_case*
- Nomes de variáveis devem ser em *snake_case*
