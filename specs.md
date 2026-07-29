# Snake

Seu objetivo é construir, em Python e em
estilo funcional, o famoso jogo Snake. Para
isso, explore todos os conceitos de
programação funcional que estudamos no curso
até o presente momento.

- código em estilo declarativo e funcional
- projete e use apenas tipos de dados imutáveis
- faça tratamento de erros em estilo monádico

## Especificação

**Jogo para o terminal** O jogo deve ser para
o terminal. Para lidar com o terminal, você
pode usar a biblioteca curses padrão de
Python ou pode experimentar a biblioteca
blessed que é uma API mais moderna para
curses e, aparentemente, mais fácil de usar.

- [Material sobre o Curses](https://docs.python.org/3/howto/curses.html)
- [Material sobre o Blessed](https://blessed.readthedocs.io/en/latest/)

> Pra instalar, crie um ambiente virtual para
> o seu app e instale com `pip install
> blessed`.

**O Jogo Snake** Sei que o jogo dispensa
apresentação, mas é importante registrar os
detalhes. Na tela devem haver sempre os
seguintes elementos: i) a _snake_; ii) a
_fruta_; e iii) uma barra de status. A
dinâmica é conhecida: a _snake_ está
continuamente em movimento e o jogador pode
apenas mudar a direção/sentido do movimento,
sempre fazendo-a virar à esquerda ou à
direita em relação à direção em que está se
movimentando. O objetivo do jogador é comer o
máximo de _frutas_ na tela. Cada vez que uma
_fruta_ é comida, a _snake_ tem seu
comprimento e sua velocidade aumentados. O
jogo acaba quando o jogador faz a _snake_ se
chocar em seu próprio corpo. À medida que as
_frutas_ vão sendo comidas, a barra de status
vai sendo atualizanda, indicando a pontuação.
A qualquer momento, o usuário também deve
poder interromper o jogo.

## Sobre o processo

**IMPORTANTE** Crie o diretório `snake`
dentro do diretório do roteiro. E dentro dele
faça seu app. Faça o arquivo
`snake/README.md` para seu app (cuidado para
não confundir com este arquivo `README.md`
que é a especificação da atividade). Faça o
arquivo `snake/README.md` conter todas as
decisões de design de seu app. Em particular,
formatos de dados e funções.

**Opcional: git** Você pode usar o git (em
linha de comando, claro), para controlar o
versionamento de seu app. Se optar por
usar, sugiro criar o repositório vazio desde
o início e fazer commits com muita frequência
(mas sempre mantendo o repo saudável). Você
não precisa complicar o _workflow_, usando
branches. Basta usar a branch _main_ ou
_master_ para tudo, até porque você é o único
desenvolvedor. Mas ter um repositório ajuda a
evitar acidentes.

**Projete estado** Lembre, que você
deve usar o estilo funcional de programação.
Em geral, isso se inicia pelo projeto do
estado do jogo: pense em todos os dados que
compõem um estado. Pense nos tipos de dados
de forma que não haja estados inválidos.

**Projete eventos** Em seguida, planeje quais
eventos ocorrem e como podemos modelá-los
através de funções que mapeiem o estado.
Pense em funções puras que façam essas
transformações. Sempre que necessário, use
funções utilitárias e de apoio. Sempre que
oportuno, use e crie funções de alta ordem.

**Núcleo funcional, Casca imperativa**
Observe que parte significativa do jogo é
não-funcional (lidar com a tela, com eventos
do teclado, com tempo, com dados aleatórios,
etc). Lide com isso, isolando ao máximo a
parte funcional da não-funcional, sempre
fazendo a não-funcional usar e acessar a
parte funcional e não o contrário. A ideia é
explorarmos o padrão arquitetural conhecido
como _núcleo funcional, casca imperativa_ (ou
_imperative shell, functional core_), em que
a orquestração é feita na _casca_, mas a
lógica _de negócio_ é feita em camadas
internas. Você pode usar tudo que a LP
oferece de mecanismos de decomposição para
separar as partes da melhor forma possível
(veja a seção "Modelagem de dados em Python"
abaixo sobre as possibilidades).

Caso queira ler sobre o tema, este pode ser
um bom lugar para começar: [Functional Core,
Imperative
Shell](https://functional-architecture.org/functional_core_imperative_shell/).

## Desafio

Um pequeno detalhe que queremos poder
adicionar a nosso jogo, mas deixe pra fazê-lo
somente depois que terminar a primeira
versão. Ao final do jogo,
seja porque o usuário perdeu, seja porque
pediu pra sair, deve ser apresentado um
pequeno "filme" do jogo desde seu início até
o final (acelerado, é claro).

## Modelagem de dados em Python

- typing: List, Optional
- namedtuple
- dataclass
- Enum, StrEnum, auto
