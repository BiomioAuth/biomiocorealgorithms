from ...constants import REDIS_PARTIAL_RESULTS_KEY, REDIS_RESULTS_COUNTER_KEY, REDIS_DO_NOT_STORE_RESULT_KEY
from recognition.messages import create_error_message, create_result_message
from ...protocol.data_stores.algorithms_data_store import AlgorithmsDataStore
from general.defs import INTERNAL_TRAINING_ERROR


def store_verification_results(result, callback_code):
    AlgorithmsDataStore.instance().delete_data(key=REDIS_RESULTS_COUNTER_KEY % callback_code)
    AlgorithmsDataStore.instance().delete_data(key=REDIS_PARTIAL_RESULTS_KEY % callback_code)
    AlgorithmsDataStore.instance().store_job_result(record_key=REDIS_DO_NOT_STORE_RESULT_KEY % callback_code,
                                                    record_dict=result, callback_code=callback_code)


def partial_results_handler(callback_code, record):
    AlgorithmsDataStore.instance().append_value_to_list(key=REDIS_PARTIAL_RESULTS_KEY % callback_code,
                                                        value=record)
    results_counter = AlgorithmsDataStore.instance().decrement_int_value(REDIS_RESULTS_COUNTER_KEY %
                                                                         callback_code)
    if results_counter <= 0:
        gathered_results = AlgorithmsDataStore.instance().get_stored_list(REDIS_PARTIAL_RESULTS_KEY %
                                                                          callback_code)
        if results_counter < 0:
            result = create_error_message(INTERNAL_TRAINING_ERROR, "jobs_counter", "Number of jobs is incorrect.")
        else:
            result = create_result_message({'data_list': gathered_results}, 'detection')
        store_verification_results(result=result, callback_code=callback_code)
        return True
    return False
