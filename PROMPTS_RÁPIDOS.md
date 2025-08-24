# ⚡ Prompts Rápidos para GitHub Copilot

## 🎯 Prompt Universal (Cole e Use)

```
Você tem acesso ao MCP Code Analyzer. Para qualquer código que eu mostrar:

1. Use @code-analyzer analyze_and_generate_complete automaticamente
2. Apresente resumo da análise (complexidade, estrutura, pontos de atenção)
3. Se eu pedir testes, execute o prompt gerado e entregue código pronto
4. Se eu pedir melhorias, sugira baseado na análise de fluxo
5. Sempre identifique a linguagem e use o framework apropriado (pytest/junit/jest)

Seja direto, prático e sempre use as ferramentas MCP como base para suas respostas.
```

## 🚀 Comandos Instantâneos

### Para Análise Rápida
```
Analise: @code-analyzer analyze_function_static

[SEU CÓDIGO AQUI]

Me dê os 3 pontos mais importantes sobre esta função.
```

### Para Testes Completos
```
Testes completos: @code-analyzer analyze_and_generate_complete

[SEU CÓDIGO AQUI]

Execute o prompt e me entregue os testes prontos para usar.
```

### Para Verificar Complexidade
```
Complexidade: @code-analyzer summarize_function_flow

[SEU CÓDIGO AQUI]

Esta função está muito complexa? Sugira simplificações.
```

### Para Prompt Personalizado
```
@code-analyzer generate_test_prompt language="[python|java|javascript]" framework="[pytest|junit|jest]"

[SEU CÓDIGO AQUI]

Use este prompt gerado para criar testes otimizados.
```

## 🎪 Templates por Cenário

### 📝 Code Review
```
Code Review usando MCP:

@code-analyzer analyze_and_generate_complete

[CÓDIGO PARA REVIEW]

Como reviewer experiente:
1. Avalie qualidade (1-10)
2. Identifique problemas críticos
3. Sugira 2-3 melhorias prioritárias
4. Aprove ou rejeite com justificativa
```

### 🔧 Debugging
```
Debugging assistido:

@code-analyzer analyze_function_static

[CÓDIGO COM BUG]

Esta função tem um bug. Use a análise para:
1. Identificar possíveis causas
2. Sugerir pontos de investigação
3. Propor correções
```

### 🎯 Refatoração Express
```
Refatoração rápida:

@code-analyzer summarize_function_flow

[CÓDIGO A REFATORAR]

Complexidade atual: [X]. Meta: reduzir para [Y].
Mantenha comportamento, melhore legibilidade.
```

### 🧪 TDD Assistant
```
TDD com MCP:

1. @code-analyzer analyze_function_static (para função existente)
   OU descreva função desejada

2. Gere testes primeiro
3. Implemente função para passar nos testes
4. Refatore se necessário

Foco: testes que guiam o design.
```

## 🎨 Customizações por Linguagem

### Python
```
Python + MCP: @code-analyzer analyze_and_generate_complete language="python" framework="pytest"

[CÓDIGO PYTHON]

Extras:
- Use type hints
- Considere async/await se aplicável  
- Sugira uso de dataclasses/pydantic se útil
- Mock para requests/db calls
```

### Java
```
Java + MCP: @code-analyzer analyze_and_generate_complete language="java" framework="junit"

[CÓDIGO JAVA]

Extras:
- Siga convenções Spring se aplicável
- Use Mockito para mocks
- Considere @ParameterizedTest para múltiplos casos
- Valide exceptions com assertThrows
```

### JavaScript
```
JavaScript + MCP: @code-analyzer analyze_and_generate_complete language="javascript" framework="jest"

[CÓDIGO JS]

Extras:
- Mock APIs com jest.mock()
- Teste async functions adequadamente
- Use describe/it para organização
- Considere snapshot testing se UI
```

## ⚡ One-Liners Úteis

```bash
# Análise express
"@code-analyzer analyze_function_static [CÓDIGO] → resumo em 3 pontos"

# Testes instantâneos  
"@code-analyzer generate_test_prompt [CÓDIGO] → execute e entregue testes"

# Check de complexidade
"@code-analyzer summarize_function_flow [CÓDIGO] → muito complexo?"

# Pipeline completo
"@code-analyzer analyze_and_generate_complete [CÓDIGO] → análise + testes"

# Comparação
"Compare complexidade: @code-analyzer summarize_function_flow [CÓDIGO1] vs [CÓDIGO2]"
```

## 🎛️ Configurações Personalizadas

### Para Equipe Junior
```
Modo Educativo: Use MCP + explique conceitos básicos
- Complexidade ciclomática significa...
- Este padrão é problemático porque...
- Testes devem cobrir estes cenários porque...
```

### Para Equipe Senior  
```
Modo Expert: Use MCP + foque em trade-offs
- Performance vs legibilidade
- Patterns alternativos
- Impactos arquiteturais
- Otimizações específicas
```

### Para Code Review
```
Modo Reviewer: Use MCP + critérios rigorosos
- Segurança, performance, manutenibilidade
- Aderência a padrões do projeto
- Cobertura de casos extremos
- Documentação adequada
```

## 🔄 Workflows Integrados

### Desenvolvimento Iterativo
```
1. Escreva função básica
2. "@code-analyzer analyze_function_static" → avalie estrutura
3. Refine baseado em feedback
4. "@code-analyzer generate_test_prompt" → crie testes
5. Execute testes, ajuste código
6. "@code-analyzer summarize_function_flow" → verifique complexidade final
```

### Manutenção de Código Legado
```
1. "@code-analyzer analyze_and_generate_complete" → entenda código existente  
2. Crie testes de regressão baseados na análise
3. Refatore incrementalmente
4. Valide com testes a cada mudança
5. Documente melhorias implementadas
```

### Code Review Automatizado
```
1. Para cada função no PR:
2. "@code-analyzer analyze_function_static" → estrutura OK?
3. "@code-analyzer summarize_function_flow" → complexidade aceitável?  
4. Gere testes se não existirem
5. Compile feedback estruturado
```

---

## 💡 Pro Tips

1. **Sempre especifique linguagem** para melhores resultados
2. **Use análise completa** como ponto de partida padrão  
3. **Execute prompts gerados** - não apenas copie
4. **Combine com seu conhecimento** - MCP é ferramenta, não substituto
5. **Itere baseado em feedback** - use análises para melhorar código
6. **Mantenha contexto** - ferramentas MCP são mais precisas com contexto claro

**🚀 Cole qualquer um desses prompts no Copilot e comece a usar imediatamente!**