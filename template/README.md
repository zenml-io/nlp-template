# {{project_name}}

This is a comprehensive supervised ML project built with the
ZenML framework and its integration. The project will be 
a comprehensive starting point for anyone looking to build
and deploy NLP models using the ZenML framework by streamlining
the process of training, promoting, and deploying NLP models
with a focus on reproducibility, scalability, and ease of use.
The project was generated from the [NLP ZenML project template](https://github.com/zenml-io/template-nlp).
with the following properties:

- Project name: {{project_name}}
- Technical Name: {{product_name}}
- Version: `{{version}}`
{%- if open_source_license %}
- Licensed with {{open_source_license}} to {{full_name}}<{{email}}>
{%- endif %}
- Deployment environment: `{{target_environment}}`
{%- if zenml_server_url!='' %}
- Remote ZenML Server URL: `{{zenml_server_url}}`
{%- endif %}

Settings of your project are:
- Accelerator: `{{accelerator}}`
{%- if metric_compare_promotion %}
- Trained model promotion to `{{target_environment}}` based on accuracy metric vs currently deployed model
{%- else %}
- Every trained model will be promoted to `{{target_environment}}`
{%- endif %}
{%- if deploy_locally %}
- Local deployment enabled
{%- endif %}
{%- if deploy_to_huggingface %}
- Deployment to HuggingFace Hub enabled
{%- endif %}
{%- if deploy_to_skypilot %}
- Deployment to SkyPilot enabled
{%- endif %}
{%- if dataset %}
- Dataset: `{{dataset}}`
{%- endif %}
{%- if model %}
- Model: `{{model}}`
{%- endif %}
{%- if cloud_provider %}
- Cloud provider: `{{cloud_provider}}`
{%- endif %}
{%- if notify_on_failures and notify_on_successes %}
- Notifications about failures and successes enabled
{%- elif notify_on_failures %}
- Notifications about failures enabled
{%- elif notify_on_successes %}
- Notifications about success enabled
{%- else %}
- All notifications disabled
{%- endif %}

## 👋 Introduction

Welcome to your newly generated "{{project_name}}" project! This is
a great way to get hands-on with ZenML using production-like template. 
The project contains a collection of standard and custom ZenML steps, 
pipelines and other artifacts and useful resources that can serve as a 
solid starting point for your smooth journey with ZenML.

What to do first? You can start by giving the the project a quick run. The
project is ready to be used and can run as-is without any further code
changes! You can try it right away by installing ZenML, the needed
ZenML integration and then calling the CLI included in the project. We also
recommend that you start the ZenML UI locally to get a better sense of what
is going on under the hood:

```bash
# Set up a Python virtual environment, if you haven't already
python3 -m venv .venv
source .venv/bin/activate
# Install requirements & integrations
make setup
# Optionally, provision default local stack
make install-local-stack
# Start the ZenML UI locally (recommended, but optional);
# the default username is "admin" with an empty password
zenml up
# Run the pipeline included in the project
python run.py
```

When the pipelines are done running, you can check out the results in the ZenML
UI by following the link printed in the terminal (or you can go straight to
the [ZenML UI pipelines run page](http://127.0.0.1:8237/workspaces/default/all-runs?page=1).

Next, you should:

* look at the CLI help to see what you can do with the project:
```bash
python run.py --help
```
* go back and [try out different parameters](https://github.com/zenml-io/template-nlp#-template-parameters)
for your generated project. For example, you could disable hyperparameters
tuning and use your favorite model architecture or promote every trained model,
if you haven't already!
* take a look at [the project structure](#📜-project-structure) and the code
itself. The code is heavily commented and should be easy to follow.
* read the [ZenML documentation](https://docs.zenml.io) to learn more about
various ZenML concepts referenced in the code and to get a better sense of
what you can do with ZenML.
* start building your own ZenML project by modifying this code

## 📦 What's in the box?

The {{project_name}} project demonstrates how the most important steps of 
the ML Production Lifecycle can be implemented in a reusable way remaining 
agnostic to the underlying infrastructure for a Natural Language Processing
(NLP) task.

This template uses one of these datasets:
* [IMDB Movie Reviews](https://huggingface.co/datasets/imdb)
* [Financial News](https://huggingface.co/datasets/zeroshot/twitter-financial-news-sentiment)
* [Airlines Reviews](https://huggingface.co/datasets/Shayanvsf/US_Airline_Sentiment)

and one of these models:
* [DistilBERT](https://huggingface.co/distilbert-base-uncased)
* [RoBERTa](https://huggingface.co/roberta-base)
* [BERT](https://huggingface.co/bert-base-uncased)

It consists of three pipelines with the following high-level setup:
<p align="center">
  <img height=500 src=".assets/00_pipelines_composition.png">
</p>

All pipelines are leveraging the Model Control Plane to bring all parts together - the training pipeline creates and promotes a new Model Control Plane version with a trained model object in it, deployment pipeline uses the inference Model Control Plane version (the one promoted during training) to create a deployment service and inference pipeline using deployment service from the inference Model Control Plane version and store back new set of predictions as a versioned data artifact for future use. This makes those pipelines closely connected while ensuring that only quality-assured Model Control Plane versions are used to produce predictions delivered to stakeholders.
* [CT] Training
  * Load the training dataset from HuggingFace Datasets
  * Load Tokenizer from HuggingFace Models based on the model name
  * Tokenize the training dataset and store the tokenizer as an artifact
  * Train and evaluate a model object using the training dataset and store it as an artifact
  * Register the model object as a new inference Model Control Plane version
* [CD] Promotion
  * Evaluate the latest Model Control Plane version using the evaluation metric
    * Compare the evaluation metric of the latest Model Control Plane version with the evaluation metric of the currently promoted Model Control Plane version
    * If the evaluation metric of the latest Model Control Plane version is better than the evaluation metric of the currently promoted Model Control Plane version, promote the latest Model Control Plane version to the specified stage
    * If the evaluation metric of the latest Model Control Plane version is worse than the evaluation metric of the currently promoted Model Control Plane version, do not promote the latest Model Control Plane version
* [CD] Deployment
  * Load the inference Model Control Plane version
    * Save the Model locally (for that this pipeline needs to be run on the local machine)
  * Deploy the Model to the specified environment
    * If the specified environment is HuggingFace Hub, upload the Model to the HuggingFace Hub
    * If the specified environment is SkyPilot, deploy the Model to the SkyPilot
    * If the specified environment is local, do not deploy the Model

In [the repository documentation](https://github.com/zenml-io/template-nlp#-how-this-template-is-implemented),
you can find more details about every step of this template.

The project code is meant to be used as a template for your projects. For
this reason, you will find several places in the code specifically marked
to indicate where you can add your code:

```python
### ADD YOUR OWN CODE HERE - THIS IS JUST AN EXAMPLE ###
...
### YOUR CODE ENDS HERE ###
```

## 📜 Project Structure

The project loosely follows [the recommended ZenML project structure](https://docs.zenml.io/user-guide/starter-guide/follow-best-practices):

```
.
├── gradio                    # Gradio app for inference
│   ├── __init__.py          # Gradio app initialization
│   ├── app.py               # Gradio app entrypoint
│   ├── Dockerfile           # Gradio app Dockerfile
│   ├── requirements.txt     # Gradio app Python dependencies
│   └── serve.yaml           # Gradio app SkyPilot deployment configuration
├── pipelines                 # `zenml.pipeline` implementations
│   ├── __init__.py
│   ├── deployment.py         # deployment pipeline
│   ├── promotion.py          # promotion pipeline
│   └── training.py           # training pipeline
├── steps                     # `zenml.steps` implementations
│   ├── __init__.py
│   ├── alerts                # `zenml.steps.alerts` implementations
│   │   ├── __init__.py
│   │   └── notify_on.py      # notify step
│   ├── dataset_loader        # `zenml.steps.dataset_loader` implementations
│   │   ├── __init__.py
│   │   └── data_loader.py    # data loader step
│   ├── deploying             # `zenml.steps.deploying` implementations
│   │   ├── __init__.py
│   │   ├── save_model.py     # save model step
│   │   ├── deploy_locally.py # deploy locally step
│   │   ├── deploy_to_huggingface.py  # deploy to HuggingFace Hub step
│   │   └── deploy_to_skypilot.py     # deploy to SkyPilot step
│   ├── promotion             # `zenml.steps.promotion` implementations
│   │   ├── __init__.py
│   │   ├── promote_latest.py # promote latest step
│   │   ├── promote_metric_compare_promoter.py  # metric compare promoter step
│   │   └── promote_get_metrics.py   # get metric step
│   ├── register            # `zenml.steps.register` implementations
│   │   ├── __init__.py
│   │   └── model_log_register.py  # model log register step
│   ├── tokenization         # `zenml.steps.tokenization` implementations
│   │   ├── __init__.py
│   │   └── tokenization.py   # tokenization step
│   ├── tokenizer_loader     # `zenml.steps.tokenizer_loader` implementations
│   │   ├── __init__.py
│   │   └── tokenizer_loader.py  # tokenizer loader step
│   └── training             # `zenml.steps.training` implementations
│       ├── __init__.py
│       └── trainer.py          # train step
└── utils                     # `zenml.utils` implementations
│   └── misc.py               # miscellaneous utilities
├── README.md                 # this file
├── requirements.txt          # extra Python dependencies
├── config.yaml               # ZenML configuration file
└── run.py                    # CLI tool to run pipelines on ZenML Stack
```
