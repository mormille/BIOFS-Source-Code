import time
from communication.pico_communication import PicoCommunication
from subsystems.filtering_system.controller import FilteringController
from subsystems.monitoring_system.controller import MonitoringController
from data.google_sheets import GoogleSheetsLogger
from scheduler import Scheduler

def main():
    try:
        print("Initializing Water Filtering System...")

        # Step 1: Setup communication with Pico 1 and Pico 2
        pico1 = PicoCommunication(port="/dev/ttyUSB0", baudrate=115200, name="Pico 1")  # Filtering Subsystem
        pico2 = PicoCommunication(port="/dev/ttyUSB1", baudrate=115200, name="Pico 2")  # Monitoring Subsystem

        # Step 2: Initialize controllers
        filtering_controller = FilteringController(pico1)
        monitoring_controller = MonitoringController(pico2)

        # Step 3: Setup Google Sheets Logger
        logger = GoogleSheetsLogger(sheet_name="WaterFilterMetrics")

        # Step 4: Scheduler for task orchestration
        scheduler = Scheduler()

        # Step 5: Register tasks
        scheduler.add_task(interval=10, function=filtering_controller.run_cycle)  # Filtering tasks every 10 sec
        scheduler.add_task(interval=15, function=monitoring_controller.run_cycle)  # Monitoring tasks every 15 sec
        scheduler.add_task(interval=30, function=lambda: log_data(filtering_controller, monitoring_controller, logger))

        print("System initialized. Starting operation...")

        # Step 6: Main loop to run the scheduler
        while True:
            scheduler.run_pending()
            time.sleep(1)  # Prevent CPU overload

    except KeyboardInterrupt:
        print("System interrupted by user. Shutting down...")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        pico1.close()
        pico2.close()
        print("System safely shut down.")

def log_data(filtering_controller, monitoring_controller, logger):
    """
    Fetch data from both controllers and log it to Google Sheets.
    """
    print("Logging data to Google Sheets...")
    data = {
        "Filtering_Flow": filtering_controller.get_flow_rate(),
        "Filtering_Pressure": filtering_controller.get_pressure(),
        "Monitoring_Turbidity": monitoring_controller.get_turbidity(),
        "Monitoring_Oxygen": monitoring_controller.get_oxygen(),
        "Monitoring_pH": monitoring_controller.get_ph(),
        "Monitoring_Temperature": monitoring_controller.get_temperature(),
        "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    logger.log(data)

if __name__ == "__main__":
    main()
