package com.zez.store;

import java.util.*;

class Product {
    String name;
    double price;
    int stock;

    public Product(String name, double price, int stock) {
        this.name = name;
        this.price = price;
        this.stock = stock;
    }
}

class OrderResult {
    double totalPrice;
    List<String> messages;

    public OrderResult(double totalPrice, List<String> messages) {
        this.totalPrice = totalPrice;
        this.messages = messages;
    }
}

public class Store {

    // Função complexa: processa pedidos, aplica descontos e valida estoque
    public static OrderResult processOrder(Map<Product, Integer> order, boolean isVIP) {
        double total = 0;
        List<String> messages = new ArrayList<>();

        for (Map.Entry<Product, Integer> entry : order.entrySet()) {
            Product product = entry.getKey();
            int quantity = entry.getValue();

            try {
                if (quantity <= 0) {
                    messages.add("Quantidade inválida para o produto: " + product.name);
                    continue;
                }

                if (quantity > product.stock) {
                    messages.add("Estoque insuficiente para o produto: " + product.name);
                    quantity = product.stock; // ajusta para o estoque disponível
                }

                double price = product.price * quantity;

                // Aplica desconto para VIPs
                if (isVIP) {
                    price *= 0.9; // 10% de desconto
                    messages.add("Desconto VIP aplicado para " + product.name);
                }

                // Desconto extra para compras grandes
                if (quantity >= 10) {
                    price *= 0.95; // 5% extra
                    messages.add("Desconto por quantidade para " + product.name);
                }

                total += price;

                // Atualiza estoque
                product.stock -= quantity;

            } catch (Exception e) {
                messages.add("Erro processando o produto " + product.name + ": " + e.getMessage());
            }
        }

        if (total == 0) {
            messages.add("Pedido não pôde ser processado.");
        }

        return new OrderResult(total, messages);
    }

    // Função principal para testar
    public static void main(String[] args) {
        Product p1 = new Product("Camiseta", 50.0, 20);
        Product p2 = new Product("Calça", 120.0, 5);

        Map<Product, Integer> order = new HashMap<>();
        order.put(p1, 12); // Pedido grande
        order.put(p2, 3);  // Pedido normal

        OrderResult result = processOrder(order, true);

        System.out.println("Total do pedido: R$ " + result.totalPrice);
        for (String msg : result.messages) {
            System.out.println(msg);
        }
    }
}
