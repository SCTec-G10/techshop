"""
Testes unitários para a classe ShoppingCart seguindo o padrão AAA (Arrange, Act, Assert).
"""

from src.cart import ShoppingCart
from src.models import Product


def test_add_new_item() -> None:
    """
    Testa a adição de um novo produto ao carrinho.
    Caminho feliz: O produto é adicionado e a lista de itens é atualizada corretamente.
    """
    # Arrange
    cart = ShoppingCart()
    product = Product(id=1, name="Laptop", price=1500.0)
    quantity = 1

    # Act
    cart.add_item(product, quantity)

    # Assert
    assert len(cart.items) == 1
    assert cart.items[0].product.id == 1
    assert cart.items[0].quantity == 1


def test_add_existing_item() -> None:
    """
    Testa a adição de um produto que já existe no carrinho.
    Caminho feliz: A quantidade do item existente é incrementada.
    """
    # Arrange
    cart = ShoppingCart()
    product = Product(id=1, name="Mouse", price=50.0)
    cart.add_item(product, 1)

    # Act
    cart.add_item(product, 2)

    # Assert
    assert len(cart.items) == 1
    assert cart.items[0].quantity == 3


def test_remove_existing_item() -> None:
    """
    Testa a remoção de um item que existe no carrinho.
    Caminho feliz: O item correspondente ao product_id é removido.
    """
    # Arrange
    cart = ShoppingCart()
    product1 = Product(id=1, name="Teclado", price=100.0)
    product2 = Product(id=2, name="Mouse", price=50.0)
    cart.add_item(product1, 1)
    cart.add_item(product2, 1)

    # Act
    cart.remove_item(1)

    # Assert
    assert len(cart.items) == 1
    assert cart.items[0].product.id == 2


def test_calculate_total_multiple_items() -> None:
    """
    Testa o cálculo do valor total com múltiplos itens no carrinho.
    Caminho feliz: A soma do preço * quantidade para todos os itens.
    """
    # Arrange
    cart = ShoppingCart()
    product1 = Product(id=1, name="Monitor", price=300.0)
    product2 = Product(id=2, name="Cabo", price=25.0)
    cart.add_item(product1, 2)  # 600.0
    cart.add_item(product2, 4)  # 100.0

    # Act
    total = cart.calculate_total()

    # Assert
    assert total == 700.0


def test_calculate_total_with_10_percent_discount() -> None:
    """
    Testa o cálculo do valor total com desconto de 10%.
    Caminho feliz: O desconto é aplicado para total > 500 e <= 1000.
    """
    # Arrange
    cart = ShoppingCart()
    product = Product(id=1, name="Cadeira Gamer", price=600.0)
    cart.add_item(product, 1)

    # Act
    total_with_discount = cart.calculate_total_with_discount()

    # Assert
    assert total_with_discount == 540.0


def test_calculate_total_with_20_percent_discount() -> None:
    """
    Testa o cálculo do valor total com desconto de 20%.
    Caminho feliz: O desconto é aplicado para total > 1000.
    """
    # Arrange
    cart = ShoppingCart()
    product = Product(id=1, name="Placa de Vídeo", price=1500.0)
    cart.add_item(product, 1)

    # Act
    total_with_discount = cart.calculate_total_with_discount()

    # Assert
    assert total_with_discount == 1200.0


def test_calculate_total_empty_cart() -> None:
    """
    Testa o cálculo do valor total em um carrinho vazio.
    Caso de borda: Carrinho sem itens.
    """
    # Arrange
    cart = ShoppingCart()

    # Act
    total = cart.calculate_total()
    total_with_discount = cart.calculate_total_with_discount()

    # Assert
    assert total == 0.0
    assert total_with_discount == 0.0


def test_calculate_total_with_discount_exact_500() -> None:
    """
    Testa o cálculo com desconto com o valor exato no limiar inferior (500).
    Caso de borda: Desconto exato no limiar. Como a regra é > 500, não deve ter desconto.
    """
    # Arrange
    cart = ShoppingCart()
    product = Product(id=1, name="Processador", price=500.0)
    cart.add_item(product, 1)

    # Act
    total_with_discount = cart.calculate_total_with_discount()

    # Assert
    assert total_with_discount == 500.0


def test_calculate_total_with_discount_exact_1000() -> None:
    """
    Testa o cálculo com desconto com o valor exato no limiar superior (1000).
    Caso de borda: Desconto exato no limiar. Como a regra é > 1000, deve cair no desconto de 10%.
    """
    # Arrange
    cart = ShoppingCart()
    product = Product(id=1, name="Placa Mãe e CPU", price=1000.0)
    cart.add_item(product, 1)

    # Act
    total_with_discount = cart.calculate_total_with_discount()

    # Assert
    assert total_with_discount == 900.0


def test_remove_non_existent_item() -> None:
    """
    Testa a remoção de um item informando um ID que não existe no carrinho.
    Caso de borda: Produto inexistente na remoção não deve quebrar nem alterar o estado.
    """
    # Arrange
    cart = ShoppingCart()
    product = Product(id=1, name="Fone de Ouvido", price=120.0)
    cart.add_item(product, 1)

    # Act
    cart.remove_item(999)  # ID que não existe no carrinho

    # Assert
    assert len(cart.items) == 1
    assert cart.items[0].product.id == 1
