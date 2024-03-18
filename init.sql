CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE products (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  description TEXT,
  price INTEGER,
  image_url TEXT,
  created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
  deleted_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL,
  CONSTRAINT products_price_check CHECK (price >= 0)
);

CREATE TABLE stores (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  description TEXT,
  created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
  deleted_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL
);

CREATE TABLE stores_products (
  store_id UUID NOT NULL,
  product_id UUID NOT NULL,
  position INTEGER NOT NULL,
  category TEXT,
  PRIMARY KEY (store_id, product_id),
  FOREIGN KEY (store_id) REFERENCES stores (id) ON DELETE CASCADE,
  FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE,
  CONSTRAINT stores_products_position_check CHECK (position >= 0),
  CONSTRAINT stores_products_position_unique UNIQUE (store_id, product_id, position)
);

INSERT INTO
  stores (id, name)
VALUES
  (
    '64580d46-ea72-4350-92ce-8cf98d230f90',
    'Shop do João'
  );

INSERT INTO
  products (id, name, description, price)
VALUES
  (
    '4488c1ef-0a2f-4776-838d-000000000001',
    'Cheese Burger',
    'Hamburguer artesanal com queijo, alface, tomate e maionese.',
    2500
  ),
  (
    '4488c1ef-0a2f-4776-838d-000000000002',
    'Cheese Bacon Burger',
    'Hamburguer artesanal com queijo, bacon, alface, tomate e maionese.',
    3000
  ),
  (
    '4488c1ef-0a2f-4776-838d-000000000003',
    'Batata Frita',
    'Porção de batata frita com molho especial.',
    1600
  ),
  (
    '4488c1ef-0a2f-4776-838d-000000000004',
    'Coca-Cola',
    'Refrigerante em lata Coca cola em 350ml.',
    500
  ),
  (
    '4488c1ef-0a2f-4776-838d-000000000005',
    'Suco de Laranja',
    'Suco de laranja feito na hora. Aprox: 500ml',
    1500
  ),
  (
    '4488c1ef-0a2f-4776-838d-000000000006',
    'Brigadeiro',
    'Brigadeiro de colher com granulado.',
    200
  ),
  (
    '4488c1ef-0a2f-4776-838d-000000000007',
    'Sorvete',
    '1 Bola de sorvete de baunilha.',
    500
  );

INSERT INTO
  stores_products (store_id, product_id, position, category)
VALUES
  (
    '64580d46-ea72-4350-92ce-8cf98d230f90',
    '4488c1ef-0a2f-4776-838d-000000000001',
    1,
    'Lanches'
  ),
  (
    '64580d46-ea72-4350-92ce-8cf98d230f90',
    '4488c1ef-0a2f-4776-838d-000000000002',
    2,
    'Lanches'
  ),
  (
    '64580d46-ea72-4350-92ce-8cf98d230f90',
    '4488c1ef-0a2f-4776-838d-000000000003',
    3,
    'Lanches'
  ),
  (
    '64580d46-ea72-4350-92ce-8cf98d230f90',
    '4488c1ef-0a2f-4776-838d-000000000004',
    4,
    'Bebidas'
  ),
  (
    '64580d46-ea72-4350-92ce-8cf98d230f90',
    '4488c1ef-0a2f-4776-838d-000000000005',
    5,
    'Bebidas'
  ),
  (
    '64580d46-ea72-4350-92ce-8cf98d230f90',
    '4488c1ef-0a2f-4776-838d-000000000006',
    6,
    'Sobremesas'
  ),
  (
    '64580d46-ea72-4350-92ce-8cf98d230f90',
    '4488c1ef-0a2f-4776-838d-000000000007',
    7,
    'Sobremesas'
  );
