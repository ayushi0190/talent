

from typing import List, Dict
from pydantic import BaseModel, validator, conlist


class ClientCategoryWeightValidations(BaseModel):
    """
    Default weights for different categories
    """
    job_category: str
    category_weights: Dict[str, float]

    @validator('category_weights')
    def category_weights_must_be_dict(cls, category_weights):
        """
        Custom validation message for weights
        :param weights:
        :return:
        """
        if not isinstance(category_weights, dict):
            raise ValueError('Must be of list type')
        if category_weights is None or len(category_weights) == 0:
            raise ValueError('category_weights can not be null')
        return category_weights

    @validator('job_category')
    def job_category_must_be_str(cls, job_category):
        """
        Custom validation message for job_category
        :param job_category:
        :return:
        """
        if not isinstance(job_category, str):
            raise ValueError('Must be of string type')
        if job_category is None or len(job_category) == 0:
            raise ValueError('job_category can not be null')
        return job_category

class ClientCategoryWeightValidations_Old(BaseModel):
    """
    Default weights for different categories
    """
    categories: conlist(str, min_items=1)
    weights: conlist(int, min_items=1)
    job_category: str

    @validator('categories')
    def categories_must_be_list_of_str(cls, categories):
        """
        Custom validation message for categories
        :param categories:
        :return:
        """
        if not isinstance(categories, list):
            raise ValueError('Must be of list type')
        if categories is None or len(categories) == 0:
            raise ValueError('Categories can not be null')
        return categories

    @validator('weights')
    def weights_must_be_list_of_str(cls, weights):
        """
        Custom validation message for weights
        :param weights:
        :return:
        """
        if not isinstance(weights, list):
            raise ValueError('Must be of list type')
        if weights is None or len(weights) == 0:
            raise ValueError('Weights can not be null')
        return weights

    @validator('job_category')
    def job_category_must_be_str(cls, job_category):
        """
        Custom validation message for job_category
        :param job_category:
        :return:
        """
        if not isinstance(job_category, str):
            raise ValueError('Must be of string type')
        return job_category
