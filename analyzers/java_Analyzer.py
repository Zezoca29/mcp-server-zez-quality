import re
import json
from typing import Dict, List, Any, Optional, Union


class JavaStaticAnalyzer:
    """Analisador estático de código Java"""
    
    def analyze_method(self, code: str) -> Dict[str, Any]:
        """Extrai informações estruturais de um método Java"""
        try:
            # Limpar código e encontrar método
            cleaned_code = self._clean_code(code)
            method_match = self._find_method(cleaned_code)
            
            if not method_match:
                raise ValueError("Nenhum método encontrado no código")
            
            method_signature = method_match.group(0)
            method_body = self._extract_method_body(cleaned_code, method_match.end())
            
            return {
                "signature": self._extract_signature(method_signature),
                "modifiers": self._extract_modifiers(method_signature),
                "parameters": self._extract_parameters(method_signature),
                "return_type": self._extract_return_type(method_signature),
                "exceptions": self._extract_exceptions(method_signature),
                "dependencies": self._extract_dependencies(code),
                "annotations": self._extract_annotations(method_signature)
            }
        except Exception as e:
            return {"error": f"Erro na análise: {str(e)}"}
    
    def _clean_code(self, code: str) -> str:
        """Remove comentários e normaliza espaços"""
        # Remove comentários de linha
        code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
        # Remove comentários de bloco
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        # Normaliza espaços
        code = re.sub(r'\s+', ' ', code).strip()
        return code
    
    def _find_method(self, code: str):
        """Encontra a declaração do método"""
        # Padrão para métodos Java
        method_pattern = r'(?:@\w+\s*)*(?:public|private|protected|static|final|abstract|synchronized|native|strictfp|\s)*\s+(?:<[^>]*>\s+)?(?!class|interface|enum)(\w+(?:<[^>]*>)?|\w+\[\]|\w+\.\.\.)\s+(\w+)\s*\([^)]*\)(?:\s+throws\s+[^{]+)?'
        return re.search(method_pattern, code)
    
    def _extract_method_body(self, code: str, start_pos: int) -> str:
        """Extrai o corpo do método"""
        # Encontra a abertura da chave
        brace_start = code.find('{', start_pos)
        if brace_start == -1:
            return ""
        
        # Conta chaves para encontrar o final
        brace_count = 1
        pos = brace_start + 1
        
        while pos < len(code) and brace_count > 0:
            if code[pos] == '{':
                brace_count += 1
            elif code[pos] == '}':
                brace_count -= 1
            pos += 1
        
        return code[brace_start:pos] if brace_count == 0 else ""
    
    def _extract_signature(self, method_signature: str) -> str:
        """Extrai a assinatura limpa do método"""
        # Remove anotações e normaliza
        signature = re.sub(r'@\w+(\([^)]*\))?\s*', '', method_signature)
        return signature.strip()
    
    def _extract_modifiers(self, method_signature: str) -> List[str]:
        """Extrai modificadores de acesso e outros"""
        modifiers = []
        modifier_pattern = r'\b(public|private|protected|static|final|abstract|synchronized|native|strictfp)\b'
        matches = re.findall(modifier_pattern, method_signature)
        return matches
    
    def _extract_parameters(self, method_signature: str) -> List[Dict[str, Any]]:
        """Extrai informações dos parâmetros"""
        # Encontra os parâmetros entre parênteses
        params_match = re.search(r'\(([^)]*)\)', method_signature)
        if not params_match or not params_match.group(1).strip():
            return []
        
        params_str = params_match.group(1)
        parameters = []
        
        # Divide por vírgulas, considerando generics
        param_parts = self._split_parameters(params_str)
        
        for param in param_parts:
            param = param.strip()
            if not param:
                continue
                
            # Extrai anotações
            annotations = re.findall(r'@\w+(?:\([^)]*\))?', param)
            param = re.sub(r'@\w+(?:\([^)]*\))?\s*', '', param)
            
            # Divide em tipo e nome
            parts = param.split()
            if len(parts) >= 2:
                param_type = ' '.join(parts[:-1])
                param_name = parts[-1]
                
                parameters.append({
                    "name": param_name,
                    "type": param_type,
                    "annotations": annotations,
                    "is_varargs": "..." in param_type
                })
        
        return parameters
    
    def _split_parameters(self, params_str: str) -> List[str]:
        """Divide parâmetros considerando generics"""
        parameters = []
        current_param = ""
        bracket_count = 0
        
        for char in params_str:
            if char == '<':
                bracket_count += 1
            elif char == '>':
                bracket_count -= 1
            elif char == ',' and bracket_count == 0:
                parameters.append(current_param.strip())
                current_param = ""
                continue
            
            current_param += char
        
        if current_param.strip():
            parameters.append(current_param.strip())
        
        return parameters
    
    def _extract_return_type(self, method_signature: str) -> str:
        """Extrai o tipo de retorno"""
        # Remove anotações
        clean_sig = re.sub(r'@\w+(\([^)]*\))?\s*', '', method_signature)
        
        # Padrão para capturar tipo de retorno
        return_pattern = r'(?:public|private|protected|static|final|abstract|synchronized|native|strictfp|\s)*\s*(?:<[^>]*>\s+)?(\w+(?:<[^>]*>)?|\w+\[\]|\w+\.\.\.)\s+\w+\s*\('
        match = re.search(return_pattern, clean_sig)
        
        if match:
            return match.group(1)
        return "void"
    
    def _extract_exceptions(self, method_signature: str) -> List[str]:
        """Extrai exceções declaradas"""
        throws_match = re.search(r'throws\s+([^{]+)', method_signature)
        if not throws_match:
            return []
        
        exceptions_str = throws_match.group(1).strip()
        return [exc.strip() for exc in exceptions_str.split(',')]
    
    def _extract_dependencies(self, code: str) -> Dict[str, List[str]]:
        """Extrai dependências (imports e chamadas)"""
        imports = []
        method_calls = []
        
        # Extrair imports
        import_pattern = r'import\s+(?:static\s+)?([^;]+);'
        imports = re.findall(import_pattern, code)
        
        # Extrair chamadas de método
        call_pattern = r'(\w+(?:\.\w+)*)\s*\('
        method_calls = list(set(re.findall(call_pattern, code)))
        
        return {
            "imports": imports,
            "method_calls": method_calls
        }
    
    def _extract_annotations(self, method_signature: str) -> List[Dict[str, Any]]:
        """Extrai anotações do método"""
        annotations = []
        annotation_pattern = r'@(\w+)(?:\(([^)]*)\))?'
        matches = re.findall(annotation_pattern, method_signature)
        
        for name, params in matches:
            annotation = {"name": name}
            if params:
                annotation["parameters"] = params
            annotations.append(annotation)
        
        return annotations


class JavaFlowSummarizer:
    """Resumidor de fluxo de execução para Java"""
    
    def summarize_flow(self, code: str) -> Dict[str, Any]:
        """Cria um mapa do fluxo de execução do método Java"""
        try:
            cleaned_code = self._clean_code(code)
            method_body = self._extract_method_body(cleaned_code)
            
            if not method_body:
                raise ValueError("Corpo do método não encontrado")
            
            flow_map = self._analyze_flow(method_body)
            
            return {
                "flow_map": flow_map,
                "complexity_score": self._calculate_complexity(flow_map),
                "summary": self._generate_flow_summary(flow_map)
            }
        except Exception as e:
            return {"error": f"Erro na análise de fluxo: {str(e)}"}
    
    def _clean_code(self, code: str) -> str:
        """Remove comentários"""
        code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        return code
    
    def _extract_method_body(self, code: str) -> str:
        """Extrai apenas o corpo do método"""
        brace_start = code.find('{')
        if brace_start == -1:
            return code
        
        brace_count = 1
        pos = brace_start + 1
        
        while pos < len(code) and brace_count > 0:
            if code[pos] == '{':
                brace_count += 1
            elif code[pos] == '}':
                brace_count -= 1
            pos += 1
        
        return code[brace_start + 1:pos - 1] if brace_count == 0 else code[brace_start + 1:]
    
    def _analyze_flow(self, body: str) -> List[Dict[str, Any]]:
        """Analisa estruturas de controle no código Java"""
        flow_elements = []
        
        # Analisar if/else
        if_pattern = r'if\s*\([^)]+\)'
        if_matches = re.finditer(if_pattern, body)
        for match in if_matches:
            condition = match.group(0)[2:].strip('()')
            flow_elements.append({
                "type": "conditional",
                "condition": condition,
                "has_else": self._has_corresponding_else(body, match.start())
            })
        
        # Analisar for loops
        for_pattern = r'for\s*\([^)]+\)'
        for_matches = re.finditer(for_pattern, body)
        for match in for_matches:
            loop_def = match.group(0)[3:].strip('()')
            flow_elements.append({
                "type": "loop_for",
                "definition": loop_def
            })
        
        # Analisar while loops
        while_pattern = r'while\s*\([^)]+\)'
        while_matches = re.finditer(while_pattern, body)
        for match in while_matches:
            condition = match.group(0)[5:].strip('()')
            flow_elements.append({
                "type": "loop_while",
                "condition": condition
            })
        
        # Analisar try-catch
        try_pattern = r'try\s*\{'
        try_matches = re.finditer(try_pattern, body)
        for match in try_matches:
            exceptions = self._extract_catch_blocks(body, match.start())
            flow_elements.append({
                "type": "try_catch",
                "exceptions": exceptions,
                "has_finally": "finally" in body[match.start():]
            })
        
        # Analisar throws
        throw_pattern = r'throw\s+new\s+(\w+)'
        throw_matches = re.findall(throw_pattern, body)
        for exception in throw_matches:
            flow_elements.append({
                "type": "exception_throw",
                "exception": exception
            })
        
        # Analisar returns
        return_pattern = r'return(?:\s+[^;]+)?;'
        return_matches = re.findall(return_pattern, body)
        for return_stmt in return_matches:
            value = return_stmt.replace('return', '').replace(';', '').strip()
            flow_elements.append({
                "type": "return",
                "value": value if value else "void"
            })
        
        return flow_elements
    
    def _has_corresponding_else(self, body: str, if_pos: int) -> bool:
        """Verifica se há um else correspondente ao if"""
        # Implementação simplificada
        return "else" in body[if_pos:if_pos + 200]
    
    def _extract_catch_blocks(self, body: str, try_pos: int) -> List[str]:
        """Extrai exceções dos blocos catch"""
        catch_pattern = r'catch\s*\(\s*(\w+)'
        catches = re.findall(catch_pattern, body[try_pos:])
        return catches
    
    def _calculate_complexity(self, flow_map: List[Dict[str, Any]]) -> int:
        """Calcula complexidade ciclomática"""
        complexity = 1
        
        for element in flow_map:
            if element["type"] in ["conditional", "loop_for", "loop_while"]:
                complexity += 1
            elif element["type"] == "try_catch":
                complexity += len(element["exceptions"])
        
        return complexity
    
    def _generate_flow_summary(self, flow_map: List[Dict[str, Any]]) -> str:
        """Gera resumo textual do fluxo"""
        summary_parts = []
        
        for element in flow_map:
            if element["type"] == "conditional":
                summary_parts.append(f"IF({element['condition']})")
            elif element["type"] == "loop_for":
                summary_parts.append(f"FOR({element['definition']})")
            elif element["type"] == "loop_while":
                summary_parts.append(f"WHILE({element['condition']})")
            elif element["type"] == "try_catch":
                exceptions = ", ".join(element["exceptions"])
                summary_parts.append(f"TRY-CATCH({exceptions})")
            elif element["type"] == "exception_throw":
                summary_parts.append(f"THROW({element['exception']})")
            elif element["type"] == "return":
                summary_parts.append(f"RETURN({element['value']})")
        
        return " -> ".join(summary_parts) if summary_parts else "Linear"


class JavaPromptGenerator:
    """Gerador de prompts para testes unitários Java"""
    
    def generate_test_prompt(self, static_analysis: Dict[str, Any], 
                           flow_analysis: Dict[str, Any],
                           test_framework: str = "junit5") -> Dict[str, Any]:
        """Gera prompt otimizado para testes unitários Java"""
        
        prompt_sections = self._build_prompt_sections(static_analysis, flow_analysis)
        output_structure = self._get_output_structure(test_framework)
        final_prompt = self._assemble_final_prompt(prompt_sections, output_structure)
        
        return {
            "prompt": final_prompt,
            "metadata": {
                "language": "java",
                "framework": test_framework,
                "complexity_score": flow_analysis.get("complexity_score", 1),
                "estimated_tests": self._estimate_test_count(flow_analysis)
            }
        }
    
    def _build_prompt_sections(self, static_analysis: Dict[str, Any], 
                              flow_analysis: Dict[str, Any]) -> Dict[str, str]:
        """Constrói seções do prompt"""
        
        method_info = f"""
MÉTODO: {static_analysis.get('signature', 'N/A')}
MODIFICADORES: {', '.join(static_analysis.get('modifiers', []))}
PARÂMETROS: {self._format_parameters(static_analysis.get('parameters', []))}
RETORNO: {static_analysis.get('return_type', 'void')}
EXCEÇÕES: {', '.join(static_analysis.get('exceptions', []))}
ANOTAÇÕES: {self._format_annotations(static_analysis.get('annotations', []))}
DEPENDÊNCIAS: {', '.join(static_analysis.get('dependencies', {}).get('imports', []))}
"""
        
        flow_info = f"""
FLUXO: {flow_analysis.get('summary', 'Linear')}
COMPLEXIDADE: {flow_analysis.get('complexity_score', 1)}
CENÁRIOS: {self._extract_test_scenarios(flow_analysis.get('flow_map', []))}
"""
        
        return {
            "method_info": method_info.strip(),
            "flow_info": flow_info.strip()
        }
    
    def _format_parameters(self, parameters: List[Dict[str, Any]]) -> str:
        """Formata parâmetros para o prompt"""
        if not parameters:
            return "Nenhum"
        
        param_strs = []
        for param in parameters:
            param_str = f"{param['type']} {param['name']}"
            if param.get('annotations'):
                annotations = ', '.join([ann if isinstance(ann, str) else ann['name'] 
                                       for ann in param['annotations']])
                param_str = f"@{annotations} {param_str}"
            param_strs.append(param_str)
        
        return ", ".join(param_strs)
    
    def _format_annotations(self, annotations: List[Dict[str, Any]]) -> str:
        """Formata anotações"""
        if not annotations:
            return "Nenhuma"
        
        return ", ".join([f"@{ann['name']}" for ann in annotations])
    
    def _extract_test_scenarios(self, flow_map: List[Dict[str, Any]]) -> str:
        """Extrai cenários de teste do mapa de fluxo"""
        scenarios = []
        
        for element in flow_map:
            if element["type"] == "conditional":
                scenarios.extend([f"Condição TRUE: {element['condition']}", 
                                f"Condição FALSE: {element['condition']}"])
            elif element["type"] in ["loop_for", "loop_while"]:
                scenarios.extend(["Loop vazio", "Loop com múltiplas iterações"])
            elif element["type"] == "try_catch":
                scenarios.extend([f"Exceção: {exc}" for exc in element["exceptions"]])
                scenarios.append("Execução sem exceção")
            elif element["type"] == "exception_throw":
                scenarios.append(f"Lança: {element['exception']}")
        
        return "; ".join(scenarios) if scenarios else "Fluxo linear"
    
    def _get_output_structure(self, framework: str) -> str:
        """Retorna estrutura de saída baseada no framework"""
        
        structures = {
            "junit5": """
```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class MethodNameTest {
    
    private ClassName classUnderTest;
    
    @BeforeEach
    void setUp() {
        classUnderTest = new ClassName();
    }
    
    @Test
    @DisplayName("Should handle normal case")
    void shouldHandleNormalCase() {
        // Arrange
        
        // Act
        
        // Assert
    }
    
    @Test
    @DisplayName("Should handle edge cases")
    void shouldHandleEdgeCases() {
        // Test edge cases
    }
    
    @Test
    @DisplayName("Should throw exception when invalid")
    void shouldThrowExceptionWhenInvalid() {
        // Test exception scenarios
        assertThrows(ExceptionType.class, () -> {
            // Code that should throw
        });
    }
    
    @ParameterizedTest
    @ValueSource(ints = {1, 2, 3})
    void shouldHandleMultipleValues(int value) {
        // Parameterized tests
    }
}
```""",
            
            "junit4": """
```java
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

@RunWith(MockitoJUnitRunner.class)
public class MethodNameTest {
    
    private ClassName classUnderTest;
    
    @Before
    public void setUp() {
        classUnderTest = new ClassName();
    }
    
    @Test
    public void shouldHandleNormalCase() {
        // Arrange
        
        // Act
        
        // Assert
    }
    
    @Test
    public void shouldHandleEdgeCases() {
        // Test edge cases
    }
    
    @Test(expected = ExceptionType.class)
    public void shouldThrowExceptionWhenInvalid() {
        // Test exception scenarios
    }
}
```"""
        }
        
        return structures.get(framework, structures["junit5"])
    
    def _assemble_final_prompt(self, sections: Dict[str, str], output_structure: str) -> str:
        """Monta o prompt final"""
        
        return f"""Gere testes unitários completos para o seguinte método Java:

{sections['method_info']}

{sections['flow_info']}

INSTRUÇÕES:
1. Cubra todos os cenários identificados no fluxo
2. Inclua testes para casos extremos e validação de parâmetros
3. Teste tratamento de exceções quando aplicável
4. Use Mockito para mockar dependências
5. Mantenha testes independentes e determinísticos
6. Use anotações @DisplayName para descrever os testes
7. Implemente testes parametrizados quando apropriado

ESTRUTURA DE SAÍDA OBRIGATÓRIA:
{output_structure}

Gere APENAS o código dos testes, sem explicações adicionais."""
    
    def _estimate_test_count(self, flow_analysis: Dict[str, Any]) -> int:
        """Estima número de testes necessários"""
        complexity = flow_analysis.get("complexity_score", 1)
        flow_map = flow_analysis.get("flow_map", [])
        
        test_count = 1  # Caso base
        test_count += complexity
        
        for element in flow_map:
            if element["type"] == "conditional":
                test_count += 1
            elif element["type"] in ["loop_for", "loop_while"]:
                test_count += 1
            elif element["type"] == "try_catch":
                test_count += len(element["exceptions"])
        
        return min(test_count, 20)  # Limitar a 20 testes