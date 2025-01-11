from quotes.config import db


class Subjects(db.Model):
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50))
    second_name = db.Column(db.String(50))
    middle_name = db.Column(db.String(50))
    birth_date = db.Column(db.Date)
    gender = db.Column(db.String(15))


class Documents(db.Model):
    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"))
    document_type = db.Column(db.String(100))
    document_number = db.Column(db.Integer)
    issue_date = db.Column(db.Date)
    subjects = db.relationship("Subjects", backref="documents")


class Products(db.Model):
    __tablename__ = "fs.products"
    # __table_args__ = {"schema": "fs"}

    product_code = db.Column(db.String(20), primary_key=True)
    type = db.Column(db.String)


# class Products(db.Model):
#     __tablename__ = "products"

#     product_code = db.Column(db.String(20), primary_key=True)
#     product_type = db.Column(db.String(50), nullable=False)

#     requests = db.relationship("Requests", back_populates="product")
#     check_product_statuses = db.relationship(
#         "CheckProductStatus", back_populates="product"
#     )
#     check_actions = db.relationship("CheckActions", back_populates="product")


class ProductsFeatures(db.Model):
    __tablename__ = "fs.product_features"
    # __table_args__ = {"schema": "fs"}

    product_code = db.Column(
        db.String(20),
        db.ForeignKey("fs.products.product_code"),
        primary_key=True,
    )
    feature_name = db.Column(db.String(150), primary_key=True)


class FeaturesValues(db.Model):
    __tablename__ = "fs.feature_values"
    # __table_args__ = {"schema": "fs"}

    subject_id = db.Column(
        db.Integer, db.ForeignKey("subjects.id"), primary_key=True
    )
    feature_name = db.Column(db.String(100), primary_key=True)
    feature_value = db.Column(db.String(150))


class Models(db.Model):
    __tablename__ = "ml.models"
    # __table_args__ = {"schema": "ml"}

    model_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_name = db.Column(db.String(25), nullable=False, unique=True)
    product_code = db.Column(
        db.String(20), db.ForeignKey("fs.products.product_code")
    )
    status = db.Column(db.Boolean, nullable=False)
    model_version = db.Column(db.String(5), nullable=False, default="1.0")
    model_description = db.Column(db.String(100))

    product = db.relationship("Products", backref="models")
