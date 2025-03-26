from enum import Enum


class MetricDescriptions(str, Enum):
    A_MEASURE_OF_THE_MODELS_OWN_CONFUSION_IN_ITS_OUTPUT_HIGHER_SCORES_INDICATE_HIGHER_UNCERTAINTY = (
        "A measure of the model's own confusion in its output. Higher scores indicate higher uncertainty."
    )
    A_RESPONSE_LEVEL_METRIC_MEASURING_OUT_OF_ALL_THE_INFORMATION_IN_THE_CONTEXT_PERTINENT_TO_THE_QUESTION_HOW_MUCH_WAS_COVERED_IN_THE_ANSWER = "A response-level metric measuring 'out of all the information in the context pertinent to the question, how much was covered in the answer?'"
    BLEU_IS_A_CASE_SENSITIVE_MEASUREMENT_OF_THE_DIFFERENCE_BETWEEN_AN_MODEL_GENERATION_AND_TARGET_GENERATION_AT_THE_SENTENCE_LEVEL = "BLEU is a case-sensitive measurement of the difference between an model generation and target generation at the sentence-level."
    CLASSIFIES_THE_SENTIMENT_IN_THE_MODELS_RESPONSE_INTO_ONE_OF_JOY_LOVE_FEAR_SURPRISE_SADNESS_ANGER_ANNOYANCE_CONFUSION_OR_NEUTRAL = "Classifies the sentiment in the model's response into one of joy, love, fear, surprise, sadness, anger, annoyance, confusion or neutral."
    CLASSIFIES_THE_SENTIMENT_OF_THE_USERS_INPUT_INTO_ONE_OF_JOY_LOVE_FEAR_SURPRISE_SADNESS_ANGER_ANNOYANCE_CONFUSION_OR_NEUTRAL = "Classifies the sentiment of the user's input into one of joy, love, fear, surprise, sadness, anger, annoyance, confusion or neutral."
    COST_OF_ALL_THE_METRICS_THAT_CALL_THE_OPENAI_API = "Cost of all the metrics that call the OpenAI API."
    COST_OF_EXECUTING_THE_RUN_AND_DOES_NOT_INCLUDE_ANY_COSTS_INCURRED_FOR_METRIC_CALCULATION = (
        "Cost of executing the run and does not include any costs incurred for metric calculation."
    )
    DETECTS_WHETHER_THE_MODEL_SELECTED_THE_RIGHT_TOOL_WITH_THE_RIGHT_ARGUMENTS = (
        "Detects whether the model selected the right Tool with the right arguments."
    )
    DETECTS_WHETHER_THE_TOOL_EXECUTED_SUCCESSFULLY_I_E_WITHOUT_ERRORS = (
        "Detects whether the Tool executed successfully (i.e. without errors)."
    )
    DETECTS_WHETHER_THE_USER_SUCCESSFULLY_ACCOMPLISHED_OR_ADVANCED_TOWARDS_THEIR_GOAL = (
        "Detects whether the user successfully accomplished or advanced towards their goal."
    )
    MEASURES_HOW_MUCH_OF_THE_TEXT_IN_THE_RETRIEVED_CHUNKS_WAS_RELEVANT_TO_THE_RESPONSE_COMPOSED_BY_THE_MODEL = (
        "Measures how much of the text in the retrieved chunks was relevant to the response composed by the model."
    )
    MEASURES_HOW_MUCH_OF_THE_TEXT_IN_THE_RETRIEVED_CHUNKS_WAS_USED_BY_THE_MODEL_TO_COMPOSE_ITS_RESPONSE = (
        "Measures how much of the text in the retrieved chunks was used by the model to compose its response."
    )
    MEASURES_HOW_SEXIST_A_RESPONSE_MIGHT_BE_PERCEIVED_RANGING_IN_THE_VALUES_OF_0_1_1_BEING_MORE_SEXIST = (
        "Measures how 'sexist' a response might be perceived ranging in the values of 0-1 (1 being more sexist)."
    )
    MEASURES_HOW_SEXIST_A_USERS_INPUT_MIGHT_BE_PERCEIVED_RANGING_IN_THE_VALUES_OF_0_1_1_BEING_MORE_SEXIST = (
        "Measures how 'sexist' a user's input might be perceived ranging in the values of 0-1 (1 being more sexist)."
    )
    MEASURES_HOW_WELL_THE_LLM_FOLLOWS_THE_SYSTEM_INSTRUCTIONS_PROVIDED_IN_THE_PROMPT = (
        "Measures how well the LLM follows the system instructions provided in the prompt."
    )
    MEASURES_HOW_WELL_THE_WORKFLOWS_RESPONSE_ALIGNS_WITH_THE_GROUND_TRUTH_PROVIDED = (
        "Measures how well the workflow's response aligns with the ground truth provided."
    )
    MEASURES_THE_PERPLEXITY_OF_THE_PROMPT_LOWER_PERPLEXITY_SCORE_IS_GENERALLY_CONSIDERED_TO_BE_BETTER_BECAUSE_IT_MEANS_THE_MODEL_IS_LESS_SURPRISED_BY_THE_TEXT_AND_CAN_PREDICT_THE_NEXT_WORD_IN_A_SENTENCE_WITH_HIGHER_ACCURACY = "Measures the perplexity of the prompt. Lower perplexity score is generally considered to be better because it means the model is less surprised by the text and can predict the next word in a sentence with higher accuracy."
    MEASURES_THE_POTENTIAL_PRESENCE_OF_FACTUAL_ERRORS_OR_INCONSISTENCIES_IN_THE_MODELS_RESPONSE = (
        "Measures the potential presence of factual errors or inconsistencies in the model's response."
    )
    MEASURES_THE_PRESENCE_AND_SEVERITY_OF_HARMFUL_OFFENSIVE_OR_ABUSIVE_LANGUAGE = (
        "Measures the presence and severity of harmful, offensive, or abusive language"
    )
    MEASURES_THE_PRESENCE_AND_SEVERITY_OF_HARMFUL_OFFENSIVE_OR_ABUSIVE_LANGUAGE_IN_THE_MODELS_RESPONSE = (
        "Measures the presence and severity of harmful, offensive, or abusive language in the model's response"
    )
    MEASURES_THE_PRESENCE_OF_PROMPT_INJECTION_ATTACKS_IN_INPUTS_TO_THE_LLM = (
        "Measures the presence of prompt injection attacks in inputs to the LLM."
    )
    MEASURES_THE_RELEVANCE_OF_THE_RETRIEVED_CONTEXT_TO_THE_USERS_QUERY_AS_THE_SEMANTIC_DISTANCE_BETWEEN_THE_TWO = (
        "Measures whether the retrieved context has enough information to answer the user's query."
    )
    MEASURES_WHETHER_THE_LLMS_RESPONSE_IS_SUPPORTED_BY_OR_BAKED_IN_THE_CONTEXT_PROVIDED = (
        "Measures whether the LLM's response is supported by (or baked in) the context provided. "
    )
    MEASURES_WHICH_DOCUMENTS_OR_CHUNKS_RETRIEVED_WERE_USED_BY_THE_MODEL_TO_GENERATE_A_RESPONSE = (
        "Measures which documents or chunks retrieved were used by the model to generate a response."
    )
    MEASURES_WHICH_DOCUMENTS_OR_CHUNKS_RETRIEVED_WERE_USED_BY_THE_MODEL_TO_GENERATE_A_RESPONSE_AND_HOW_MUCH_OF_THE_TEXT_IN_THE_RETRIEVED_CHUNKS_WAS_USED_BY_THE_MODEL_TO_COMPOSE_ITS_RESPONSE = "Measures which documents or chunks retrieved were used by the model to generate a response, and how much of the text in the retrieved chunks was used by the model to compose its response."
    ROUGE_MEASURES_THE_UNIGRAM_OVERLAP_BETWEEN_MODEL_GENERATION_AND_TARGET_GENERATION_AS_A_SINGLE_F_1_SCORE = (
        "ROUGE measures the unigram overlap between model generation and target generation as a single F-1 score."
    )
    TRACKS_THE_PRESENCE_OF_PERSONAL_IDENTIFIABLE_INFORMATION_IN_THE_LLMS_RESPONSES = (
        "Tracks the presence of personal identifiable information in the LLM's responses"
    )
    TRACKS_THE_PRESENCE_OF_PERSONAL_IDENTIFIABLE_INFORMATION_IN_THE_USERS_INPUT = (
        "Tracks the presence of personal identifiable information in the user's input"
    )

    def __str__(self) -> str:
        return str(self.value)
