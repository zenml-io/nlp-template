# {% include 'template/license_header' %}

from typing import Optional, Tuple
from typing_extensions import Annotated

import mlflow
from datasets import DatasetDict
from transformers import (
    DataCollatorWithPadding,
    PreTrainedModel,
    PreTrainedTokenizerBase,
    Trainer,
    TrainingArguments,
    AutoModelForSequenceClassification,
)
from zenml import step
from zenml.client import Client
from zenml.integrations.mlflow.experiment_trackers import MLFlowExperimentTracker
from zenml.logger import get_logger

from template.utils.misc import compute_metrics

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
def model_trainer(
    tokenized_dataset: DatasetDict,
    tokenizer: PreTrainedTokenizerBase,
    num_labels: Optional[int] = None,
    train_batch_size: Optional[int] = 16,
    num_epochs: Optional[int] = 3,
    learning_rate: Optional[float] = 2e-5,
    load_best_model_at_end: Optional[bool] = True,
    eval_batch_size: Optional[int] = 16,
    weight_decay: Optional[float] = 0.01,
    mlflow_model_name: Optional[str] = "model",
) -> Tuple[Annotated[PreTrainedModel, "model"], Annotated[PreTrainedTokenizerBase, "tokenizer"]]:
    """
    Configure and train a model on the training dataset.

    This step takes in a dataset artifact previously loaded and pre-processed by 
    other steps in your pipeline, then configures and trains a model on it. The 
    model is then returned as a step output artifact.

    Model training steps should have caching disabled if they are not deterministic 
    (i.e. if the model training involve some random processes like initializing 
    weights or shuffling data that are not controlled by setting a fixed random seed). 


    Args:
        hf_pretrained_model: The pre-trained model.
        tokenized_dataset: The tokenized dataset.
        tokenizer: The tokenizer.
        num_labels: The number of labels.
        train_batch_size: The training batch size.
        num_epochs: The number of epochs.
        learning_rate: The learning rate.
        load_best_model_at_end: Whether to load the best model at the end.
        eval_batch_size: The evaluation batch size.
        weight_decay: The weight decay.

    Returns:
        The trained model and tokenizer.
    """
    ### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
    # Select the appropriate datasets based on the dataset type
    {%- if dataset == 'imdb' %}
    train_dataset = tokenized_dataset['train']
    eval_dataset = tokenized_dataset['test']
    {%- else %}
    train_dataset = tokenized_dataset['train']
    eval_dataset = tokenized_dataset['validation']
    {%- endif %}

    # Initialize data collator
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    # Set the number of labels
    num_labels = num_labels or len(train_dataset.unique("labels"))

    # Set the logging steps
    logging_steps = len(train_dataset) // train_batch_size

    # Initialize training arguments
    training_args = TrainingArguments(
        output_dir="zenml_artifact",
        learning_rate=learning_rate,
        per_device_train_batch_size=train_batch_size,
        per_device_eval_batch_size=eval_batch_size,
        num_train_epochs=num_epochs,
        weight_decay=weight_decay,
        evaluation_strategy='steps',
        save_strategy='steps',
        logging_steps=logging_steps,
        save_total_limit=5,
        report_to="mlflow",
        load_best_model_at_end=load_best_model_at_end,
    )
    logger.info(f"Training arguments: {training_args}")

    # Load the model
    model = AutoModelForSequenceClassification.from_pretrained(
        {{model}}, num_labels=num_labels
    )

    # Enable autologging
    mlflow.transformers.autolog()

    # Initialize the trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        compute_metrics=compute_metrics,
        data_collator=data_collator,
    )

    # Train and evaluate the model
    trainer.train()
    trainer.evaluate()
    ### YOUR CODE ENDS HERE ###

    return model, tokenizer