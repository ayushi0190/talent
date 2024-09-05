
from datetime import datetime
from mongoengine.errors import SaveConditionError, ValidationError
from src.db.config.db import DataManager
from src.db.models.sovren.audit_trails import AuditTrails
from src.services.common.config.common_config import common_url_settings

DataManager.get_instance()


class AuditTrailsSchema:
    """Audit Trails Schema"""

    def add(self, service_name: str, client_id: str) -> bool:
        """
        Add record
        :param service_name: String
        :param client_id: String
        :return:
        """
        # Check if searched content already exist or not
        try:
            count = 1
            proc_date = datetime.today().date()
            existing_record = AuditTrails.objects(client_id=client_id).first()
            if existing_record is None:
                new_record = AuditTrails(
                    service_name=service_name,
                    client_id=client_id,
                    count=count,
                    proc_date = proc_date
                )
                if new_record.save():
                    return True
                return False
            else:
                existing_record = AuditTrails.objects(client_id=client_id,service_name=service_name).first()
                if existing_record is None:
                    new_record = AuditTrails(
                        service_name=service_name,
                        client_id=client_id,
                        count=count,
                        proc_date = proc_date
                    )
                    if new_record.save():
                        return True
                    return False
                else:
                    existing_record = AuditTrails.objects(client_id=client_id,service_name=service_name,proc_date=proc_date).first()
                    if existing_record is None:
                        new_record = AuditTrails(
                            service_name=service_name,
                            client_id=client_id,
                            count=count,
                            proc_date = proc_date
                        )
                        if new_record.save():
                            return True
                        return False
                    else:
                        existing_record.count = existing_record.count + 1
                        existing_record.save()
                        return False

        except (SaveConditionError, ValidationError):
            return False

    def get_data(self, client_id : str, service_name: str, start_date: str) -> dict:
        """
        Get the audit trails record by client_id,service_name
        :param service_name: String
        :param client_id: String
        :return:
        """
        if service_name == common_url_settings.get("AUDIT_ALL"):
            audit_data = AuditTrails.objects(client_id=client_id,proc_date__gte=start_date)
        else:
            audit_data = AuditTrails.objects(client_id=client_id,service_name = service_name, proc_date__gte=start_date)
        return audit_data
