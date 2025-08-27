# ⚡ Prompts Rápidos para GitHub Copilot

## 🎯 Prompt Universal (Cole e Use)

```
Você tem acesso ao MCP Code Analyzer com detecção automática avançada. Para qualquer código que eu mostrar:

1. Use @code-analyzer analyze_and_generate_complete automaticamente
2. Linguagem detectada automaticamente (Python, Java, JavaScript)
3. Framework selecionado automaticamente (Python→pytest, Java→junit5, JS→jest)
4. Apresente resumo da análise (complexidade, estrutura, pontos de atenção)
5. Se eu pedir testes, execute o prompt gerado e entregue código pronto
6. Se eu pedir melhorias, sugira baseado na análise de fluxo
7. Para Java: considere modificadores, anotações e exceções automaticamente

Seja direto, prático e sempre use as ferramentas MCP como base para suas respostas.
```

## 🚀 Comandos Instantâneos

### Para Análise Rápida
```
Análise: @code-analyzer analyze_function_static

[SEU CÓDIGO AQUI]

Me dê os 3 pontos mais importantes sobre esta função/método.
```

### Para Testes Completos (RECOMENDADO)
```
Testes completos: @code-analyzer analyze_and_generate_complete

[SEU CÓDIGO AQUI]

Detecta linguagem automaticamente e usa framework padrão.
Execute o prompt e me entregue os testes prontos para usar.
```

### Para Verificar Complexidade
```
Complexidade: @code-analyzer summarize_function_flow

[SEU CÓDIGO AQUI]

Esta função/método está muito complexo? Sugira simplificações.
```

### Para Forçar Linguagem/Framework Específico
```
@code-analyzer analyze_and_generate_complete language="[python|java|javascript]" framework="[pytest|junit5|jest]"

[SEU CÓDIGO AQUI]

Use este prompt gerado para criar testes otimizados.
```

### Para Java Específico
```
Java especializado: @code-analyzer analyze_and_generate_java_complete

[SEU CÓDIGO JAVA AQUI]

Análise otimizada para modificadores, anotações e exceções Java.
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

### Python (Auto-Detectado)
```
Python + MCP: @code-analyzer analyze_and_generate_complete

[CÓDIGO PYTHON]

Framework: pytest (automático)
Extras:
- Use type hints
- Considere async/await se aplicável  
- Sugira uso de dataclasses/pydantic se útil
- Mock para requests/db calls
```

### Java (Auto-Detectado + Melhorado)
```
Java + MCP: @code-analyzer analyze_and_generate_complete

[CÓDIGO JAVA]

Framework: junit5 (automático)
Recursos avançados:
- Detecta modificadores automaticamente (public, static, etc.)
- Analisa anotações (@Override, @Test, etc.)
- Mapeia exceções declaradas
- Siga convenções Spring se aplicável
- Use Mockito para mocks
- Considere @ParameterizedTest para múltiplos casos
- Valide exceptions com assertThrows
```

### JavaScript (Auto-Detectado)
```
JavaScript + MCP: @code-analyzer analyze_and_generate_complete

[CÓDIGO JS]

Framework: jest (automático)
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

# Testes instantâneos com auto-detecção
"@code-analyzer analyze_and_generate_complete [CÓDIGO] → detecta linguagem + testes"

# Check de complexidade
"@code-analyzer summarize_function_flow [CÓDIGO] → muito complexo?"

# Pipeline completo com auto-detecção
"@code-analyzer analyze_and_generate_complete [CÓDIGO] → análise + testes"

# Java especializado
"@code-analyzer analyze_and_generate_java_complete [CÓDIGO JAVA] → análise otimizada"

# Forçar framework específico
"@code-analyzer analyze_and_generate_complete language='java' framework='junit5' [CÓDIGO]"

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

1. **Auto-detecção avançada**: analyze_and_generate_complete detecta linguagem e framework automaticamente
2. **Use análise completa** como ponto de partida padrão - mais eficiente que ferramentas individuais
3. **Java melhorado**: Suporte completo para modificadores, anotações e exceções
4. **Execute prompts gerados** - não apenas copie
5. **Combine com seu conhecimento** - MCP é ferramenta, não substituto
6. **Itere baseado em feedback** - use análises para melhorar código
7. **Frameworks automáticos**: Python→pytest, Java→junit5, JS→jest
8. **Forçe apenas quando necessário** - especifique language/framework apenas em casos especiais

**🚀 Cole qualquer um desses prompts no Copilot e comece a usar imediatamente!**