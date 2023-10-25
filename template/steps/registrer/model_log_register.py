# {% include 'template/license_header' %}

from typing import Optional

import mlflow
from transformers import (
    PreTrainedModel,
    PreTrainedTokenizerBase,
)
from zenml import step
from zenml.client import Client
from zenml.integrations.mlflow.experiment_trackers import MLFlowExperimentTracker
from zenml.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

# Get experiment tracker
experiment_tracker = Client().active_stack.experiment_tracker

# Check if experiment tracker is set and is of type MLFlowExperimentTracker
if not experiment_tracker or not isinstance(
    experiment_tracker, MLFlowExperimentTracker
):
    raise RuntimeError(
        "Your active stack needs to contain a MLFlow experiment tracker for "
        "this example to work."
    )


@step(experiment_tracker=experiment_tracker.name)
def model_log_register(
    model: PreTrainedModel,
    tokenizer: PreTrainedTokenizerBase,
    mlflow_model_name: Optional[str] = "model",
):
    """
    Register model to MLFlow.

    This step takes in a model and tokenizer artifact previously loaded and pre-processed by
    other steps in your pipeline, then registers the model to MLFlow for deployment.

    Model training steps should have caching disabled if they are not deterministic
    (i.e. if the model training involve some random processes like initializing
    weights or shuffling data that are not controlled by setting a fixed random seed).

    Args:
        model: The model.
        tokenizer: The tokenizer.

    Returns:
        The trained model and tokenizer.
    """
    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    # Log the model
    components = {
        "model": model,
        "tokenizer": tokenizer,
    }
    mlflow.transformers.log_model(
        transformers_model=components,
        artifact_path=mlflow_model_name,
        registered_model_name=mlflow_model_name,
    )
    ### YOUR CODE ENDS HERE ###
