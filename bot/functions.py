from db.model import User, Category, Product,Order


async def save_user(**kwargs):
    check = await User.get(User.user_id, kwargs.get('user_id'))
    if not check:
        await User.create(**kwargs)

async def get_category():
    category:list[Category]=await Category.get_all()
    return category

async def get_products(category_id:str):
    id_=''.join([ i for i in category_id if i.isdigit()])
    products:list[Product]=await Product.get(Product.category_id,int(id_))
    return products

async def products_inf(product_id:str):
    id_ = ''.join([i for i in product_id if i.isdigit()])
    name= await Product.gets(Product.id, int(id_),Product.name)
    price= await Product.gets(Product.id, int(id_),Product.price)
    count= await Product.gets(Product.id, int(id_),Product.count)
    image= await Product.gets(Product.id, int(id_),Product.image)
    product_id= await Product.gets(Product.id, int(id_),Product.id)
    return name[0],price[0],count[0],image[0],product_id[0]

async def check_count(count: str, total: float, price: float):
    res = 1
    count = count.lower()

    if "day" in count:
        num = ''.join(filter(str.isdigit, count))
        if num:
            res = float(num) * total
    elif "hour" in count:
        num = ''.join(filter(str.isdigit, count))
        if num:
            res = float(num) * price
    return res

async def order_save(**kwargs):
     await Order.create(**kwargs)

async def get_order(user_id):
    name:list[Order]=await Order.gets(Order.user_id,user_id,Order.product_name)
    price:list[Order]=await Order.gets(Order.user_id,user_id,Order.product_price)
    time:list[Order]=await Order.gets(Order.user_id,user_id,Order.product_time)
    return name,price,time

async def searching_products(product_id):
    price = await Product.gets(Product.id, product_id, Product.price)
    image = await Product.gets(Product.id, product_id, Product.image)
    count = await Product.gets(Product.id, product_id, Product.count)
    name = await Product.gets(Product.id, product_id, Product.name)
    return name[0], price[0], count[0], image[0]

async def to_string(iters:list):
    res=''
    for i in iters:
        res+=' '+str(i)
    return res

admin= 0