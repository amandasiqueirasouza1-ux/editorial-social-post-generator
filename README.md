# Editorial Social Post Generator

Gerador local e configurável de posts editoriais em SVG para redes sociais.

O projeto lê uma planilha CSV, aplica a identidade definida em um arquivo JSON e cria versões claras e escuras de cada post. Não utiliza API, não envia dados para serviços externos e funciona apenas com a biblioteca padrão do Python.

## Recursos

- formato padrão de 1080 × 1350;
- versões clara e escura;
- trecho do título com cor de destaque;
- quebra automática de linhas;
- validação de textos excessivamente longos;
- saída em SVG editável;
- identidade visual configurável;
- exemplos neutros;
- testes automatizados.

## Requisitos

- Python 3.10 ou superior.

## Como usar

1. Copie os arquivos de exemplo:

```bash
cp config/brand.example.json config/brand.json
cp content/posts.example.csv content/posts.csv
```

2. Edite as cores, o nome da marca e os conteúdos.

3. Execute:

```bash
python3 src/generate.py
```

Os SVGs serão criados na pasta `output/`.

## Colunas do CSV

| Coluna | Uso |
|---|---|
| `filename` | Nome do arquivo sem extensão |
| `title` | Texto principal |
| `highlight` | Trecho que receberá a cor de destaque |
| `category` | Primeira informação do rodapé |
| `topic` | Segunda informação do rodapé |

## Configuração visual

O arquivo `config/brand.json` controla:

- nome exibido;
- cores clara e escura;
- cor de destaque;
- dimensões;
- famílias tipográficas usadas pelo SVG.

As fontes não são distribuídas neste repositório. Use famílias instaladas no seu computador ou fontes abertas compatíveis.

## Testes

```bash
python3 -m unittest discover -s tests -v
```

## Limites

O projeto gera SVG. A conversão para PNG pode ser feita em um editor gráfico, navegador ou ferramenta compatível. Esse recorte mantém o gerador portátil e sem dependências externas.

## Contribuições

Leia [CONTRIBUTING.md](CONTRIBUTING.md) antes de enviar alterações.

## Licença

[MIT](LICENSE)

## English

An English overview is available in [README_EN.md](README_EN.md).
