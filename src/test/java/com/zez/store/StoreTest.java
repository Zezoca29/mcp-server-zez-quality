package com.zez.store;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class StoreTest {
    
    private Product product1;
    private Product product2;
    private Map<Product, Integer> order;
    
    @BeforeEach
    void setUp() {
        product1 = new Product("Camiseta", 50.0, 20);
        product2 = new Product("Calça", 120.0, 5);
        order = new HashMap<>();
    }
    
    @Test
    @DisplayName("Deve processar pedido normal sem descontos")
    void shouldProcessNormalOrderWithoutDiscounts() {
        // Arrange
        order.put(product1, 2);
        order.put(product2, 1);
        
        // Act
        OrderResult result = Store.processOrder(order, false);
        
        // Assert
        assertEquals(220.0, result.totalPrice, 0.01);
        assertEquals(0, result.messages.size());
        assertEquals(18, product1.stock);
        assertEquals(4, product2.stock);
    }
    
    @Test
    @DisplayName("Deve aplicar desconto VIP")
    void shouldApplyVIPDiscount() {
        // Arrange
        order.put(product1, 2);
        order.put(product2, 1);
        
        // Act
        OrderResult result = Store.processOrder(order, true);
        
        // Assert
        assertEquals(198.0, result.totalPrice, 0.01); // 10% desconto
        assertTrue(result.messages.contains("Desconto VIP aplicado para Camiseta"));
        assertTrue(result.messages.contains("Desconto VIP aplicado para Calça"));
    }
    
    @Test
    @DisplayName("Deve aplicar desconto por quantidade")
    void shouldApplyQuantityDiscount() {
        // Arrange
        order.put(product1, 12);
        
        // Act
        OrderResult result = Store.processOrder(order, false);
        
        // Assert
        assertEquals(570.0, result.totalPrice, 0.01); // 5% desconto
        assertTrue(result.messages.contains("Desconto por quantidade para Camiseta"));
    }
    
    @Test
    @DisplayName("Deve aplicar ambos os descontos")
    void shouldApplyBothDiscounts() {
        // Arrange
        order.put(product1, 12);
        
        // Act
        OrderResult result = Store.processOrder(order, true);
        
        // Assert
        assertEquals(513.0, result.totalPrice, 0.01); // 10% VIP + 5% quantidade
        assertTrue(result.messages.contains("Desconto VIP aplicado para Camiseta"));
        assertTrue(result.messages.contains("Desconto por quantidade para Camiseta"));
    }
    
    @Test
    @DisplayName("Deve lidar com quantidade inválida")
    void shouldHandleInvalidQuantity() {
        // Arrange
        order.put(product1, 0);
        order.put(product2, -1);
        
        // Act
        OrderResult result = Store.processOrder(order, false);
        
        // Assert
        assertEquals(0.0, result.totalPrice);
        assertTrue(result.messages.contains("Quantidade inválida para o produto: Camiseta"));
        assertTrue(result.messages.contains("Quantidade inválida para o produto: Calça"));
        assertTrue(result.messages.contains("Pedido não pôde ser processado."));
    }
    
    @Test
    @DisplayName("Deve ajustar quantidade para estoque disponível")
    void shouldAdjustQuantityToAvailableStock() {
        // Arrange
        order.put(product2, 10); // Estoque é apenas 5
        
        // Act
        OrderResult result = Store.processOrder(order, false);
        
        // Assert
        assertEquals(600.0, result.totalPrice, 0.01);
        assertTrue(result.messages.contains("Estoque insuficiente para o produto: Calça"));
        assertEquals(0, product2.stock);
    }
    
    @Test
    @DisplayName("Deve processar pedido vazio")
    void shouldHandleEmptyOrder() {
        // Act
        OrderResult result = Store.processOrder(order, false);
        
        // Assert
        assertEquals(0.0, result.totalPrice);
        assertTrue(result.messages.contains("Pedido não pôde ser processado."));
    }
    
    @Test
    @DisplayName("Deve lidar com pedido nulo")
    void shouldHandleNullOrder() {
        // Act & Assert
        assertThrows(NullPointerException.class, () -> {
            Store.processOrder(null, false);
        });
    }
}
