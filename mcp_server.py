import ast
import re
import json
from typing import Dict, List, Any, Optional, Union
from mcp.server.fastmcp import FastMCP

# Inicializar o servidor MCP
mcp = FastMCP("Code Analysis MCP Server")

class StaticAnalyzer:
    """Analisador estático de código Python"""
    
    def analyze_function(self, code: str) -> Dict[str, Any]:
        """Extrai informações estruturais de uma função"""
        try:
            tree = ast.parse(code)
            function_node = None
            
            # Encontrar a primeira função no código
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    function_node = node
                    break
            
            if not function_node:
                raise ValueError("Nenhuma função encontrada no código")
            
            return {
                "signature": self._extract_signature(function_node),
                "parameters": self._extract_parameters(function_node),
                "return_type": self._extract_return_type(function_node),
                "dependencies": self._extract_dependencies(tree),
                "decorators": self._extract_decorators(function_node)
            }
        except Exception as e:
            return {"error": f"Erro na análise: {str(e)}"}
    
    def _extract_signature(self, node: ast.FunctionDef) -> str:
        """Extrai a assinatura completa da função"""
        args = []
        
        # Argumentos posicionais
        for arg in node.args.args:
            arg_str = arg.arg
            if arg.annotation:
                arg_str += f": {ast.unparse(arg.annotation)}"
            args.append(arg_str)
        
        # Argumentos com valores padrão
        defaults = node.args.defaults
        default_offset = len(args) - len(defaults)
        for i, default in enumerate(defaults):
            args[default_offset + i] += f" = {ast.unparse(default)}"
        
        # *args
        if node.args.vararg:
            vararg = f"*{node.args.vararg.arg}"
            if node.args.vararg.annotation:
                vararg += f": {ast.unparse(node.args.vararg.annotation)}"
            args.append(vararg)
        
        # **kwargs
        if node.args.kwarg:
            kwarg = f"**{node.args.kwarg.arg}"
            if node.args.kwarg.annotation:
                kwarg += f": {ast.unparse(node.args.kwarg.annotation)}"
            args.append(kwarg)
        
        signature = f"{node.name}({', '.join(args)})"
        
        # Tipo de retorno
        if node.returns:
            signature += f" -> {ast.unparse(node.returns)}"
        
        return signature
    
    def _extract_parameters(self, node: ast.FunctionDef) -> List[Dict[str, Any]]:
        """Extrai informações detalhadas dos parâmetros"""
        params = []
        
        for arg in node.args.args:
            param_info = {
                "name": arg.arg,
                "type": ast.unparse(arg.annotation) if arg.annotation else "Any",
                "has_default": False,
                "default_value": None
            }
            params.append(param_info)
        
        # Adicionar valores padrão
        defaults = node.args.defaults
        default_offset = len(params) - len(defaults)
        for i, default in enumerate(defaults):
            params[default_offset + i]["has_default"] = True
            params[default_offset + i]["default_value"] = ast.unparse(default)
        
        return params
    
    def _extract_return_type(self, node: ast.FunctionDef) -> str:
        """Extrai o tipo de retorno da função"""
        if node.returns:
            return ast.unparse(node.returns)
        return "Any"
    
    def _extract_dependencies(self, tree: ast.AST) -> Dict[str, List[str]]:
        """Extrai dependências internas e externas"""
        imports = []
        internal_calls = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports.append(f"{module}.{alias.name}")
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    internal_calls.append(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    internal_calls.append(ast.unparse(node.func))
        
        return {
            "imports": list(set(imports)),
            "internal_calls": list(set(internal_calls))
        }
    
    def _extract_decorators(self, node: ast.FunctionDef) -> List[str]:
        """Extrai decoradores da função"""
        return [ast.unparse(decorator) for decorator in node.decorator_list]


class FlowSummarizer:
    """Resumidor de fluxo de execução"""
    
    def summarize_flow(self, code: str) -> Dict[str, Any]:
        """Cria um mapa minimalista do fluxo da função"""
        try:
            tree = ast.parse(code)
            function_node = None
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    function_node = node
                    break
            
            if not function_node:
                raise ValueError("Nenhuma função encontrada no código")
            
            flow_map = self._analyze_flow(function_node.body)
            
            return {
                "flow_map": flow_map,
                "complexity_score": self._calculate_complexity(flow_map),
                "summary": self._generate_flow_summary(flow_map)
            }
        except Exception as e:
            return {"error": f"Erro na análise de fluxo: {str(e)}"}
    
    def _analyze_flow(self, body: List[ast.stmt]) -> List[Dict[str, Any]]:
        """Analisa o fluxo de controle do código"""
        flow_elements = []
        
        for node in body:
            if isinstance(node, ast.If):
                flow_elements.append({
                    "type": "conditional",
                    "condition": ast.unparse(node.test),
                    "has_else": len(node.orelse) > 0,
                    "nested_flow": self._analyze_flow(node.body)
                })
                if node.orelse:
                    flow_elements.append({
                        "type": "else",
                        "nested_flow": self._analyze_flow(node.orelse)
                    })
            
            elif isinstance(node, ast.For):
                flow_elements.append({
                    "type": "loop_for",
                    "target": ast.unparse(node.target),
                    "iter": ast.unparse(node.iter),
                    "nested_flow": self._analyze_flow(node.body)
                })
            
            elif isinstance(node, ast.While):
                flow_elements.append({
                    "type": "loop_while",
                    "condition": ast.unparse(node.test),
                    "nested_flow": self._analyze_flow(node.body)
                })
            
            elif isinstance(node, ast.Try):
                flow_elements.append({
                    "type": "try_except",
                    "exceptions": [ast.unparse(handler.type) if handler.type else "Exception" 
                                 for handler in node.handlers],
                    "has_finally": len(node.finalbody) > 0,
                    "nested_flow": self._analyze_flow(node.body)
                })
            
            elif isinstance(node, ast.Raise):
                flow_elements.append({
                    "type": "exception_raise",
                    "exception": ast.unparse(node.exc) if node.exc else "Re-raise"
                })
            
            elif isinstance(node, ast.Return):
                flow_elements.append({
                    "type": "return",
                    "value": ast.unparse(node.value) if node.value else "None"
                })
        
        return flow_elements
    
    def _calculate_complexity(self, flow_map: List[Dict[str, Any]]) -> int:
        """Calcula complexidade ciclomática simplificada"""
        complexity = 1  # Base complexity
        
        for element in flow_map:
            if element["type"] in ["conditional", "loop_for", "loop_while"]:
                complexity += 1
            elif element["type"] == "try_except":
                complexity += len(element["exceptions"])
            
            if "nested_flow" in element:
                complexity += self._calculate_complexity(element["nested_flow"]) - 1
        
        return complexity
    
    def _generate_flow_summary(self, flow_map: List[Dict[str, Any]]) -> str:
        """Gera resumo textual do fluxo"""
        summary_parts = []
        
        for element in flow_map:
            if element["type"] == "conditional":
                summary_parts.append(f"IF({element['condition']})")
            elif element["type"] == "loop_for":
                summary_parts.append(f"FOR({element['target']} in {element['iter']})")
            elif element["type"] == "loop_while":
                summary_parts.append(f"WHILE({element['condition']})")
            elif element["type"] == "try_except":
                exceptions = ", ".join(element["exceptions"])
                summary_parts.append(f"TRY-EXCEPT({exceptions})")
            elif element["type"] == "exception_raise":
                summary_parts.append(f"RAISE({element['exception']})")
            elif element["type"] == "return":
                summary_parts.append(f"RETURN({element['value']})")
        
        return " -> ".join(summary_parts)


class PromptGenerator:
    """Gerador de prompts minimalistas para LLMs"""
    
    def generate_test_prompt(self, static_analysis: Dict[str, Any], 
                           flow_analysis: Dict[str, Any], 
                           language: str = "python", 
                           test_framework: str = "pytest") -> Dict[str, Any]:
        """Gera prompt otimizado para geração de testes unitários"""
        
        # Determinar framework baseado na linguagem se não especificado
        if test_framework == "auto":
            test_framework = "junit" if language.lower() == "java" else "pytest"
        
        prompt_sections = self._build_prompt_sections(static_analysis, flow_analysis)
        
        output_structure = self._get_output_structure(language, test_framework)
        
        final_prompt = self._assemble_final_prompt(prompt_sections, output_structure, language)
        
        return {
            "prompt": final_prompt,
            "metadata": {
                "language": language,
                "framework": test_framework,
                "complexity_score": flow_analysis.get("complexity_score", 1),
                "estimated_tests": self._estimate_test_count(flow_analysis)
            }
        }
    
    def _build_prompt_sections(self, static_analysis: Dict[str, Any], 
                              flow_analysis: Dict[str, Any]) -> Dict[str, str]:
        """Constrói seções do prompt"""
        
        function_info = f"""
FUNÇÃO: {static_analysis.get('signature', 'N/A')}
PARÂMETROS: {self._format_parameters(static_analysis.get('parameters', []))}
RETORNO: {static_analysis.get('return_type', 'Any')}
DEPENDÊNCIAS: {', '.join(static_analysis.get('dependencies', {}).get('imports', []))}
"""
        
        flow_info = f"""
FLUXO: {flow_analysis.get('summary', 'Linear')}
COMPLEXIDADE: {flow_analysis.get('complexity_score', 1)}
CENÁRIOS: {self._extract_test_scenarios(flow_analysis.get('flow_map', []))}
"""
        
        return {
            "function_info": function_info.strip(),
            "flow_info": flow_info.strip()
        }
    
    def _format_parameters(self, parameters: List[Dict[str, Any]]) -> str:
        """Formata parâmetros para o prompt"""
        if not parameters:
            return "Nenhum"
        
        param_strs = []
        for param in parameters:
            param_str = f"{param['name']}: {param['type']}"
            if param['has_default']:
                param_str += f" = {param['default_value']}"
            param_strs.append(param_str)
        
        return ", ".join(param_strs)
    
    def _extract_test_scenarios(self, flow_map: List[Dict[str, Any]]) -> str:
        """Extrai cenários de teste do mapa de fluxo"""
        scenarios = []
        
        for element in flow_map:
            if element["type"] == "conditional":
                scenarios.extend([f"Condição TRUE: {element['condition']}", 
                                f"Condição FALSE: {element['condition']}"])
            elif element["type"] in ["loop_for", "loop_while"]:
                scenarios.extend(["Loop vazio", "Loop com múltiplas iterações"])
            elif element["type"] == "try_except":
                scenarios.extend([f"Exceção: {exc}" for exc in element["exceptions"]])
                scenarios.append("Execução sem exceção")
        
        return "; ".join(scenarios) if scenarios else "Fluxo linear"
    
    def _get_output_structure(self, language: str, framework: str) -> str:
        """Retorna estrutura de saída baseada na linguagem e framework"""
        
        structures = {
            ("python", "pytest"): """
```python
import pytest
from unittest.mock import Mock, patch

class TestFunctionName:
    def test_case_name(self):
        # Arrange
        
        # Act
        
        # Assert
        
    def test_edge_case(self):
        # Test edge cases
        
    def test_exception_handling(self):
        # Test exception scenarios
```""",
            
            ("java", "junit"): """
```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;

class FunctionNameTest {
    
    @BeforeEach
    void setUp() {
        // Setup
    }
    
    @Test
    void testCaseName() {
        // Arrange
        
        // Act
        
        // Assert
    }
    
    @Test
    void testEdgeCase() {
        // Test edge cases
    }
    
    @Test
    void testExceptionHandling() {
        // Test exception scenarios
    }
}
```""",
            
            ("javascript", "jest"): """
```javascript
const { functionName } = require('./module');

describe('functionName', () => {
    test('should handle normal case', () => {
        // Arrange
        
        // Act
        
        // Assert
    });
    
    test('should handle edge cases', () => {
        // Test edge cases
    });
    
    test('should handle errors', () => {
        // Test error scenarios
    });
});
```"""
        }
        
        key = (language.lower(), framework.lower())
        return structures.get(key, structures[("python", "pytest")])
    
    def _assemble_final_prompt(self, sections: Dict[str, str], 
                              output_structure: str, language: str) -> str:
        """Monta o prompt final"""
        
        return f"""Gere testes unitários completos para a seguinte função em {language}:

{sections['function_info']}

{sections['flow_info']}

INSTRUÇÕES:
1. Cubra todos os cenários identificados no fluxo
2. Inclua testes para casos extremos e validação de parâmetros
3. Teste tratamento de exceções quando aplicável
4. Use mocks para dependências externas
5. Mantenha testes independentes e determinísticos

ESTRUTURA DE SAÍDA OBRIGATÓRIA:
{output_structure}

Gere APENAS o código dos testes, sem explicações adicionais."""
    
    def _estimate_test_count(self, flow_analysis: Dict[str, Any]) -> int:
        """Estima número de testes necessários"""
        complexity = flow_analysis.get("complexity_score", 1)
        flow_map = flow_analysis.get("flow_map", [])
        
        # Base: 1 teste para o caso feliz
        test_count = 1
        
        # Adicionar testes baseados na complexidade
        test_count += complexity
        
        # Contar cenários específicos
        for element in flow_map:
            if element["type"] == "conditional":
                test_count += 1  # Teste para else/elif
            elif element["type"] in ["loop_for", "loop_while"]:
                test_count += 1  # Teste para loop vazio
            elif element["type"] == "try_except":
                test_count += len(element["exceptions"])
        
        return min(test_count, 15)  # Limitar a 15 testes por função


# Instanciar as classes
static_analyzer = StaticAnalyzer()
flow_summarizer = FlowSummarizer()
prompt_generator = PromptGenerator()


@mcp.tool()
def analyze_function_static(code: str) -> Dict[str, Any]:
    """
    Ferramenta 1: Analisador Estático
    
    Extrai informações estruturais de uma função:
    - Assinatura completa
    - Parâmetros e tipos
    - Tipo de retorno
    - Dependências internas e externas
    - Decoradores
    
    Args:
        code: Código fonte da função a ser analisada
        
    Returns:
        Dicionário com informações estruturais da função
    """
    return static_analyzer.analyze_function(code)


@mcp.tool()
def summarize_function_flow(code: str) -> Dict[str, Any]:
    """
    Ferramenta 2: Resumidor de Fluxo
    
    Analisa o fluxo de execução da função e cria um mapa minimalista:
    - Estruturas de controle (if/else, loops)
    - Tratamento de exceções
    - Pontos de retorno
    - Complexidade ciclomática
    
    Args:
        code: Código fonte da função a ser analisada
        
    Returns:
        Dicionário com mapa de fluxo e métricas de complexidade
    """
    return flow_summarizer.summarize_flow(code)


@mcp.tool()
def generate_test_prompt(code: str, language: str = "python", 
                        test_framework: str = "pytest") -> Dict[str, Any]:
    """
    Ferramenta 3: Gerador de Prompt Minimalista
    
    Combina análise estática e de fluxo para gerar um prompt otimizado
    para LLMs criarem testes unitários com estrutura de saída fixa.
    
    Args:
        code: Código fonte da função
        language: Linguagem de programação (python, java, javascript)
        test_framework: Framework de teste (pytest, junit, jest, auto)
        
    Returns:
        Dicionário com prompt otimizado e metadados
    """
    # Executar análises
    static_analysis = static_analyzer.analyze_function(code)
    flow_analysis = flow_summarizer.summarize_flow(code)
    
    # Verificar se houve erros nas análises
    if "error" in static_analysis:
        return {"error": f"Erro na análise estática: {static_analysis['error']}"}
    
    if "error" in flow_analysis:
        return {"error": f"Erro na análise de fluxo: {flow_analysis['error']}"}
    
    # Gerar prompt
    return prompt_generator.generate_test_prompt(
        static_analysis, flow_analysis, language, test_framework
    )


@mcp.tool()
def analyze_and_generate_complete(code: str, language: str = "python", 
                                 test_framework: str = "pytest") -> Dict[str, Any]:
    """
    Ferramenta Combinada: Análise Completa e Geração de Prompt
    
    Executa todas as três ferramentas em sequência e retorna
    um relatório completo com análise detalhada e prompt otimizado.
    
    Args:
        code: Código fonte da função
        language: Linguagem de programação
        test_framework: Framework de teste
        
    Returns:
        Relatório completo com todas as análises e prompt final
    """
    static_analysis = static_analyzer.analyze_function(code)
    flow_analysis = flow_summarizer.summarize_flow(code)
    
    if "error" in static_analysis or "error" in flow_analysis:
        return {
            "static_analysis": static_analysis,
            "flow_analysis": flow_analysis,
            "error": "Erro em uma ou mais análises"
        }
    
    prompt_result = prompt_generator.generate_test_prompt(
        static_analysis, flow_analysis, language, test_framework
    )
    
    return {
        "static_analysis": static_analysis,
        "flow_analysis": flow_analysis,
        "prompt_generation": prompt_result,
        "summary": {
            "function_signature": static_analysis.get("signature"),
            "complexity_score": flow_analysis.get("complexity_score"),
            "estimated_tests": prompt_result.get("metadata", {}).get("estimated_tests"),
            "ready_for_llm": True
        }
    }


if __name__ == "__main__":
    mcp.run()
