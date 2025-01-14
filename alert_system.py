import time
import threading
import random
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Mock function for metric queries
def run_metric_query(metric_query, condition_operator, condition_value):
    """Simulate a metric query with random result and delay."""
    time.sleep(random.uniform(0.1, 1.0))  # Simulate query delay
    metric_result = random.uniform(0, 100)  # Simulate a metric value
    if condition_operator == ">":
        return metric_result > condition_value
    elif condition_operator == "<":
        return metric_result < condition_value
    elif condition_operator == "==":
        return metric_result == condition_value
    return False

class Alert:
    def __init__(self, alert_id, interval, metric_query, condition_operator, condition_value):
        self.alert_id = alert_id
        self.interval = interval
        self.metric_query = metric_query
        self.condition_operator = condition_operator
        self.condition_value = condition_value
        self.next_execution = datetime.now() + timedelta(minutes=self.interval)

class AlertSystem:
    def __init__(self):
        self.alerts = {}
        self.lock = threading.Lock()
        self.running = True

    def add_alert(self, alert_id, interval, metric_query, condition_operator, condition_value):
        """Add a new alert to the system."""
        with self.lock:
            self.alerts[alert_id] = Alert(alert_id, interval, metric_query, condition_operator, condition_value)
            logging.info(f"Alert {alert_id} added with interval {interval} minutes.")

    def evaluate_alert(self, alert):
        """Evaluate a single alert."""
        now = datetime.now()
        if now >= alert.next_execution:
            lag = (now - alert.next_execution).total_seconds()
            if lag > 0:
                logging.warning(f"Alert {alert.alert_id} is lagging by {lag:.2f} seconds.")

            # Run the metric query
            result = run_metric_query(alert.metric_query, alert.condition_operator, alert.condition_value)
            if result:
                logging.info(f"Alert {alert.alert_id} triggered.")
            else:
                logging.info(f"Alert {alert.alert_id} condition not met.")

            # Schedule the next execution
            alert.next_execution = now + timedelta(minutes=alert.interval)

    def worker(self):
        """Worker thread to evaluate alerts."""
        while self.running:
            with self.lock:
                alerts = list(self.alerts.values())

            for alert in alerts:
                self.evaluate_alert(alert)

            time.sleep(1)  # Prevent busy-waiting

    def start(self):
        """Start the alert evaluation system."""
        self.running = True
        self.worker_thread = threading.Thread(target=self.worker)
        self.worker_thread.start()
        logging.info("Alert system started.")

    def stop(self):
        """Stop the alert evaluation system."""
        self.running = False
        self.worker_thread.join()
        logging.info("Alert system stopped.")

# Example usage
if __name__ == "__main__":
    alert_system = AlertSystem()

    # Add some test alerts
    alert_system.add_alert("id1", 1, "-1h:now:some_metric:avg", ">", 50)
    alert_system.add_alert("id2", 2, "-1h:now:some_metric:avg", "<", 30)
    alert_system.add_alert("id3", 5, "-1h:now:some_metric:avg", "==", 75)

    # Start the alert system
    alert_system.start()

    try:
        # Run the system for 30 seconds
        time.sleep(30)
    finally:
        # Stop the system
        alert_system.stop()
