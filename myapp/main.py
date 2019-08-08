from myapp.models import Products, ProductImages, ProductFeatures, Comments

Products.fillTableWithInitialData()
print(Products.getAllProducts('', 0, 0, [], []))
