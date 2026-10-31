from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(20))
    city: Mapped[str] = mapped_column(String(100))

    orders: Mapped[list["Order"]] = relationship(back_populates="client")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column()
    stock: Mapped[int] = mapped_column(default=0)

    orders: Mapped[list["Order"]] = relationship(back_populates="product")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)

    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    quantity: Mapped[int] = mapped_column()

    client: Mapped["Client"] = relationship(back_populates="orders")
    product: Mapped["Product"] = relationship(back_populates="orders")