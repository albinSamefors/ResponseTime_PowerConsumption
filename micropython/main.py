def run():
    from STM32_scripts import interrupt_tests, set_interval_tests

    times = set_interval_tests.lightsleep_test(100, 500 * 1000000)
    print(times)