"""
Main Analyzer worker class.
"""
import logging
import threading
import time
import traceback
from os import getpid
from typing import Any, Callable, Dict, Optional
from threading import Thread, Timer

import sdnotify

from analyzer import __version__
from analyzer.configuration import Config
from analyzer.utils.enums import State
from analyzer.utils.exceptions import OperationalException, TemporaryError
from analyzer.analyzer_bot import Analyzer
from analyzer.configuration import constants
from analyzer.utils.repeatable_timer import TimerEx

logger = logging.getLogger(__name__)


class Worker:
    """
    Analyzer worker class
    """

    def __init__(self, config: Config) -> None:
        """
        Init all variables and objects the bot needs to work
        """
        logger.info(f"Starting worker {__version__}")

        self._config = config
        self._init(False)

        # def f(id):
        #     print 'thread function %s' %(id)
        #     return

        # if __name__ == '__main__':
        #     for i in range(3):
        #         t = threading.Thread(target=f, args=(i,))
        #         t.start()

        # Tell systemd that we completed initialization phase
        self._notify("READY=1")

    def _init(self, reconfig: bool) -> None:
        """
        Also called from the _reconfigure() method (with reconfig=True).
        """
        if reconfig or self._config is None:
            # Load configuration
            self._config = Config()

        # Init the instance of the bot
        self.Analyzer = Analyzer(self._config)

        # self._get_running_threads
        # self._stop_threads(self._get_running_threads)

        self._throttle_secs = self._config.PROCESS_THROTTLE_SECS
        self._heartbeat_interval = self._config.HEARTBEAT_INTERVAL

        self._short_throttle_secs = self._config.SHORT_THROTTLE
        self._medium_throttle_secs = self._config.MEDIUM_THROTTLE
        self._long_throttle_secs = self._config.LONG_THROTTLE

        self.short_shredder = TimerEx(
            self._config.HEARTBEAT_INTERVAL, self.Analyzer.process_short())
        self.medium_shredder = TimerEx(
            self._medium_throttle_secs, self.Analyzer.process_medium())
        self.long_shredder = TimerEx(
            self._long_throttle_secs, self.Analyzer.process_long())

        logger.info(
            f"Short shreader is alive? {self.short_shredder.is_alive()}")
        logger.info(
            f"Med shreader is alive? {self.medium_shredder.is_alive()}")
        logger.info(f"Long shreader is alive? {self.long_shredder.is_alive()}")

        # Make daemons
        # self.short_shredder.daemon = True
        # self.medium_shredder.daemon = True
        # self.long_shredder.daemon = True

        self._sd_notify = sdnotify.SystemdNotifier()
        #  if \
        #     self._config.get('internals', {}).get('sd_notify', False) else None

    def _notify(self, message: str) -> None:
        """
        Removes the need to verify in all occurrences if sd_notify is enabled
        :param message: Message to send to systemd if it's enabled.
        """
        if self._sd_notify:
            logger.debug(f"sd_notify: {message}")
            self._sd_notify.notify(message)

    def run(self) -> None:
        state = None
        while True:
            state = self._worker(old_state=state)
            if state == State.RELOAD_CONFIG:
                self._reconfigure()

    def _get_running_threads(self):
        return threading.enumerate()

    def _worker(self, old_state: Optional[State]) -> State:
        """
        The main routine that runs each throttling iteration and handles the states.
        :param old_state: the previous service state from the previous call
        :return: current service state
        """
        state = self.Analyzer.state

        # Log state transition
        if state != old_state:
            self.Analyzer.notify_status(f'{state.name.lower()}')

            logger.info(f"Changing state to: {state.name}")
            # if state == State.RUNNING:

            # if state == State.STOPPED:
            #     self.Analyzer.check_for_open_trades()

            # Reset heartbeat timestamp to log the heartbeat message at
            # first throttling iteration when the state changes
            self._heartbeat_msg = 0

        if state == State.STOPPED:
            # Ping systemd watchdog before sleeping in the stopped state
            self._notify("WATCHDOG=1\nSTATUS=State: STOPPED.")

            self._throttle(func=self._process_stopped,
                           throttle_secs=self._throttle_secs)
            self.short_shredder.cancel()
            self.medium_shredder.cancel()
            self.long_shredder.cancel()

        elif state == State.RUNNING:
            # Ping systemd watchdog before throttling
            self._notify("WATCHDOG=1\nSTATUS=State: RUNNING.")
            # self._throttle(func=self._process_running,
            #                throttle_secs=self._short_throttle_secs)
            self.short_shredder.start()
            self.medium_shredder.start()
            self.long_shredder.start()

        if self._heartbeat_interval:
            now = time.time()
            if (now - self._heartbeat_msg) > self._heartbeat_interval:
                logger.info(f"Bot heartbeat. PID={getpid()}, "
                            f"version='{__version__}', state='{state.name}'")
                self._heartbeat_msg = now

        return state

    def _throttle(self, func: Callable[..., Any], throttle_secs: float, *args, **kwargs) -> Any:
        """
        Throttles the given callable that it
        takes at least `min_secs` to finish execution.
        :param func: Any callable
        :param throttle_secs: throttling interation execution time limit in seconds
        :return: Any (result of execution of func)
        """
        self.last_throttle_start_time = time.time()
        logger.debug("========================================")
        result = func(*args, **kwargs)
        time_passed = time.time() - self.last_throttle_start_time
        sleep_duration = max(throttle_secs - time_passed, 0.0)
        logger.debug(f"Throttling with '{func.__name__}()': sleep for {sleep_duration:.2f} s, "
                     f"last iteration took {time_passed:.2f} s.")
        time.sleep(sleep_duration)
        return result

    def _process_stopped(self) -> None:
        self.Analyzer.process_stopped()

    def _process_running(self) -> None:
        try:
            logger.info("processing")
        except TemporaryError as error:
            logger.warning(
                f"Error: {error}, retrying in {constants.RETRY_TIMEOUT} seconds...")
            time.sleep(constants.RETRY_TIMEOUT)
        except OperationalException:
            tb = traceback.format_exc()
            hint = 'Issue `/start` if you think it is safe to restart.'

            self.Analyzer.notify_status(
                f'OperationalException:\n```\n{tb}```{hint}')

            logger.exception('OperationalException. Stopping trader ...')
            self.Analyzer.state = State.STOPPED

    def _reconfigure(self) -> None:
        """
        Cleans up current Analyzerbot instance, reloads the configuration and
        replaces it with the new instance
        """
        # Tell systemd that we initiated reconfiguration
        self._notify("RELOADING=1")

        # Clean up current Analyzer modules
        self.Analyzer.cleanup()

        # Load and validate config and create new instance of the bot
        self._init(True)

        self.Analyzer.notify_status('config reloaded')

        # Tell systemd that we completed reconfiguration
        self._notify("READY=1")

    def exit(self) -> None:
        # Tell systemd that we are exiting now
        self._notify("STOPPING=1")

        if self.Analyzer:
            self.Analyzer.notify_status('process died')
            self.Analyzer.cleanup()
