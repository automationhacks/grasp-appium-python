import time


def wait_till(expected, func, *args, timeout=10, sleep_for=2, sleep_factor=0.5):
    start_time = time.time()
    sleep_time = sleep_for

    while time.time() - start_time < timeout:
        if args and args[0] is not None:
            result = func(*args)
        else:
            result = func()

        if result == expected:
            return result

        print("Still not expected result: {}".format(result))
        print("Snoozing for {} seconds".format(sleep_time))
        time.sleep(sleep_time * sleep_factor)

    return None
