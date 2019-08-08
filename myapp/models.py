from django.db import models
from django.db import connection, transaction
from operator import itemgetter

class Products(models.Model):

    name = models.CharField(max_length=50)
    price = models.IntegerField()
    brand = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    pos_votes = models.IntegerField(default=0)
    neg_votes = models.IntegerField(default=0)

    @staticmethod
    def addProduct(name, price, brand, category, imagesList, featuresList, pos_votes=0, neg_votes=0):

        cursor = connection.cursor()
        cursor.execute('insert into myapp_products(name, price , brand, category, pos_votes, neg_votes) values(:a,:b,:c,:d,:e,:f)',
                       {'a': name, 'b': price, 'c':brand, 'd':category, 'e':pos_votes, 'f':neg_votes})

        newId = -1
        res = cursor.execute('select last_insert_rowid()')
        for x in res:
            newId = x[0]
            break

        for image in imagesList:
            cursor.execute('insert into myapp_productimages(pid, image_url) values(:a,:b)',
                {'a': newId, 'b': image})

        for (feature, value) in featuresList:
            cursor.execute('insert into myapp_productfeatures(pid, feature, value) values(:a,:b, :c)',
                {'a': newId, 'b': feature, 'c':value})

        transaction.commit()

    @staticmethod
    def clear():
        ProductImages.clear()
        ProductFeatures.clear()
        Comments.clear()
        cursor = connection.cursor()
        cursor.execute('delete from myapp_products')
        transaction.commit()

    @staticmethod
    def fillTableWithInitialData():
        Products.clear()
        Products.addProduct('Infinix Hot S3', 200, 'Infinix', 'Phones',
                            ['phone1_1.jpg', 'phone1_2.jpg'],
                            [('Screen Size', '5.7 inch'), ('SIM', 'dual'), ('Generation', '4G'), ('RAM', '3 GB'), ('Storage', '32 GB'), ('Front Cam', '13 Megapixel'), ('Back cam', '20 Megapixel')])
        Products.addProduct('Showmi A1', 250, 'Showmi', 'Phones',
                            ['phone2_1.jpg', 'phone2_2.jpg', 'phone2_3.jpg'],
                            [('Screen Size', '5.5 inch'), ('SIM', 'dual'), ('CPU', 'Octa core 2.0 GHz'), ('RAM', '4 GB'), ('Storage', '32 GB'), ('Front Cam', '5 Megapixel'), ('Back cam', '12 Megapixel')])
        Products.addProduct('Showmi Redmi 4x', 135, 'Showmi', 'Phones',
                            ['phone3_1.jpg', 'phone3_2.jpg', 'phone3_3.jpg'],
                            [('Screen Size', '5 inch'), ('CPU', 'Octa core 2.0 GHz'), ('RAM', '2 GB'), ('Storage', '16 GB'), ('Front Cam', '5 Megapixel'), ('Back cam', '13 Megapixel')])
        Products.addProduct('Apple Iphone 6', 450, 'Apple', 'Phones',
                            ['phone4_1.jpg', 'phone4_2.jpg', 'phone4_3.jpg'],
                            [('Screen Size', '4.7 inch'), ('CPU', 'Dual core 1.4 GHz'), ('SIM', 'Single'), ('RAM', '1 GB'), ('Storage', '32 GB'), ('Front Cam', '5 Megapixel'), ('Back cam', '8 Megapixel')])
        Products.addProduct('Lenovo Ideapad 320', 420, 'Lenovo', 'Laptops',
                            ['laptop1_1.jpg', 'laptop1_2.jpg'],
                            [('CPU', 'I3-6006U'), ('RAM', '4 GB'), ('Hard disk', '1 TB')])
        Products.addProduct('HP 14 Notebook', 420, 'HP', 'Laptops',
                            ['laptop2_1.jpg', 'laptop2_2.jpg', 'laptop2_3.jpg'],
                            [('CPU', 'Celeron Dual core 2 GHz'), ('RAM', '4 GB'), ('Hard disk', '500 GB')])
        Products.addProduct('Apple MacBook Air MQD32', 1220, 'Apple', 'Laptops',
                            ['laptop3_1.jpg', 'laptop3_2.jpg', 'laptop3_3.jpg'],
                            [('CPU', 'Core i5'), ('RAM', '8 GB'), ('Hard disk', '128 GB')])
        Products.addProduct('UnionAir 32 Inch HD LED TV', 200, 'UnionAir', 'TVs',
                            ['tv1_1.jpg'],
                            [('Resolution', '1366*768'), ('Viewing Angle', '178H/178V'), ('Backlight life', '30000 Hrs')])
        Products.addProduct('Toshiba 32 Inch Smart HD LED TV', 250, 'Toshiba', 'TVs',
                            ['tv2_1.jpg', 'tv2_2.jpg', 'tv2_3.jpg', 'tv2_4.jpg'],
                            [('Resolution', '1366*768'), ('Display Type', 'LED'),
                             ('HD Type', 'Full HD')])
        Products.addProduct('Sony 65 Inch 4K HDR Android TV', 2250, 'Sony', 'TVs',
                            ['tv3_1.jpg', 'tv3_2.jpg', 'tv3_3.jpg', 'tv3_4.jpg'],
                            [('Resolution', '3840*2160'), ('Display Type', 'LCD'),
                             ('HD Type', '4K Ultra HD'), ('Viewing Angle', 'Wide Viewing Angle')])


    @staticmethod
    def get_pos_percentage(pos_votes, neg_votes):
        pos_percentage = 0.5
        if pos_votes + neg_votes != 0:
            pos_percentage = pos_votes / (pos_votes + neg_votes)
        return pos_percentage


    @staticmethod
    def updateVotes(pid, vote_type):
        cursor = connection.cursor()
        res = cursor.execute('select pos_votes, neg_votes from myapp_products where id = ' + str(pid))
        votes = {}
        for p in res:
            votes = {'pos': p[0], 'neg': p[1]}
            break
        if vote_type != 'neu':
            votes[vote_type] += 1
            col_name = vote_type + '_votes'
            cursor.execute('update myapp_products set {} = {} where id = {}'.format(col_name, str(votes[vote_type]), pid))
            transaction.commit()
        return Products.get_pos_percentage(votes['pos'], votes['neg'])


    @staticmethod
    def getAllProducts(name, priceMin, priceMax, categoriesList, brandsList):

        max_price_condition = ''
        if priceMax > 0:
            max_price_condition = 'and price <= {}'.format(priceMax)

        categories_condition = ''
        if len(categoriesList) > 0:
            categories_condition = 'and category in {}'.format(str(categoriesList).replace('[', '(').replace(']', ')'))

        brands_condition = ''
        if len(brandsList) > 0:
            brands_condition = 'and brand in {}'.format(str(brandsList).replace('[', '(').replace(']', ')'))

        query = """
            select      id, name, brand, price, pos_votes, neg_votes 
            from        myapp_products
            where       name like '%{}%' 
                        and price >= {}
                        {}
                        {}
                        {}
                """.format(name, priceMin, max_price_condition, categories_condition, brands_condition)

        cursor = connection.cursor()
        res = cursor.execute(query)

        products_result_list = []
        for product in res:
            product_dict = {'pid':product[0], 'pname':product[1], 'brand':product[2], 'price':product[3]}
            product_dict['pos_percentage'] = Products.get_pos_percentage(product[4], product[5])
            product_dict['img'] = ProductImages.get_first_image_of_product(product[0])
            products_result_list.append(product_dict)
        return sorted(products_result_list, key=itemgetter('pos_percentage'), reverse=True)


    @staticmethod
    def getCategories():
        cursor = connection.cursor()
        res = cursor.execute('select distinct category from myapp_products')
        categories = []
        for category in res:
            categories.append(category[0])
        return categories


    @staticmethod
    def getProduct(pid):
        cursor = connection.cursor()
        res = cursor.execute('select name, brand, price, pos_votes, neg_votes from myapp_products where id = ' + str(pid))
        product = {}
        for p in res:
            product = {'pname':p[0], 'brand':p[1], 'price':p[2],
                       'images':ProductImages.getImages(pid),
                       'pos_percentage':Products.get_pos_percentage(p[3], p[4]),
                       'feature_table':ProductFeatures.getFeatures(pid)}
            break
        return product


    @staticmethod
    def getBrands():
        cursor = connection.cursor()
        res = cursor.execute('select distinct brand from myapp_products')
        brands = []
        for brand in res:
            brands.append(brand[0])
        return brands


    @staticmethod
    def compareProducts(pidsList):
        cursor = connection.cursor()
        res = cursor.execute("""
            select      id, name, brand, price, pos_votes, neg_votes 
            from        myapp_products
            where       id in {}
            """.format(str(pidsList).replace('[', '(').replace(']', ')')))
        names = ['PRODUCT']
        images = ['IMAGE']
        brands = ['BRAND']
        prices = ['PRICE']
        votes = ['VOTES']
        for product in res:
            names.append(product[1])
            images.append(ProductImages.get_first_image_of_product(product[0]))
            brands.append(product[2])
            prices.append(product[3])
            votes.append(Products.get_pos_percentage(product[4], product[5]))
        table_data = [names, images, brands, prices, votes]


        select_str = 'f{0}.feature, '.format(str(pidsList[0]))
        table_names_str = ''
        join_str = ''
        pids_str = ''
        for i in range(len(pidsList)):
            if i > 0:
                select_str += ', '
                table_names_str += ', '
                if i < len(pidsList) - 1:
                    join_str += ' and '
                pids_str += ' and '
            select_str += 'f{0}.value'.format(str(pidsList[i]))
            table_names_str += 'myapp_productfeatures as f' + str(pidsList[i])
            if i < len(pidsList)-1:
                join_str += 'f{0}.feature = f{1}.feature'.format(str(pidsList[i]), str(pidsList[i+1]))
            pids_str += 'f{0}.pid = {0}'.format(str(pidsList[i]))

        query = """
            select  {} 
            from    {}
            where   {}
            and     {}
            """.format(select_str, table_names_str, join_str, pids_str)

        res = cursor.execute(query)

        for x in res:
            table_data.append(list(x))

        final_result = {'pids': pidsList, 'table_data':table_data}

        return final_result


################################################################################################################
################################################################################################################
################################################################################################################
################################################################################################################


class ProductImages(models.Model):

    pid = models.ForeignKey(Products, db_column='pid', on_delete=models.CASCADE)
    image_url = models.CharField(max_length=150)

    class Meta:
        unique_together = (('pid', 'image_url'),)


    @staticmethod
    def addImage(pid, image):
        cursor = connection.cursor()
        cursor.execute('insert into myapp_products(pid, image) values(:a, :b)',{'a': pid, 'b': image})
        #transaction.commit()   no need to commit


    @staticmethod
    def getImages(pid):
        cursor = connection.cursor()
        res = cursor.execute('select image_url from myapp_productimages where pid = ' + str(pid))
        images = []
        for img in res:
            images.append(img[0])
        return images


    @staticmethod
    def get_first_image_of_product(pid):
        cursor = connection.cursor()
        res = cursor.execute('select image_url from myapp_productimages where pid = ' + str(pid) +' order by id')
        image = None
        for img in res:
            image = img[0]
            break
        if image is None:
            image = 'NO IMAGE'
        return image

    @staticmethod
    def clear():
        cursor = connection.cursor()
        cursor.execute('delete from myapp_productimages')
        transaction.commit()


################################################################################################################
################################################################################################################
################################################################################################################
################################################################################################################


class ProductFeatures(models.Model):

    pid = models.ForeignKey(Products, db_column='pid', on_delete=models.CASCADE)
    feature = models.CharField(max_length=30)
    value = models.CharField(max_length=30)

    class Meta:
        unique_together = (('pid', 'feature'),)


    @staticmethod
    def addFeature(pid, feature, value):
        cursor = connection.cursor()
        cursor.execute('insert into myapp_products(pid, feature, value) values(:a, :b, :c)', {'a': pid, 'b': feature, 'c':value})
        # transaction.commit()   no need to commit

    @staticmethod
    def getFeatures(pid):
        cursor = connection.cursor()
        res = cursor.execute('select feature, value from myapp_productfeatures where pid = ' + str(pid))
        features = []
        for f in res:
            features.append([f[0], f[1]])
        return features


    @staticmethod
    def clear():
        cursor = connection.cursor()
        cursor.execute('delete from myapp_productfeatures')
        transaction.commit()


################################################################################################################
################################################################################################################
################################################################################################################
################################################################################################################

class Comments(models.Model):

    pid = models.ForeignKey(Products, db_column='pid', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    comment_str = models.CharField(max_length=300)

    @staticmethod
    def addComment(pid, name, comment_str):
        cursor = connection.cursor()
        cursor.execute('insert into myapp_comments(pid, name, comment_str) values(:a, :b, :c)',
                       {'a': pid, 'b': name, 'c':comment_str})
        transaction.commit()

    @staticmethod
    def viewComments(pid):
        cursor = connection.cursor()
        res = cursor.execute('select name, comment_str from myapp_comments where pid = ' + str(pid) + ' order by id desc')
        comments_list = []
        for comment in res:
            comments_list.append({'name':comment[0], 'comment':comment[1]})
        return comments_list


    @staticmethod
    def clear():
        cursor = connection.cursor()
        cursor.execute('delete from myapp_comments')
        cursor.execute('update myapp_products set pos_votes = 0, neg_votes = 0')
        transaction.commit()

