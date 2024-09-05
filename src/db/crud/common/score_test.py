
from mongoengine.errors import SaveConditionError, ValidationError

from src.db.config.db import DataManager
from src.db.models.common.score_test import ScoreTestModel

DataManager.get_instance()


class ScoreTest:
    """ ScoreTest """

    def add_score(self, request, data):
        """

        """

        try:
            new_record = ScoreTestModel(
                score_resp=data

            )
            if new_record.save():
                request.app.logger.info("Score Test result saved in DB: %s" % data)
                return True
            return False
        except (SaveConditionError, ValidationError):
            request.app.logger.info("Error while saving record for Submission Testing score")
            return False
