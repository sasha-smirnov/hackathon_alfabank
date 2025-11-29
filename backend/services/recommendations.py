from schemas import Product


def get_mock_recommendations(client_id: int):
    
    income = 100000 + client_id * 7 

    products = []

    if income > 200000:
        products.append(Product(
            id=1,
            name="Alfa Premium",
            description="Премиальная карта с повышенным кешбэком",
            reason="Доход выше 200 000₽"
        ))
    else:
        products.append(Product(
            id=2,
            name="Travel карта",
            description="Кешбэк 5% на путешествия",
            reason="Средний доход"
        ))

    products.append(Product(
        id=3,
        name="Дебетовая карта Cashback",
        description="2% кешбэк на все покупки",
        reason="Подходит всем клиентам"
    ))

    return products