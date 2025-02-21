# Bot para Minecraft

Bot em Python para Minecraft com movimentação automática e sistema de segurança.

## Instalação no Termux (Android)

1. Instale o Termux pela Play Store ou F-Droid
2. Abra o Termux e execute:
   ```bash
   curl -o instalar_termux.sh https://raw.githubusercontent.com/seu_usuario/minecraft_bot/main/instalar_termux.sh
   chmod +x instalar_termux.sh
   ./instalar_termux.sh
   ```

## Instalação no PC

1. **Requisitos**
   - Python 3.7 ou superior
   - Node.js (versão 14 ou superior)
   - Conexão com internet

2. **Instale as dependências**
   ```bash
   npm install mineflayer mineflayer-pathfinder
   pip install javascript pytz requests
   ```

## Configuração

1. Abra o arquivo `config/configuracoes.py`
2. Configure:
   ```python
   # Endereço do servidor
   SERVIDOR = "endereco.do.servidor"

   # Porta do servidor (padrão: 25565)
   PORTA = 25565

   # Nome do bot
   NOME_BOT = "MeuBot"

   # Tipo de autenticação ('offline' para servidor pirata)
   TIPO_AUTENTICACAO = "offline"

   # Versão do Minecraft
   VERSAO_MINECRAFT = "1.8.8"
   ```

## Como Usar

1. **Iniciar o bot**
   - No PC: `python iniciar_bot.py`
   - No Termux: `./executar_bot.sh`

2. **Comandos do Painel de Controle**
   - `start` - Inicia o bot
   - `stop` - Para o bot
   - `restart` - Reinicia o bot
   - `status` - Mostra status atual
   - `config` - Mostra configurações
   - `servidor` - Muda servidor de conexão
   - `help` - Mostra todos os comandos
   - `exit` - Sai do painel

3. **Comandos In-Game**
   - `!vem` - Bot vai até você
   - `!parar` - Para movimentos
   - `!ir x y z` - Vai às coordenadas
   - `!pular` - Faz o bot pular
   - `!status` - Mostra posição atual
   - `!olhar jogador` - Olha para o jogador
   - `!inventario` - Mostra inventário
   - `!dima` - 64 diamantes (Stackzzx)
   - `!criativo` - Modo criativo
   - `!skin url` - Muda skin
   - `!nome novo_nome` - Muda nome (Stackzzx)

## Solução de Problemas

1. **Bot não conecta?**
   - Verifique conexão com servidor
   - Confira endereço/porta
   - Verifique versão do Minecraft

2. **Erro de autenticação?**
   - Para servidores piratas: `TIPO_AUTENTICACAO = "offline"`
   - Para originais: `TIPO_AUTENTICACAO = "online"`

3. **Outros problemas?**
   - Veja logs em `minecraft_bot.log`
   - Reinstale dependências
   - Reinicie o bot

## Recursos de Segurança

- Prevenção de quedas
- Desvio de perigos
- Parada automática
- Reconexão automática

## Direitos Reservados

Desenvolvido por Stackzzx

Instagram: @pedroz.jpg