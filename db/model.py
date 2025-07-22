from sqlalchemy import Text, String, BIGINT, DECIMAL, ForeignKey, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base, db
from db.utils import CreatedModel


class User(CreatedModel):
    user_id: Mapped[int] = mapped_column(BIGINT, unique=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    order = relationship('Order', back_populates='user', lazy='selectin')

    async def save_user(**kwargs):
        check = await User.get(User.user_id, kwargs.get('user_id'))
        if not check:
            await User.create(**kwargs)


class Category(CreatedModel):
    __tablename__ = 'categories'

    name: Mapped[str] = mapped_column(String)
    product = relationship('Product', back_populates='category')

    def __repr__(self):
        return f"{self.name}"


class Product(CreatedModel):
    name: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)
    image: Mapped[str] = mapped_column(Text,nullable=True)
    count: Mapped[int] = mapped_column(Integer, default=1)
    link: Mapped[str] = mapped_column(Text,nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id', ondelete='CASCADE'))
    category = relationship('Category', back_populates='product', lazy='selectin')
    order = relationship('Order', back_populates='product', lazy='selectin')

    def __repr__(self):
        return f"{self.name},{self.price},{self.image},{self.category_id},{self.count}"


class Order(CreatedModel):
    time: Mapped[str] = mapped_column(String)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id', ondelete='CASCADE'))
    total_price: Mapped[float] = mapped_column(Float)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id', ondelete='CASCADE'))
    product = relationship('Product', back_populates='order', lazy='selectin')
    user = relationship('User', back_populates='order', lazy='selectin')

    def __repr__(self):
        return f"{self.product_name},{self.product_id},{self.product_id}"





metadata = Base.metadata
