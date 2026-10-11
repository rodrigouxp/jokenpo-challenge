# Jokenpo Challenge — versão refatorada

Refatoração do projeto original (https://github.com/rodrigouxp/jokenpo-challenge),
mantendo o mesmo jogo (pedra, papel, tesoura contra o computador, com modo
rápido e melhor de 3), mas reorganizado em módulos:

- `constants.py`  — cores, tamanhos, e os enums `Move`, `Character`, `Screen`
- `assets.py`     — carrega todas as imagens e sons uma única vez
- `sprites.py`    — `Button` e `AnimatedCharacter` (unifica as antigas
                     classes `Player` e `Computer`, que eram quase idênticas)
- `game_logic.py` — a regra "quem ganha de quem", sem nenhuma dependência de
                     pygame (fácil de testar isoladamente)
- `state.py`      — `GameState`: todo o estado do jogo num único objeto, em
                     vez de variáveis globais soltas
- `screens.py`    — funções de desenho de cada tela
- `main.py`       — loop principal e tratamento de eventos

## Rodando localmente

```bash
pip install -r requirements.txt
python main.py
```

## Gerando um executável (.exe) para mandar pros amigos

**Importante:** o PyInstaller empacota para o sistema operacional em que ele
roda. Ou seja, pra gerar um `.exe` do Windows, você precisa rodar o comando
*num Windows* (o seu ou de algum amigo/máquina virtual). Rodando no Mac você
gera um app de Mac; no Linux, um binário de Linux. Não dá pra gerar o `.exe`
do Windows a partir de outro sistema.

1. No Windows, instale o Python (python.org) se ainda não tiver.
2. Abra o terminal (cmd/PowerShell) na pasta do projeto.
3. `pip install -r requirements.txt`
4. Rode `build_exe.bat` (duplo clique também funciona).
5. O executável final fica em `dist\JokenpoChallenge.exe`.
6. Mande esse único arquivo pros seus amigos — não precisa instalar Python
   nem pygame na máquina deles, é só dar dois cliques.

No Mac/Linux o processo é o mesmo, usando `build_exe.sh` em vez do `.bat`.

### Alternativa: jogar no navegador (zero instalação, qualquer SO)

Se quiser que os amigos joguem sem baixar nenhum arquivo — só abrindo um
link no navegador — dá pra compilar o jogo para WebAssembly com a ferramenta
[pygbag](https://pypi.org/project/pygbag/) e hospedar de graça no
[itch.io](https://itch.io) ou GitHub Pages. É mais trabalho de configurar
uma vez, mas depois é só mandar um link.
