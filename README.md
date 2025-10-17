Floresta Encantada - Jogo de Aventura Top-Down Um jogo de aventura em estilo top-down desenvolvido em Python com Pygame, onde o jogador explora diferentes mapas, coleta armas, derrota inimigos e enfrenta bosses finais.

Feito por: Renan Tuma
          Alyson Eugenio
          Matheus Azevedo


🎮 Sobre o Jogo O jogador começa em um mundo aberto (overworld) e deve entrar na casa para escolher sua arma: Espada (guerreiro) ou Cajado Mágico (mago). Cada arma desbloqueia áreas específicas:

Espada: Arena do Guerreiro

Cajado Mágico: Floresta Mágica

Após derrotar todos os inimigos em uma área, o jogador coleta uma chave que permite acessar a Arena do Boss final.

🚀 Requisitos do Sistema Software Necessário Python 3.7 ou superior

Pygame 2.0 ou superior

Instalação das Dependências bash

Instalar Pygame
pip install pygame

Ou se estiver usando conda
conda install pygame Estrutura de Arquivos Necessários text projeto/ ├── main.py # Arquivo principal do jogo ├── imagens/ # Pasta para sprites e texturas │ ├── arvore.png │ ├── pedra.png │ ├── Casa_Madeira.png │ ├── placa.png │ ├── Sword.png │ ├── slash.png │ ├── Staff.png │ ├── cactus.png │ ├── mato.png │ ├── pinheiro.png │ └── Key.png ├── musicas/ # Pasta para trilha sonora │ ├── Musica1.mp3 (ou .wav/.ogg) │ └── Musica2.mp3 (ou .wav/.ogg) 🎵 Formatos de Áudio Suportados MP3 (recomendado)

WAV

OGG

🎯 Como Executar Certifique-se de que todos os arquivos estão na estrutura correta

Execute o jogo:

bash python game.py Ou se estiver em ambiente de desenvolvimento:

bash python3 game.py ⌨️ Controles do Jogo Movimento W / ↑ - Mover para cima

S - Mover para baixo

A  - Mover para esquerda

D - Mover para direita

Ações ESPAÇO - Atacar (quando tiver arma)

H - Ativar/Desativar hitboxes de debug

ESC - Sair do jogo

Sistema de Música M - Mute/Unmute

Aumentar volume
Diminuir volume
Game Over R - Reiniciar jogo

🗺️ Mapas do Jogo

Overworld Mapa principal com casa, portais e entradas
Música: Musica1

House Interior Onde o jogador escolhe sua arma permanente
Música: Musica1

Warrior Arena Disponível apenas para portadores da espada
Inimigos: Guerreiros

Recompensa: Chave do Guerreiro

Música: Musica2

Forest Magic Disponível apenas para portadores do cajado
Inimigos: Magos

Recompensa: Chave do Mago

Música: Musica2

Boss Arena Área final que requer chave para acessar
Boss diferente dependendo da arma escolhida

Música: Musica2

⚔️ Sistema de Combate Com Espada Ataque corpo a corpo

Cooldown de 0.5 segundos

Efeito visual de slash

Com Cajado Mágico Projéteis à distância

Múltiplos feitiços simultâneos

Dano contra inimigos magos

🏥 Sistema de Vida Vida inicial: 5 pontos

Inimigos comuns: 1 de dano

Boss: 2 de dano

Invulnerabilidade: 2 segundos após levar dano

🎮 Progressão do Jogo Início: Overworld → Casa

Escolha de Arma: Espada OU Cajado (permanente)

Área Específica:

Espada → Warrior Arena

Cajado → Forest Magic

Chave: Derrotar todos inimigos para obter chave

Boss Final: Usar chave para acessar Boss Arena

Vitória: Derrotar o boss

🐛 Solução de Problemas Erro: "Arquivo não encontrado" Verifique se as pastas imagens/ e musicas/ existem

Confirme os nomes dos arquivos (case-sensitive em alguns sistemas)

Erro: "No module named 'pygame'" bash pip install --upgrade pygame Música não toca Verifique se os arquivos de música estão nos formatos suportados

Teste o volume do sistema

Confirme permissões de leitura dos arquivos

Performance ruim Reduza a resolução nas configurações

Feche outros aplicativos

Verifique se há processos Python antigos em execução

🛠️ Desenvolvimento Estrutura do Código Principal Config: Configurações gerais do jogo

Player: Controle do jogador e sistema de combate

Enemy: Inimigos (Mago, Guerreiro, Boss)

Camera: Sistema de câmera suave

TileRenderer: Renderização de mapas e sprites

Game: Loop principal e gerenciamento de estado

Personalização Modifique config.TILE_SIZE para alterar o zoom

Ajuste config.PLAYER_SPEED para mudar velocidade

Edite os mapas nas variáveis no início do código

📝 Notas Importantes A escolha de arma é permanente durante a partida

É necessário coletar a chave para acessar o boss final

O jogo salva automaticamente chaves coletadas

Use H para debug visual de colisões

🎊 Finalização Ao derrotar o boss final, o jogador vê uma tela de vitória e retorna automaticamente ao overworld após 5 segundos.

Divirta-se explorando a Floresta Encantada! 🌳✨
