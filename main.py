from FanSpeedController import FanSpeedController

def main():
    # Initialize controller
    fan_controller = FanSpeedController()

    # Input values
    try:
        print("Enter a temperature value:")
        temperature_input = float(input())
        
        print("Enter a humidity value:")
        humidity_input = float(input())
        
        # Compute fan speed
        fan_speed = fan_controller.compute_fan_speed(temperature_input, humidity_input)
        
        print(f"Fan speed: {fan_speed:.2f}%")
        
    except ValueError:
        print("Invalid input. Please enter numeric values.")
    except Exception as e:
        print(f"There is an exception: {e}")
        
if __name__ == "__main__":
    main()
