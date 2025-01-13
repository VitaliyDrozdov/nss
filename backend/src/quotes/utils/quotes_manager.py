import logging

from sqlalchemy.exc import SQLAlchemyError

from quotes.config import db
from quotes.models.core import Scores
from quotes.models.quotes import QuoteData

logger = logging.getLogger(__name__)


class QuoteManager:
    """
    Класс для управления загрузкой, валидацией и сохранением котировок.
    """

    def __init__(self):
        self._record = False

    @staticmethod
    def check_existing_record(run_id, quote_id):
        existing_score = Scores.query.filter_by(
            run_id=run_id, quote_id=quote_id
        ).first()
        return existing_score is not None

    def save_quote(self, quote_data, prediction):
        """
        Сохраняет данные котировки и результат предсказания в базу данных.

        :param quote_data: объект типа QuoteData
        :param prediction: результат предсказания модели
        """
        try:
            if not isinstance(quote_data, QuoteData):
                raise ValueError(
                    f"quote_data должен быть объектом QuoteData. "
                    f"Получено: {type(quote_data)}"
                )

            run_id = quote_data.quote.header.runId
            quote_id = quote_data.quote.header.quoteId
            model_id = prediction.get("predict").get("model_id")
            predict = prediction.get("predict").get("score")

            if not all([run_id, quote_id, model_id, predict]):
                raise ValueError(
                    f"Некоторые поля отсутствуют в методе save_quote. "
                    f"Данные: run_id={run_id}, quote_id={quote_id}, "
                    f"model_id={model_id}, predict={predict}"
                )
            self._record = self.check_existing_record(run_id, quote_id)
            if self._record:
                logger.info(
                    f"Запись с quote_id={quote_id}"
                    "и run_id={run_id} уже существует."
                )
                return
            score_entry = Scores(
                model_id=model_id,
                predict=predict,
                run_id=run_id,
                quote_id=quote_id,
            )

            db.session.add(score_entry)
            db.session.commit()
            logger.info(f"Данные сохранены в базу: {quote_id} ({run_id})")

        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Ошибка при сохранении данных Score в БД: {e}")
            raise
        except Exception as e:
            logger.error(f"Ошибка при вызове QuoteManager: {e}")
            raise

    @staticmethod
    def load_scores(run_id=None, quote_id=None):
        """
        Загружает результаты расчёта по идентификаторам.

        :param run_id: идентификатор запуска
        :param quote_id: идентификатор котировки
        :return: список результатов
        """
        try:
            query = Scores.query
            if run_id:
                query = query.filter_by(run_id=run_id)
            if quote_id:
                query = query.filter_by(quote_id=quote_id)

            scores = query.all()
            return scores

        except SQLAlchemyError as e:
            logger.error(f"Ошибка при загрузке данных: {e}")
            raise
