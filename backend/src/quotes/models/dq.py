from quotes.config import db


class Actions(db.Model):
    __tablename__ = "dq.actions"

    action_id = db.Column(db.SmallInteger, primary_key=True)
    action_name = db.Column(db.String(50), nullable=False)

    request_actions = db.relationship(
        "RequestActions", back_populates="action"
    )
    check_actions = db.relationship("CheckActions", back_populates="action")


class Requests(db.Model):
    __tablename__ = "dq.requests"

    runId = db.Column(db.String(128), primary_key=True)
    request = db.Column(db.JSON, nullable=False)
    product_code = db.Column(
        db.String(20),
        db.ForeignKey("fs.products.product_code"),
        nullable=False,
    )
    status = db.Column(db.String(20), nullable=False)
    date = db.Column(db.TIMESTAMP, nullable=False)
    deleted = db.Column(db.Boolean, default=False, nullable=False)

    # product = db.relationship("Products", back_populates="requests")
    request_actions = db.relationship(
        "RequestActions", back_populates="request"
    )
    request_responses = db.relationship(
        "RequestResponse", back_populates="request"
    )


class RequestActions(db.Model):
    __tablename__ = "dq.request_actions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FIO = db.Column(db.String(100), nullable=False)
    runId = db.Column(
        db.String(128), db.ForeignKey("dq.requests.runId"), nullable=False
    )
    action_id = db.Column(
        db.SmallInteger, db.ForeignKey("dq.actions.action_id"), nullable=False
    )
    date = db.Column(db.TIMESTAMP, nullable=False)

    request = db.relationship("Requests", back_populates="request_actions")
    action = db.relationship("Actions", back_populates="request_actions")


class RequestResponse(db.Model):
    __tablename__ = "dq.request_response"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )
    runId = db.Column(
        db.String(128), db.ForeignKey("dq.requests.runId"), nullable=False
    )
    response_id = db.Column(
        db.Integer,
        db.ForeignKey("dq.responses.id"),
        nullable=False,
    )

    request = db.relationship("Requests", back_populates="request_responses")
    response = db.relationship("Responses", back_populates="request_responses")


class Responses(db.Model):
    __tablename__ = "dq.responses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    response_code = db.Column(db.SmallInteger)
    description = db.Column(db.Text, nullable=True)

    request_responses = db.relationship(
        "RequestResponse", back_populates="response"
    )


class CheckActions(db.Model):
    __tablename__ = "dq.scheck_actions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FIO = db.Column(db.String(100), nullable=False)
    product_code = db.Column(
        db.String(20),
        db.ForeignKey("fs.products.product_code"),
        nullable=False,
    )
    action_id = db.Column(
        db.SmallInteger, db.ForeignKey("dq.actions.action_id"), nullable=False
    )
    check_id = db.Column(
        db.SmallInteger, db.ForeignKey("dq.checks.check_id"), nullable=False
    )
    date = db.Column(db.TIMESTAMP, nullable=False)

    # product = db.relationship("Products", back_populates="check_actions")
    action = db.relationship("Actions", back_populates="check_actions")
    check = db.relationship("Checks", back_populates="check_actions")


class CheckProductStatus(db.Model):
    __tablename__ = "dq.check_product_status"

    id = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(
        db.String(20),
        db.ForeignKey("fs.products.product_code"),
        nullable=False,
    )
    check_id = db.Column(
        db.SmallInteger, db.ForeignKey("dq.checks.check_id"), nullable=False
    )
    condition = db.Column(db.Boolean, nullable=False)

    # product = db.relationship(
    #     "Products", back_populates="check_product_status"
    # )
    check = db.relationship("Checks", back_populates="check_product_status")


class Checks(db.Model):
    __tablename__ = "dq.checks"

    check_id = db.Column(db.SmallInteger, primary_key=True, autoincrement=True)
    type = db.Column(db.String(20), nullable=False)
    check_name = db.Column(db.String(100), nullable=False)

    check_actions = db.relationship("CheckActions", back_populates="check")
    check_product_status = db.relationship(
        "CheckProductStatus", back_populates="check"
    )
    check_history = db.relationship("CheckHistory", back_populates="check")
    # __table_args__ = (
    #     db.CheckConstraint(
    #         "type IN ('DQ1', 'DQ2.1', 'DQ2.2', 'DQ2.3')",
    # name="check_type_constraint"
    #     ),
    # )


class CheckHistory(db.Model):
    __tablename__ = "dq.check_history"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    runId = db.Column(db.String(128), nullable=False)
    check_id = db.Column(
        db.SmallInteger, db.ForeignKey("dq.checks.check_id"), nullable=False
    )
    product_type = db.Column(db.String(20), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    date = db.Column(
        db.TIMESTAMP, default=db.func.current_timestamp(), nullable=False
    )

    check = db.relationship("Checks", back_populates="check_history")
