# Controles de Volume Individual - Musickera

## 🎧 Funcionalidades Implementadas

### 1. **Volume Master**
- Controle principal de volume que afeta todos os canais
- Slider com design Material UI
- Exibição do valor em tempo real (0-100%)

### 2. **Volume Individual por Canal**
- **Canal Esquerdo (D)**: Controle independente do volume do fone esquerdo
- **Canal Direito (R)**: Controle independente do volume do fone direito
- Ícones estilizados com design Material UI
- Controles independentes que não afetam o outro canal

### 3. **Controle de Balance**
- Slider para ajustar o balance entre os canais esquerdo e direito
- Valores de -100 (totalmente esquerdo) a +100 (totalmente direito)
- Indicador visual: D (esquerdo), C (centro), R (direito)

### 4. **Presets de Volume**
- Botões de acesso rápido para volumes comuns: 25%, 50%, 75%, 100%
- Aplicação instantânea de configurações predefinidas
- Indicador visual do preset ativo

### 5. **Botão de Teste**
- Função para testar os canais de áudio
- Gera um tom de teste para verificar o funcionamento

### 6. **🆕 Controle de Visibilidade**
- **Botão Toggle**: Esconder/mostrar todos os controles de volume
- **Posicionamento**: Botão flutuante no canto superior direito
- **Estados Visuais**: Verde (visível) / Vermelho (escondido)
- **Ícones**: ⚙️ Settings (avançado) / 🎛️ Tune (simples)
- **Persistência**: Lembra o estado entre sessões
- **Atalho de Teclado**: Ctrl + V para alternar
- **Auto-hide**: Controles aparecem temporariamente quando volume é alterado

## 🎨 Design Material UI

### Características Visuais:
- **Gradientes**: Uso de gradientes verdes (#1DB954 → #1ed760)
- **Backdrop Filter**: Efeito de blur para transparência
- **Animações**: Transições suaves e hover effects
- **Ícones**: Material Symbols Rounded para consistência
- **Responsividade**: Adaptação para dispositivos móveis

### Elementos Estilizados:
- Sliders com thumb personalizado
- Botões com hover effects
- Ícones de fone com gradiente circular
- Containers com bordas arredondadas e sombras
- **Botão Toggle**: Circular com gradiente e animações

## 🔧 Funcionalidades Técnicas

### Web Audio API:
- **AudioContext**: Para processamento de áudio em tempo real
- **ChannelSplitter**: Separação dos canais esquerdo e direito
- **GainNode**: Controle individual de ganho por canal
- **Balance Control**: Aplicação matemática do balance

### JavaScript Features:
- Controle em tempo real dos volumes
- Persistência de configurações
- Event listeners otimizados
- Tratamento de erros e fallbacks
- **Sistema de Toggle**: Controle de visibilidade com localStorage

## 📱 Responsividade

### Mobile (< 768px):
- Controles compactos
- Fontes menores
- Espaçamento reduzido
- Botões de preset em múltiplas linhas
- **Botão Toggle**: Tamanho reduzido para mobile

### Desktop (> 768px):
- Layout expandido
- Controles maiores
- Melhor espaçamento
- Efeitos hover completos

## 🎵 Como Usar

1. **Volume Master**: Ajuste o volume geral
2. **Canal D (Esquerdo)**: Controle o volume do fone esquerdo
3. **Canal R (Direito)**: Controle o volume do fone direito
4. **Balance**: Ajuste a distribuição entre os canais
5. **Presets**: Use os botões para configurações rápidas
6. **Test**: Clique em "Test" para verificar os canais
7. **🆕 Toggle**: Clique no botão circular para esconder/mostrar controles
8. **🆕 Atalho**: Use Ctrl + V para alternar visibilidade

## 🎛️ Controle de Visibilidade

### Funcionalidades:
- **Botão Toggle**: Posicionado no canto superior direito
- **Estados**: 
  - 🟢 Verde: Controles visíveis
  - 🔴 Vermelho: Controles escondidos
- **Persistência**: Estado salvo no localStorage
- **Auto-revelação**: Controles aparecem quando volume é alterado
- **Auto-hide**: Controles escondem automaticamente após 5 segundos
- **Atalho**: Ctrl + V para alternar rapidamente

### Comportamento:
1. Clique no botão toggle para esconder/mostrar
2. Quando escondido, controles aparecem temporariamente ao alterar volume
3. Estado é lembrado entre sessões do navegador
4. Atalho de teclado disponível para acesso rápido

## 🔮 Próximas Melhorias

- [x] **Botão para esconder/mostrar controles de volume**
- [ ] Salvar configurações no localStorage
- [ ] Perfis de volume personalizados
- [ ] Equalizador integrado
- [ ] Visualização de forma de onda
- [ ] Controles por teclado (atalhos)
- [ ] Integração com fones Bluetooth
- [ ] Animações mais suaves
- [ ] Temas personalizáveis

---

**Desenvolvido com ❤️ para o Musickera**

